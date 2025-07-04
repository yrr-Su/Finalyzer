import pickle
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By

from config.setting import CONFIG

# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.service import Service
user_agent = UserAgent().random

args = [
    f'user-agent={user_agent}',
    # '--headless=new',
    '--disable-gpu',
    "--window-size=1980,1080",
    '--ignore-certificate-errors',
    "--log-level=3",
    "start-maximized",
    "--disable-blink-features=AutomationControlled"
]

exp_args = [
            ('excludeSwitches', ['enable-automation']),
            ('useAutomationExtension', False),
            # ('prefs', {'download.default_directory' : str(Path())})
        ]

options = webdriver.ChromeOptions()
for arg in args:
    options.add_argument(arg)

for key, val in exp_args:
    options.add_experimental_option(key, val)


driver = webdriver.Chrome(options=options)

try:
    # Navigate to the login page
    driver.get("https://thefew.tw/cb")

    # Wait for the page to load
    time.sleep(1)
    # Click the login button on the top right
    login_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/nav/div[2]/div/div[2]/a"
        )
    login_button.click()

    # Wait for the page to load
    time.sleep(1)

    # Click the Google login button
    google_login_button = driver.find_element(
        By.XPATH,
        "/html/body/div/div/div/div/div[2]/a"
        )
    google_login_button.click()

    # Wait for the Google login page to load
    time.sleep(1)
    # Locate the username and password fields
    # Locate the email field and input email
    email_field = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/" \
        "div/div/div[1]/form/span/section/div/div/div[1]" \
        "/div/div[1]/div/div[1]/input"
        )
    # email = input("Enter your email: ")
    email_field.send_keys(CONFIG.GOOGLE_ACCOUNT)

    # Click the next button after entering email
    next_button_email = driver.find_element(
        By.XPATH,
        "//*[@id='identifierNext']/div/button/span"
        )
    next_button_email.click()

    # Wait for the password field to load
    time.sleep(1)
    # Locate the password field and input password
    password_field = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]" \
        "/div/div/div[1]/form/span/section[2]/div/div/div[1]/" \
        "div[1]/div/div/div/div/div[1]/div/div[1]/input"
        )
    # password = input("Enter your password: ")
    password_field.send_keys(CONFIG.GOOGLE_PASSWORD)

    # Click the next button after entering password
    next_button_password = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/c-wiz/div/" \
        "div[3]/div/div[1]/div/div/button/span"
        )
    next_button_password.click()

    # Submit the login form
    # password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete
    time.sleep(5)

    # Retrieve cookies
    cookies = driver.get_cookies()
    with open("thefew_cookie.pkl", "wb") as f:
        pickle.dump(cookies, f)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()

