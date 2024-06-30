import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CURRENT_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_PATH = os.path.join(CURRENT_BASE_PATH, "token.pickle")
CREDENTIALS_PATH = os.path.join(CURRENT_BASE_PATH, "credentials.json")


def authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
                )

            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


if __name__ == "__main__":
    service = authenticate()
    print("Authentication successful!")
