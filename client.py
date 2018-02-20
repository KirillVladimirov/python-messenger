#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geekmessenger.app.client.models import Client
from geekmessenger.app import app


if __name__ == "__main__":
    client = Client()
    client.run()
