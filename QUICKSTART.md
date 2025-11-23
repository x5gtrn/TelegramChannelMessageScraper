# Quick Start Guide

Get started with the Telegram Channel Scraper in 5 minutes!

## Prerequisites

- Python 3.7+ installed
- Telegram account
- 5 minutes of your time

## Step-by-Step Setup

### 1. Get Telegram API Credentials (2 minutes)

1. Open https://my.telegram.org/auth in your browser
2. Login with your phone number
3. Click "API Development Tools"
4. Fill in the form:
   - App title: `My Scraper` (or any name)
   - Short name: `scraper` (or any name)
   - Platform: Choose any (e.g., Desktop)
5. Click "Create application"
6. **Copy your `api_id` and `api_hash`** - you'll need these!

### 2. Install Dependencies (1 minute)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Credentials (1 minute)

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890
TELEGRAM_PHONE=+1234567890
```

### 4. Run the Scraper (1 minute)

```bash
python main.py <channel_username>
```

Example:
```bash
python main.py durov
```

**First time only:** You'll be asked to enter a verification code from Telegram.

### 5. View Results

Open `messages.csv` in Excel, Google Sheets, or any spreadsheet application!

## Common Channels to Test

Public channels you can try (no membership required):

```bash
python main.py telegram       # Telegram News
python main.py durov          # Pavel Durov's channel
```

## Troubleshooting Quick Fixes

### "Missing required credentials"
→ Check your `.env` file has all three values set

### "Channel is private"
→ Join the channel in Telegram first, then try again

### "Username not found"
→ Check the channel username is correct (without @)

### Script runs but finds no messages
→ The channel might not have "admin" users, or you might not have permission to see members

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [examples.py](examples.py) for advanced usage
- Run `python check_config.py` to verify your setup

## Quick Tips

✅ **DO:**
- Keep your `.env` file secure
- Start with small public channels to test
- Use the resume feature for large channels

❌ **DON'T:**
- Share your API credentials
- Commit `.env` to git
- Run multiple instances simultaneously

## Support

Need help? Check:
1. [README.md](README.md) - Full documentation
2. [Telethon Docs](https://docs.telethon.dev/) - API reference
3. [Telegram API Docs](https://core.telegram.org/api) - Protocol details

---

**Estimated total time:** 5 minutes
**Difficulty:** Beginner-friendly

Happy scraping! 🚀
