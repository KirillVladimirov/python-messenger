import socket
import sys
import datetime
from corelib import config
from corelib import jim
from corelib.user import User


def run(args, options_file):
    conf = get_options(args, options_file)
    try:
        sock = socket.create_connection((conf['DEFAULT']['HOST'], conf['DEFAULT']['PORT']), 5)
    except socket.error as err:
        print("Connection error: {}".format(err))
        sys.exit(2)
    print("create socket...")
    try:
        msg = auth()
        sock.sendall(msg)
        print("send message...")
    except sock.timeout:
        print("Send data timeout")
    except socket.error as er:
        print("Send data error", er)
    while True:
        try:
            msg = sock.recv(1024)
            print(jim.unpack(msg))
        except socket.timeout:
            print("Close connection by timeout.")
            break
        if not msg:
            break
    sock.close()
    print("client close...")


def get_options(args, options_file):
    """
    Get server config
    :param args: Command line arguments
    :param options_file: Config file name
    :return: dict
    """
    options = config.get_json_options(options_file)
    cl_options = config.get_command_options(args, "a:p:")
    for opt in cl_options:
        if opt[0] == "-a":
            options['DEFAULT']['HOST'] = opt[1]
        elif opt[0] == "-p":
            options['DEFAULT']['PORT'] = opt[1]
    return options


def get_user():
    return User("User", "Password")


def auth():
    user = get_user()
    time = datetime.datetime.now()
    msg = {
        "action": "authenticate",
        "time": time.isoformat(),
        "user": {
            "account_name": user.name,
            "password": user.password,
        },
    }
    return jim.pack(msg)
