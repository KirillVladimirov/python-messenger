# -*- coding: utf-8 -*-

"""


Example:
    pass

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

"""
import socketserver
from app import app
from app.common.jim import JIM, JimResponse


class Handler(socketserver.BaseRequestHandler):
    """
    Client request handler
    """

    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        if JIM.unpack(data):
            self.request.sendall(JimResponse.status_200())


class Server:
    """
    Server application class
    """

    def __init__(self, base_app):
        """Summary line.

        Extended description of function.

        Args:
            base_app (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        self.host = base_app.config['SERVER']['HOST']
        self.port = base_app.config['SERVER']['PORT']

    def run(self):
        """
        Start server main loop
        :return:
        """

        with socketserver.TCPServer((self.host, self.port), Handler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
