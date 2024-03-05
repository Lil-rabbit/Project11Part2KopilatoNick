"""Use to calculate and edit weather for set weather locations"""
import requests
import json
# om datetime naar date te converte
import datetime

# ze zijn buiten de functie want vorige message string was in verschillende functie
data_info_dict = {}
message_string = ""
score = 0
rain_list = []
totaal_temp = []


def weather(plaats, lat, lon):
    global score
    global message_string
    global data_info_dict
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=55324226498c187fb750c027464f6da7&units=metric")

    finalresponse = response.json()
    timestamps = finalresponse.get("list")
    for timestamp in timestamps:
        date = timestamp.get("dt_txt")
        # [] geeft de value van de key
        temp = timestamp.get("main")['temp']
        rain = timestamp.get("rain")
        # .strftime() geeft de datetime objecten in de dictionary in een string
        # date() geeft alleen de date
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        # [key] = {values} makkelijk om dictionary van dictionary te maken
        data_info_dict[date_obj] = {'temp': temp, 'rain': rain}

    for data in data_info_dict.values():
        if rain == None:
            pass
        else:
            rains = float(rain['3h'])
            rain_list.append(rains)
    # sum() geeft de som van alle items in een iterable
    totaal_rain = sum(rain_list)

    for data in data_info_dict.values():
        temperaturen = float(temp)
        totaal_temp.append(temperaturen)
    gemiddelde_temp = (sum(totaal_temp)) / len(totaal_temp)

    if gemiddelde_temp > 10:
        score += 1
    elif 5 < gemiddelde_temp and gemiddelde_temp < 10:
        score += 3
    elif 0 < gemiddelde_temp and gemiddelde_temp < 5:
        score += 4
    elif gemiddelde_temp < 0:
        score += 5

    if totaal_rain > 5:
        score += 1

    # zodat score niet groter dan 5 is
    if score >= 5:
        score = 5
    else:
        score = score

    # buiten de functie: zodat ze niet herhalen
    message_string += f"{plaats}\n"
    message_string += f"Score: {score}/5\n"
    for date, info in data_info_dict.items():
        message_string += f"{date}\n"
        # info[''] een value uit de info nemen, en de value van ' ' nemen
        message_string += f"Temperature: {info['temp']}\n"
    message_string += f"Totaal Rain: {totaal_rain}\n"
    message_string += "\n"


weather("Ankara, Turkey", 39.9334, 32.8597)
weather("Athens, Greece", 37.9838, 23.7275)
weather("Valletta, Malta", 35.8989, 14.5146)
weather("Sardinia, Italy", 40.1209, 9.0129)
weather("Sicily, Italy", 37.5990, 14.0154)
weather("Nicosia, Cyprus", 35.1856, 33.3823)
weather("Mallorca, Spain", 39.6953, 3.0176)
weather("Lagos, Portugal", 37.1028, -8.6741)
weather("Mauritius", -20.3484, 57.5522)
weather("Bucharest, Romania", 44.4268, 26.1025)