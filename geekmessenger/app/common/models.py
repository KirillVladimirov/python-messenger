# coding=utf-8

from time import time

from geekmessenger.app import db
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Base(db.Base):
    """
    Define a base model for other database tables to inherit
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=time())
    date_updated = Column(DateTime, default=time(), onupdate=time())


class User(Base):
    """
    Define a User model
    """

    __tablename__ = 'auth_user'

    # User Name
    name = Column(String(128), nullable=False)

    # Identification Data: email & password
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(192), nullable=False)

    # Authorisation Data: role & status
    role = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    def __init__(self, name, email, password):
        """
        New instance instantiation procedure
        :param name:
        :param email:
        :param password:
        """
        self.name = name
        self.email = email
        self.password = password


class Dialog(Base):
    """
    Dialog model
    """

    __tablename__ = 'dialogs'

    id = Column(Integer, primary_key=True)
    comments = relationship("Message")


class Message(Base):
    """
    Message model
    """

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    dialog_id = Column(Integer, ForeignKey('dialog.id'))
