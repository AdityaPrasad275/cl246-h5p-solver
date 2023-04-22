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


#switching to iframe
try:
    # Wait for the element with the ID of h5p-iframe
    iframe = WebDriverWait(driver, delay).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'h5p-iframe'))
    )
    print("iframe is present in the DOM now")
        
    # Switch the driver's focus to the iframe
    driver.switch_to.frame(iframe)
except TimeoutException:
    print("iframe did not show up")
    exit()

#extracting percentages from seekbar
try:
    # Wait for the element with the xpath of h5p-content-interaction/seekbar 
    seekbar = WebDriverWait(driver, delay).until(
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



#finding total time
try:
    # Wait for the element with the ID of h5p-iframe
    yt_iframe = WebDriverWait(driver, delay).until(
      EC.presence_of_element_located((By.ID, 'h5p-youtube-0'))
    )
    print("yt iframe is present in the DOM now")

    # Switch the driver's focus to the iframe
    driver.switch_to.frame(yt_iframe)

    # Wait for the element with the xpath of video 
    video_stream = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/video'))
        )
    print("video is present in the DOM now, finding total time")

    totalTime = driver.execute_script("""
        //const xpath = "/html/body/div/div/div[1]/video";
        //const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        //return container.duration
        document.querySelectorAll('.video-stream')[0].duration
    """)
    print(totalTime)
except TimeoutException:
    print("video did not show up for measuring total time")
    exit()


# # iterating through array of percentages
# for percentage in percentages:
#     try:
#         # Wait for the element with the xpath of video stream
#         video_stream = WebDriverWait(driver, delay).until(
#         EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/video'))
#         )
#         print("video is present in the DOM now")

#         percentages = driver.execute_script("""
#             document.querySelectorAll('.video-stream')[0].currentTime = totalTime*{percentage} - 2
#         """)
#     except TimeoutException:
#         print("seekbar did not show up")
#         exit()