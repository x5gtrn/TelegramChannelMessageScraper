# Quick Start Guide

Get started with the Telegram Channel Scraper in 5 minutes!

## Prerequisites

- Python 3.7+ installed
- Telegram account
- Member of at least one channel
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

**Interactive Mode** (Recommended - Browse your channels):
```bash
python telegram_channel_message_scraper.py <your_username>
```

Example:
```bash
python telegram_channel_message_scraper.py alice
```

This will:
1. Log you in
2. Show all channels you've joined
3. Let you select which one to scrape

**Direct Mode** (If you know the channel):
```bash
python telegram_channel_message_scraper.py --channel <channel_username>
```

Example:
```bash
python telegram_channel_message_scraper.py --channel durov
```

**First time only:** You'll be asked to enter a verification code from Telegram.

### 5. View Results

Open `messages.csv` in Excel, Google Sheets, or any spreadsheet application!

## Common Channels to Test

Public channels you can try (use direct mode):

```bash
python telegram_channel_message_scraper.py --channel telegram       # Telegram News
python telegram_channel_message_scraper.py --channel durov          # Pavel Durov's channel
```

Or use interactive mode to browse your own channels:
```bash
python telegram_channel_message_scraper.py myusername
```

## Troubleshooting Quick Fixes

### "Missing required credentials"
→ Check your `.env` file has all three values set

### "Channel is private"
→ Join the channel in Telegram first, then try again

### "Username not found" (Direct mode)
→ Check the channel username is correct (without @)
→ Try interactive mode instead to browse your joined channels

### Script runs but finds no messages
→ The channel might be empty
→ Check that you're a member of the channel
→ Verify the channel allows message viewing

### "No joined channels were found" (Interactive mode)
→ Make sure you've joined at least one channel in Telegram
→ Try refreshing your Telegram app and waiting a minute

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [examples.py](examples.py) for advanced usage
- Run `python check_config.py` to verify your setup

## Quick Tips

✅ **DO:**
- Keep your `.env` file secure
- Use interactive mode to discover channels you've joined
- Start with small public channels to test
- Use the resume feature for large channels
- Use different usernames for multiple Telegram accounts

❌ **DON'T:**
- Share your API credentials
- Commit `.env` or `.session` files to git
- Run multiple instances simultaneously
- Try to scrape channels you're not a member of

## Support

Need help? Check:
1. [README.md](README.md) - Full documentation
2. [Telethon Docs](https://docs.telethon.dev/) - API reference
3. [Telegram API Docs](https://core.telegram.org/api) - Protocol details

---

**Estimated total time:** 5 minutes
**Difficulty:** Beginner-friendly

Happy scraping! 🚀
