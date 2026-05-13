import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:5000"


class SidebarTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def test_sidebar_opens(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/login")  # any page with base.html works

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
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        sidebar = driver.find_element(By.ID, "mySidenav")

        # open
        driver.find_element(By.TAG_NAME, "button").click()

        self.wait.until(
            lambda d: "open" in d.find_element(By.ID, "mySidenav").get_attribute("class")
        )

        # close (X button inside sidebar)
        close_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "closebtn"))
        )

        close_button.click()

        self.wait.until(
            lambda d: "open" not in d.find_element(By.ID, "mySidenav").get_attribute("class")
        )

        self.assertNotIn("open", sidebar.get_attribute("class"))