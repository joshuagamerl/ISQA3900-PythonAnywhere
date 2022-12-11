# Unit test file to determine functionality of the Summary button
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

    def test_ll(self):

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000")
        time.sleep(5)  # pause to allow screen to load

        # click the login button - user must be logged in to logout of the program
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul/li[5]/a').click()

        # find the username and password input boxes and login
        user = "testuser"  # must be a valid username for the application
        pwd = "test123!@#"  # must be the password for a valid user

        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)  # pause to allow screen to load
        # if the Logout Link Text is found on the screen
        #   assert "Logged in" is True


        # find 'Customers' and click it
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul/li[5]/a').click()
        time.sleep(5)  # pause to allow screen to change

        # find 'Summary' and click it
        elem = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/table/tbody/tr[10]/td[10]/a').click()
        time.sleep(5)  # pause to allow screen to change

        try:
            # verify screen says 'Total of Order Charges'
            elem = driver.find_element(By.XPATH,
                                       '/html/body/div[2]/div/table/thead/tr/th')
            print("Test passed - Summary Functionality")
            assert True

        except NoSuchElementException:
            self.fail("Summary functionality does not work - test failed")

