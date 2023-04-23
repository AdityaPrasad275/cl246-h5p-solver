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
percentages = functions.percentage_extractor(driver)
print(percentages)

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
for percentage in percentages:
        
    driver.switch_to.default_content()
    functions.switchToFrame(driver, 'h5p-iframe', "class")
    functions.switchToFrame(driver, "h5p-youtube-0", "id")

    print(totalTime*percentage)
    driver.execute_script("""
        const xpath = "/html/body/div/div/div[1]/video";
        const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        container.currentTime = arguments[0]*arguments[1] - 2;
    """, totalTime, percentage)

    driver.switch_to.default_content()
    #switching to h5p iframe
    functions.switchToFrame(driver, 'h5p-iframe', "class")

    #finding to quiz_button
    quiz_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div'))
    )
    print("quiz button is present in the DOM now")
    quiz_button.click()

    time.sleep(0.5)
    
    #solving multiple choice multiple correct question (mcmc) 
    functions.mcmc_solver(driver)

functions.aaaaaaaaand_submit(driver, totalTime)

time.sleep(200)