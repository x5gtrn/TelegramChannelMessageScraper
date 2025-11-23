# Project Structure

Overview of the Telegram Channel Scraper project files and directories.

```
telegram_scraper/
│
├── telegram_channel_message_scraper.py  # Main scraper application
├── examples.py                          # Advanced usage examples
├── check_config.py                      # Configuration validation tool
│
├── config.yaml             # Configuration file (user-created)
├── .env                    # Environment variables (user-created, gitignored)
├── .env.example            # Environment variables template
│
├── requirements.txt        # Python dependencies
├── setup.sh               # Unix/Linux setup script
├── setup.bat              # Windows setup script
│
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── LICENSE                # MIT License
├── .gitignore             # Git ignore rules
│
├── progress.json          # Progress tracking (auto-generated, gitignored)
├── messages.csv           # Output file (auto-generated, gitignored)
├── *.session              # Telegram session files (auto-generated, gitignored)
│
└── venv/                  # Virtual environment (user-created, gitignored)
```

## Core Files

### telegram_channel_message_scraper.py
The main application containing:
- `TelegramChannelMessageScraper` class: Core scraping logic
- Connection and authentication handling
- Message fetching with admin filtering
- CSV export functionality
- Progress tracking and resume capability
- Error handling and rate limiting

**Key Methods:**
- `connect()`: Authenticate with Telegram
- `fetch_messages()`: Retrieve messages from channel
- `is_admin()`: Check if user is admin
- `save_to_csv()`: Export messages to CSV
- `run()`: Main execution flow

### examples.py
Advanced usage examples demonstrating:
- Date range filtering
- Media type filtering
- Custom CSV fields
- Channel statistics
- Media file downloads

### check_config.py
Configuration validation tool that checks:
- Environment variables
- Config file validity
- Package dependencies
- File permissions
- Session files

## Configuration Files

### .env
Contains sensitive credentials (never commit this):
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone
```

### config.yaml
Optional configuration for:
- Session name
- Output filename
- Timezone settings
- Rate limiting
- Batch sizes

## Setup Scripts

### setup.sh (Unix/Linux/macOS)
Automated setup script that:
1. Checks Python version
2. Creates virtual environment
3. Installs dependencies
4. Creates .env from template

### setup.bat (Windows)
Windows version of the setup script with equivalent functionality.

## Auto-Generated Files

### *.session
Telegram authentication session files:
- Created on first authentication
- Contains encrypted session data
- Allows skip authentication on subsequent runs
- **Keep secure!** Contains auth tokens

### progress.json
Progress tracking file:
```json
{
  "last_message_id": 12345
}
```
- Updated every 100 messages
- Enables resume functionality
- Deleted on successful completion

### messages.csv
Output file containing:
- Message ID, date, sender info
- Message text and media type
- View counts, reactions, forwards
- Forward and reply information

## Dependencies

Key Python packages (see requirements.txt):
- **telethon**: Telegram MTProto API client
- **python-dotenv**: Environment variable management
- **PyYAML**: YAML configuration parsing
- **tqdm**: Progress bar display
- **cryptg**: Optional, speeds up encryption

## File Flow

```
User runs telegram_channel_message_scraper.py
    ↓
Load .env and config.yaml
    ↓
Check for progress.json (resume)
    ↓
Create/load *.session
    ↓
Connect to Telegram
    ↓
Fetch messages (save progress periodically)
    ↓
Export to messages.csv
    ↓
Delete progress.json on success
```

## Security Considerations

### Sensitive Files (gitignored):
- `.env` - API credentials
- `*.session` - Auth tokens
- `config.yaml` - May contain credentials
- `progress.json` - Channel information
- `*.csv` - Exported data

### Public Files:
- `.env.example` - Template only
- `config.yaml` - If using env vars only
- All `.py` files
- Documentation files

## Adding New Features

### To add a new message field:
1. Update `_extract_message_data()` in telegram_channel_message_scraper.py
2. Add field to CSV fieldnames in `save_to_csv()`
3. Update README.md documentation

### To add a new filter:
1. Add filter logic in `fetch_messages()`
2. Create example in examples.py
3. Document in README.md

### To add a new export format:
1. Create new export method (e.g., `save_to_json()`)
2. Add option to config.yaml
3. Update documentation

## Best Practices

### Development:
1. Always use virtual environment
2. Run `check_config.py` before testing
3. Test with small channels first
4. Keep dependencies updated

### Production:
1. Use environment variables for credentials
2. Regular backups of session files
3. Monitor rate limits
4. Handle errors gracefully

### Version Control:
1. Never commit .env or sessions
2. Update .gitignore as needed
3. Document all changes
4. Tag stable releases

## Maintenance

### Regular Updates:
- Update Telethon to latest version
- Check for Python security updates
- Review and update dependencies

### Monitoring:
- Check for API changes
- Monitor error logs
- Track rate limit issues
- Validate output quality

---

For questions about project structure, open an issue on the repository.
