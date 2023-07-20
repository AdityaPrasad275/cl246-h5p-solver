from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time	

def login(driver, username, password):
    # Wait for the page to load
    driver.implicitly_wait(1)

    # Find the username and password input fields, and enter your credentials
    input_username = driver.find_element(By.ID, "username")
    input_username.send_keys(username)
    input_password = driver.find_element(By.ID, "password")
    input_password.send_keys(password)

    # Find the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    
def mcmc_solver(driver, delay = 5):
    try:
        options = driver.find_elements(By.CSS_SELECTOR, '.h5p-answer')

        for option in options:
            option.click()
        
        driver.find_element(By.CSS_SELECTOR, '.h5p-question-check-answer').click()
        time.sleep(0.5)
        correctOptions = []
        options_1 = driver.find_elements(By.CSS_SELECTOR, '.h5p-answer')
        for option in options_1:
            if "h5p-correct" in option.get_attribute("class"):
                correctOptions.append(option.text.split('\n')[0])

        driver.find_element(By.CSS_SELECTOR, '.h5p-question-try-again').click()

        options_2 = driver.find_elements(By.CSS_SELECTOR, '.h5p-answer')

        for option in options_2:
            if option.text.split('\n')[0] in correctOptions:
                option.click()

        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.h5p-question-check-answer').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.h5p-question-iv-continue').click()
        time.sleep(3)
        
    
    except TimeoutException:
        print("options did not show up")
        exit()  
        
    # Wait until the element disappears from the DOM
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed (in seconds)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.h5p-interaction-button')))


def question_stamps(driver, delay = 5):
    try:
        # Wait for the element with the xpath of h5p-content-interaction/seekbar 
        seekbar = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "h5p-interactions-container"))
        )

        # Get an array of all the child div elements with the class name 'h5p-seekbar-interaction'
        seekbar_interactions = seekbar.find_elements(By.CSS_SELECTOR, '.h5p-seekbar-interaction')

        # Get the width of the container element
        seekbar_width = seekbar.size['width']

        # Create an empty list to store the percentage and question type pairs
        percentage_question_type_pairs = []

        # Loop through the seekbar interactions and extract the percentage value from each element
        for interaction in seekbar_interactions:
            # Get the left value in pixels
            left_value_in_pixels = interaction.value_of_css_property('left')

            # Convert the left value to a percentage
            left_value_in_percentage = float(left_value_in_pixels[:-2]) / seekbar_width

            # Append the percentage value and corresponding question type in array
            question_type = interaction.get_attribute('class').split()[-1]
            percentage_question_type_pairs.append((left_value_in_percentage, question_type))

        print(percentage_question_type_pairs)
        # Now the percentages are stored in the 'percentages' array
        return percentage_question_type_pairs
    except TimeoutException:
        print("seekbar didnt show up")
        exit()

def get_iframe(driver, delay):
    h5p_iframe = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(h5p_iframe[0])
 
    yt_iframe = driver.find_elements(By.TAG_NAME, 'iframe')
    
    return h5p_iframe[0], yt_iframe[0]

def play_video(driver, yt):
    driver.switch_to.frame(yt)
    driver.find_element(By.CLASS_NAME, 'ytp-large-play-button').click()
    time.sleep(0.5)
    
    totalTime = driver.find_element(By.TAG_NAME, 'video').get_property('duration')
    driver.switch_to.parent_frame()
    
    return totalTime
    
    