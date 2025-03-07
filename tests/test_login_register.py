import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Impor modul time

class LoginRegisterTest(unittest.TestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = 'http://docker-apache:4444'
        self.browser = webdriver.Remote(command_executor=server, options=options)
        self.browser.implicitly_wait(10)
        self.addCleanup(self.browser.quit)

    def test_login_success(self):
        """Test Case 1: Login Berhasil"""
        self.browser.get("http://docker-apache/login.php")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "InputPassword")
        submit_button = self.browser.find_element(By.NAME, "submit")

        username_input.send_keys("syubbanul")
        password_input.send_keys("password123")
        submit_button.click()

        # Cek redirect ke index.php
        self.assertIn("index.php", self.browser.current_url)
        time.sleep(5)  # Jeda 5 detik

    def test_login_failed_wrong_username(self):
        """Test Case 2: Login Gagal (Username Salah)"""
        self.browser.get("http://docker-apache/login.php")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "InputPassword")
        submit_button = self.browser.find_element(By.NAME, "submit")

        username_input.send_keys("user_tidak_ada")
        password_input.send_keys("password123")
        submit_button.click()

        # Cek pesan error
        error_message = self.browser.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Username atau Password salah !!")
        time.sleep(5)  # Jeda 5 detik

    def test_login_failed_empty_data(self):
        """Test Case 3: Login Gagal (Data Kosong)"""
        self.browser.get("http://docker-apache/login.php")
        submit_button = self.browser.find_element(By.NAME, "submit")
        submit_button.click()

        # Cek pesan error
        error_message = self.browser.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Data tidak boleh kosong !!")
        time.sleep(5)  # Jeda 5 detik

    def test_register_success(self):
        """Test Case 4: Registrasi Berhasil"""
        self.browser.get("http://docker-apache/register.php")
        name_input = self.browser.find_element(By.ID, "name")
        email_input = self.browser.find_element(By.ID, "InputEmail")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "InputPassword")
        repassword_input = self.browser.find_element(By.ID, "InputRePassword")
        submit_button = self.browser.find_element(By.NAME, "submit")

        name_input.send_keys("Syubbanul Siddiq")
        email_input.send_keys("siddiq@example.com")
        username_input.send_keys("siddiq_new")
        password_input.send_keys("password123")
        repassword_input.send_keys("password123")
        submit_button.click()

        # Cek redirect ke index.php
        self.assertIn("index.php", self.browser.current_url)
        time.sleep(5)  # Jeda 5 detik

    def test_register_failed_duplicate_username(self):
        """Test Case 5: Registrasi Gagal (Username Sudah Ada)"""
        self.browser.get("http://docker-apache/register.php")
        name_input = self.browser.find_element(By.ID, "name")
        email_input = self.browser.find_element(By.ID, "InputEmail")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "InputPassword")
        repassword_input = self.browser.find_element(By.ID, "InputRePassword")
        submit_button = self.browser.find_element(By.NAME, "submit")

        name_input.send_keys("Jane Doe")
        email_input.send_keys("jane.doe@example.com")
        username_input.send_keys("siddiq")  # Username sudah ada
        password_input.send_keys("password123")
        repassword_input.send_keys("password123")
        submit_button.click()

        # Cek pesan error
        error_message = self.browser.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Username sudah terdaftar !!")
        time.sleep(5)  # Jeda 5 detik

    def test_register_failed_empty_data(self):
        """Test Case 6: Registrasi Gagal (Data Kosong)"""
        self.browser.get("http://docker-apache/register.php")
        submit_button = self.browser.find_element(By.NAME, "submit")
        submit_button.click()

        # Cek pesan error
        error_message = self.browser.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(error_message, "Data tidak boleh kosong !!")
        time.sleep(5)  # Jeda 5 detik

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')