# coding=utf-8

from .application import Application
from .sqlalchemy import SQLAlchemy
import os


app = Application()
app.config.from_json("config/env.json")

app.logger.info("Application start ...")

if app.config["SQLALCHEMY"]["SCHEMA"] == "sqlite":
    sql_path = os.path.join(app.config["APPLICATION_ROOT"], "databases", app.config["SQLALCHEMY"]["DB"])
    sql_uri = "sqlite:///{}".format(sql_path)
else:
    err_mes = "Database connection parameters are not set."
    app.logger.error(err_mes)
    raise Exception(err_mes)

db = SQLAlchemy(sql_uri)
if not db.check_connection():
    err_mes = "Could not connect to database."
    app.logger.error(err_mes)
    raise Exception(err_mes)

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
