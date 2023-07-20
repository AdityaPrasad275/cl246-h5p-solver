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

# Open the browser 
driver = webdriver.Edge()
driver.get(url)
fn.login(driver, username, password) #and login

#get iframes
h5p_iframe, yt_iframe = fn.get_iframe(driver, delay)

time.sleep(1)

#extract percentages
question_stamps = fn.question_stamps(driver)
print(question_stamps)

time.sleep(0.5)

#playing the video and finding total time
totalTime = fn.play_video(driver, yt_iframe)

# iterating through array of percentages
for question_stamp in question_stamps:
    driver.switch_to.frame(yt_iframe)

    driver.execute_script("""
        const xpath = "/html/body/div/div/div[1]/video";
        const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        container.currentTime = arguments[0]*arguments[1] - 2;
    """, totalTime, question_stamp[0])
    
    driver.switch_to.parent_frame()
    
    if question_stamp[1] == 'h5p-multichoice-interaction':
        #finding to quiz_button
        quiz_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'h5p-interaction-button'))
        )
        quiz_button.click()

        time.sleep(0.5)
        fn.mcmc_solver(driver)
    else:
        time.sleep(4)
        driver.execute_script("alert('I cannot solve this question do it yourself and submit and/or hit enter in the terminal where it asks to continue (the code is stopped till you input)');")
        input("CAUTION  !! make sure you have submitted the quiz and made its dialogue box and the purple quiz button dissapear before hitting enter here to continue: ")

driver.execute_script("alert('Done ! Please submit the quiz.');")
time.sleep(10)
exit()