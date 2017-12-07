import sys
from corelib.server import MessengerServer

config = "config_server.json"

if __name__ == "__main__":
    server = MessengerServer(sys.argv, config)
    try:
        print("Server run...")
        server.run()
    except KeyboardInterrupt as e:
        print("Server shutdown...")
        server.shutdown()
