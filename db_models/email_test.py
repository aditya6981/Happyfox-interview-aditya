from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Email(Base):
    """
    Define the Email model which maps to the emails table in the database.
    """
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)  # Primary Key
    message_id = Column(String, unique=True)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    body = Column(Text)
    received_date = Column(DateTime)
    read_status = Column(String, default="unread")
    mailbox = Column(String, default="inbox")


DATABASE_URL = "sqlite:///emails_test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
