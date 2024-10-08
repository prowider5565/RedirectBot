from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()  # Add the path to your WebDriver

try:
    print("Getting into the process...")
    driver.get("https://chatgpt.com/")  # Adjust URL as needed
    print("Opening site...")

    # Print the page source to check if it loaded correctly
    time.sleep(5)
    print(driver.page_source)  # Useful for debugging

    # Wait for the input box to be present for up to 40 seconds
    input_box = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Send a message"]')
        )           
    )
    print("Finding the input element...")

    # Type the question in the input box
    question = "Describe an elephant in short"
    input_box.send_keys(question)       
    print("Sending the message...")

    # Press Enter to submit
    input_box.send_keys(Keys.ENTER)
    print("Pressing enter...")

    # Wait for response element (adjust selector as needed)
    response_element = WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".message"))
    )
    print("Getting the response element...")

    # Get the last generated response text and print it
    print("Response: ", response_element[-1].text)

finally:
    driver.quit()
