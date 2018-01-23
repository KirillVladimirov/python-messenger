# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DisconnectionError


class SQLAlchemy(object):

    def __init__(self, app, config_db_uri):
        self._app = app
        self.Base = declarative_base()
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
