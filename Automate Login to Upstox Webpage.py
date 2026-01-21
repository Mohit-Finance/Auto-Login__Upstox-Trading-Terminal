import os
import sys
import time
import json
import pyotp
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##############################################################################

def show_totp(secret):
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    return otp

os.makedirs('Credentials', exist_ok=True)

if not os.path.exists('Credentials/login_details.json'):
    print("User Details not found. First Create a User Base & Retry. Exiting program:", end=" ")
    sys.exit()

with open('Credentials/login_details.json', 'r') as file_read:
    users_data = json.load(file_read)

allowed_namess = users_data.keys()
allowed_names = [name.lower() for name in allowed_namess]

while True:
    acc_name = input(f'\nEnter Name of Account Holder to Login From {list(allowed_namess)} : ').lower()
    if acc_name in allowed_names:
        break
    else:
        print(f"\nInvalid User. Please Enter Registered User Name {list(allowed_namess)}'.")

with open('Credentials/login_details.json', 'r') as file_read:
    login_details = json.load(file_read)

api_auth = login_details[f'{acc_name.capitalize()}']['api_auth']
api_pin = login_details[f'{acc_name.capitalize()}']['pin']
mobile_no = login_details[f'{acc_name.capitalize()}']['Mob No.']
hold_name = login_details[f'{acc_name.capitalize()}']['full_name']

print(f'\nTrying to Login from Account Holder: {hold_name}')

trading_url = "https://pro.upstox.com"  # or https://app.upstox.com
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

driver.get(trading_url)
wait = WebDriverWait(driver, 30)

phone_input = wait.until(EC.presence_of_element_located((By.ID, "mobileNum")))
phone_input.send_keys(mobile_no)

otp_button = wait.until(EC.element_to_be_clickable((By.ID, "getOtp")))
otp_button.click()

totp_value = show_totp(api_auth)
totp_input = wait.until(EC.presence_of_element_located((By.ID, "otpNum")))
totp_input.send_keys(totp_value)

proceed_button = wait.until(EC.element_to_be_clickable((By.ID, "continueBtn")))
proceed_button.click()

pin_input = wait.until(EC.presence_of_element_located((By.ID, "pinCode")))
pin_input.send_keys(api_pin)

proceed_button = wait.until(EC.element_to_be_clickable((By.ID, "pinContinueBtn")))
proceed_button.click()

time.sleep(5)

print(f'\nLogin Successful from Account : {acc_name.capitalize()}')

input("\n✅ Browser will remain open.\nPress ENTER to exit the script, only after closing the browser manually.")
