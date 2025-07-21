from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config_reader import ConfigReader

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_field = (By.NAME, 'username')
        self.password_field = (By.NAME, 'password')
        self.login_button = (By.XPATH, "//button[@type='submit']")

    def enter_username(self, username: str):
        self.send_keys(self.username_field, username)

    def enter_password(self, password: str):
        self.send_keys(self.password_field, password)

    def click_login(self):
        self.click(self.login_button)

    def do_login(self, username, password):
        # self.enter_username(username)
        # self.enter_password(password)
        # self.click_login()
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def load(self):
        self.driver.get(ConfigReader.get_base_url())
