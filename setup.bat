@echo off
REM Telegram Scraper Setup Script for Windows
REM Automates the setup process for the Telegram channel scraper

echo =====================================
echo Telegram Channel Scraper Setup
echo =====================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org
    pause
    exit /b 1
)

python --version
echo Python found!
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Activated!
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed!
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created!
    echo.
    echo WARNING: Edit .env file and add your Telegram API credentials
    echo          Get credentials from: https://my.telegram.org/auth
    echo.
) else (
    echo .env file already exists!
    echo.
)

echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo Next steps:
echo 1. Edit .env file with your Telegram API credentials
echo 2. Activate the virtual environment: venv\Scripts\activate
echo 3. Run the scraper: python main.py ^<channel_username^>
echo.
echo For more information, see README.md
echo.
pause
