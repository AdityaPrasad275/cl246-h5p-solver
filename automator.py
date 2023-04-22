from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = input("Enter the Moodle lecture URL: ")
username = input("Enter your Moodle username: ")
password = input("Enter your Moodle password: ")

# Open the browser and navigate to the Moodle login page
driver = webdriver.Edge()
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(2)

# Find the username and password input fields, and enter your credentials
username = driver.find_element(By.ID, "username")
username.send_keys(username)
password = driver.find_element(By.ID, "password")
password.send_keys(password)

# Find the login button and click it
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

# read percentage extractor.js
with open('percentage_extractor.js', 'r') as file:
    script_pe = file.read()
  
percentages = driver.execute_script(script_pe)
