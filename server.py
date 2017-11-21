import sys
from corelib import server

config = "config_server.json"

if __name__ == "__main__":
    server.run(sys.argv, config)

