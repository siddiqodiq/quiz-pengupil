import os
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfigurasi Logging
LOG_DIR = "test-results"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Fungsi untuk cek apakah server sudah aktif
def wait_for_server(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Server is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            print("⏳ Waiting for server to start...")
        time.sleep(5)
    raise RuntimeError("❌ Server failed to start!")

# Cek server sebelum Selenium berjalan
BASE_URL = "http://127.0.0.1:8000/"
wait_for_server(BASE_URL)

# Set up WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# List untuk menyimpan hasil test
test_results = []

def log_result(test_name, status, message=""):
    result = f"{test_name}: {status} - {message}"
    print(result)
    logging.info(result)

def run_test(test_function):
    """
    Helper function untuk menjalankan setiap test case tanpa menghentikan eksekusi.
    Jika ada error, akan dicatat dan test berikutnya tetap dijalankan.
    """
    try:
        test_function()
        test_results.append((test_function.__name__, "✅ PASSED", ""))
    except AssertionError as e:
        test_results.append((test_function.__name__, "❌ FAILED", str(e)))
    except Exception as e:
        test_results.append((test_function.__name__, "⚠️ ERROR", str(e)))

# Test Case 1: Login Berhasil
def test_login_success():
    driver.get(BASE_URL + "login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("syubbanul")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url, "Error: Login gagal, tidak diarahkan ke index.php."

# Test Case 2: Login Gagal (Username Salah)
def test_login_failed_username():
    driver.get(BASE_URL + "login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("user_tidak_ada")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Error: Pesan gagal login tidak muncul."

# Test Case 3: Login Gagal (Data Kosong)
def test_login_failed_empty_data():
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Error: Input kosong tidak ditangani dengan benar."

# Test Case 4: Registrasi Berhasil
def test_register_success():
    driver.get(BASE_URL + "register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Syubbanul Siddiq")
    driver.find_element(By.NAME, "email").send_keys("siddiq@example.com")
    driver.find_element(By.NAME, "username").send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url, "Error: Registrasi gagal, tidak diarahkan ke index.php."

# Test Case 5: Registrasi Gagal (Username Sudah Ada)
def test_register_failed_username_exists():
    driver.get(BASE_URL + "register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Jane Doe")
    driver.find_element(By.NAME, "email").send_keys("jane.doe@example.com")
    driver.find_element(By.NAME, "username").send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Username sudah terdaftar !!" in error_message, "Error: Sistem tidak mendeteksi username yang sudah ada."

# Test Case 6: Registrasi Gagal (Data Kosong)
def test_register_failed_empty_data():
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Error: Input kosong tidak ditangani dengan benar."

# Test Case 7: Registrasi Gagal (Satu Kolom Kosong)
def test_register_failed_partial_empty_data():
    driver.get(BASE_URL + "register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Syubbanul Siddiq")
    driver.find_element(By.NAME, "username").send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Error: Sistem tidak menangani kolom yang kosong dengan benar."

# Test Case 8: SQL Injection Attempt (Login)
def test_sql_injection_login():
    driver.get(BASE_URL + "login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Error: SQL Injection berhasil, sistem tidak aman!"

# Test Case 9: SQL Injection Attempt (Register)
def test_sql_injection_register():
    driver.get(BASE_URL + "register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "email").send_keys("hacker@example.com")
    driver.find_element(By.NAME, "username").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "repassword").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Username sudah terdaftar !!" in error_message, "Error: SQL Injection berhasil, sistem tidak aman!"

# Jalankan semua test case menggunakan run_test()
test_cases = [
    test_login_success,
    test_login_failed_username,
    test_login_failed_empty_data,
    test_register_success,
    test_register_failed_username_exists,
    test_register_failed_empty_data,
    test_register_failed_partial_empty_data,
    test_sql_injection_login,
    test_sql_injection_register
]

for test in test_cases:
    run_test(test)

# Cetak hasil semua test dengan format rapi
print("\n=== TEST RESULTS ===")
print(f"{'Test Case':<30} {'Status':<10} {'Message'}")
print("="*80)
for name, status, message in test_results:
    print(f"{name:<30} {status:<10} {message}")

# Tutup browser
driver.quit()