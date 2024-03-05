
import requests
import json
#om datetime naar date te converte
import datetime

#ze zijn buiten de functie want vorige message string was in verschillende functie
data_info_dict = {}
message_string = ""
score = 0
sneeuw_list = []
totaal_temp = []
def weather( plaats, lat, lon):
    global score
    global message_string
    global data_info_dict
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=209a27e0f30caf73a52128da234cf8f0&units=metric")

    finalresponse = response.json()
    timestamps = finalresponse.get("list")
    for timestamp in timestamps:
        date = timestamp.get("dt_txt")
        # [] geeft de value van de key
        temp = timestamp.get("main")['temp']
        sneeuw = timestamp.get("snow")
        # .strftime() geeft de datetime objecten in de dictionary in een string
        # date() geeft alleen de date
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        # [key] = {values} makkelijk om dictionary van dictionary te maken
        data_info_dict[date_obj] = {'temp': temp, 'sneeuw': sneeuw}

    for data in data_info_dict.values():
        if sneeuw == None:
            pass
        else:
            snows = float(sneeuw['3h'])
            sneeuw_list.append(snows)
    #sum() geeft de som van alle items in een iterable
    totaal_sneeuw = sum(sneeuw_list)

    for data in data_info_dict.values():
        temperaturen = float(temp)
        totaal_temp.append(temperaturen)
    gemiddelde_temp = (sum(totaal_temp))/len(totaal_temp)

    if gemiddelde_temp > 10:
        score += 1
    elif 5 < gemiddelde_temp and gemiddelde_temp < 10:
        score += 3
    elif 0 < gemiddelde_temp and gemiddelde_temp < 5:
        score += 4
    elif gemiddelde_temp < 0:
        score += 5

    if totaal_sneeuw > 5:
        score += 1

    #zodat score niet groter dan 5 is
    if score >= 5:
        score = 5
    else:
        score = score

    #buiten de functie: zodat ze niet herhalen
    message_string += f"{plaats}\n"
    message_string += f"Score: {score}/5\n"
    for date, info in data_info_dict.items():
        message_string += f"{date}\n"
        # info[''] een value uit de info nemen, en de value van ' ' nemen
        message_string += f"Temperature: {info['temp']}\n"
    message_string += f"Totaal Sneeuw: {totaal_sneeuw}\n"
    message_string += "\n"



weather( "Sölden", 46.9654937,11.0076232)
weather("Les Trois Vallés", 45.3499986, 6.5999976)
weather("Chamonix-Mont-Blanc",   45.92375000, 6.86933000)
weather("Val di Fassa", 46.4424081, 11.6968477)
weather("Salzburger sportwelt", 47.3202,  13.3590)
weather("Alpenarena Flims-Laax-Falera", 46.8379, 9.2756)
weather("Kitzsteinhorn Kaprun",  47.2408, 12.6867)
weather("Ski Arlberg", 47.129635, 10.268179)
weather("Espace Killy", 45.619386, 6.770892)
weather("Spindleruv Mlyn", 50.72615, 15.60944)