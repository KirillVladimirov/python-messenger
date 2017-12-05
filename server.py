import sys
from corelib.server import MessengerServer

config = "config_server.json"

if __name__ == "__main__":
    server = MessengerServer(sys.argv, config)
    server.run()

