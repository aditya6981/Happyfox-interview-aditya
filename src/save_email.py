def save_emails(session, emails, Email):

    for email in emails:
        new_email = Email(**email)
        session.add(new_email)
    session.commit()
