from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time	
import functions

delay = 5

url = input("Enter the Moodle lecture URL: ")
username = input("Enter your Moodle username: ")
password = input("Enter your Moodle password: ")

# Open the browser and navigate to the Moodle login page
driver = webdriver.Edge()
driver.get(url)
functions.login(driver, username, password) #and login

#switching to h5p iframe
functions.switchToFrame(driver, 'h5p-iframe', "class")
time.sleep(1)

#extract percentages
question_stamps = functions.question_stamps(driver)
print(question_stamps)

functions.switchToFrame(driver, "h5p-youtube-0", "id")

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
    time.sleep(1) 

    totalTime = video_stream.get_property('duration')
except TimeoutException:
    print("video did not show up for measuring total time")
    exit()
print(totalTime)

driver.switch_to.default_content()

#switching to h5p iframe
functions.switchToFrame(driver, 'h5p-iframe', "class")

# iterating through array of percentages
for question_stamp in question_stamps:
        
    driver.switch_to.default_content()
    functions.switchToFrame(driver, 'h5p-iframe', "class")
    functions.switchToFrame(driver, "h5p-youtube-0", "id")

    driver.execute_script("""
        const xpath = "/html/body/div/div/div[1]/video";
        const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        container.currentTime = arguments[0]*arguments[1] - 2;
    """, totalTime, question_stamp[0])

    driver.switch_to.default_content()
    #switching to h5p iframe
    functions.switchToFrame(driver, 'h5p-iframe', "class")
    
    if question_stamp[1] == 'h5p-multichoice-interaction':
        #finding to quiz_button
        quiz_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div'))
        )
        print("quiz button is present in the DOM now")
        quiz_button.click()

        time.sleep(0.5)
        functions.mcmc_solver(driver)
    else:
        time.sleep(4)
        driver.execute_script("alert('I cannot solve this question do it yourself and submit and/or hit enter in the terminal where it asks to continue');")
        input("CAUTION  !! make sure you have submitted the quiz and made its dialogue box and the purple quiz button dissapear before hitting enter here to continue: ")


functions.aaaaaaaaand_submit(driver, totalTime)

time.sleep(5)