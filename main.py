from credentials import credentials
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 88
HEIGHT_CM = 189
AGE = 24

APP_ID = credentials["APP_ID"]
API_KEY = credentials["API_KEY"]
SHEET_ID = credentials["SHEET_ID"]
SHEET_KEY = credentials["SHEET_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheets_endpoint = "https://api.sheety.co/a06a0ddda139c41cae8be24a4eacd9eb/minTräning/workouts"

exercise_text = input("Tell me what exercise you did: ")


headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

sheet_respone = requests.post(
    sheets_endpoint, json=sheet_inputs, auth=(SHEET_ID, SHEET_KEY))

print(sheet_respone.text)
