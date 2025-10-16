from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time

class TrafikverketBooking:
    def __init__(self, headless=False, use_chromium=False):
        """
        Initialize the Selenium WebDriver
        
        Args:
            headless (bool): Run browser in headless mode
            use_chromium (bool): Use Chromium instead of Chrome
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')  # Helpful for headless mode
        
        # Use webdriver_manager to automatically download and manage ChromeDriver
        try:
            if use_chromium:
                driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            else:
                driver_path = ChromeDriverManager().install()
            
            # Extract the actual chromedriver executable path
            if 'THIRD_PARTY_NOTICES' in driver_path:
                import os
                driver_path = os.path.join(os.path.dirname(driver_path), 'chromedriver')
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error initializing ChromeDriver: {e}")
            print("Trying to find chromedriver in system PATH...")
            self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def login_with_bankid(self):
        """Handle the BankID login process"""
        print("Starting login process...")
        
        # Navigate to login page
        self.driver.get("https://fp.trafikverket.se/Boka/ng/")
        time.sleep(2)
        
        # Click on desktop login button
        try:
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "desktop-login-button"))
            )
            print("Found login button, clicking...")
            login_button.click()
            time.sleep(2)
        except TimeoutException:
            print("Could not find desktop-login-button")
            return False
        
        # Click on "Fortsätt" button
        try:
            fortsatt_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fortsätt')]"))
            )
            print("Found 'Fortsätt' button, clicking...")
            fortsatt_button.click()
            time.sleep(2)
        except TimeoutException:
            print("Could not find 'Fortsätt' button")
            return False
        
        # Wait for manual BankID authentication
        print("\n" + "="*60)
        print("PLEASE COMPLETE BANKID AUTHENTICATION ON YOUR DEVICE")
        print("="*60 + "\n")
        
        # Wait for user to complete BankID
        input("Press ENTER after you have completed BankID authentication...")
        
        time.sleep(2)
        print(f"Login completed. Current URL: {self.driver.current_url}")
        
        # Automatically redirect to booking page
        print("\nRedirecting to booking page...")
        self.navigate_to_booking_page()
        
        return True
    
    def navigate_to_booking_page(self):
        """Navigate to the booking search page"""
        print("Navigating to booking page...")
        self.driver.get("https://fp.trafikverket.se/Boka/ng/search/xYihrXpXhCRiRl/5/0/0/0")
        time.sleep(3)
        print(f"Current URL: {self.driver.current_url}")
    
    def fill_booking_form(self, search_criteria):
        """
        Fill the booking form with search criteria.
        Location can be a single string or a list of strings.
        
        Args:
            search_criteria (dict): Dictionary containing form fields
                Example: {
                    'examination_type': 'Körprov',
                    'location': ['Järfälla', 'Sollentuna'],
                    'vehicle_type': 'Automatbil'
                }
        """
        print("Filling booking form...")
        
        try:
            # Fill examination type dropdown
            if 'examination_type' in search_criteria:
                print(f"Setting examination type to: {search_criteria['examination_type']}")
                exam_dropdown = self.wait.until(
                    EC.presence_of_element_located((By.ID, "examination-type-select"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", exam_dropdown)
                time.sleep(0.5)
                from selenium.webdriver.support.ui import Select
                select = Select(exam_dropdown)
                select.select_by_visible_text(search_criteria['examination_type'])
                time.sleep(0.5)
                print(f"✓ Examination type set to: {search_criteria['examination_type']}")
            
            # Fill location field
            if 'location' in search_criteria:
                locations = search_criteria['location']
                if isinstance(locations, str):
                    locations = [loc.strip() for loc in locations.split(',')]
                
                print(f"Setting locations to: {', '.join(locations)}")
                
                # Click the location button to open popup
                location_button = self.wait.until(EC.element_to_be_clickable((By.ID, "select-location-search")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_button)
                time.sleep(0.5)
                location_button.click()
                time.sleep(0.5)
                print("✓ Opened location popup")
                
                # Loop through each location and add it
                for loc in locations:
                    print(f"  - Adding location: {loc}")
                    location_input = self.wait.until(EC.presence_of_element_located((By.ID, "location-search-input")))
                    location_input.clear()
                    location_input.send_keys(loc)
                    time.sleep(1.5)
                    print(f"    ✓ Entered '{loc}' in search box")
                    
                    location_container = self.wait.until(EC.presence_of_element_located((By.ID, "location-container")))
                    location_buttons = location_container.find_elements(By.TAG_NAME, "button")
                    
                    if not location_buttons:
                        print(f"    ⚠ No location found for '{loc}'. Skipping.")
                        continue

                    print(f"    ✓ Found {len(location_buttons)} match(es) for '{loc}'")
                    for idx, btn in enumerate(location_buttons):
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                            time.sleep(0.2)
                            btn.click()
                            print(f"    ✓ Clicked location button {idx + 1}")
                        except Exception as e:
                            print(f"    Could not click button {idx + 1}: {e}")
                    time.sleep(0.5)

                # Click the Bekräfta (Confirm) button
                confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Bekräfta')]" )))
                confirm_button.click()
                time.sleep(0.5)
                print(f"✓ All locations confirmed: {', '.join(locations)}")
            
            # Fill vehicle type dropdown
            if 'vehicle_type' in search_criteria:
                print(f"Setting vehicle type to: {search_criteria['vehicle_type']}")
                vehicle_dropdown = self.wait.until(
                    EC.presence_of_element_located((By.ID, "vehicle-select"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vehicle_dropdown)
                time.sleep(0.5)
                select = Select(vehicle_dropdown)
                select.select_by_visible_text(search_criteria['vehicle_type'])
                time.sleep(0.5)
                print(f"✓ Vehicle type set to: {search_criteria['vehicle_type']}")
            
            print("\n✓ All form fields filled successfully!")
            time.sleep(1)
            
        except Exception as e:
            print(f"Error filling form: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
    
    def check_for_available_times(self):
        """
        Check if there are available times or if the 'no times available' message appears.
        This is now more robust, waiting for either the success or failure message.
        
        Returns:
            bool: True if times are available, False if not
        """
        try:
            # Wait up to 10 seconds for either the success state (slots) or failure state (no times message)
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Hittar inga lediga tider som matchar dina val')]")),
                    EC.presence_of_element_located((By.CLASS_NAME, "appointment-slot"))
                )
            )
            
            # Now that we know one of the conditions is met, we check for the "no times" message.
            # If it's not there, it means appointment slots were found.
            no_times_message = self.driver.find_elements(
                By.XPATH, 
                "//*[contains(text(), 'Hittar inga lediga tider som matchar dina val')]"
            )
            
            if no_times_message:
                print("⚠ No available times found")
                return False
            else:
                print("✓ Available times found!")
                return True
                
        except TimeoutException:
            # This can happen if the page returns neither a message nor slots (e.g., an empty results page)
            print("⚠ Timed out waiting for search results. Assuming no times are available.")
            return False
        except Exception as e:
            print(f"Error checking for available times: {e}")
            return False
    
    def play_beep(self):
        """Play a system beep sound"""
        import sys
        if sys.platform == "linux" or sys.platform == "linux2":
            # Linux
            import os
            os.system('echo -e "\a"')
            # Alternative: paplay /usr/share/sounds/freedesktop/stereo/complete.oga
        elif sys.platform == "darwin":
            # macOS
            import os
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif sys.platform == "win32":
            # Windows
            import winsound
            winsound.Beep(1000, 500)  # frequency, duration in ms
    
    def book_appointment(self, appointment_index=0):
        """
        Book an available appointment
        
        Args:
            appointment_index (int): Index of the appointment to book (0 for first available)
        """
        print("Attempting to book appointment...")
        
        try:
            # Find available appointment slots (adjust selector based on actual page)
            appointments = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "appointment-slot"))  # Update selector
            )
            
            if len(appointments) == 0:
                print("No appointments available")
                return False
            
            print(f"Found {len(appointments)} available appointments")
            
            # Click on the selected appointment
            appointments[appointment_index].click()
            time.sleep(2)
            
            # Confirm booking (adjust selector as needed)
            confirm_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Boka') or contains(text(), 'Bekräfta')]"))
            )
            confirm_button.click()
            
            print("Appointment booked successfully!")
            return True
            
        except Exception as e:
            print(f"Error booking appointment: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        print("Closing browser...")
        self.driver.quit()

def main():
    """Main execution function"""
    # Set use_chromium=True if you installed Chromium instead of Chrome
    bot = TrafikverketBooking(headless=False, use_chromium=False)
    
    try:
        # Step 1: Login with BankID (will automatically redirect to booking page)
        if not bot.login_with_bankid():
            print("Login failed")
            return
        
        # Now you're on the booking page
        print("\n" + "="*60)
        print("YOU ARE NOW ON THE BOOKING PAGE")
        print("="*60 + "\n")
        
        # Define your search criteria here
        search_criteria = {
            'examination_type': 'Körprov',
            'location': 'Uppsala,Uppland,Järfälla',  # Comma-separated locations
            'vehicle_type': 'Automatbil'
        }
        
        locations = [loc.strip() for loc in search_criteria['location'].split(',')]
        print(f"Bot will search for appointments in the following locations: {', '.join(locations)}")

        # Loop until available times are found
        attempt = 1
        while True:
            print(f"\n{'='*60}")
            print(f"ATTEMPT #{attempt}")
            print(f"{'='*60}\n")
            
            # Step 2: Fill the booking form. The form should auto-submit after the last field.
            print("Filling form fields...")
            if not bot.fill_booking_form(search_criteria):
                print("Failed to fill form. Retrying after a refresh...")
                time.sleep(5)
                bot.navigate_to_booking_page()
                continue

            # Step 3: Check for available times. This will wait for the results to load.
            if bot.check_for_available_times():
                # Times found! Play beep and stop
                print("\n" + "🎉"*30)
                print("AVAILABLE TIMES FOUND!")
                print("Please check the browser to complete the booking.")
                print("🎉"*30 + "\n")
                
                # Play system beep multiple times
                for _ in range(10):
                    bot.play_beep()
                    time.sleep(0.5)
                
                # Keep browser open for manual booking
                input("\nPress ENTER to close the browser...")
                break
            else:
                # No times found, wait and try again
                print(f"\n⏳ No times found. Waiting 60 seconds before next attempt...")
                time.sleep(60)
                attempt += 1
                
                # Refresh the page to try again
                bot.navigate_to_booking_page()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Script interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.close()

if __name__ == "__main__":
    main()
