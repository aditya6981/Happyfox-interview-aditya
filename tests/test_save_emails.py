import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from db_models.email_test import Email

from src.save_email import save_emails

import os

Base = declarative_base()


class TestSaveEmails(unittest.TestCase):


    def setUp(self):

        self.db_engine = create_engine("sqlite:///emails_test.db")
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()

    def tearDown(self):
        # Rollback any changes and close the session
        self.session.rollback()
        self.session.close()
        # Drop all tables and dispose of the engine
        Base.metadata.drop_all(self.db_engine)
        self.db_engine.dispose()

        os.remove("emails_test.db")

    def test_save_emails(self):

        emails = [
            {
                "sender": "example1@example.com",
                "subject": "Test Email 1",
                "body": "This is a test email",
                "received_date": datetime(2021, 8, 1),
                "read_status": "unread",
                "mailbox": "inbox",
                "message_id": "1"
            },
            {
                "sender": "example2@example.com",
                "subject": "Test Email 2",
                "body": "This is another test email",
                "received_date": datetime(2021, 8, 2),
                "read_status": "unread",
                "mailbox": "inbox",
                "message_id": "2"
            }
        ]

        _ = save_emails(self.session, emails, Email)
        saved_emails = self.session.query(Email).all()

        for s in saved_emails:
            print(s.__dict__)

        self.assertEqual(len(saved_emails), 2)
        self.assertEqual(saved_emails[0].subject, "Test Email 1")
        self.assertEqual(saved_emails[1].subject, "Test Email 2")


if __name__ == "__main__":
    unittest.main()
