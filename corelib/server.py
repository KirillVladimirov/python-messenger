import socket
from corelib import config


def run(args, options_file):
    """
    Run server
    :param args: Command line arguments
    :param options_file: Config file name
    :return:
    """
    conf = get_options(args, options_file)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((conf['DEFAULT']['HOST'], conf['DEFAULT']['PORT']))
    sock.listen(socket.SOMAXCONN)
    while True:
        conn, _ = sock.accept()
        conn.settimeout(5)
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    print("Close connection by timeout.")
                    break
                if not data:
                    break
                print(data.decode("utf8"))
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
