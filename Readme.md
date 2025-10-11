# Trafikverket Booking Bot

Automated booking script for Swedish driving test appointments (körprov). Monitors for available slots and alerts you when found.

## Quick Setup

### 1. Install Google Chrome

**Ubuntu/Debian:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

**Or run the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Setup Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
selenium==4.26.1
webdriver-manager==4.0.2
```

### 4. Install ChromeDriver

ChromeDriver is downloaded automatically by the script. If you have issues:

```bash
# Clear cache and retry
rm -rf ~/.wdm
```

## Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the bot
python book_appointment.py
```

### Configuration

Edit in `book_appointment.py`:

```python
search_criteria = {
    'examination_type': 'Körprov',
    'location': 'Järfälla',
    'vehicle_type': 'Automatbil'
}
```

## How It Works

1. Opens browser and waits for you to complete BankID login
2. Fills the booking form automatically
3. Checks for available appointments every 60 seconds
4. Plays continuous beep when slots are found
5. Keeps browser open for you to complete booking

## Troubleshooting

**ChromeDriver errors:**
```bash
rm -rf ~/.wdm
python book_appointment.py
```

**Chrome not found:**
```bash
# Install Chrome (see setup section above)
```

**Stop the script:**
- Press `Ctrl+C`

---

**Note:** For personal use only. Respect Trafikverket's terms of service.