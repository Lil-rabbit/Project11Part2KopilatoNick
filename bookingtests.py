import requests
import json
import datetime

data_info_dict = {}
message_string = ""

def weather(plaats, lat, lon, ideal_temp, rain_tolerance):
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
        if date_obj not in data_info_dict:
            data_info_dict[date_obj] = {'temp': [], 'rain': []}
        data_info_dict[date_obj]['temp'].append(temp)
        if rain:
            data_info_dict[date_obj]['rain'].append(float(rain['3h']))

    for date, info in data_info_dict.items():
        avg_temp = sum(info['temp']) / len(info['temp'])
        avg_rain = sum(info['rain']) if info['rain'] else 0
        totaal_temp.append(avg_temp)
        rain_list.append(avg_rain)

    gemiddelde_temp = round(sum(totaal_temp) / len(data_info_dict))
    totaal_rain = round(sum(rain_list))

    score = 0
    # Temperature score calculation
    temp_difference = abs(gemiddelde_temp - ideal_temp)
    if temp_difference <= 2:
        score += 5
    elif temp_difference <= 3:
        score += 4
    elif temp_difference <= 5:
        score += 3
    elif temp_difference <= 7:
        score += 2
    elif temp_difference <= 10:
        score += 1

    # Rain score calculation based on user preference
    if rain_tolerance == 1:
        if totaal_rain < 1:
            score += 4
    elif rain_tolerance == 2:
        if totaal_rain < 2:
            score += 4
    elif rain_tolerance == 3:
        score += 4

    # Limiting the score to maximum 5
    score = min(score, 5)

    message_string += f"{plaats}\n"
    message_string += f"Score: {score}/5\n"
    message_string += f"Weekly Forecast:\n"
    message_string += f"Average Temperature: {gemiddelde_temp}°C\n"
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

# User input for ideal temperature and rain tolerance
ideal_temp = float(input("Enter your ideal temperature in °C: "))
print("Choose your rain tolerance:")
print("1. Zeer weinig regen (filter op minder dan 1mm per dag)")
print("2. Minder dan 2mm per dag (het Belgische gemiddelde)")
print("3. Geen voorkeur")
rain_tolerance = int(input("Enter your choice (1/2/3): "))

for location in locations:
    weather(location["plaats"], location["lat"], location["lon"], ideal_temp, rain_tolerance)

print(message_string)
