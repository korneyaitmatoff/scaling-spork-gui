from src.api.base_client import BaseClient


class ApiClient(BaseClient):
    def __init__(self, url: str):
        super().__init__(url)

    def is_employee_creds_correct(self, login: str, password: str) -> bool:
        return self.post(
            path="/employee/is_user_creds_correct",
            json={
                "login": login,
                "password": password
            }
        ).json()
