import pytest
from api.api_setup import ApiSetup
from utils.config_reader import ConfigReader

class TestEmployeeAPI(ApiSetup):

    def test_get_employee_list(self):
        response = self.session.get(f"{self.base_url}/web/index.php/api/v2/pim/employees", verify=False)
        print("GET status:", response.status_code)
        print("Response:", response.text)
        assert response.status_code == 200

    def test_post_employee(self):
        payload = ConfigReader.get_add_employee_payload()
        response = self.session.post(
            f"{self.base_url}/web/index.php/api/v2/pim/employees",
            json=payload,
            verify=False
        )
        print("POST status:", response.status_code)
        print("Response:", response.text)
        assert response.status_code in [200, 201]

    def test_update_employee(self):
        payload = ConfigReader.get_update_employee_payload()
        employee_id = "001"
        response = self.session.put(
            f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}",
            json=payload,
            verify=False
        )
        print(response.status_code, response.text)
        assert response.status_code == 200

    def test_delete_employee(self):
        employee_id = "001"
        response = self.session.delete(
            f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}",
            verify=False
        )
        print(response.status_code, response.text)
        assert response.status_code != 500, "Server error"