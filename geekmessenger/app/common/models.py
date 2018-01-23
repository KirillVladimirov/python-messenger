# coding=utf-8

import datetime

from geekmessenger.app import app
from geekmessenger.app import db

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import hashlib


class Base(db.Base):
    """
    Define a base model for other database tables to inherit
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_updated = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class User(Base):
    """
    Define a User model
    """

    __tablename__ = 'users'

    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, index=True, unique=True)
    password = Column(String(192), nullable=False)
    status = Column(Integer, nullable=True)

    def __init__(self, name, email, password):
        """
        New instance instantiation procedure
        :param name:
        :param email:
        :param password:
        """
        self.name = name
        self.email = email
        self.password = self._set_password(password)

    def _set_password(self, plain_password):
        hash_object = hashlib.sha512(bytes(plain_password, 'utf-8'))
        return hash_object.hexdigest()

    def correct_password(self, plain_password):
        hash_password = self._set_password(plain_password)
        return hash_password == self.password


class Message(db.Base):
    """
    Message model
    """

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    dialog_id = Column(Integer, ForeignKey('dialogs.id'))


class Dialog(db.Base):
    """
    Dialog model
    """

    __tablename__ = 'dialogs'

    id = Column(Integer, primary_key=True)
    comments = relationship("Message")


if __name__ == "__main__":
    db.create_tables()
