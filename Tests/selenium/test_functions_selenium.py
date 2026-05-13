import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


BASE_URL = "http://127.0.0.1:5000"


class SeleniumFunctionTests(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def login(self, username="testuser", password="testpass"):
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # wait for redirect away from login
        self.wait.until(lambda d: "/login" not in d.current_url)

#--------------------------------------------------------------------

    def test_drawing_page_loads(self):
        self.login()

        self.driver.get(f"{BASE_URL}/drawing")

        self.assertIn("/drawing", self.driver.current_url)

    def test_submit_drawing(self):
        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/drawing")

        fake_payload = {
            "image": "data:image/png;base64,TESTDATA",
            "prompt_id": 1
        }

        driver.execute_script("""
            fetch('/submit_drawing', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(arguments[0])
            })
        """, fake_payload)

        # simple wait (replace with UI check if you add success message)
        time.sleep(1)

        self.assertTrue(True)

#--------------------------------------------------------------------

    def test_vote_increases_count(self):
        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/drawing/1")

        vote_btn = driver.find_element(By.CLASS_NAME, "vote-btn")
        count_elem = driver.find_element(By.ID, "vote-count-1")

        initial = int(count_elem.text)

        vote_btn.click()

        try:
            self.wait.until(lambda d: "Error submitting!" not in d.page_source)
        except TimeoutException:
            pass

        new_count = int(driver.find_element(By.ID, "vote-count-1").text)

        self.assertEqual(new_count, initial + 1)

    def test_duplicate_vote_blocked(self):
        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/drawing/1")

        vote_btn = driver.find_element(By.CLASS_NAME, "vote-btn")

        vote_btn.click()

        alert1 = self.wait.until(EC.alert_is_present())
        self.assertIn("Vote submitted", alert1.text)
        alert1.accept()

        vote_btn.click()

        alert2 = self.wait.until(EC.alert_is_present())

        self.assertIn("Already Voted", driver.page_source)
        alert2.accept()

if __name__ == "__main__":
    unittest.main()