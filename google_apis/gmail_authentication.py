import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CURRENT_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SCOPES = [
          'https://www.googleapis.com/auth/gmail.modify'
          ]

TOKEN_PATH = os.path.join(CURRENT_BASE_PATH, "token.pickle")
CREDENTIALS_PATH = os.path.join(CURRENT_BASE_PATH, "credentials.json")


def authenticate():
    """
        Function to authenticate gmail service api

        It will open the browser and prompt to authorize the first time, this
        will create 'token.pickle' file needed for the api.
        'token.pickle' will be used to autorefresh authentication without any
        prompts from the second time.
    """

    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        # Refreshes token if token already exists
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Pass the credentials file and access scopes to create the token
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
                )

            creds = flow.run_local_server(port=0)

        # Save the tokens in a pickle file
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    # return token for authentication
    return creds


if __name__ == "__main__":
    creds = authenticate()
    print("Authentication successful!")
