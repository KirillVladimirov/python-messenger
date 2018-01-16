# coding=utf-8

import sys
from app.client import Client

if __name__ == "__main__":
    client = Client(sys.argv)
    client.send()
