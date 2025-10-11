#!/bin/bash

# Trafikverket Booking Bot - Setup Script
# This script automates the installation process for Linux systems

set -e  # Exit on any error

echo "=============================================="
echo "Trafikverket Booking Bot - Setup Script"
echo "=============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    print_info "Detected OS: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_info "Detected OS: macOS"
else
    print_error "Unsupported OS: $OSTYPE"
    exit 1
fi

echo ""
echo "Step 1: Checking Python installation..."
echo "----------------------------------------"

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 3 is installed: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed"
    echo "Please install Python 3.7 or higher:"
    if [ "$OS" == "linux" ]; then
        echo "  sudo apt update && sudo apt install python3 python3-venv python3-pip"
    else
        echo "  brew install python3"
    fi
    exit 1
fi

echo ""
echo "Step 2: Creating virtual environment..."
echo "----------------------------------------"

# Create virtual environment
if [ -d ".venv" ]; then
    print_info "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
        print_success "Virtual environment recreated"
    fi
else
    python3 -m venv .venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source .venv/bin/activate
print_success "Virtual environment activated"

echo ""
echo "Step 3: Creating requirements.txt..."
echo "----------------------------------------"

# Create requirements.txt
cat > requirements.txt << EOF
selenium==4.26.1
webdriver-manager==4.0.2
EOF

print_success "requirements.txt created"

echo ""
echo "Step 4: Installing Python dependencies..."
echo "----------------------------------------"

pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

echo ""
echo "Step 5: Checking Google Chrome installation..."
echo "----------------------------------------"

# Check if Chrome is installed
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version)
    print_success "Google Chrome is installed: $CHROME_VERSION"
    CHROME_INSTALLED=true
elif command -v chromium-browser &> /dev/null; then
    CHROMIUM_VERSION=$(chromium-browser --version)
    print_success "Chromium is installed: $CHROMIUM_VERSION"
    CHROME_INSTALLED=true
elif command -v chromium &> /dev/null; then
    CHROMIUM_VERSION=$(chromium --version)
    print_success "Chromium is installed: $CHROMIUM_VERSION"
    CHROME_INSTALLED=true
else
    print_error "Google Chrome is not installed"
    CHROME_INSTALLED=false
fi

if [ "$CHROME_INSTALLED" = false ]; then
    echo ""
    read -p "Do you want to install Google Chrome now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ "$OS" == "linux" ]; then
            # Detect Linux distribution
            if [ -f /etc/debian_version ]; then
                # Debian/Ubuntu
                echo "Installing Google Chrome for Debian/Ubuntu..."
                wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
                sudo apt install -y ./google-chrome-stable_current_amd64.deb
                rm google-chrome-stable_current_amd64.deb
                print_success "Google Chrome installed"
            elif [ -f /etc/redhat-release ]; then
                # Fedora/RHEL/CentOS
                echo "Installing Google Chrome for Fedora/RHEL/CentOS..."
                wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
                sudo dnf install -y ./google-chrome-stable_current_x86_64.rpm
                rm google-chrome-stable_current_x86_64.rpm
                print_success "Google Chrome installed"
            else
                print_error "Unsupported Linux distribution"
                print_info "Please install Google Chrome manually"
            fi
        elif [ "$OS" == "macos" ]; then
            if command -v brew &> /dev/null; then
                brew install --cask google-chrome
                print_success "Google Chrome installed"
            else
                print_error "Homebrew not found. Please install Chrome manually from:"
                echo "  https://www.google.com/chrome/"
            fi
        fi
    else
        print_info "Skipping Chrome installation"
        print_info "You can install it later with:"
        if [ "$OS" == "linux" ]; then
            echo "  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
            echo "  sudo apt install ./google-chrome-stable_current_amd64.deb"
        else
            echo "  brew install --cask google-chrome"
        fi
    fi
fi

echo ""
echo "Step 6: Setting up ChromeDriver..."
echo "----------------------------------------"

print_info "ChromeDriver will be downloaded automatically by webdriver-manager"
print_info "If you encounter issues, you can clear the cache with: rm -rf ~/.wdm"
print_success "ChromeDriver setup configured"

echo ""
echo "Step 7: Creating .gitignore..."
echo "----------------------------------------"

# Create .gitignore
cat > .gitignore << EOF
.venv/
__pycache__/
*.pyc
.DS_Store
*.log
chromedriver
google-chrome-stable_current_amd64.deb
google-chrome-stable_current_x86_64.rpm
EOF

print_success ".gitignore created"

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
print_success "Virtual environment created and activated"
print_success "Python dependencies installed"
print_success "Chrome/Chromium checked"
print_success "Project files created"
echo ""
echo "Next steps:"
echo "1. Make sure book_appointment.py is in this directory"
echo "2. Run the bot with:"
echo "   source .venv/bin/activate"
echo "   python book_appointment.py"
echo ""
echo "To deactivate virtual environment later, run:"
echo "   deactivate"
echo ""
print_info "If you encounter ChromeDriver issues, run:"
echo "   rm -rf ~/.wdm"
echo ""
echo "Happy booking! 🚗"
echo ""