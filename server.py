#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geekmessenger.app.server import Server
from geekmessenger.app import app


if __name__ == "__main__":
    server = Server(app)
    try:
        server.start()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.stop()
