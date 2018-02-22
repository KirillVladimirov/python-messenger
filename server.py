#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbserver.server import Server
from gbcore import app


if __name__ == "__main__":
    server = Server(app)
    try:
        server.start()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.stop()
