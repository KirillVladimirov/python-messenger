#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbserver.server import Server
from gbcore.app.application import Application


if __name__ == "__main__":
    app = Application()
    # setup config file
    app.config.from_json("config/env.json")
    app.logger.info("{} | Application start ...".format(__name__))
    server = Server(app)
    try:
        server.start()
    except KeyboardInterrupt:
        # Press Ctrl+C to stop
        pass
    finally:
        app.logger.info("{} | Application stop. Goodbye!".format(__name__))
