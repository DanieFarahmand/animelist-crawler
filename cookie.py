import time
from abc import ABC, abstractmethod

import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException
from registration_data import EMAIL, PASSWORD


class AbstractBrowser(ABC):

    @abstractmethod
    def get_cookie(self, browsing_url  ):
        pass


class ExecutedScriptCookie(AbstractBrowser):
    def __init__(self):
        self.driver = webdriver.Firefox()

    def __click_on_subtitle_button(self):
        try:
            # Wait up to 30 seconds for the subtitle button to be clickable
            subtitle_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[4]/div/div[2]/div[2]/div/div/div[2]/div"))
            )
            # Scroll to the subtitle button and click it
            self.driver.execute_script("arguments[0].scrollIntoView();", subtitle_button)
            subtitle_button.click()
        except NoSuchElementException:
            print("subtitle button not found")

    def get_cookie(self, browsing_url):
        self.driver.get(browsing_url)
        self.__click_on_subtitle_button()
        cookies = {}
        driver_cookies = self.driver.get_cookies()
        for cookie in driver_cookies:
            if "expiry" in cookie:
                del cookie["expiry"]
            cookies[cookie["name"]] = cookie["value"]
        return cookies


class LoginCookie(AbstractBrowser):
    def __init__(self):
        self.driver = webdriver.Firefox()

    def __click_on_login_button(self, xpath):
        try:
            # Wait up to 30 seconds for the login button to be clickable
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # Scroll to the login button and click it
            self.driver.execute_script("arguments[0].scrollIntoView();", login_button)
            login_button.click()
        except NoSuchElementException:
            print("login button not found")

    def __login_process(self, email_input_xpath, password_input_xpath, submit_button_xpath):
        try:
            # Find the email input field and fill it with the email constant
            email_input = self.driver.find_element(
                By.XPATH, email_input_xpath)
            email_input.clear()
            email_input.send_keys(EMAIL)
        except NoSuchElementException:
            print("email input button not found")
        try:
            # Find the password input field and fill it with the password constant
            password_input = self.driver.find_element(
                By.XPATH, password_input_xpath)
            password_input.clear()
            password_input.send_keys(PASSWORD)
        except NoSuchElementException:
            print("password input button not found")
        try:
            # Find the submit button and click it
            submit_button = self.driver.find_element(
                By.XPATH, submit_button_xpath)
            submit_button.click()
        except NoSuchElementException:
            print("submit button not found")

    def get_cookie(self, browsing_url):
        self.driver.get(browsing_url)
        self.__click_on_login_button(xpath="/html/body/header/div[5]/div[1]/div[3]/div/span/a")
        self.__login_process(
            email_input_xpath="/html/body/form/div/div[2]/input[1]",
            password_input_xpath="/html/body/form/div/div[2]/input[2]",
            submit_button_xpath="/html/body/form/div/div[3]/div[2]/button")
        # self.driver.close()
        cookies = {}
        driver_cookies = self.driver.get_cookies()
        for cookie in driver_cookies:
            if "expiry" in cookie:
                del cookie["expiry"]
            cookies[cookie["name"]] = cookie["value"]
        return cookies


class SingletonLoginCookie(LoginCookie):
    """
    SingletonLoginCookie is a subclass of LoginCookie that implements the singleton design pattern.
    This class ensures that only one instance of LoginCookie is created and provides a global point
    of access to it. SingletonLoginCookie also provides a method to reset the instance and check if
    the login cookie needs to be reset based on a time expiration period.

    Attributes:
        __instance (LoginCookie): A private class variable to store the instance of LoginCookie.
        login_expiration_period (int): A class variable that represents the duration after which the
        login cookie should be reset. The default value is set to 3600 seconds, or 1 hour.
    """
    __instance = None
    login_expiration_period = 3600

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @classmethod
    def reset(cls):
        """
            reset is a class method that resets the instance of LoginCookie to None. This is useful when
            we want to create a new instance of LoginCookie with new credentials.

            Args:
                cls (class): The class object that we want to reset the instance of.
            """
        cls.__instance = None

    @classmethod
    def check_reset(cls):
        """
           check_reset is a class method that checks if the login cookie needs to be reset based on a
           time expiration period. If the time since the last reset is greater than the expiration period,
           the instance of LoginCookie is reset to None.

           Args:
               cls (class): The class object that we want to check the reset time for.
           """
        current_time = time.time()
        if not hasattr(cls, "_last_reset_time"):
            cls._last_reset_time = current_time
        elif current_time - cls._last_reset_time > cls.login_expiration_period:
            cls.reset()
            cls._last_reset_time = current_time

