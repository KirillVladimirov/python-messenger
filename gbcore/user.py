#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from gbcore.base import Base


class User(Base):
    """
    Define a User model
    """

    __tablename__ = 'users'

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

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
