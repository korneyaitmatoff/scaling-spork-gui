from typing import Any

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

    def get_students(self) -> list[dict[str, Any]]:
        return self.get(
            path="/student/?limit=100&offset=0"
        ).json()

    def get_student_by_id(self, s_id: int) -> dict[str, Any]:
        return self.get(
            path="/student/" + str(s_id)
        ).json()

    def get_students_by_name(self, name: str) -> list[dict[str, Any]]:
        return self.get(
            path="/student/get_students_by_name/" + name
        ).json()
