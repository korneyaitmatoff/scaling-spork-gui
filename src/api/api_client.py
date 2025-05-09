from typing import Any, TypedDict

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

    def add_student(self, json: TypedDict(
        "Dict",
        {
            "name": str,
            "group_code": str,
            "inn": str,
            "is_resident": bool,
            "passport_data": TypedDict(
                "Dict",
                {
                    "serial_number": str,
                    "birthdate": str
                }
            )
        }
    )):
        return self.post(
            path="/student",
            json=json
        )

    def create_incoming_request(
            self,
            json: TypedDict(
                "Dict",
                {
                    "reason": str,
                    "study_kind": str,
                    "student_name": str,
                    "is_commerce": bool,
                    "faculty": str,
                    "course": int,
                    "student_group_code": str,
                    "contact": str
                }
            )
    ):
        return self.post(
            path="/incoming_request/create",
            json=json
        )
