import requests
# om datetime naar date te converten
import datetime


def get_weather_data(lat, lon):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}"
        f"&appid=55324226498c187fb750c027464f6da7&units=metric")
    return response.json()


def process_weather_data(weather_data):
    data_info_dict = {}
    for timestamp in weather_data["list"]:
        date = timestamp["dt_txt"]
        # [] geeft de value van de key
        temp = timestamp["main"]["temp"]
        rain = timestamp.get("rain", {}).get("3h", 0)
        # .strftime() geeft de datetime objecten in de dictionary in een string
        # date() geeft alleen de date
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        if date_obj not in data_info_dict:
            # [key] = {values} makkelijk om dictionary van dictionary te maken
            data_info_dict[date_obj] = {"temps": [], "rain": []}
        data_info_dict[date_obj]["temps"].append(temp)
        data_info_dict[date_obj]["rain"].append(float(rain))
    return data_info_dict


def calculate_scores(data_info_dict, ideal_temp, rain_tolerance):
    total_temp = []
    total_rain = 0   # beginning of rain for the week = 0
    num_days_with_rain = 0  # Track number of days with rain for average
    for date, info in data_info_dict.items():
        avg_temp = sum(info["temps"]) / len(info["temps"])
        total_temp.append(avg_temp)
        if info["rain"]:  # Check if there's any rain for the day
            total_rain += sum(info["rain"])  # sum of all daily rain
            num_days_with_rain += 1  # amount of days with rain

    weekly_avg_temp = round(sum(total_temp) / len(data_info_dict), 1)

    if num_days_with_rain > 0:  # check if there were days with rain in the week
        weekly_avg_rain = round(total_rain / num_days_with_rain, 1)  # get weekly average rain
    else:
        weekly_avg_rain = 0  # if there was no rain during the week -> set average rain to 0

# calculate score based on user input
    score = 0
    temp_difference = abs(weekly_avg_temp - ideal_temp)
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

    if rain_tolerance == 1:
        if weekly_avg_rain < 1:
            score += 4
    elif rain_tolerance == 2:
        if weekly_avg_rain < 2:
            score += 4
    elif rain_tolerance == 3:
        score += 4

    return score, weekly_avg_temp, weekly_avg_rain


def generate_message(plaats, gemiddelde_temp, average_rain_per_day, rain_tolerance):
    message_string = f"{plaats}\n"
    message_string += f"Weekly Forecast:\n"
    message_string += f"Average Temperature: {gemiddelde_temp}°C\n"

    if average_rain_per_day <= 1:
        message_string += "Expected Rainfall: Very little (less than 1mm)\n"
    elif average_rain_per_day <= 2:
        message_string += "Expected Rainfall: Moderate (less than 2mm)\n"
    else:
        message_string += "Expected Rainfall: High (more than 2mm)\n"

    message_string += "\n"
    return message_string


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

ideal_temp = float(input("Enter your ideal temperature in °C: "))
print("Choose your rain tolerance:")
print("1. Very little rain (filter for less than 1mm per day)")
print("2. Less than 2mm per day (Belgian average)")
print("3. No preference")
rain_tolerance = int(input("Enter your choice (1/2/3): "))

print(" Please wait...")


sorted_locations = sorted(locations, key=lambda x: -
calculate_scores(process_weather_data(get_weather_data(x["lat"], x["lon"])), ideal_temp, rain_tolerance)[0])

# empty string to store message
message_string = ""
for location in sorted_locations:
    # calculate score for the current location based on weather data
    score, gemiddelde_temp, average_rain_per_day = calculate_scores(
        process_weather_data(get_weather_data(location["lat"], location["lon"])), ideal_temp, rain_tolerance)

    # Generate message for the current location using the calculated scores (based on user input)
    location_message = generate_message(location["plaats"], gemiddelde_temp, average_rain_per_day, rain_tolerance)

    # add generated message for current location to message string
    message_string += location_message
