import random
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up a list of random user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # Add more user agents as needed
]

# Telegram bot credentials
telegram_token = '7590799899:AAGWjV76tWQCT7ddebglJ09Iv6AigWhg17E'
chat_id = '6065149701'

# Twitter handle to monitor
handle = input("Enter Twitter handle to monitor: ")
twitter_url = f'https://x.com/{handle}'

# Function to set up a new Selenium WebDriver with a random user agent and cookies
def setup_driver():
    # Randomly select a user agent from the list
    user_agent = random.choice(user_agents)
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')  # Run in headless mode for background execution
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Set up the WebDriver
    service = Service('/path/to/chromedriver')  # Update path to your chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    # Rotate cookies: You can set new cookies if needed here
    driver.get("https://x.com")
    time.sleep(2)  # Wait for the page to load

    # Clear cookies and load any specific cookies if needed
    driver.delete_all_cookies()
    # Example of setting a specific cookie
    driver.add_cookie({"name": "example_cookie", "value": "cookie_value_here"})
    
    return driver

def get_following_count(driver):
    """Retrieve the following count from a Twitter profile."""
    driver.get(twitter_url)
    try:
        # Wait until the following count element is visible
        following_count_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@href,'/following')]//span[1]"))
        )
        following_count = int(following_count_element.text.replace(',', ''))
        return following_count
    except Exception as e:
        print("Error retrieving following count:", e)
        return None

def send_telegram_message(message):
    """Send a message to Telegram."""
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Telegram notification sent.")
    else:
        print("Failed to send Telegram notification.")

# Initialize driver and get initial following count
driver = setup_driver()
try:
    previous_following_count = get_following_count(driver)
    print(f"Initial following count for {handle}: {previous_following_count}")
except Exception as e:
    print("Error retrieving initial following count:", e)
    driver.quit()
    exit()

# Loop to monitor changes in following count
while True:
    try:
        # Rotate user-agent and cookies by creating a new driver
        driver.quit()
        driver = setup_driver()

        current_following_count = get_following_count(driver)
        if current_following_count is not None and current_following_count > previous_following_count:
            new_follows = current_following_count - previous_following_count
            message = f"{handle} just followed {new_follows} new accounts."
            send_telegram_message(message)
            previous_following_count = current_following_count

        # Wait 60 seconds before checking again (adjust as needed)
        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
