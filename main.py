#Natural Language Processing
import os
import requests
import datetime

#Track your workouts and also provide you with how many desserts you need after your workouts

GENDER = "MALE"
WEIGHT_KG = 83
HEIGHT_CM = 173
AGE = 25

# We want to store these in an environment variable for security reasons in case someone sees our code.
# Sensitive data should not be hard coded
# We can create ENVIRONMENT VARIABLES via Pycharm by going to RUN > EDIT CONFIGURATION
# These app id and app keys are from
APP_ID = os.environ["APPID"]
APP_KEYS = os.environ["APPKEYS"]
bearer_token = {
    "Authorization": f"Bearer {os.environ['BEARERTOKEN']}"
}
workout_Tracker_API_endpoint = os.environ["WORKOUT_TRACKER_API_ENDPOINT"]

#headers store our token or API key
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEYS,
}

exercise_input = input("What exercises were done?")

# #POST request - this requests sends info to the trackapi endpoint and then we get calories from it.
exercise_API_endpoints = "https://trackapi.nutritionix.com//v2/natural/exercise"

#Parameters go in the body
parameters = {
     "query": exercise_input,
     "gender":GENDER,
     "weight_kg": WEIGHT_KG,
     "height_cm": HEIGHT_CM,
     "age": AGE
 }

response = requests.post(url=exercise_API_endpoints,json=parameters,headers=headers)
result = response.json()

print(result)

today_date = datetime.datetime.now().strftime("%x")
now_time = datetime.datetime.now().strftime("%X")



# ------------ POST | Add a row to our Workout Sheet excel file ----------------


#duration = result["exercises"][0]["duration_min"]
#print(duration)

#datetime objects cannot be added as a JSON parameter so that's why you have to put "now.strftime("%x")
#calories multiply by 2 because this generates
for exercise in result["exercises"]:
    gymworkouts = {
            "exercise":{
        "date": today_date,
        "time": now_time,
        "exercise": exercise["name"].title(),
        "duration": exercise["duration_min"],
        "calories": exercise["nf_calories"]*2
            }
    }
add_row_response = requests.post(url=workout_Tracker_API_endpoint,json=gymworkouts,headers=bearer_token)
add_row_response.raise_for_status()
print(add_row_response.text)

# GET = gets the row from our spreadsheet
# get_response = requests.get(url=workout_Tracker_API_endpoint)
# get_response.raise_for_status()
# print(get_response.text)


# DELETE ---------- deletes the row from our spreadsheet
#delete_row_API_endpoint = os.environ["WORKOUT_TRACKER_API_ENDPOINT"]
#enter id at the end of the endpoint
#response = requests.delete(url=f"{delete_row_API_endpoint}/3",headers=bearer_token)
#print(response.text)

