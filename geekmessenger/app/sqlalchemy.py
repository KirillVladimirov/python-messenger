# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DisconnectionError


class SQLAlchemy(object):

    def __init__(self, config_db_uri):
        self.Base = declarative_base()
        self.engine = create_engine(config_db_uri)
        self.Session = sessionmaker(bind=self.engine)

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
