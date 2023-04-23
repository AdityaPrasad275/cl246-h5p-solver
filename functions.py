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

def switchToFrame(driver, id_or_class, status, delay = 5):
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

def mcmc_solver(driver, delay = 5):
    try:
        # Wait for the element with the xpath of h5p-content-interaction/seekbar 
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

def percentage_extractor(driver):
    # Get the container element
    container = driver.find_element(By.CLASS_NAME, "h5p-interactions-container")

    # Get an array of all the child div elements with the class name 'h5p-seekbar-interaction'
    seekbar_interactions = container.find_elements(By.CSS_SELECTOR, '.h5p-seekbar-interaction')

    # Get the width of the container element
    container_width = container.size['width']

    # Create an empty array to store the percentages
    percentages = []

    # Loop through the seekbar interactions and extract the percentage value from each element
    for interaction in seekbar_interactions:
        # Get the left value in pixels
        left_value_in_pixels = interaction.value_of_css_property('left')
        # Convert the left value to a percentage
        left_value_in_percentage = float(left_value_in_pixels[:-2]) / container_width
        # Append the percentage value to the array
        percentages.append(left_value_in_percentage)

    # Now the percentages are stored in the 'percentages' array
    return percentages
