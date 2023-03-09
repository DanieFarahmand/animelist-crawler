from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException
from registration_data import EMAIL, PASSWORD


class Browser:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def __click_on_subtitle_button(self, x_path):
        try:
            subtitle_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, x_path)))
            self.driver.execute_script("arguments[0].scrollIntoView();", subtitle_button)
            subtitle_button.click()
        except NoSuchElementException:
            print("login button didnt find")

    def __click_on_login_button(self):
        try:
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[4]/div[4]/div/div[2]/div[2]/div/ul/li[2]/div[1]/span/a[1]")))
            login_button.click()
        except NoSuchElementException:
            print("login button didnt find")

    def __login_process(self):
        email_input = self.driver.find_element(
            By.XPATH, "/html/body/form/div/div[2]/input[1]"
        )
        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input = self.driver.find_element(
            By.XPATH, "/html/body/form/div/div[2]/input[2]"
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)
        submit_button = self.driver.find_element(
            By.XPATH, "/html/body/form/div/div[3]/div[2]/button"
        )
        submit_button.click()

    def login(self, browsing_link):
        self.driver.get(browsing_link)
        self.__click_on_subtitle_button(x_path="/html/body/div[4]/div[4]/div/div[2]/div[2]/div/div/div[2]/div")
        self.__click_on_login_button()
        self.__login_process()
        self.__click_on_subtitle_button(x_path="/html/body/div[3]/div[4]/div/div[2]/div[2]/div/div/div[2]/div")
        cookie = self.driver.get_cookies()
        self.driver.close()

        return cookie
