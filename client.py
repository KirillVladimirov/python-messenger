import sys
from corelib.client import MessengerClient

config = "config_client.json"

if __name__ == "__main__":
    client = MessengerClient(sys.argv, config)
    client.send()
