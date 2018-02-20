#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from sqlalchemy import Column, Integer, String, ForeignKey
from geekmessenger.app.common.base import Base


class Message(Base):
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

    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id

    def __str__(self):
        return json.dumps({'user_id': self.user_id, 'message': self.message})

    @classmethod
    def load(cls, string):
        msg, user_id = json.loads(string)
        return Message(msg, user_id)
