import unittest
from src.fetch_emails import fetch_emails
from google_apis.gmail_authentication import authenticate
from db_models.email import Session


class TestFetchEmails(unittest.TestCase):

    def setUp(self):
        self.gmail_service = authenticate()
        self.session = Session()

    def test_email_fetch(self):

        status, _, _ = fetch_emails(self.gmail_service,
                                    self.session)
        self.assertTrue(status)


if __name__ == "__main__":
    unittest.main()
