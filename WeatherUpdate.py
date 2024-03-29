"""Use to send mail"""
import base64
from email.message import EmailMessage
from Booking import *
import re

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

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


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
      """
    try:
        # create gmail api client
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()

        message.set_content(f"{message_string}")

        message["To"] = f"{email_adress}"
        message["From"] = "nick.decoster07@gmail.com"
        message["Subject"] = "☀️Weather for your summer holiday☀️"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}

        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        print("email sent")

        service.users().drafts().send(
            userId='me', body=draft).execute()


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
        draft = None

    return draft


def send_email():
    if __name__ == "__main__":
        main()


send_email()
