# coding=utf-8

import sys
from app.server import Server

if __name__ == "__main__":
    server = Server(sys.argv)
    server.run()
