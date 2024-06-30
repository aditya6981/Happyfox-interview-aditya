import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db_models.email_test import Email

from src.save_email import save_emails

from src.process_emails import (evaluate_conditions,
                                process_email,
                                apply_predicate)

Base = declarative_base()


class TestProcessEmails(unittest.TestCase):

    def setUp(self):
        self.db_engine = create_engine("sqlite:///emails_test.db")
        Base.metadata.create_all(self.db_engine)
        self.Session = sessionmaker(bind=self.db_engine)
        self.session = self.Session()

        emails = [
            {
                "sender": "example1@example.com",
                "subject": "Test Email 1",
                "body": "This is a test email",
                "received_date": datetime(2021, 8, 1),
                "read_status": "unread",
                "mailbox": "inbox"
            },
            {
                "sender": "example2@example.com",
                "subject": "Test Email 2",
                "body": "This is another test email",
                "received_date": datetime(2021, 8, 2),
                "read_status": "unread",
                "mailbox": "inbox"
            }
        ]

        save_emails(self.session, emails, Email)

    def tearDown(self):
        # Rollback any changes and close the session
        self.session.rollback()
        self.session.close()
        # Drop all tables and dispose of the engine
        Base.metadata.drop_all(self.db_engine)
        self.db_engine.dispose()

    def test_apply_rules(self):

        rules = [
            {
                "predicate": "all",
                "conditions": [
                    {"field": "subject", "predicate": "contains", "value": "Test"},
                    {"field": "sender", "predicate": "contains", "value": "example1"}
                ],
                "action": [
                    {"action_type": "read_status", "value": "read"},
                    {"action_type": "mailbox", "value": "inbox"}
                ]
            }
        ]

        emails = self.session.query(Email).all()
        for email in emails:
            for rule in rules:
                if evaluate_conditions(email, rule['conditions'], rule['predicate']):          
                    process_email(email, rule['action'])

        email1 = self.session.query(Email).filter_by(id=1).first()
        self.assertEqual(email1.read_status, "read")
        self.assertEqual(email1.mailbox, 'inbox')

    def test_apply_predicate(self):
        email = Email(id=1,
                      sender='example1@example.com',
                      subject='Test Email 1',
                      body='This is a test email',
                      received_date=datetime(2021, 8, 1))

        condition = {"field": "subject",
                     "predicate": "contains",
                     "value": "Test"}

        self.assertTrue(apply_predicate(email, condition))

    def test_process_action(self):
        email = Email(id=1,
                      sender='example1@example.com',
                      subject='Test Email 1',
                      body='This is a test email',
                      received_date=datetime(2021, 8, 1))
        actions = [
            {"action_type": "read_status", "value": "read"},
            {"action_type": "mailbox", "value": "inbox"}
        ]

        process_email(email, actions, self.session)
        self.assertEqual(email.read_status, "read")
        self.assertEqual(email.mailbox, 'inbox')


if __name__ == "__main__":
    unittest.main()
