import requests
import json
import datetime

data_info_dict = {}
message_string = ""


def weather(plaats, lat, lon):
    global message_string
    rain_list = []
    totaal_temp = []

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=55324226498c187fb750c027464f6da7&units=metric")

    finalresponse = response.json()
    timestamps = finalresponse.get("list")
    for timestamp in timestamps:
        date = timestamp.get("dt_txt")
        temp = timestamp.get("main")['temp']
        rain = timestamp.get("rain")
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        data_info_dict[date_obj] = {'temp': temp, 'rain': rain}

    for data in data_info_dict.values():
        if data['rain'] is not None:
            rain_list.append(float(data['rain']['3h']))

    totaal_rain = sum(rain_list)

    for data in data_info_dict.values():
        totaal_temp.append(float(data['temp']))
    gemiddelde_temp = sum(totaal_temp) / len(totaal_temp)

    score = 0
    if gemiddelde_temp > 10:
        score += 1
    elif 5 < gemiddelde_temp <= 10:
        score += 3
    elif 0 < gemiddelde_temp <= 5:
        score += 4
    elif gemiddelde_temp <= 0:
        score += 5

    if totaal_rain > 5:
        score += 1

    if score >= 5:
        score = 5

    message_string += f"{plaats}\n"
    message_string += f"Score: {score}/5\n"
    for date, info in data_info_dict.items():
        message_string += f"{date}\n"
        message_string += f"Temperature: {info['temp']}°c\n"
    message_string += f"Total Rain: {totaal_rain}mm\n\n"


locations = [
    {"plaats": "Ankara, Turkey", "lat": 39.9334, "lon": 32.8597},
    {"plaats": "Athens, Greece", "lat": 37.9838, "lon": 23.7275},
    {"plaats": "Valletta, Malta", "lat": 35.8989, "lon": 14.5146},
    {"plaats": "Sardinia, Italy", "lat": 40.1209, "lon": 9.0129},
    {"plaats": "Sicily, Italy", "lat": 37.5990, "lon": 14.0154},
    {"plaats": "Nicosia, Cyprus", "lat": 35.1856, "lon": 33.3823},
    {"plaats": "Mallorca, Spain", "lat": 39.6953, "lon": 3.0176},
    {"plaats": "Lagos, Portugal", "lat": 37.1028, "lon": -8.6741},
    {"plaats": "Mauritius", "lat": -20.3484, "lon": 57.5522},
    {"plaats": "Bucharest, Romania", "lat": 44.4268, "lon": 26.1025}
]

for location in locations:
    weather(location["plaats"], location["lat"], location["lon"])

print(message_string)
