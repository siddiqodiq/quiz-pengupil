import os
import logging
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Install ChromeDriver yang sesuai dengan versi Google Chrome
chromedriver_autoinstaller.install()

# Setup logging
TEST_LOG_DIR = "test-logs"
os.makedirs(TEST_LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(TEST_LOG_DIR, "test-execution.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Setup WebDriver
browser_options = webdriver.ChromeOptions()
browser_options.add_argument("--headless")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("--disable-dev-shm-usage")
web_browser = webdriver.Chrome(options=browser_options)
web_browser.implicitly_wait(10)

# List to store test outcomes
test_summary = []

def log_test_outcome(test_name, result, details=""):
    outcome = f"{test_name}: {result} - {details}"
    print(outcome)
    logging.info(outcome)

def execute_test_case(test_function):
    """
    Helper function to execute each test case and handle errors gracefully.
    """
    try:
        test_function()
        test_summary.append((test_function.__name__, "PASS", ""))
    except AssertionError as e:
        test_summary.append((test_function.__name__, "FAIL", str(e)))
    except Exception as e:
        test_summary.append((test_function.__name__, "ERROR", str(e)))

# Test Case 5: Verify successful registration
def verify_successful_registration():
    web_browser.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("New User")
    web_browser.find_element(By.NAME, "email").send_keys("newuser@example.com")
    web_browser.find_element(By.NAME, "username").send_keys("newuser")
    web_browser.find_element(By.NAME, "password").send_keys("password123")
    web_browser.find_element(By.NAME, "repassword").send_keys("password123")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in web_browser.current_url, "Failed: User was not redirected to index.php after registration."

# Test Case 1: Verify successful login
def verify_successful_login():
    web_browser.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("newuser")
    web_browser.find_element(By.NAME, "password").send_keys("password123")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in web_browser.current_url, "Failed: User was not redirected to index.php after login."

# Test Case 2: Verify login failure with incorrect username
def verify_login_failure_incorrect_username():
    web_browser.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("invalid_user")
    web_browser.find_element(By.NAME, "password").send_keys("password123")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Failed: Error message for incorrect username did not appear."

# Test Case 3: Verify login failure with incorrect password
def verify_login_failure_incorrect_password():
    web_browser.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("newuser")
    web_browser.find_element(By.NAME, "password").send_keys("wrong_password")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Failed: Error message for incorrect password did not appear."

# Test Case 4: Verify login failure with empty fields
def verify_login_failure_empty_fields():
    web_browser.get("http://127.0.0.1:8000/login.php")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Failed: Error message for empty fields did not appear."

# Test Case 6: Verify registration failure with existing username
def verify_registration_failure_existing_username():
    web_browser.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Existing User")
    web_browser.find_element(By.NAME, "email").send_keys("existing@example.com")
    web_browser.find_element(By.NAME, "username").send_keys("newuser")
    web_browser.find_element(By.NAME, "password").send_keys("password123")
    web_browser.find_element(By.NAME, "repassword").send_keys("password123")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Username sudah terdaftar !!" in error_message, "Failed: Error message for existing username did not appear."

# Test Case 7: Verify registration failure with mismatched passwords
def verify_registration_failure_mismatched_passwords():
    web_browser.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Another User")
    web_browser.find_element(By.NAME, "email").send_keys("another@example.com")
    web_browser.find_element(By.NAME, "username").send_keys("anotheruser")
    web_browser.find_element(By.NAME, "password").send_keys("password123")
    web_browser.find_element(By.NAME, "repassword").send_keys("different_password")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Password tidak sama !!" in error_message, "Failed: Error message for mismatched passwords did not appear."

# Test Case 8: Verify registration failure with empty fields
def verify_registration_failure_empty_fields():
    web_browser.get("http://127.0.0.1:8000/register.php")
    web_browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = web_browser.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Failed: Error message for empty fields did not appear."

# Execute test cases in the specified order
test_cases_to_run = [
    verify_successful_registration,  # Test Case 5
    verify_successful_login,         # Test Case 1
    verify_login_failure_incorrect_username,  # Test Case 2
    verify_login_failure_incorrect_password,  # Test Case 3
    verify_login_failure_empty_fields,        # Test Case 4
    verify_registration_failure_existing_username,  # Test Case 6
    verify_registration_failure_mismatched_passwords,  # Test Case 7
    verify_registration_failure_empty_fields  # Test Case 8
]

for test in test_cases_to_run:
    execute_test_case(test)

# Print test results in a clean format
print("\n=== TEST EXECUTION SUMMARY ===")
print(f"{'Test Case':<50} {'Result':<10} {'Details'}")
print("="*80)
for name, result, details in test_summary:
    print(f"{name:<50} {result:<10} {details}")

# Close the browser
web_browser.quit()