# Trafikverket Booking Bot

Automated booking script for Swedish driving test appointments (körprov) on Trafikverket's website. The bot automatically monitors for available appointment slots and alerts you when one becomes available.

## Features

- ✅ Automated BankID login flow
- ✅ Automatic form filling (examination type, location, vehicle type)
- ✅ Continuous monitoring for available appointment slots
- ✅ Audible alert when appointments are found
- ✅ Auto-retry every 60 seconds if no slots available
- ✅ Keeps browser open for manual booking completion

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Swedish BankID (for authentication)

## Installation

### 1. Clone or Download

Download the project files to your local machine:

```bash
mkdir trafikverket-booking
cd trafikverket-booking
```

### 2. Create Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies

Create a `requirements.txt` file with the following content:

```
selenium==4.26.1
webdriver-manager==4.0.2
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Install Google Chrome

**Ubuntu/Debian:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
google-chrome --version
```

**Fedora/RHEL/CentOS:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo dnf install ./google-chrome-stable_current_x86_64.rpm
google-chrome --version
```

**macOS:**
```bash
brew install --cask google-chrome
```

**Windows:**
Download and install from: https://www.google.com/chrome/

### 5. Install ChromeDriver

**Automatic (Recommended):**
The script uses `webdriver-manager` which automatically downloads the correct ChromeDriver version. However, if you encounter issues, follow the manual installation:

**Manual Installation:**

```bash
# 1. Check your Chrome version
google-chrome --version

# 2. Download matching ChromeDriver (replace 141.0.7390.76 with your version)
wget https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.76/linux64/chromedriver-linux64.zip

# 3. Extract and install
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 4. Verify installation
chromedriver --version

# 5. Clean up
rm -rf chromedriver-linux64 chromedriver-linux64.zip
```

**If webdriver-manager has issues:**
```bash
# Clear the cache
rm -rf ~/.wdm

# Run the script again
python book_appointment.py
```

## Configuration

### Customize Search Criteria

Edit the `search_criteria` dictionary in the `main()` function:

```python
search_criteria = {
    'examination_type': 'Körprov',      # Exam type
    'location': 'Järfälla',             # Location
    'vehicle_type': 'Automatbil'        # Vehicle type (Automatbil/Manuell)
}
```

### Available Options

**Examination Types:**
- `Körprov` - Driving test
- Other types available on the website

**Vehicle Types:**
- `Automatbil` - Automatic transmission
- `Manuell` - Manual transmission

**Locations:**
- Any valid location from Trafikverket (e.g., Stockholm, Göteborg, Malmö, Järfälla, etc.)

### Adjust Check Interval

Change the wait time between checks (default is 60 seconds):

```python
# In main() function, find this line:
time.sleep(60)  # Change 60 to your desired seconds
```

## Usage

### Run the Bot

1. Activate your virtual environment (if not already activated):
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

2. Run the script:
   ```bash
   python book_appointment.py
   ```

### Workflow

1. **Browser Opens**: Chrome will open and navigate to Trafikverket login page
2. **Login Process**:
   - Script clicks "desktop-login-button"
   - Script clicks "Fortsätt" button
   - **YOU MUST**: Complete BankID authentication on your device
   - Press ENTER in terminal after authentication completes
3. **Automatic Form Filling**: Script fills examination type, location, and vehicle type
4. **Monitoring Loop**:
   - Script checks for available appointment slots
   - If no slots found: waits 60 seconds and tries again
   - If slots found: plays continuous beep alert
5. **Alert**: When appointments are available:
   - Continuous beeping starts 🔔
   - Browser shows available slots
   - Press ENTER to stop beeping
6. **Manual Booking**: Complete your booking manually in the browser
7. **Close**: Press ENTER to close the browser

### Stop the Script

- Press `Ctrl+C` at any time to stop the monitoring
- Press `ENTER` when prompted to close the browser

## Troubleshooting

### ChromeDriver Issues

**Error: "google-chrome: not found"**
```bash
# Install Google Chrome (see Installation section)
```

**Error: "Exec format error" or ChromeDriver mismatch**
```bash
# Clear webdriver cache
rm -rf ~/.wdm

