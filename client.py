#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbclient.client import Client
from gbcore.application import Application

if __name__ == "__main__":
    app = Application("config/env.json")
    app.logger.info("{} | Application start ...".format(__name__))

    client = Client(app)
    client.run()
