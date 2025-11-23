# .env Setup Guide

## Step-by-Step Instructions

### Step 1: Copy the Template File

**On Unix/Linux/macOS:**
```bash
cp .env.example .env
```

**On Windows:**
```cmd
copy .env.example .env
```

### Step 2: Get Telegram API Credentials

1. Visit https://my.telegram.org/auth
2. Login with your Telegram phone number
3. Enter the verification code sent to your Telegram app
4. Click on **"API Development Tools"**
5. Fill in the application form:
   - **App title:** Any name (e.g., "My Scraper")
   - **Short name:** Any short name (e.g., "scraper")
   - **Platform:** Select any (e.g., "Desktop")
   - **Description:** Optional
6. Click **"Create application"**
7. You will see your credentials:
   - **api_id** - A numeric value (e.g., 12345678)
   - **api_hash** - A 32-character hexadecimal string

### Step 3: Edit the .env File

Open `.env` in a text editor and replace the example values:

```env
# Replace with your actual api_id
TELEGRAM_API_ID=12345678

# Replace with your actual api_hash
TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef

# Replace with your phone number (include country code)
TELEGRAM_PHONE=+819012345678
```

### Step 4: Save the File

Save the `.env` file in the same directory as `main.py`.

## Example .env File

### For US Phone Number:
```env
TELEGRAM_API_ID=87654321
TELEGRAM_API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TELEGRAM_PHONE=+12025551234
```

### For Japan Phone Number:
```env
TELEGRAM_API_ID=87654321
TELEGRAM_API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TELEGRAM_PHONE=+819087654321
```

### For UK Phone Number:
```env
TELEGRAM_API_ID=87654321
TELEGRAM_API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TELEGRAM_PHONE=+447700900123
```

## Phone Number Format

The phone number must include:
- **+** (plus sign)
- **Country code** (no leading zeros)
- **Phone number** (no spaces, dashes, or parentheses)

### Common Country Codes:
- USA: +1
- UK: +44
- Japan: +81
- Germany: +49
- France: +33
- China: +86
- India: +91

### Format Examples:
✅ Correct: `+819012345678`
✅ Correct: `+12025551234`
❌ Wrong: `819012345678` (missing +)
❌ Wrong: `+81 90 1234 5678` (has spaces)
❌ Wrong: `+81-90-1234-5678` (has dashes)

## Verification

After creating your `.env` file, verify it's correct:

```bash
python check_config.py
```

This will validate:
- ✓ .env file exists
- ✓ All required variables are set
- ✓ Values are not the default examples
- ✓ Dependencies are installed

## Security Notes

⚠️ **Important:**
- Never share your `.env` file
- Never commit `.env` to git
- Keep your API credentials secure
- The `.gitignore` file already excludes `.env`

## Troubleshooting

### "Missing required credentials" Error
- Make sure `.env` file exists in the project directory
- Check that all three variables are set
- Ensure no extra spaces around `=` signs

### "Invalid phone number" Error
- Phone number must start with `+`
- Include country code
- Remove all spaces and special characters
- Example: `+819012345678`

### "API ID must be integer" Error
- TELEGRAM_API_ID should be numeric only
- No quotes needed
- Example: `TELEGRAM_API_ID=12345678`

## Need Help?

If you're having trouble:
1. Run `python check_config.py` to diagnose issues
2. Check the main README.md for troubleshooting
3. Verify your credentials at https://my.telegram.org
4. Make sure `.env` is in the same directory as `main.py`

## Next Steps

Once `.env` is configured:
1. Run configuration check: `python check_config.py`
2. Test the scraper: `python main.py durov`
3. View results: Open `messages.csv`

---

For more information, see README.md
