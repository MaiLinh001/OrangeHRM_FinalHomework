import sys
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config_reader import ConfigReader
import allure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_call", rep)

class BaseTest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request):
        s = Service(executable_path="D:\\chromedriver-win64\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        request.cls.driver = self.driver
        request.cls.wait_for_element = self.wait_for_element

        yield

        if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Screenshot error: {e}")
        self.driver.quit()

    def wait_for_element(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
