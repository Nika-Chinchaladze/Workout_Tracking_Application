import requests
import os


class GetAnswer:
    def __init__(self):
        self.my_id = os.environ.get("N_ID")
        self.my_key = os.environ.get("N_KEY")
        self.my_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
        self.my_header = {
            "x-app-id": self.my_id,
            "x-app-key": self.my_key
        }

    def get_answer(self, workout, gender, weight, height, age):
        exercise_info = {
            "query": workout,
            "gender": gender,
            "weight_kg": weight,
            "height_cm": height,
            "age": age
        }
        response = requests.post(url=self.my_endpoint, json=exercise_info, headers=self.my_header)
        result = response.json()["exercises"][0]
        return result
