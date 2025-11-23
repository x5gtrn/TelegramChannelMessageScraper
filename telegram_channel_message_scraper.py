#!/usr/bin/env python3
"""
Telegram Channel Message Scraper
Fetches all messages from a Telegram channel (admin posts only) and saves to CSV.
"""

import asyncio
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from telethon import TelegramClient
from telethon.errors import (
    SessionPasswordNeededError,
    FloodWaitError,
    ChannelPrivateError,
    UsernameNotOccupiedError,
)
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    Channel,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
    MessageMediaGeo,
    MessageMediaContact,
    MessageMediaPoll,
)
from tqdm import tqdm
import yaml
from dotenv import load_dotenv


class TelegramChannelMessageScraper:
    """Main class for scraping Telegram channel messages."""

    def __init__(self, config_path: str = "config.yaml", username: Optional[str] = None):
        """Initialize the scraper with configuration."""
        self.config = self._load_config(config_path)
        self.username = username
        self.client = None
        self.current_user_id = None
        self.progress_file = Path("progress.json")
        self.last_message_id = self._load_progress()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file and environment variables."""
        # Load environment variables
        load_dotenv()

        # Load YAML config
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}

        # Override with environment variables if available
        api_id = os.getenv("TELEGRAM_API_ID") or config.get("api_id")
        api_hash = os.getenv("TELEGRAM_API_HASH") or config.get("api_hash")
        phone = os.getenv("TELEGRAM_PHONE") or config.get("phone_number")

        if not all([api_id, api_hash, phone]):
            raise ValueError(
                "Missing required credentials. Set TELEGRAM_API_ID, "
                "TELEGRAM_API_HASH, and TELEGRAM_PHONE in .env file or config.yaml"
            )

        return {
            "api_id": int(api_id),
            "api_hash": api_hash,
            "phone_number": phone,
            "session_name": config.get("session_name", "telegram_session"),
            "output_file": config.get("output_file", "messages.csv"),
            "timezone": config.get("timezone", "UTC"),
            "batch_size": config.get("batch_size", 100),
            "rate_limit_delay": config.get("rate_limit_delay", 1),
        }

    def _load_progress(self) -> int:
        """Load last processed message ID from progress file."""
        if self.progress_file.exists():
            with open(self.progress_file, "r") as f:
                data = json.load(f)
                return data.get("last_message_id", 0)
        return 0

    def _save_progress(self, message_id: int):
        """Save current progress to file."""
        with open(self.progress_file, "w") as f:
            json.dump({"last_message_id": message_id}, f)

    async def connect(self):
        """Connect to Telegram and authenticate."""
        session_name = self.username if self.username else self.config["session_name"]

        self.client = TelegramClient(
            session_name,
            self.config["api_id"],
            self.config["api_hash"],
        )

        await self.client.connect()

        if not await self.client.is_user_authorized():
            print("First time authentication required.")
            await self.client.send_code_request(self.config["phone_number"])

            try:
                code = input("Enter the code you received: ")
                await self.client.sign_in(self.config["phone_number"], code)
            except SessionPasswordNeededError:
                password = input("Two-factor authentication enabled. Enter your password: ")
                await self.client.sign_in(password=password)

        # Get current user ID
        me = await self.client.get_me()
        self.current_user_id = me.id
        print(f"Successfully connected to Telegram as {me.first_name} (@{me.username or 'no username'})")

    async def is_admin(self, channel: Channel, user_id: int) -> bool:
        """Check if a user is an admin in the channel."""
        try:
            participant = await self.client(
                GetParticipantRequest(channel, user_id)
            )
            return isinstance(
                participant.participant,
                (ChannelParticipantAdmin, ChannelParticipantCreator),
            )
        except Exception as e:
            print(f"Warning: Could not check admin status for user {user_id}: {e}")
            return False

    async def get_joined_channels(self) -> List[Dict[str, Any]]:
        """Get all channels the user has joined."""
        channels = []
        async for dialog in self.client.iter_dialogs():
            if isinstance(dialog.entity, Channel) and dialog.entity.broadcast:
                # Note: We don't check admin status here to avoid permission errors
                channels.append({
                    "id": dialog.entity.id,
                    "title": dialog.entity.title,
                    "username": dialog.entity.username,
                })
        return channels

    def select_channel(self, channels: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Display channels and allow user to select one."""
        if not channels:
            print("No channels found.")
            return None

        print("\nList of joined channels:")
        print("-" * 80)
        for idx, channel in enumerate(channels, 1):
            username_str = f"@{channel['username']}" if channel["username"] else "Private"
            print(f"{idx}. {channel['title']}")
            print(f"   {username_str} (ID: {channel['id']})")
            print()

        while True:
            try:
                choice = input("\nEnter the target channel number (0 to cancel): ")
                choice_num = int(choice)

                if choice_num == 0:
                    print("Cancelled.")
                    return None

                if 1 <= choice_num <= len(channels):
                    selected = channels[choice_num - 1]
                    print(f"\nSelected channel: {selected['title']}")
                    return selected
                else:
                    print(f"Please enter a number between 1 and {len(channels)}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nCancelled.")
                return None

    def _get_media_type(self, message) -> Optional[str]:
        """Determine the type of media in a message."""
        if not message.media:
            return None

        media_types = {
            MessageMediaPhoto: "photo",
            MessageMediaDocument: "document",
            MessageMediaWebPage: "webpage",
            MessageMediaGeo: "location",
            MessageMediaContact: "contact",
            MessageMediaPoll: "poll",
        }

        for media_class, media_name in media_types.items():
            if isinstance(message.media, media_class):
                if media_name == "document" and message.media.document:
                    # Check if it's a video, audio, or other document type
                    mime_type = message.media.document.mime_type
                    if mime_type.startswith("video/"):
                        return "video"
                    elif mime_type.startswith("audio/"):
                        return "audio"
                    return "document"
                return media_name

        return "other"

    def _extract_message_data(self, message) -> Dict[str, Any]:
        """Extract relevant data from a message."""
        # Handle forwarded messages
        forward_info = {}
        if message.forward:
            forward_info = {
                "forwarded": True,
                "forward_date": message.forward.date.isoformat() if message.forward.date else None,
                "forward_from_id": getattr(message.forward.from_id, "user_id", None)
                if hasattr(message.forward, "from_id")
                else None,
            }
        else:
            forward_info = {"forwarded": False, "forward_date": None, "forward_from_id": None}

        return {
            "message_id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "sender_id": message.sender_id,
            "sender_name": getattr(message.sender, "first_name", "") or "",
            "sender_username": getattr(message.sender, "username", "") or "",
            "message_text": message.message or "",
            "media_type": self._get_media_type(message),
            "views": message.views or 0,
            "forwards": message.forwards or 0,
            "reactions": len(message.reactions.results) if message.reactions else 0,
            **forward_info,
            "reply_to_msg_id": message.reply_to_msg_id,
            "edit_date": message.edit_date.isoformat() if message.edit_date else None,
        }

    async def fetch_messages(self, channel_identifier: str, exclude_self_posts: bool = True) -> List[Dict[str, Any]]:
        """
        Fetch all messages from a channel (channels typically only allow admins to post).

        Args:
            channel_identifier: Channel username (without @) or channel ID
            exclude_self_posts: If True, exclude the current user's posts

        Returns:
            List of message dictionaries
        """
        try:
            # Resolve channel
            channel = await self.client.get_entity(channel_identifier)

            if not isinstance(channel, Channel):
                raise ValueError(f"{channel_identifier} is not a channel")

            print(f"Fetching messages from: {channel.title}")
            print(f"Channel ID: {channel.id}")
            print(f"Note: Typically, only admins can post in channels. Fetching all posts.")
            if exclude_self_posts:
                print(f"(Your own posts will be excluded)")

            messages_data = []

            # Count total messages first for progress bar
            print("Counting messages...")
            total_count = 0
            async for _ in self.client.iter_messages(
                channel, limit=None, reverse=True, min_id=self.last_message_id
            ):
                total_count += 1

            print(f"Total messages to process: {total_count}")
            print(f"\nFetching messages (resuming from ID: {self.last_message_id})...")

            with tqdm(total=total_count, desc="Processing messages") as pbar:
                async for message in self.client.iter_messages(
                    channel, limit=None, reverse=True, min_id=self.last_message_id
                ):
                    # Exclude current user's posts if requested
                    if exclude_self_posts and message.sender_id == self.current_user_id:
                        pbar.update(1)
                        continue

                    # In channels, typically only admins can post, so we collect all messages
                    # (excluding service messages, etc.)
                    if message.message or message.media:
                        message_data = self._extract_message_data(message)
                        messages_data.append(message_data)

                        # Save progress periodically
                        if len(messages_data) % 100 == 0:
                            self._save_progress(message.id)

                    pbar.update(1)

                    # Rate limiting
                    await asyncio.sleep(self.config["rate_limit_delay"] / 1000)

            print(f"\nTotal messages collected: {len(messages_data)}")
            return messages_data

        except ChannelPrivateError:
            print(f"Error: Channel {channel_identifier} is private or you don't have access.")
            sys.exit(1)
        except UsernameNotOccupiedError:
            print(f"Error: Channel {channel_identifier} does not exist.")
            sys.exit(1)
        except FloodWaitError as e:
            print(f"Rate limited. Please wait {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
            return await self.fetch_messages(channel_identifier, exclude_self_posts)
        except Exception as e:
            print(f"Error fetching messages: {e}")
            raise

    def save_to_csv(self, messages: List[Dict[str, Any]], filename: Optional[str] = None):
        """Save messages to CSV file."""
        if not messages:
            print("No messages to save.")
            return

        filename = filename or self.config["output_file"]
        
        # Define CSV columns
        fieldnames = [
            "message_id",
            "date",
            "sender_id",
            "sender_name",
            "sender_username",
            "message_text",
            "media_type",
            "views",
            "forwards",
            "reactions",
            "forwarded",
            "forward_date",
            "forward_from_id",
            "reply_to_msg_id",
            "edit_date",
        ]

        # Write CSV file
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(messages)

        print(f"Successfully saved {len(messages)} messages to {filename}")

    async def run(self, channel_identifier: Optional[str] = None, interactive: bool = False):
        """Main execution method."""
        try:
            await self.connect()

            # If interactive mode, show channel selection
            if interactive:
                print("\nFetching channel information...")
                channels = await self.get_joined_channels()

                if not channels:
                    print("No joined channels were found.")
                    return

                selected_channel = self.select_channel(channels)
                if not selected_channel:
                    return

                # Use channel ID as identifier
                channel_identifier = selected_channel["id"]

            if not channel_identifier:
                print("Error: No channel specified.")
                return

            messages = await self.fetch_messages(channel_identifier)
            self.save_to_csv(messages)

            # Clear progress file on successful completion
            if self.progress_file.exists():
                self.progress_file.unlink()
                print("Progress file cleared.")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Progress has been saved.")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            raise
        finally:
            if self.client:
                await self.client.disconnect()


async def main():
    """Entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Interactive mode: python telegram_channel_message_scraper.py <username>")
        print("  Direct mode:      python telegram_channel_message_scraper.py --channel <channel_username_or_id>")
        print()
        print("Examples:")
        print("  python telegram_channel_message_scraper.py x5gtrn")
        print("  python telegram_channel_message_scraper.py --channel my_channel")
        print("  python telegram_channel_message_scraper.py --channel 1234567890")
        sys.exit(1)

    # Check if running in channel mode or username mode
    if sys.argv[1] == "--channel":
        if len(sys.argv) < 3:
            print("Error: --channel requires a channel identifier")
            sys.exit(1)

        channel_identifier = sys.argv[2]

        # Remove @ prefix if present
        if channel_identifier.startswith("@"):
            channel_identifier = channel_identifier[1:]

        scraper = TelegramChannelMessageScraper()
        await scraper.run(channel_identifier=channel_identifier, interactive=False)
    else:
        # Interactive mode with username
        username = sys.argv[1]
        scraper = TelegramChannelMessageScraper(username=username)
        await scraper.run(interactive=True)


if __name__ == "__main__":
    asyncio.run(main())
