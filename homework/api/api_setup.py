import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader

class ApiSetup:
    def setup_method(self):
        self.session = requests.Session()
        self.base_url = ConfigReader.get_base_url()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(5)

        # Login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys("Admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("dashboard"))

        for cookie in self.driver.get_cookies():
            self.session.cookies.set(
                name=cookie["name"],
                value=cookie["value"],
                domain=cookie["domain"],
                path=cookie["path"]
            )

        print("SESSION COOKIES:", self.session.cookies.get_dict())

    def teardown_method(self):
        self.driver.quit()
        self.session.close()



    def get(self, endpoint):
        return self.session.get(f"{self.base_url}{endpoint}", verify=False)

    def post(self, endpoint, data):
        return self.session.post(f"{self.base_url}{endpoint}", json=data, verify=False)

    def put(self, endpoint, data):
        return self.session.put(f"{self.base_url}{endpoint}", json=data, verify=False)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}", verify=False)