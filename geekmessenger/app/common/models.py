# -*- coding:utf-8 -*-

import datetime
import hashlib

from sqlalchemy import Table, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import validates

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

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, index=True, unique=True)
    _password = Column("password", String(192), nullable=False)
    status = Column(Integer, nullable=True)

    dialogs = relationship("Dialog", secondary='users_dialogs_association')

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

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String, nullable=False)
    dialog_id = Column(Integer, ForeignKey('dialogs.id'))

    def __init__(self, message, dialog, user):
        self.message = message
        self.dialog_id = dialog.id
        self.user_id = user.id


class Dialog(db.Base):
    """
    Dialog model
    """

    __tablename__ = 'dialogs'

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True)
    comments = relationship("Message")

    users = relationship("User", secondary='users_dialogs_association')


class AssociationUsersDialogs(Base):
    """
    Таблица связи многие ко многим для пользователей и диалогов
    """

    __tablename__ = 'users_dialogs_association'

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    dialog_id = Column(Integer, ForeignKey('dialogs.id'), index=True)

    user = relationship("User", backref=backref("dialogs_assoc"))
    dialog = relationship("Dialog", backref=backref("users_assoc"))


if __name__ == "__main__":
    """
    Перед вводом в эксплуатацию нужно создать таблици в БД
    """
    db.create_tables()
