import argparse
import socketserver
from corelib import config
from corelib.jim import JIM, JimResponse


class MessengerHandler(socketserver.BaseRequestHandler):
    """

    """

    clients = set()

    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.clients.add(self.request)
        if JIM.unpack(data):
            self.request.sendall(JimResponse.status_200())


class MessengerServer:
    """
    TODO Нужно использовать ассинхронный неблокирующий сервер
    """

    def __init__(self, args, options_file):
        conf = self.__get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']
        self.server = None

    def run(self):
        """
        Запуск сервера
        :return:
        """
        self.server = socketserver.TCPServer((self.host, self.port), MessengerHandler)
        self.server.serve_forever()

    def shutdown(self):
        """
        Отключение сервера
        :return:
        """
        self.server.shutdown()

    def __get_options(self, args, options_file):
        """

        :param args:
        :param options_file:
        :return:
        """
        options = config.get_json_options(options_file)
        cl_options = config.get_command_options(args, "a:p:")
        for opt in cl_options:
            if opt[0] == "-a":
                options['DEFAULT']['HOST'] = opt[1]
            elif opt[0] == "-p":
                options['DEFAULT']['PORT'] = opt[1]
        return options

