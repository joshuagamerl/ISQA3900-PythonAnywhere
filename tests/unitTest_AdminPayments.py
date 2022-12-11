# Unit test file to determine proper payment functionality
# through the Admin Page

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings


class ll_ATS(unittest.TestCase):
    # set up the test class - assign the driver to Chrome - if using a different
    # browser, change the browser name below
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning)  # ignore resource warning if occurs

    # Test if Customer list is displayed when Customers are clicked in the Navigation bar
    # Customer list is shown if the 'summary' button exists on the page
    def test_ll(self):

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/admin/")
        time.sleep(5)  # pause to allow screen to load

        # find the username and password input boxes and login
        user = "testuser"  # must be a valid username for the application
        pwd = "test123!@#"  # must be the password for a valid user

        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)  # pause to allow screen to load
        # if the Logout Link Text is found on the screen
        #   assert "Logged in" is True


        # find 'Payments' and click it
        elem = driver.find_element(By.XPATH, '//*[@id="content-main"]/div[2]/table/tbody/tr[5]/th/a').click()
        time.sleep(5)  # pause to allow screen to change

        # find 'Add Payments' and click it
        elem = driver.find_element(By.XPATH, '//*[@id="content-main"]/ul/li/a').click()
        time.sleep(5)  # pause to allow screen to change


        try:
            # verify 'Payment Type' drop down list exists ''
            elem = driver.find_element(By.XPATH,
                                       '//*[@id="id_payment_type"]')
            print("Test passed - Add Payment Functionality")
            assert True

        except NoSuchElementException:
            self.fail("Add payment functionality does not work - test failed")

