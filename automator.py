from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = input("Enter the Moodle lecture URL: ")
username = input("Enter your Moodle username: ")
password = input("Enter your Moodle password: ")


# Open the browser and navigate to the Moodle login page
driver = webdriver.Edge()
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(2)

# Find the username and password input fields, and enter your credentials
input_username = driver.find_element(By.ID, "username")
input_username.send_keys(username)
input_password = driver.find_element(By.ID, "password")
input_password.send_keys(password)

# Find the login button and click it
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

delay = 5

try:
    # Wait for the element with the ID of h5p-iframe
    wrapper = WebDriverWait(driver, delay).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'h5p-iframe'))
    )
    print("iframe is present in the DOM now")
    # Find the iframe element by its ID or index
    iframe = driver.find_element(By.CLASS_NAME, 'h5p-iframe')
        
    # Switch the driver's focus to the iframe
    driver.switch_to.frame(iframe)
except TimeoutException:
    print("iframe did not show up")
    exit()


try:
    # Wait for the element with the xpath of h5p-content-interaction/seekbar 
    wrapper = WebDriverWait(driver, delay).until(
      EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[3]/div[2]/div[4]'))
    )
    print("seekbar is present in the DOM now")

    # read percentage extractor.js
    with open('percentage_extractor.js', 'r') as file:
        script_pe = file.read()

    percentages = driver.execute_script(script_pe + "; return percentage_extracter()")
except TimeoutException:
    print("seekbar did not show up")
    exit()

