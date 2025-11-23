# Telegram Channel Message Scraper

A Python tool to fetch all messages from Telegram channels and save them to CSV format using Telethon.

## Features

- ✅ Fetch all messages from a Telegram channel (oldest to newest)
- ✅ Interactive mode: Browse and select from your joined channels
- ✅ Session-based login: Multiple user account support
- ✅ Automatic self-post exclusion (excludes your own messages)
- ✅ Export to CSV with comprehensive metadata
- ✅ Resume capability (continue from interruption)
- ✅ Progress tracking with visual progress bar
- ✅ Rate limiting to avoid API restrictions
- ✅ Async/await for optimal performance
- ✅ Unicode support (handles Japanese, emoji, etc.)
- ✅ Secure credential management
- ✅ Comprehensive error handling
- ✅ No admin permissions required

## Message Data Extracted

Each message includes:
- Message ID
- Date/time (ISO 8601 format)
- Sender ID, name, and username
- Message text content
- Media type (photo, video, document, etc.)
- View count
- Forward count
- Reaction count
- Forward information (if forwarded)
- Reply-to message ID
- Edit date (if edited)

## Prerequisites

- Python 3.7 or higher
- Telegram account
- Telegram API credentials (api_id and api_hash)

## Installation

### 1. Clone or download this repository

```bash
git clone git@github.com:x5gtrn/TelegramChannelMessageScraper.git
cd TelegramChannelMessageScraper
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Telegram API credentials

1. Go to https://my.telegram.org/auth
2. Log in with your phone number
3. Click on "API Development Tools"
4. Create a new application (if you haven't already)
5. Note down your `api_id` and `api_hash`

### 5. Configure credentials

**Option A: Using .env file (Recommended)**

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:
```
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=+1234567890
```

**Option B: Using config.yaml**

Edit `config.yaml` and uncomment the credential lines:
```yaml
api_id: 12345678
api_hash: "your_api_hash_here"
phone_number: "+1234567890"
```

⚠️ **Security Note**: Never commit `.env` or `config.yaml` with real credentials to version control!

## Usage

### Two Modes Available

**Interactive Mode** (Recommended for browsing channels):
```bash
python telegram_channel_message_scraper.py <username>
```

**Direct Mode** (For specific channel):
```bash
python telegram_channel_message_scraper.py --channel <channel_username_or_id>
```

### Interactive Mode Examples

```bash
# Login as user 'x5gtrn' and browse joined channels
python telegram_channel_message_scraper.py x5gtrn

# Login as user 'myaccount'
python telegram_channel_message_scraper.py myaccount
```

This mode will:
1. Log you in with the specified username (creates a session file named after the username)
2. Display all channels you've joined
3. Let you select which channel to scrape interactively

Example interactive session:
```
Successfully connected to Telegram as Daisuke (@x5gtrn)

Fetching channel information...

List of joined channels:
--------------------------------------------------------------------------------
1. Tech News Channel
   @technews (ID: -1001234567890)

2. Private Investment Group
   Private (ID: -1009876543210)

3. Crypto Updates
   @cryptoupdates (ID: -1001111222333)

Enter the target channel number (0 to cancel): 1

Selected channel: Tech News Channel
Fetching messages from: Tech News Channel
Channel ID: -1001234567890
Note: Typically, only admins can post in channels. Fetching all posts.
(Your own posts will be excluded)
...
```

### Direct Mode Examples

```bash
# Using channel username (without @)
python telegram_channel_message_scraper.py --channel durov

# Using channel ID
python telegram_channel_message_scraper.py --channel 1234567890

# Using negative channel ID (for supergroups)
python telegram_channel_message_scraper.py --channel -1001234567890

# With @ symbol (will be automatically removed)
python telegram_channel_message_scraper.py --channel @durov
```

### First Run

On first run, you will be prompted to:
1. Enter the verification code sent to your Telegram account
2. Enter your 2FA password (if enabled)

This authentication is saved in a session file, so you won't need to do it again.

**Note**: In interactive mode, the session file is named after the username you provide (e.g., `x5gtrn.session`), allowing you to manage multiple accounts easily.

### Output

The script will:
1. Connect to Telegram
2. (Interactive mode only) Display your joined channels for selection
3. Fetch all messages from the selected/specified channel with a progress bar
4. Automatically exclude your own posts
5. Save messages to `messages.csv` (or configured filename)

Example output (Direct Mode):
```
Successfully connected to Telegram as Daisuke (@x5gtrn)
Fetching messages from: Example Channel
Channel ID: -1001234567890
Note: Typically, only admins can post in channels. Fetching all posts.
(Your own posts will be excluded)
Counting messages...
Total messages to process: 5000

Fetching messages (resuming from ID: 0)...
Processing messages: 100%|████████████████| 5000/5000 [05:30<00:00, 15.15it/s]

