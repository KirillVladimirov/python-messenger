import socket
from corelib import config
from corelib import jim


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
    print("create socket...")
    sock.listen(socket.SOMAXCONN)
    print("server listen...")
    while True:
        conn, _ = sock.accept()
        conn.settimeout(5)
        with conn:
            while True:
                try:
                    msg = conn.recv(1024)
                    print(jim.unpack(msg))
                    conn.sendall(response_200())
                except socket.timeout:
                    print("Close connection by timeout.")
                    break
                if not msg:
                    break
    sock.close()
    print("server close...")


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


def response_200():
    msg = {
        "response": 200,
        "alert": "Необязательное сообщение/уведомление"
    }
    return jim.pack(msg)


def response_402():
    msg = {
        "response": 402,
        "error": "This could be wrong password or no account with that name"
    }
    return jim.pack(msg)


def response_409():
    msg = {
        "response": 409,
        "alert": "Someone is already connected with the given user name"
    }
    return jim.pack(msg)
