#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbserver.server import Server

if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        server.logger.info("Stop Server begin ...")
    finally:
        server.stop()
        server.logger.info("Server stop. Goodbye!")
