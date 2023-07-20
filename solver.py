from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time	
import functions as fn

delay = 5

url = input("Enter the Moodle lecture URL: ")
username = input("Enter your Moodle username: ")
password = input("Enter your Moodle password: ")

# Open the browser and navigate to the Moodle login page
driver = webdriver.Edge()
driver.get(url)
fn.login(driver, username, password) #and login

#list iframes
# Wait for the element with the ID of h5p-iframe
try:
    h5p_iframe = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, "h5p-iframe"))
    )
    driver.switch_to.frame(h5p_iframe)
except TimeoutException:
    print('iframe didnt show up in DOM, abort mission, fall back')
    exit()

try:
    yt_iframe = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.ID, "h5p-youtube-0"))
    )
except TimeoutException:
    print("yt-iframe didn't show up in DOM, abort mission, fall back")
    exit()
driver.switch_to.default_content()

time.sleep(1)

#extract percentages
driver.switch_to.frame(h5p_iframe)
question_stamps = fn.question_stamps(driver)
print(question_stamps)

time.sleep(0.5)

#playing the video
try:
    # Find the video element
    driver.switch_to.frame(yt_iframe)
    video_stream = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/video'))
    )
    # Click the "play" button using Selenium's .click() method
    play_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/button'))
    )
    play_button.click()
except TimeoutException:
    print("video did not show up for measuring total time")
    exit()

# Wait for the page to load
time.sleep(0.5) 

#finding total time
totalTime = video_stream.get_property('duration')
print(totalTime)

#switching to h5p iframe
driver.switch_to.default_content()
driver.switch_to.frame(h5p_iframe)

# iterating through array of percentages
for question_stamp in question_stamps:
    driver.switch_to.default_content()
    driver.switch_to.frame(h5p_iframe)
    driver.switch_to.frame(yt_iframe)

    driver.execute_script("""
        const xpath = "/html/body/div/div/div[1]/video";
        const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        container.currentTime = arguments[0]*arguments[1] - 2;
    """, totalTime, question_stamp[0])
    driver.switch_to.default_content()
    driver.switch_to.frame(h5p_iframe)
    
    if question_stamp[1] == 'h5p-multichoice-interaction':
        #finding to quiz_button
        quiz_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div'))
        )
        print("quiz button is present in the DOM now")
        quiz_button.click()

        time.sleep(0.5)
        fn.mcmc_solver(driver)
    else:
        time.sleep(4)
        driver.execute_script("alert('I cannot solve this question do it yourself and submit and/or hit enter in the terminal where it asks to continue (the code is stopped till you input)');")
        input("CAUTION  !! make sure you have submitted the quiz and made its dialogue box and the purple quiz button dissapear before hitting enter here to continue: ")


fn.aaaaaaaaand_submit(driver, h5p_iframe, yt_iframe, totalTime)

time.sleep(5)