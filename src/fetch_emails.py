import base64
import datetime

from db_models.email import Session, Email
from google_apis.gmail_authentication import authenticate

from src.save_email import save_emails


def fetch_emails(gmail_service, session):
    """
    Fetch emails from Gmail and store them in the database.
    """
    results = gmail_service.users().messages().list(userId="", maxResults=10).execute()  # Fetch the list of emails
    messages = results.get("messages", [])
    email_list = []
    for message in messages:
        msg = gmail_service.users().messages().get(userId="me", id=message["id"]).execute()
        payload = msg["payload"]
        headers = payload["headers"]
        labels = msg["labelIds"]

        if "data" in msg["payload"]["body"]:
            body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode("utf-8")
        else:
            for part in msg["payload"]["parts"]:
                if "data" in part["body"]:
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

        email_data = {
            "message_id": message["id"],
            "sender": next(header["value"] for header in headers if header["name"] == "From"),
            "recipient": next(header["value"] for header in headers if header["name"] == "To"),
            "subject": next(header["value"] for header in headers if header["name"] == "Subject"),
            "body": body,
            "received_date": datetime.datetime.fromtimestamp(int(msg["internalDate"]) / 1000),
            "read_status": labels[0],
            "mailbox": labels[2]
        }

        email_list.append(email_data)

    save_emails(session, email_list, Email)
    session.commit()


def main():
    gmail_service = authenticate()
    session = Session()
    fetch_emails(gmail_service, session)


if __name__ == "__main__":
    main()
