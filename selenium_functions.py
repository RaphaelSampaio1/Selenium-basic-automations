"""
SELENIUM PYTHON RPA CHEAT SHEET
Save this file as a reference. All commands are simplified and ready to copy.
Prerequisites: pip install selenium
For video recording: pip install subprocess (built-in) + ensure ffmpeg is installed on your OS.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import subprocess
import os

# ==============================================================================
# 1. DRIVER SETUP & CONFIGURATION
# ==============================================================================
def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Run in background
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    
    # Auto-download files to a specific folder without prompts
    download_dir = os.path.join(os.getcwd(), "downloads")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # Initialize driver (Service is optional in newer Selenium versions but recommended)
    driver = webdriver.Chrome(options=options)
    return driver

# ==============================================================================
# 2. NAVIGATION
# ==============================================================================
def navigation_examples(driver):
    driver.get("https://example.com")       # Open URL
    driver.back()                           # Go back
    driver.forward()                        # Go forward
    driver.refresh()                        # Refresh page
    current_url = driver.current_url        # Get current URL
    title = driver.title                    # Get page title

# ==============================================================================
# 3. FINDING ELEMENTS (LOCATORS)
# ==============================================================================
def locator_examples(driver):
    # Find SINGLE element (raises NoSuchElementException if not found)
    elem_id = driver.find_element(By.ID, "submit-btn")
    elem_name = driver.find_element(By.NAME, "username")
    elem_xpath = driver.find_element(By.XPATH, "//button[@class='primary']")
    elem_css = driver.find_element(By.CSS_SELECTOR, "div.container > input")
    elem_class = driver.find_element(By.CLASS_NAME, "form-control")
    elem_tag = driver.find_element(By.TAG_NAME, "h1")
    elem_link = driver.find_element(By.LINK_TEXT, "Click Here")
    elem_partial = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

    # Find MULTIPLE elements (returns a list, empty list if none found)
    all_rows = driver.find_elements(By.XPATH, "//table/tr")

# ==============================================================================
# 4. BASIC INTERACTIONS
# ==============================================================================
def basic_interactions(driver):
    elem = driver.find_element(By.ID, "input-field")
    
    elem.clear()                            # Clear existing text
    elem.send_keys("Hello World")           # Type text
    elem.send_keys(Keys.ENTER)              # Press Enter key
    elem.send_keys(Keys.TAB)                # Press Tab key
    
    elem.click()                            # Left click
    elem.is_displayed()                     # Returns True if visible
    elem.is_enabled()                       # Returns True if interactive
    elem.is_selected()                      # Returns True if checkbox/radio is checked

# ==============================================================================
# 5. ADVANCED INTERACTIONS (ActionChains)
# ==============================================================================
def advanced_interactions(driver):
    actions = ActionChains(driver)
    elem = driver.find_element(By.ID, "menu-item")
    target = driver.find_element(By.ID, "drop-zone")
    
    actions.move_to_element(elem).perform()         # Hover / Pass mouse over
    actions.double_click(elem).perform()            # Double click
    actions.context_click(elem).perform()           # Right click
    actions.drag_and_drop(elem, target).perform()   # Drag and drop
    # Alternative drag and drop with offset:
    # actions.click_and_hold(elem).move_by_offset(50, 50).release().perform()

# ==============================================================================
# 6. DATA EXTRACTION
# ==============================================================================
def extraction_examples(driver):
    elem = driver.find_element(By.ID, "result")
    
    text = elem.text                                # Get visible text
    href = elem.get_attribute("href")               # Get attribute (href, value, class, etc.)
    
    # --- EXTRACT TABLE DATA ---
    table_data = []
    rows = driver.find_elements(By.XPATH, "//table[@id='myTable']//tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        # Extract text from each column, strip whitespace
        row_data = [col.text.strip() for col in cols]
        if row_data:  # Avoid empty rows
            table_data.append(row_data)
    # table_data is now a list of lists: [['col1', 'col2'], ['col1', 'col2']]

# ==============================================================================
# 7. DROPDOWNS (Select Class)
# ==============================================================================
def dropdown_examples(driver):
    dropdown = Select(driver.find_element(By.ID, "country-select"))
    
    dropdown.select_by_visible_text("Brazil")       # Select by visible text
    dropdown.select_by_value("BR")                  # Select by value attribute
    dropdown.select_by_index(1)                     # Select by index (0-based)
    
    all_options = dropdown.options                  # Get all options
    first_selected = dropdown.first_selected_option.text # Get currently selected

# ==============================================================================
# 8. FILE OPERATIONS (Upload & Download)
# ==============================================================================
def file_operations(driver):
    # UPLOAD: Find the <input type="file"> and send absolute path
    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
    upload_input.send_keys(os.path.abspath("document.pdf"))
    
    # DOWNLOAD: Handled automatically if Chrome options (Section 1) are set correctly.
    # Just click the download button:
    # driver.find_element(By.ID, "download-btn").click()

# ==============================================================================
# 9. WAITS (CRITICAL FOR RPA)
# ==============================================================================
def wait_examples(driver):
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    
    # Wait until element is present in DOM
    elem = wait.until(EC.presence_of_element_located((By.ID, "dynamic-element")))
    
    # Wait until element is visible
    elem = wait.until(EC.visibility_of_element_located((By.ID, "modal")))
    
    # Wait until element is clickable
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submit']")))
    btn.click()

# ==============================================================================
# 10. WINDOWS, TABS, AND FRAMES
# ==============================================================================
def window_frame_examples(driver):
    # Switch to new tab/window (index 1 is the second tab)
    driver.switch_to.window(driver.window_handles[1])
    
    # Switch back to original tab
    driver.switch_to.window(driver.window_handles[0])
    
    # Switch to iframe
    driver.switch_to.frame("iframe_name_or_id")
    # OR driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    
    # Return to main page content
    driver.switch_to.default_content()

# ==============================================================================
# 11. ALERTS & POPUPS
# ==============================================================================
def alert_examples(driver):
    alert = driver.switch_to.alert
    
    alert_text = alert.text           # Get alert message
    alert.accept()                    # Click "OK"
    # alert.dismiss()                 # Click "Cancel"
    # alert.send_keys("Some text")    # Send text to prompt alert

# ==============================================================================
# 12. COOKIES HANDLING
# ==============================================================================
def cookie_examples(driver):
    cookies = driver.get_cookies()                # Get all cookies (list of dicts)
    
    # Add a specific cookie
    driver.add_cookie({"name": "session_id", "value": "12345abcde", "domain": "example.com"})
    
    driver.delete_cookie("session_id")            # Delete specific cookie
    driver.delete_all_cookies()                   # Clear all cookies

# ==============================================================================
# 13. SCREENSHOTS
# ==============================================================================
def screenshot_examples(driver):
    # Full page screenshot
    driver.save_screenshot("full_page.png")
    
    # Specific element screenshot (Selenium 4+)
    elem = driver.find_element(By.ID, "chart")
    elem.screenshot("element_only.png")

# ==============================================================================
# 14. VIDEO RECORDING (RPA Workaround)
# ==============================================================================
# Selenium has NO native video recording. The standard RPA approach is using 
# FFmpeg via subprocess. Ensure 'ffmpeg' is installed on your system.
def start_recording(output_file="recording.mp4"):
    """Starts ffmpeg screen recording in the background."""
    command = [
        "ffmpeg", "-f", "gdigrab", "-framerate", "10", "-i", "desktop",
        "-vcodec", "libx264", "-preset", "ultrafast", output_file
    ]
    # For Linux/Mac, replace "-f", "gdigrab", "-i", "desktop" with "-f", "x11grab", "-i", ":0.0"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_recording(process):
    """Stops the ffmpeg recording process."""
    process.terminate()
    process.wait()

# ==============================================================================
# 15. JAVASCRIPT EXECUTION
# ==============================================================================
def js_examples(driver):
    # Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Scroll to a specific element
    elem = driver.find_element(By.ID, "footer")
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    
    # Click an element that is blocked by another overlay (force click)
    driver.execute_script("arguments[0].click();", elem)
    
    # Return a value from JS
    page_height = driver.execute_script("return document.body.scrollHeight;")

# ==============================================================================
# MAIN EXECUTION EXAMPLE
# ==============================================================================
if __name__ == "__main__":
    driver = setup_driver()
    
    try:
        driver.get("https://sampaiodev-rpa-desafios.vercel.app/")
        
        # Example: Wait, Interact, Extract
        wait = WebDriverWait(driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.ID, "some-button")))
        btn.click()
        
        print("Page Title:", driver.title)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # ALWAYS quit the driver to free up memory and close the browser
        driver.quit()