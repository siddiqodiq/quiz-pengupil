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

# Konfigurasi Logging
LOG_DIR = "test-results"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Set up WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

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
        test_results.append((test_function.__name__, "🟢PASSED", ""))
    except AssertionError as e:
        test_results.append((test_function.__name__, "🔴 FAILED", str(e)))
    except Exception as e:
        test_results.append((test_function.__name__, "🟡 ERROR", str(e)))

# Test Case 1: Login Berhasil
def test_login_success():
    driver.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("siddiq123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url, "Error: Login gagal, tidak diarahkan ke index.php."

def clear_browser_cache():
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    

# Test Case 2: Login Gagal (Username Salah)
def test_login_failed_username():
    clear_browser_cache()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("user_tidak_ada")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Error: Pesan gagal login tidak muncul."

# Test Case 3: Login Gagal (Password Salah)
def test_login_failed_password():
    driver.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("syubbanul")
    driver.find_element(By.NAME, "password").send_keys("salah_password")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Register User Gagal !!" in error_message, "Error: Pesan gagal login tidak muncul."

# Test Case 4: Login Gagal (Data Kosong)
def test_login_failed_empty_data():
    driver.get("http://127.0.0.1:8000/login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong !!" in error_message, "Error: Input kosong tidak ditangani dengan benar."

# Test Case 5: Registrasi Berhasil
def test_register_success():
    driver.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Syubbanul Siddiq")
    driver.find_element(By.NAME, "email").send_keys("siddiq@example.com")
    driver.find_element(By.NAME, "username").send_keys("siddiq2")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "index.php" in driver.current_url, "Error: Registrasi gagal, tidak diarahkan ke index.php."

# Test Case 6: Registrasi Gagal (Username Sudah Ada)
def test_register_failed_username_exists():
    clear_browser_cache()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/login.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("siddiq123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("siddiq")
    driver.find_element(By.NAME, "email").send_keys("siddiqodiq@gmail.com")
    driver.find_element(By.NAME, "username").send_keys("siddiq")
    driver.find_element(By.NAME, "password").send_keys("siddiq123")
    driver.find_element(By.NAME, "repassword").send_keys("siddiq123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(5)
    
    # Tunggu elemen alert muncul
    error_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
    )

    error_message = error_element.text
    assert "Username sudah terdaftar !!" in error_message, "Error: Input kosong tidak ditangani dengan benar."

# Test Case 7: Registrasi Gagal (Password dan Re-Password Tidak Sama)
def test_register_failed_password_mismatch():
    driver.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("Alice")
    driver.find_element(By.NAME, "email").send_keys("alice@example.com")
    driver.find_element(By.NAME, "username").send_keys("alice")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)  # Tunggu form memproses input

    # Cari elemen dengan XPath yang benar
    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/section/section/section/form/div[5]/p"))
    )

    error_message = error_element.text
    assert "Password tidak sama !!" in error_message, "Error: Pesan error tidak ditemukan atau tidak sesuai."

# Test Case 8: Registrasi Gagal (Data Kosong)
def test_register_failed_empty_data():
    clear_browser_cache()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/register.php")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(" ")
    driver.find_element(By.NAME, "email").send_keys("siddiq@gmail.com")
    driver.find_element(By.NAME, "username").send_keys(" ")
    driver.find_element(By.NAME, "password").send_keys(" ")
    driver.find_element(By.NAME, "repassword").send_keys(" ")
    driver.find_element(By.NAME, "submit").click()
    
    # Tunggu elemen alert muncul
    error_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
    )

    error_message = error_element.text
    assert "Data tidak boleh kosong !!" in error_message, "Error: Input kosong tidak ditangani dengan benar."

# Jalankan semua test case menggunakan run_test()
test_cases = [
    test_login_success,
    test_login_failed_username,
    test_login_failed_password,
    test_login_failed_empty_data,
    test_register_success,
    test_register_failed_username_exists,
    test_register_failed_password_mismatch,
    test_register_failed_empty_data
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