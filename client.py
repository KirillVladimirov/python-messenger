import sys
from corelib import client

config = "config_client.json"

if __name__ == "__main__":
    client.run(sys.argv, config)
