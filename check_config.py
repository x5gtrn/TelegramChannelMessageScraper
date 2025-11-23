#!/usr/bin/env python3
"""
Configuration Checker
Validates the Telegram scraper configuration before running.
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    import yaml
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def check_env_file():
    """Check if .env file exists and has required variables."""
    print("Checking .env file...")
    
    if not os.path.exists(".env"):
        print("  ❌ .env file not found")
        print("  Create it from .env.example: cp .env.example .env")
        return False
    
    load_dotenv()
    
    required_vars = {
        "TELEGRAM_API_ID": "Telegram API ID",
        "TELEGRAM_API_HASH": "Telegram API Hash",
        "TELEGRAM_PHONE": "Phone number",
    }
    
    all_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            print(f"  ❌ {var} not set ({description})")
            all_ok = False
        elif value == "12345678" or value == "your_api_hash_here" or value == "+1234567890":
            print(f"  ⚠️  {var} has example value - please set real credentials")
            all_ok = False
        else:
            # Mask sensitive values
            if "HASH" in var or "PHONE" in var:
                masked = value[:4] + "****" + value[-4:] if len(value) > 8 else "****"
                print(f"  ✓ {var} = {masked}")
            else:
                print(f"  ✓ {var} = {value}")
    
    return all_ok


def check_config_file():
    """Check if config.yaml exists and is valid."""
    print("\nChecking config.yaml...")
    
    if not os.path.exists("config.yaml"):
        print("  ⚠️  config.yaml not found (optional)")
        return True
    
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        
        print(f"  ✓ config.yaml is valid YAML")
        print(f"  Session name: {config.get('session_name', 'telegram_session')}")
        print(f"  Output file: {config.get('output_file', 'messages.csv')}")
        print(f"  Rate limit delay: {config.get('rate_limit_delay', 1)} ms")
        
        return True
    except Exception as e:
        print(f"  ❌ config.yaml has errors: {e}")
        return False


def check_dependencies():
    """Check if all required packages are installed."""
    print("\nChecking dependencies...")
    
    required_packages = [
        ("telethon", "Telethon"),
        ("tqdm", "tqdm"),
        ("yaml", "PyYAML"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} not installed")
            all_ok = False
    
    if not all_ok:
        print("\n  Install missing packages: pip install -r requirements.txt")
    
    return all_ok


def check_file_permissions():
    """Check if we have write permissions for output."""
    print("\nChecking file permissions...")
    
    try:
        # Check if we can write to current directory
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("  ✓ Write permission in current directory")
        return True
    except Exception as e:
        print(f"  ❌ Cannot write to current directory: {e}")
        return False


def check_session_file():
    """Check if session file exists."""
    print("\nChecking session file...")
    
    session_files = list(Path(".").glob("*.session"))
    
    if session_files:
        print(f"  ✓ Found {len(session_files)} session file(s)")
        for session in session_files:
            print(f"    - {session.name}")
        print("  Note: You won't need to authenticate again")
    else:
        print("  ℹ️  No session file found")
        print("  Note: You'll need to authenticate on first run")
    
    return True


def main():
    """Run all configuration checks."""
    print("=" * 50)
    print("Telegram Scraper Configuration Checker")
    print("=" * 50)
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_env_file),
        ("Configuration File", check_config_file),
        ("File Permissions", check_file_permissions),
        ("Session Files", check_session_file),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\nError in {check_name}: {e}")
            results[check_name] = False
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} {check_name}")
        if not result:
            all_passed = False
    
    print()
    
    if all_passed:
        print("✓ All checks passed! You're ready to run the scraper.")
        print("\nRun: python main.py <channel_username>")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nFor help, see README.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
