import requests
import pandas as pd
import os


class SpreadSheetDealer:
    def __init__(self):
        self.my_token = os.environ.get("TOKEN")
        self.my_header = {
            "Authorization": self.my_token
        }
        self.my_id = os.environ.get("S_ID")
        self.project_name = "burntCalories"
        self.sheet_name = "calories"
        self.my_endpoint = f"https://api.sheety.co/{self.my_id}/{self.project_name}/{self.sheet_name}"

    def post_method(self, current_date, exercise_type, duration_min, calories):
        sheet_info = {
            "calory": {
                "date": current_date,
                "exercise": exercise_type,
                "duration": duration_min,
                "calories": calories
            }
        }
        response = requests.post(url=self.my_endpoint, json=sheet_info, headers=self.my_header)
        return response.status_code

    def get_method(self):
        response = requests.get(url=self.my_endpoint, headers=self.my_header)
        result = response.json()["calories"]
        answer = pd.DataFrame(result)
        return answer

    def delete_method(self, object_id):
        delete_endpoint = f"{self.my_endpoint}/{object_id}"
        response = requests.delete(url=delete_endpoint, headers=self.my_header)
        return response.status_code

    def update_method(self, object_id, new_current_date, new_exercise_type, new_duration_min, new_calories):
        sheet_info = {
            "calory": {
                "date": new_current_date,
                "exercise": new_exercise_type,
                "duration": new_duration_min,
                "calories": new_calories
            }
        }
        update_endpoint = f"{self.my_endpoint}/{object_id}"
        response = requests.put(url=update_endpoint, json=sheet_info, headers=self.my_header)
        return response.status_code
