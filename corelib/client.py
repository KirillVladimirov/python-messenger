import socket
import sys
from corelib import config


def run(args, options_file):
    conf = get_options(args, options_file)
    print(conf)
    try:
        sock = socket.create_connection((conf['DEFAULT']['HOST'], conf['DEFAULT']['PORT']), 5)
    except socket.error as err:
        print("Connection error: {}".format(err))
        sys.exit(2)
    try:
        message = "Hello server"
        sock.sendall(message.encode("utf8"))
    except sock.timeout:
        print("Send data timeout")
    except socket.error as er:
        print("Send data error", er)
    sock.close()


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