# Run script again
python book_appointment.py
```

**Error: ChromeDriver version mismatch**
```bash
# Update Chrome browser
sudo apt update && sudo apt upgrade google-chrome-stable

# Or manually download matching ChromeDriver
```

### Virtual Environment Issues

**Deactivate virtual environment:**
```bash
deactivate
```

**Reactivate virtual environment:**
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**Delete and recreate:**
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Script Issues

**Element not found errors:**
- Trafikverket may have updated their website
- Check if element IDs have changed
- Run with browser visible (not headless) to debug

**BankID timeout:**
- Make sure you complete BankID authentication quickly
- Check that your BankID app is working

**No beep sound:**
- On Linux, make sure system sound is enabled
- Try alternative: `sudo apt install beep` then use `beep` command

### Headless Mode

To run without showing the browser window:

```python
# In main() function, change:
bot = TrafikverketBooking(headless=True, use_chromium=False)
```

Note: Not recommended for first-time use as you need to complete BankID authentication.

## Project Structure

```
trafikverket-booking/
├── .venv/                      # Virtual environment (gitignored)
├── book_appointment.py         # Main script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                 # Git ignore file (optional)
```

## Optional: Git Setup

Create a `.gitignore` file:

```
.venv/
__pycache__/
*.pyc
.DS_Store
*.log
chromedriver
```

## How It Works

### Login Flow
1. Opens Trafikverket booking page
2. Clicks desktop login button
3. Clicks "Fortsätt" (Continue)
4. Waits for manual BankID authentication
5. Redirects to booking search page

### Form Filling
1. **Examination Type**: Selects from dropdown using Selenium Select
2. **Location**: 
   - Clicks location button to open popup
   - Enters location in search textbox
   - Clicks all matching location buttons
   - Confirms with "Bekräfta" button
3. **Vehicle Type**: Selects from dropdown using Selenium Select

### Monitoring
- Checks page for "Hittar inga lediga tider som matchar dina val" message
- If found: waits 60 seconds, refreshes, and tries again
- If not found: assumes slots are available and triggers alert

### Alert System
- Uses system beep (`echo -e "\a"` on Linux, `afplay` on macOS, `winsound.Beep` on Windows)
- Beeps continuously in separate thread until user presses ENTER
- Keeps browser open for manual booking

## Customization

### Change Booking URL

Edit the URL in `navigate_to_booking_page()` method:

```python
def navigate_to_booking_page(self):
    self.driver.get("YOUR_BOOKING_URL_HERE")
    time.sleep(3)
```

### Use Chromium Instead of Chrome

```python
bot = TrafikverketBooking(headless=False, use_chromium=True)
```

### Adjust Timeouts

Modify the WebDriverWait timeout (default is 30 seconds):

```python
self.wait = WebDriverWait(self.driver, 30)  # Change 30 to desired seconds
```

## Legal & Ethical Considerations

- ⚠️ This bot is for personal use only
- ⚠️ Respect Trafikverket's terms of service
- ⚠️ Do not run multiple instances simultaneously
- ⚠️ Be mindful of server load
- ⚠️ Use reasonable check intervals (60+ seconds recommended)

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify Chrome and ChromeDriver versions match
3. Make sure all dependencies are installed
4. Check that Trafikverket website hasn't changed

## License

This script is provided as-is for educational purposes. Use at your own risk.

## Version History

- **v1.0.0** (2025-10-11)
  - Initial release
  - BankID authentication support
  - Automatic form filling
  - Continuous monitoring with alerts
  - Multi-platform beep support

---

**Note**: This is an unofficial tool and is not affiliated with or endorsed by Trafikverket.