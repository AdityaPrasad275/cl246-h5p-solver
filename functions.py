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
        # Wait for the element with the xpath of options
        options = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[5]/div/div[2]/div/div[2]/ul"))
        )
        print("options are present in the DOM now")

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
        driver.switch_to.default_content()

    except TimeoutException:
        print("options did not show up")
        exit()  

def question_stamps(driver, delay = 5):
    try:
        # Wait for the element with the xpath of h5p-content-interaction/seekbar 
        seekbar = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "h5p-interactions-container"))
        )
        print("skeebar are present in the DOM now")

        # Get an array of all the child div elements with the class name 'h5p-seekbar-interaction'
        seekbar_interactions_temp = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.h5p-seekbar-interaction'))
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

        # Now the percentages are stored in the 'percentages' array
        return percentage_question_type_pairs
    except TimeoutException:
        print("seekbar didnt show up")
        exit()

def aaaaaaaaand_submit(driver, h5p_iframe, yt_iframe, totalTime, delay = 5):
    #switching to yt iframe
    driver.switch_to.default_content()
    driver.switch_to.frame(h5p_iframe)
    driver.switch_to.frame(yt_iframe)

    driver.execute_script("""
        const xpath = "/html/body/div/div/div[1]/video";
        const container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        container.currentTime = arguments[0] - 1;
    """, totalTime)

    #switching to  h5p iframe
    driver.switch_to.default_content()
    driver.switch_to.frame(h5p_iframe)

    #finding to quiz_button
    submit_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[9]/div[2]/div[2]/div/div[1]/div[2]/div[3]/button'))
    )
    print("submit button is present in the DOM now")
    submit_button.click()