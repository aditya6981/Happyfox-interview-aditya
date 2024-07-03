import base64
import datetime

from google_apis.gmail_authentication import authenticate
from db_models.email import Session, Email

from src.save_email import save_emails
from src.constants import ACCEPTED_FOLDER_LABELS

import traceback


def fetch_emails(gmail_service, session):
    """
    Function to Fetch emails from Gmail and store them in the database.
    """

    # Fetch the list of emails using gmail api service
    results = gmail_service.users().messages().list(userId="",
                                                    maxResults=10).execute()

    messages = results.get("messages", [])
    email_list = []
    try:
        """
        Iterate the email messages in response and create email records to 
        save in DB
        """
        for message in messages:
            msg = gmail_service.users().messages().get(userId="me", id=message["id"]).execute()     
            payload = msg["payload"]
            headers = payload["headers"]
            labels = msg["labelIds"]

            # Decoding email body from base64 format to normal strings
            if "data" in msg["payload"]["body"]:
                body = base64.urlsafe_b64decode(
                    msg["payload"]["body"]["data"]).decode("utf-8")           
            else:
                for part in msg["payload"]["parts"]:
                    if "data" in part["body"]:
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"]).decode("utf-8")
            print("Labels :", labels)

            read_status = 'unread' if 'UNREAD' in labels else 'read'

            for label in labels:
                if label in ACCEPTED_FOLDER_LABELS:
                    mailbox = label.lower()
                    break

            # Creating email record
            email_data = {
                "message_id": message["id"],
                "sender": next(header["value"] for header in headers if header["name"] == "From"),
                "recipient": next(header["value"] for header in headers if header["name"] == "To"),
                "subject": next(header["value"] for header in headers if header["name"] == "Subject"),
                "body": body,
                "received_date": datetime.datetime.fromtimestamp(int(msg["internalDate"]) / 1000),
                "read_status": read_status,
                "mailbox": mailbox
            }

            print("Email Sender, Subject:", email_data["sender"], email_data["recipient"])
            email_list.append(email_data)

        # Save the email records in DB and commit
        ingested_count = save_emails(session, email_list, Email)
        saved_emails = session.query(Email).all()
        session.commit()

    except Exception as e:
        print(traceback.format_exc())
        saved_emails = session.query(Email).all()
        ingested_count = 0
        return False, ingested_count, len(saved_emails)

    return True, ingested_count, len(saved_emails)


if __name__ == "__main__":
    # authenticate gmail and return gmail service api
    gmail_service = authenticate()

    # Create a DB session to store data
    session = Session()
    status, ingested_count, total_saved_emails = fetch_emails(gmail_service,
                                                              session)
    print("Status :",status)
    print("New Emails fetched from Gmail : ", ingested_count)
    print("Total Emails in DB:", total_saved_emails)
    print("Emails fetched and saved to DB successfully !")
