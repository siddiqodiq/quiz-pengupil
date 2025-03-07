import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginRegisterTest(unittest.TestCase):
    def setUp(self):
        # Setup Selenium WebDriver
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # Run in headless mode for CI/CD
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        self.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load
        self.base_url = "http://localhost"  # Base URL for the application

    def tearDown(self):
        self.driver.quit()

    def test_login_success(self):
        """Test Case 1: Login Berhasil"""
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys("syubbanul")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        self.assertIn("index.php", self.driver.current_url)  # Check if redirected to index.php

    def test_login_failed_wrong_username(self):
        """Test Case 2: Login Gagal (Username Salah)"""
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys("user_tidak_ada")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Register User Gagal !!")

    def test_login_failed_empty_data(self):
        """Test Case 3: Login Gagal (Data Kosong)"""
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "submit").click()
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Data tidak boleh kosong !!")

    def test_register_success(self):
        """Test Case 4: Registrasi Berhasil"""
        self.driver.get(f"{self.base_url}/register.php")
        self.driver.find_element(By.NAME, "name").send_keys("Syubbanul Siddiq")
        self.driver.find_element(By.NAME, "email").send_keys("siddiq@example.com")
        self.driver.find_element(By.NAME, "username").send_keys("siddiq")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "repassword").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        self.assertIn("index.php", self.driver.current_url)  # Check if redirected to index.php

    def test_register_failed_existing_username(self):
        """Test Case 5: Registrasi Gagal (Username Sudah Ada)"""
        self.driver.get(f"{self.base_url}/register.php")
        self.driver.find_element(By.NAME, "name").send_keys("Jane Doe")
        self.driver.find_element(By.NAME, "email").send_keys("jane.doe@example.com")
        self.driver.find_element(By.NAME, "username").send_keys("siddiq")  # Username sudah ada
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "repassword").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Username sudah terdaftar !!")

    def test_register_failed_empty_data(self):
        """Test Case 6: Registrasi Gagal (Data Kosong)"""
        self.driver.get(f"{self.base_url}/register.php")
        self.driver.find_element(By.NAME, "submit").click()
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Data tidak boleh kosong !!")

    def test_register_failed_one_field_empty(self):
        """Test Case 7: Registrasi Gagal (Satu Kolom Kosong)"""
        self.driver.get(f"{self.base_url}/register.php")
        self.driver.find_element(By.NAME, "name").send_keys("Syubbanul Siddiq")
        self.driver.find_element(By.NAME, "username").send_keys("siddiq")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "repassword").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Data tidak boleh kosong !!")

if __name__ == '__main__':
    unittest.main(verbosity=2)