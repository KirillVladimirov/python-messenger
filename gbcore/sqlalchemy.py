#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DisconnectionError


class SQLAlchemy(object):

    DB_BASE = declarative_base()

    def __init__(self, app, config_db_uri):
        self._app = app
        if self._app.config["DEBUG_LEVEL"] == "DEBUG":
            echo = True
        else:
            echo = False
        self.engine = create_engine(config_db_uri, echo=echo)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def check_connection(self):
        result = False
        try:
            conn = self.engine.connect()
            result = True
        except DisconnectionError:
            pass
        finally:
            conn.close()

        return result

    def create_tables(self):
        self.DB_BASE.metadata.create_all(self.engine)

    def drop_tables(self):
        self.DB_BASE.metadata.drop_all(self.engine)
