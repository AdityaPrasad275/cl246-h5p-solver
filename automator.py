from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = input("Enter the Moodle lecture URL: ")
username = input("Enter your Moodle username: ")
password = input("Enter your Moodle password: ")

# Open the browser and navigate to the Moodle login page
driver = webdriver.Edge()
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(2)

# Find the username and password input fields, and enter your credentials
username = driver.find_element(By.ID, "username")
username.send_keys(username)
password = driver.find_element(By.ID, "password")
password.send_keys(password)

# Find the login button and click it
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

percentages = driver.execute_script("""
  // Get the container div element
  const container = document.querySelector('.h5p-interactions-container');

  // Get an array of all the child div elements with the class name 'h5p-seekbar-interaction'
  const seekbarInteractions = container.querySelectorAll('.h5p-seekbar-interaction');

  // Create apn empty array to store the 'left' values
  const leftValues = [];

  // Loop through the seekbar interactions and extract the 'left' value from each element
  seekbarInteractions.forEach((interaction) => {
    leftValues.push(interaction.style.left);
  });

  // Now the left values are stored in the 'leftValues' array
  console.log(leftValues);
  // Assume the array of left values is stored in a variable called 'leftValues'

  // Map over the array and convert each left value to a number
  const leftNumbers = leftValues.map(leftValue => {
      // Remove the percentage sign and convert to number
      const valueWithoutPercentage = parseFloat(leftValue.replace('%', ''));
      // Divide by 100 and return the resulting number
      return valueWithoutPercentage / 100;
    });

  // Now 'leftNumbers' contains an array of numbers instead of strings with percentages
  return leftNumbers
  
"""
)
