"""Use to send mail"""
import re
from WeatherUpdate import *

# Ik denk het 2 keer input vraagt want ik heb deze file in WeatherUpdate gezrtten
email_adress = input("Enter your email address: ")


def check_email(email_adress):
    # \b makes sure that the whole email is read as a 1 string
    # r : raw string (letterlijk)
    # all possible "errors" for email adress
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # fullmatch() geeft True als het een match is
    if re.fullmatch(pattern, email_adress):
        pass
    else:
        print("invalid email address")


check_email(email_adress)


def send_email():
    if __name__ == "__main__":
        main()


send_email()
