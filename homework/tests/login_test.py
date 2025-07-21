from selenium.webdriver.common.by import By
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
import allure

class Test_Login(BaseTest):
    INVALID_CREDENTIALS_LOCATOR = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    REQUIRED_FIELD_LOCATOR = (By.CLASS_NAME, "oxd-input-field-error-message")
    DASHBOARD_LOCATOR = (By.XPATH, "//h6[text()='Dashboard']")

    @allure.story("Invalid Username")
    def test_login_invalid_username(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_invalid_username(), ConfigReader.get_password())
        error_element = self.wait_for_element(self.INVALID_CREDENTIALS_LOCATOR)
        assert "Invalid credentials" in error_element.text

    @allure.story("Blank Username")
    def test_login_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_blank_username(), ConfigReader.get_password())
        error_element = self.wait_for_element(self.REQUIRED_FIELD_LOCATOR)
        assert "Required" in error_element.text

    @allure.story("Valid Login")
    def test_login_success(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_username(), ConfigReader.get_password())
        dashboard_header = self.wait_for_element(self.DASHBOARD_LOCATOR)
        assert "Dashboard" in dashboard_header.text

""" Nếu chạy từng test bằng lệnh:
    pytest tests/login_test.py::Test_Login::test_login_invalid_username
    pytest tests/login_test.py::Test_Login::test_login_invalid_password
    pytest tests/login_test.py::Test_Login::test_login_success
thì PASSED, Nếu chạy cùng lúc bằng lệnh:
    pytest tests/login_test.py -s 
thì chỉ PASSED test đầu tiên """