from requests import options

from app import create_app, db
from app.models import User
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
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        user = User.query.filter_by(username="testuser").first()
        if user:
            db.session.delete(user)
            db.session.commit()

        user = User(username="testuser")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")

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

    def test_prompt_page_loads(self):
        """Test that the main prompt page loads after login."""
        self.login()

        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/")

    def test_01_submit_drawing(self):
        """Test that submitting a drawing shows a success page."""
        self.login()

        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "submit_btn"))
        )
        submit_btn.click()

        self.wait.until(lambda d: "Daily Doodle" not in d.page_source)

        self.assertIn("http://127.0.0.1:5000/success", self.driver.current_url)



#--------------------------------------------------------------------
    def test_vote_increases_count(self):
        """Test that voting on a drawing increases the vote count."""
        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/drawing/1")

        count_elem = self.wait.until(
            lambda d: d.find_element(By.ID, "vote-count-1")
        )

        initial = int(count_elem.text)

        driver.find_element(By.CLASS_NAME, "vote-btn").click()

        alert1 = self.wait.until(EC.alert_is_present())
        self.assertIn("Vote submitted!", alert1.text)
        alert1.accept()

        new_count = int(driver.find_element(By.ID, "vote-count-1").text)

        self.assertEqual(new_count, initial + 1)

    def test_duplicate_vote_blocked(self):
        """Test that voting twice on the same drawing is blocked."""
        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/drawing/1")

        vote_btn = driver.find_element(By.CLASS_NAME, "vote-btn")

        vote_btn.click()

        alert1 = self.wait.until(EC.alert_is_present())
        alert1.accept()

        self.assertFalse(vote_btn.is_enabled())


#--------------------------------------------------------------------

    def test_sidebar_opens(self):

        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}/")  # any page with base.html works

        sidebar = driver.find_element(By.ID, "mySidenav")
        menu_button = driver.find_element(By.TAG_NAME, "button")

        # ensure sidebar is initially closed
        self.assertNotIn("open", sidebar.get_attribute("class"))

        # click menu button
        menu_button.click()

        # wait until "open" class appears
        self.wait.until(
            lambda d: "open" in d.find_element(By.ID, "mySidenav").get_attribute("class")
        )

        sidebar = driver.find_element(By.ID, "mySidenav")
        self.assertIn("open", sidebar.get_attribute("class"))

    def test_sidebar_opens_and_closes(self):

        self.login()

        driver = self.driver
        driver.get(f"{BASE_URL}")  # any page with base.html works

        sidebar = driver.find_element(By.ID, "mySidenav")
        menu_button = driver.find_element(By.TAG_NAME, "button")

        # ensure sidebar is initially closed
        self.assertNotIn("open", sidebar.get_attribute("class"))

        # click menu button
        menu_button.click()

        # wait until "open" class appears
        self.wait.until(
            lambda d: "open" in d.find_element(By.ID, "mySidenav").get_attribute("class")
        )

        sidebar = driver.find_element(By.ID, "mySidenav")
        self.assertIn("open", sidebar.get_attribute("class"))

        # close (X button inside sidebar)
        close_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "closebtn"))
        )

        close_button.click()

        self.wait.until(
            lambda d: "open" not in d.find_element(By.ID, "mySidenav").get_attribute("class")
        )

        self.assertNotIn("open", sidebar.get_attribute("class"))


if __name__ == "__main__":
    unittest.main()