Total messages collected: 1234
Successfully saved 1234 messages to messages.csv
Progress file cleared.
```

## Resume Feature

If the script is interrupted:
- Progress is automatically saved every 100 messages
- Run the same command again to resume from where it stopped
- The `progress.json` file tracks the last processed message ID

To start fresh:
```bash
# Delete progress file
rm progress.json
```

## Configuration Options

Edit `config.yaml` to customize:

```yaml
session_name: "telegram_session"      # Session file name
output_file: "messages.csv"           # Output CSV filename
timezone: "UTC"                       # Timezone for timestamps
batch_size: 100                       # Messages per batch
rate_limit_delay: 1                   # Delay in ms between requests
```

## CSV Output Format

| Column | Description |
|--------|-------------|
| message_id | Unique message identifier |
| date | Message timestamp (ISO 8601) |
| sender_id | Telegram user ID of sender |
| sender_name | Display name of sender |
| sender_username | Username of sender |
| message_text | Message content |
| media_type | Type of media (photo, video, document, etc.) |
| views | Number of views |
| forwards | Number of forwards |
| reactions | Number of reactions |
| forwarded | Boolean - is forwarded message |
| forward_date | Original message date (if forwarded) |
| forward_from_id | Original sender ID (if forwarded) |
| reply_to_msg_id | ID of message being replied to |
| edit_date | Last edit timestamp |

## Troubleshooting

### "Missing required credentials" error
- Ensure your `.env` file exists and has correct values
- Check that environment variables are properly set
- Verify `config.yaml` has uncommented credential lines (if not using .env)

### "Channel is private" error
- You must be a member of the channel
- The account associated with your API credentials must have access

### "FloodWaitError" - Rate limiting
- The script will automatically wait and retry
- Consider increasing `rate_limit_delay` in config.yaml
- Telegram has rate limits; wait a few hours if repeatedly blocked

### Session authentication issues
- Delete the `.session` file and run again
- Ensure your phone number includes country code (e.g., +1234567890)

### No messages found
- The channel might be empty
- Check that you have access to view the channel's messages
- Verify the channel ID is correct (negative IDs for supergroups start with -100)

## Advanced Usage

### Multiple User Accounts

You can manage multiple Telegram accounts by using different usernames:

```bash
# Account 1
python telegram_channel_message_scraper.py alice

# Account 2
python telegram_channel_message_scraper.py bob
```

Each username creates its own session file (e.g., `alice.session`, `bob.session`), allowing you to switch between accounts easily.

### Custom Output Filename

Modify `config.yaml`:
```yaml
output_file: "custom_messages.csv"
```

### Adjust Rate Limiting

If you're getting rate limited frequently:
```yaml
rate_limit_delay: 5  # Increase delay to 5ms
```

### Include Your Own Posts

By default, your own posts are excluded. To include them, modify the `fetch_messages` call in `telegram_channel_message_scraper.py`:

```python
messages = await self.fetch_messages(channel_identifier, exclude_self_posts=False)
```

### Process Specific Date Range

Edit the `fetch_messages` method in `telegram_channel_message_scraper.py` to add date filtering:
```python
async for message in self.client.iter_messages(
    channel,
    limit=None,
    reverse=True,
    offset_date=datetime(2024, 1, 1),  # Start from this date
):
```

## Security Best Practices

1. ✅ Never commit `.env` or session files
2. ✅ Use environment variables for credentials
3. ✅ Keep session files secure (they contain auth tokens)
4. ✅ Don't share your `api_id` and `api_hash`
5. ✅ Use a separate Telegram account for scraping if needed
6. ✅ Review the `.gitignore` file before committing

## Technical Details

- **Telethon Version**: 1.37.0+
- **Protocol**: MTProto 2.0
- **Async Framework**: asyncio
- **CSV Encoding**: UTF-8
- **Python Version**: 3.7+

## Performance

- Processes ~15-20 messages per second (depends on API rate limits)
- Memory efficient: streams messages without loading all into RAM
- Progress saved every 100 messages
- Automatic retry on network errors

## Limitations

- Telegram API rate limits apply (typically ~20 requests/second)
- Large channels (100k+ messages) may take hours to process
- You must be a member of the channel to scrape messages
- Some private channels may not be accessible
- The tool fetches all channel posts (typically only admins can post in channels)
- Group chats (where all members can post) are not filtered by admin status

## License

This project is provided as-is for educational purposes. Ensure compliance with Telegram's Terms of Service and API usage policies.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Telethon documentation: https://docs.telethon.dev/
3. Open an issue on the repository

## Resources

- [Complete Guide to Telegram Channel Data Retrieval](https://daisuke.masuda.tokyo/article-2025-11-08-0057) - Detailed setup instructions and usage examples

## Changelog

### Version 2.0.0
- Added interactive mode for channel selection
- Session-based login with username support
- Automatic self-post exclusion
- Removed admin permission requirements
- Simplified message fetching (no admin checks)
- Multi-account support via session files

### Version 1.0.0
- Initial release
- Admin message filtering
- CSV export
- Resume functionality
- Progress tracking
- Comprehensive error handling
