# Telegram Channel Message Scraper

A Python tool to fetch all messages from a Telegram channel (admin posts only) and save them to CSV format using Telethon.

## Features

- ✅ Fetch all messages from a Telegram channel (oldest to newest)
- ✅ Filter messages by admin users only
- ✅ Export to CSV with comprehensive metadata
- ✅ Resume capability (continue from interruption)
- ✅ Progress tracking with visual progress bar
- ✅ Rate limiting to avoid API restrictions
- ✅ Async/await for optimal performance
- ✅ Unicode support (handles Japanese, emoji, etc.)
- ✅ Secure credential management
- ✅ Comprehensive error handling

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
git clone <repository-url>
cd telegram_scraper
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

### Basic Usage

```bash
python main.py <channel_username>
```

### Examples

```bash
# Using channel username (without @)
python main.py durov

# Using channel ID
python main.py 1234567890

# With @ symbol (will be automatically removed)
python main.py @durov
```

### First Run

On first run, you will be prompted to:
1. Enter the verification code sent to your Telegram account
2. Enter your 2FA password (if enabled)

This authentication is saved in a session file, so you won't need to do it again.

### Output

The script will:
1. Connect to Telegram
2. Identify admin users in the channel
3. Fetch all admin messages with a progress bar
4. Save messages to `messages.csv` (or configured filename)

Example output:
```
Successfully connected to Telegram!
Fetching messages from: Example Channel
Channel ID: 1234567890
Identifying admin users...
Found admin: 123456
Found admin: 789012

Fetching messages (resuming from ID: 0)...
Total messages to process: 5000
Processing messages: 100%|████████████████| 5000/5000 [05:30<00:00, 15.15it/s]

Total admin messages collected: 1234
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
output_file: "messages.csv"            # Output CSV filename
timezone: "UTC"                        # Timezone for timestamps
batch_size: 100                        # Messages per batch
rate_limit_delay: 1                    # Delay in ms between requests
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

### No admin messages found
- Verify you have permission to view channel members
- The channel might not have traditional "admins" (check channel type)
- Try running without admin filtering (modify code as needed)

## Advanced Usage

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

### Process Specific Date Range

Edit the `fetch_messages` method in `main.py` to add date filtering:
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
- Admin detection requires channel member permissions
- Some private channels may not be accessible

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

## Changelog

### Version 1.0.0
- Initial release
- Admin message filtering
- CSV export
- Resume functionality
- Progress tracking
- Comprehensive error handling
