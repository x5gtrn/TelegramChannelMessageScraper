# Security Checklist

Essential security measures for the Telegram Channel Scraper project.

## Pre-Commit Checklist

Before committing any code, verify:

### Critical Security Items 🔴

- [ ] **`.env` file is NOT staged for commit**
  ```bash
  git status | grep ".env"
  # Should return nothing or show "Untracked"
  ```

- [ ] **No `*.session` files are staged**
  ```bash
  git status | grep "session"
  # Should return nothing
  ```

- [ ] **`config.yaml` does not contain credentials**
  ```bash
  grep -i "api_id\|api_hash\|phone" config.yaml
  # Should return only example values
  ```

- [ ] **No API keys in source code**
  ```bash
  grep -r "api_id.*=.*[0-9]" *.py
  # Should return nothing
  ```

### Important Security Items 🟡

- [ ] **`.gitignore` is up to date**
- [ ] **Session files are in `.gitignore`**
- [ ] **Output files with data are ignored**
- [ ] **No hardcoded credentials in comments**

### Good Practice Items 🟢

- [ ] **Virtual environment is ignored**
- [ ] **IDE files are ignored**
- [ ] **Temporary files are ignored**
- [ ] **Documentation is included**

## Installation Security

### When Setting Up

1. **Use Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   ✓ Isolates project dependencies
   ✓ Prevents system-wide package conflicts

2. **Install from requirements.txt**
   ```bash
   pip install -r requirements.txt
   ```
   ✓ Uses known good versions
   ✓ Reproducible environment

3. **Set File Permissions**
   ```bash
   chmod 600 .env          # Only owner can read/write
   chmod 600 *.session     # Protect session files
   ```

4. **Verify Package Integrity**
   ```bash
   pip check
   ```

## Credential Management

### DO ✅

- **Use environment variables**
  ```env
  TELEGRAM_API_ID=12345678
  TELEGRAM_API_HASH=abc123
  TELEGRAM_PHONE=+1234567890
  ```

- **Use `.env` file (never commit it)**
  - Add to `.gitignore`
  - Store separately from code
  - Use `.env.example` as template

- **Rotate credentials regularly**
  - Change API keys periodically
  - Revoke old credentials at https://my.telegram.org

- **Use separate credentials for testing**
  - Don't use production keys for development
  - Create test applications

### DON'T ❌

- **Never hardcode credentials**
  ```python
  # BAD - Never do this!
  api_id = 12345678
  api_hash = "abc123def456"
  ```

- **Never commit `.env` file**
  ```bash
  # Check before committing
  git status | grep ".env"
  ```

- **Never share credentials**
  - Not in chat messages
  - Not in screenshots
  - Not in issues/PRs

- **Never log credentials**
  ```python
  # BAD
  print(f"Using API key: {api_key}")
  
  # GOOD
  print("Connecting to Telegram API...")
  ```

## Session File Security

### Session File Contains:
- Authentication tokens
- Account information
- Access credentials

### Protection Measures:

1. **Never commit session files**
   ```gitignore
   *.session
   *.session-journal
   ```

2. **Set proper permissions**
   ```bash
   chmod 600 *.session
   ```

3. **Store securely**
   - Keep in project directory only
   - Don't copy to cloud storage
   - Don't share via email/chat

4. **Revoke if compromised**
   - Login to Telegram
   - Settings → Privacy and Security → Active Sessions
   - Terminate suspicious sessions

## Network Security

### When Running Scraper:

- **Use secure network**
  - Avoid public WiFi
  - Use VPN if on untrusted network
  - Prefer wired connection

- **Monitor rate limits**
  - Respect Telegram's rate limits
  - Don't run multiple instances
  - Use appropriate delays

- **Check for updates**
  ```bash
  pip list --outdated
  pip install --upgrade telethon
  ```

## Data Security

### Exported Data:

1. **CSV files may contain sensitive data**
   ```gitignore
   *.csv
   messages.csv
   ```

2. **Protect exported files**
   ```bash
   chmod 600 *.csv
   ```

3. **Encrypt if sharing**
   ```bash
   # Example: using gpg
   gpg -c messages.csv
   # Share messages.csv.gpg, not messages.csv
   ```

4. **Delete when no longer needed**
   ```bash
   shred -u messages.csv  # Secure deletion
   ```

## Access Control

### File Permissions:

