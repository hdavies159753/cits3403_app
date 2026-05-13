import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:5000"


class LoginSeleniumTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def test_login_failure(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.NAME, "username").send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")

        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        alert = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )

        self.assertIn("Invalid username or password", alert.text)

    def test_login_success(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpass")

        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # wait for redirect away from login
        self.wait.until(lambda d: "/login" not in d.current_url)

        self.assertTrue(driver.current_url.endswith("/"))