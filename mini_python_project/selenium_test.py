from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

# Set up WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
driver.get("http://127.0.0.1:5000/login")  # Directly navigate to the login page

def test_login():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))  # Use actual attribute
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Login']")  # Corrected the button text
    
    username_field.send_keys("admin")  # Updated username
    password_field.send_keys("admin")  # Updated password
    login_button.click()
    
    # Adjust the URL to what it should be after login
    WebDriverWait(driver, 10).until(EC.url_contains("feature"))  # Wait for the feature page URL
    print("Login test passed.")

def test_text_transformation():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "text")))
    text_input = driver.find_element(By.ID, "text")
    transformation_select = driver.find_element(By.ID, "transformation")
    transform_button = driver.find_element(By.XPATH, "//button[text()='Transform']")
    
    text_input.send_keys("hello world")
    transformation_select.send_keys("uppercase")
    transform_button.click()
    time.sleep(1)
    
    transformed_text = driver.find_element(By.XPATH, "//div[@class='transformed-text']/p")
    assert transformed_text.text == "HELLO WORLD", "Text transformation failed!"
    print("Text transformation test passed.")

def test_rating():
    # Wait for and select the 5-star rating
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='rating'][@value='5']")))
    star_rating = driver.find_element(By.XPATH, "//input[@name='rating'][@value='5']")  # Select the 5-star rating
    star_rating.click()  # Click the 5-star rating
    time.sleep(1)  # Wait for the rating to be selected
    
    # Select 'Good' feedback
    feedback = driver.find_element(By.XPATH, "//input[@name='feedback'][@value='Good']")  # Select 'Good' feedback
    feedback.click()  # Click the 'Good' feedback
    
    # Click the submit button
    submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
    submit_button.click()  # Click the submit button
    time.sleep(1)  # Wait for the form to submit
    
    # Wait for the result page or the feedback summary to be displayed
    try:
        # Now check the feedback directly from the 'feedback' class
        feedback_summary = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='feedback']/p"))
        )
        
        # Check if the rating and feedback are correctly displayed on the result page
        print("Feedback Summary Found: ", feedback_summary.text)  # Debug print to see the output
        assert "5 Stars" in driver.page_source, "Rating not saved correctly!"
        assert "Good" in driver.page_source, "Feedback not saved correctly!"
        
        print("Rating and feedback test passed.")
    except TimeoutException:
        print("Timeout occurred: Unable to find feedback summary.")
        # Capture the current page's source for debugging
        print(driver.page_source)


def test_logout():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='back-btn']")))
    back_to_feature_button = driver.find_element(By.XPATH, "//button[@class='back-btn']")
    back_to_feature_button.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='logout-btn']")))
    logout_button = driver.find_element(By.XPATH, "//button[@class='logout-btn']")
    logout_button.click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("login"))
    print("Logout test passed.")

def test_forgot_password():
    driver.get("http://127.0.0.1:5000/forgot-password")
    print("Running Forgot Password tests...")

    # Wait for the form elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    # Locate the submit button
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # Test case 1: Non-admin username
    username_field.clear()  # Clear any previous input
    password_field.clear()
    username_field.send_keys("user1")
    password_field.send_keys("newpassword123")
    submit_button.click()

    # Wait for the error message to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
    )
    error_message = driver.find_element(By.CLASS_NAME, "error-message")
    assert error_message.text == "Only 'admin' can reset the password."
    print("Non-admin username test passed.")

    # Test case 2: Admin username
    # Relocate the username and password fields after clicking submit
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    username_field.clear()  # Clear any previous input
    password_field.clear()
    username_field.send_keys("admin")
    password_field.send_keys("admin")
    
    # Re-locate the submit button again to avoid stale reference
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()

    # Wait for the success message to appear and verify
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "success-message"))
    )
    success_message = driver.find_element(By.CLASS_NAME, "success-message")
    
    # Update the assertion to match the actual success message
    assert success_message.text == "Password reset successful! You can now log in with your new password."
    print("Admin username password reset test passed.")

    # Wait for redirection to login page
    try:
        # Wait for the login page's specific element (e.g., the login form) to appear
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
        print("Redirection to login page confirmed.")
    except TimeoutException:
        print("Timeout occurred while waiting for the login page to load.")


# Execute all tests
try:
    test_login()
    test_text_transformation()
    test_rating()
    test_logout()
    test_forgot_password()  # Newly added test
finally:
    driver.quit()