```bash
# Recommended permissions
chmod 755 main.py          # Executable scripts
chmod 644 README.md        # Documentation
chmod 600 .env             # Credentials
chmod 600 *.session        # Session files
chmod 644 requirements.txt # Public files
```

### Directory Permissions:

```bash
chmod 755 telegram_scraper/     # Project directory
chmod 700 telegram_scraper/.git # Git directory
```

## Incident Response

### If Credentials Are Compromised:

1. **Immediate Actions:**
   - [ ] Change API credentials at https://my.telegram.org
   - [ ] Delete compromised session files
   - [ ] Revoke old credentials
   - [ ] Create new credentials

2. **Git Repository Cleanup:**
   ```bash
   # If credentials were committed
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (WARNING: rewrites history)
   git push origin --force --all
   ```

3. **Verify Removal:**
   ```bash
   # Check Git history
   git log --all --full-history -- .env
   # Should return nothing
   ```

4. **Update All Machines:**
   - Pull latest changes
   - Delete old session files
   - Update credentials

### If Session File Is Exposed:

1. **Terminate all Telegram sessions:**
   - Open Telegram app
   - Settings → Privacy and Security → Active Sessions
   - Terminate all sessions
   - Log back in

2. **Delete exposed session files:**
   ```bash
   rm *.session*
   ```

3. **Re-authenticate:**
   ```bash
   python main.py <channel>
   # Will prompt for new authentication
   ```

## Regular Security Audits

### Weekly:
- [ ] Check for package updates
- [ ] Review `.gitignore`
- [ ] Verify no sensitive files in staging

### Monthly:
- [ ] Rotate API credentials (if high-security)
- [ ] Review Telegram active sessions
- [ ] Update dependencies
- [ ] Check for security advisories

### Before Public Release:
- [ ] Scan for hardcoded secrets
- [ ] Review all committed files
- [ ] Test `.gitignore` rules
- [ ] Verify example files are safe

## Security Tools

### Recommended Tools:

1. **git-secrets** - Prevent committing secrets
   ```bash
   git secrets --install
   git secrets --register-aws
   ```

2. **detect-secrets** - Find secrets in code
   ```bash
   pip install detect-secrets
   detect-secrets scan
   ```

3. **truffleHog** - Search Git history for secrets
   ```bash
   pip install truffleHog
   trufflehog git file://path/to/repo
   ```

4. **Safety** - Check for known vulnerabilities
   ```bash
   pip install safety
   safety check
   ```

## Compliance Checklist

### Telegram ToS Compliance:

- [ ] Using official API
- [ ] Respecting rate limits
- [ ] Not spamming or abusing service
- [ ] Proper attribution

### Legal Compliance:

- [ ] Have permission to access channels
- [ ] Comply with local data protection laws
- [ ] Respect privacy of channel members
- [ ] Proper data handling procedures

## Emergency Contacts

### If Security Breach Occurs:

1. **Telegram Support:**
   - Email: abuse@telegram.org
   - App: @TelegramAuditions (for serious issues)

2. **Project Maintainer:**
   - Check project repository for contact info

## Security Resources

### Documentation:
- Telegram API Security: https://core.telegram.org/api/security
- Git Security: https://git-scm.com/book/en/v2/GitHub-Account-Administration-and-Security
- Python Security: https://python.readthedocs.io/en/latest/library/security_warnings.html

### Best Practices:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/

---

## Quick Security Check

Run this before any commit:

```bash
# Quick security verification
echo "=== Security Check ==="
echo ""
echo "1. Checking for .env in staging:"
git status | grep ".env" && echo "❌ FAIL: .env is staged!" || echo "✓ PASS"
echo ""
echo "2. Checking for session files:"
git status | grep "session" && echo "❌ FAIL: Session files staged!" || echo "✓ PASS"
echo ""
echo "3. Checking for credentials in code:"
grep -r "api_id.*=.*[0-9]" *.py && echo "❌ FAIL: Hardcoded credentials!" || echo "✓ PASS"
echo ""
echo "4. Verifying .gitignore exists:"
[ -f .gitignore ] && echo "✓ PASS" || echo "❌ FAIL: No .gitignore!"
echo ""
echo "=== End Security Check ==="
```

**Remember**: Security is not a one-time task. Stay vigilant!

---

Last Updated: 2024
Version: 1.0
