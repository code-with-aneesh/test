import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the Chrome WebDriver
        cls.driver = webdriver.Chrome()  # Make sure to specify the path if not in PATH
        cls.driver.get("http://127.0.0.1:5000/")  # URL of the Flask app

    def test_register(self):
        self.driver.find_element(
            By.LINK_TEXT, "Register"
        ).click()  # Navigate to the registration page
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(
            By.XPATH, "//button[@type='submit']"
        ).click()  # Submit the registration form
        time.sleep(1)  # Wait for the redirect
        self.assertIn(
            "Login", self.driver.title
        )  # Check if redirected to the login page

    def test_login(self):
        self.driver.find_element(
            By.LINK_TEXT, "Login"
        ).click()  # Navigate to the login page
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(
            By.XPATH, "//button[@type='submit']"
        ).click()  # Submit the login form
        time.sleep(1)  # Wait for the redirect
        self.assertIn(
            "Dashboard", self.driver.title
        )  # Check if redirected to the dashboard

    def test_logout(self):
        self.driver.find_element(
            By.LINK_TEXT, "Logout"
        ).click()  # Logout from the dashboard
        time.sleep(1)  # Wait for the redirect
        self.assertIn(
            "Login", self.driver.title
        )  # Check if redirected to the login page

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Close the browser after tests


if __name__ == "__main__":
    unittest.main()
