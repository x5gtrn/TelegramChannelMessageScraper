#!/bin/bash

# Telegram Scraper Setup Script
# Automates the setup process for the Telegram channel scraper

set -e

echo "====================================="
echo "Telegram Channel Scraper Setup"
echo "====================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "Error: Python 3.7 or higher is required. You have Python $python_version"
    exit 1
fi

echo "Python version: $python_version ✓"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created ✓"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Activated ✓"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed ✓"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created ✓"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Telegram API credentials"
    echo "   Get credentials from: https://my.telegram.org/auth"
    echo ""
else
    echo ".env file already exists ✓"
    echo ""
fi

# Display next steps
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Telegram API credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the scraper: python main.py <channel_username>"
echo ""
echo "For more information, see README.md"
echo ""
