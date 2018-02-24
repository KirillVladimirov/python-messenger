#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Column, DateTime, Integer
from gbcore.sqlalchemy import SQLAlchemy


class Base(SQLAlchemy.DB_BASE):
    """
    Define a base model for other database tables to inherit
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_updated = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
