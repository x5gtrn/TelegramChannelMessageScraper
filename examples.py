#!/usr/bin/env python3
"""
Advanced Usage Examples
Demonstrates additional features and customization options.
"""

import asyncio
from datetime import datetime, timedelta
from main import TelegramScraper


async def example_with_date_range():
    """Example: Fetch messages from a specific date range."""
    print("Example: Fetch messages from last 30 days")
    print("-" * 50)
    
    scraper = TelegramScraper()
    await scraper.connect()
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    channel = await scraper.client.get_entity("your_channel")
    
    messages = []
    async for message in scraper.client.iter_messages(
        channel,
        offset_date=end_date,
        reverse=True,
    ):
        if message.date < start_date:
            break
        
        if message.sender_id and await scraper.is_admin(channel, message.sender_id):
            message_data = scraper._extract_message_data(message)
            messages.append(message_data)
    
    scraper.save_to_csv(messages, "messages_last_30_days.csv")
    await scraper.client.disconnect()


async def example_filter_by_media():
    """Example: Fetch only messages with specific media types."""
    print("Example: Fetch only messages with photos")
    print("-" * 50)
    
    scraper = TelegramScraper()
    await scraper.connect()
    
    channel = await scraper.client.get_entity("your_channel")
    
    messages = []
    async for message in scraper.client.iter_messages(channel, limit=None, reverse=True):
        if not message.sender_id:
            continue
        
        if not await scraper.is_admin(channel, message.sender_id):
            continue
        
        # Filter by media type
        media_type = scraper._get_media_type(message)
        if media_type == "photo":
            message_data = scraper._extract_message_data(message)
            messages.append(message_data)
    
    scraper.save_to_csv(messages, "photo_messages.csv")
    await scraper.client.disconnect()


async def example_custom_csv_fields():
    """Example: Export with custom CSV fields."""
    print("Example: Export with custom fields")
    print("-" * 50)
    
    import csv
    
    scraper = TelegramScraper()
    await scraper.connect()
    
    channel = await scraper.client.get_entity("your_channel")
    
    # Custom CSV with only essential fields
    with open("minimal_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Author", "Text", "Views"])
        
        async for message in scraper.client.iter_messages(
            channel, limit=100, reverse=True
        ):
            if message.sender_id and await scraper.is_admin(channel, message.sender_id):
                writer.writerow([
                    message.id,
                    message.date.isoformat() if message.date else "",
                    getattr(message.sender, "first_name", ""),
                    message.message or "",
                    message.views or 0,
                ])
    
    print("Saved to minimal_export.csv")
    await scraper.client.disconnect()


async def example_statistics():
    """Example: Generate channel statistics."""
    print("Example: Generate channel statistics")
    print("-" * 50)
    
    scraper = TelegramScraper()
    await scraper.connect()
    
    channel = await scraper.client.get_entity("your_channel")
    
    stats = {
        "total_messages": 0,
        "total_views": 0,
        "total_reactions": 0,
        "media_count": 0,
        "admin_posts": 0,
    }
    
    async for message in scraper.client.iter_messages(channel, limit=1000):
        stats["total_messages"] += 1
        stats["total_views"] += message.views or 0
        
        if message.reactions:
            stats["total_reactions"] += len(message.reactions.results)
        
        if message.media:
            stats["media_count"] += 1
        
        if message.sender_id and await scraper.is_admin(channel, message.sender_id):
            stats["admin_posts"] += 1
    
    print(f"\nChannel Statistics (last 1000 messages):")
    print(f"  Total messages: {stats['total_messages']}")
    print(f"  Admin posts: {stats['admin_posts']}")
    print(f"  Total views: {stats['total_views']:,}")
    print(f"  Average views: {stats['total_views'] // stats['total_messages']:,}")
    print(f"  Messages with media: {stats['media_count']}")
    print(f"  Total reactions: {stats['total_reactions']}")
    
    await scraper.client.disconnect()


async def example_download_media():
    """Example: Download media files from messages."""
    print("Example: Download media files")
    print("-" * 50)
    
    from pathlib import Path
    
    scraper = TelegramScraper()
    await scraper.connect()
    
    channel = await scraper.client.get_entity("your_channel")
    
    # Create media directory
    media_dir = Path("downloaded_media")
    media_dir.mkdir(exist_ok=True)
    
    downloaded = 0
    async for message in scraper.client.iter_messages(channel, limit=10):
        if message.media and message.sender_id:
            if await scraper.is_admin(channel, message.sender_id):
                # Download media
                filename = f"{message.id}_{message.date.strftime('%Y%m%d')}"
                filepath = await scraper.client.download_media(
                    message, file=media_dir / filename
                )
                if filepath:
                    print(f"Downloaded: {filepath}")
                    downloaded += 1
    
    print(f"\nTotal files downloaded: {downloaded}")
    await scraper.client.disconnect()


def print_menu():
    """Print example menu."""
    print("\n" + "=" * 60)
    print("Telegram Scraper - Advanced Examples")
    print("=" * 60)
    print("\nAvailable examples:")
    print("1. Fetch messages from last 30 days")
    print("2. Fetch only messages with photos")
    print("3. Export with custom CSV fields")
    print("4. Generate channel statistics")
    print("5. Download media files")
    print("0. Exit")
    print("\nNote: Update channel names in examples before running!")
    print()


async def main():
    """Main function to run examples."""
    examples = {
        "1": example_with_date_range,
        "2": example_filter_by_media,
        "3": example_custom_csv_fields,
        "4": example_statistics,
        "5": example_download_media,
    }
    
    while True:
        print_menu()
        choice = input("Select example (0-5): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        
        if choice in examples:
            try:
                await examples[choice]()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"Error: {e}")
                input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("WARNING: These are example scripts.")
    print("Please edit the channel names before running!")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
