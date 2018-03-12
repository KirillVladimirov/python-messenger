#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DisconnectionError
import os


def make_db(config_dict):
    sql_path = os.path.join(config_dict["APPLICATION_ROOT"], "sql", config_dict["SQLALCHEMY"]["DB"])
    sql_uri = "sqlite:///{}".format(sql_path)
    return SQLAlchemy(config_dict, sql_uri)


class SQLAlchemy(object):
    DB_BASE = declarative_base()

    def __init__(self, config_dict, config_db_uri):
        self.config = config_dict
        if self.config["DEBUG_LEVEL"] is "DEBUG":
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
