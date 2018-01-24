# coding=utf-8

import datetime
import hashlib

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from geekmessenger.app import db


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
    _password = Column("password", String(192), nullable=False)
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
        # self.password = self._set_password(password)
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.hash_password(password)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def correct_password(self, plain_password):
        hash_password = self.hash_password(plain_password)
        return hash_password == self.password

    def hash_password(self, password):
        hash_object = hashlib.sha512(bytes(password, 'utf-8'))
        return hash_object.hexdigest()


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
