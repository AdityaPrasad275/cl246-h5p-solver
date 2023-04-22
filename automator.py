from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

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

def switchToFrame(id_or_class, status):
    if status == "class":
        try:
            # Wait for the element with the ID of h5p-iframe
            iframe = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, id_or_class))
            )
            print("iframe with class " + id_or_class + " is present in the DOM now")

            # Switch the driver's focus to the iframe
            driver.switch_to.frame(iframe)
        except TimeoutException:
            print("unable to switch to iframe with class " + id_or_class)
            exit()
    elif status == "id":
        try:
            # Wait for the element with the ID of h5p-iframe
            iframe = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, id_or_class))
            )
            print("iframe with id " + id_or_class + " is present in the DOM now")

            # Switch the driver's focus to the iframe
            driver.switch_to.frame(iframe)
        except TimeoutException:
            print("unable to switch to iframe with id " + id_or_class)
            exit()

def operation(xpath, what_is_it, script_or_function_name):
    try:
        # Wait for the element with the xpath of h5p-content-interaction/seekbar 
        seekbar = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(what_is_it + " is present in the DOM now")

        # read percentage extractor.js
        with open(script_or_function_name + '.js', 'r') as file:
            script = file.read()

        return driver.execute_script(script + "; return" +  script_or_function_name + "()")
    except TimeoutException:
        print("seekbar did not show up")
        exit()

#switching to h5p iframe
switchToFrame('h5p-iframe', "class")

#extract percentages
percentages = operation('/html/body/div/div/div[3]/div[2]/div[4]', 'seekbar', 'percentage_extractor')

switchToFrame("h5p-youtube-0", "id")

#finding total time
try:
    # Find the video element
    video_stream = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/video'))
    )
    # Click the "play" button using Selenium's .click() method
    play_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/button'))
    )
    play_button.click()

    # Wait for the page to load
    time.sleep(2) 

    totalTime = video_stream.get_property('duration')
except TimeoutException:
    print("video did not show up for measuring total time")
    exit()


# # iterating through array of percentages
# for percentage in percentages:
#     try:
#         # Wait for the element with the xpath of video stream
#         video_stream = WebDriverWait(driver, delay).until(
#           EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/video'))
#         )
#         print("video is present in the DOM now")

#         percentages = driver.execute_script("""
#             document.querySelectorAll('.video-stream')[0].currentTime = totalTime*{percentage} - 2
#         """)
#     except TimeoutException:
#         print("seekbar did not show up")
#         exit()

