# -*- coding: utf-8 -*-

"""
Server processes requests from some clients in multithreading mode

Todo:
    * Протестировать обработку сообщений
    * Протестировать конвертацию в json
    * Протестировать генерацию ответа

"""
import json
import socket
import threading
import socketserver

from geekmessenger.app.common.jim import JIM, JimResponse


class Server:
    """
    Server application class
    """

    WRONG_MESSAGE_TYPE = "Wrong message type."

    def __init__(self, base_app):
        """
        Args:
            base_app (app.Application): application object
        """
        self.host = base_app.config['SERVER']['HOST']
        self.port = base_app.config['SERVER']['PORT']
        self.encode = base_app.config['SERVER']['ENCODE']
        self.logger = base_app.logger

    def run(self):
        """
        Start server main loop.

        Activate the server; this will keep running until you
        interrupt the program with Ctrl-C
        """
        with socketserver.TCPServer((self.host, self.port), Handler) as server:
                server.serve_forever()

    def get_request(self, request_byte):
        """
        Generate json from bytes

        Args:
            request_byte (bytes): client message

        Returns:
            json: client message in json format

        Raises:
            TypeError: If request_byte is not instance of bytes
        """
        if not isinstance(request_byte, bytes):
            raise TypeError(self.WRONG_MESSAGE_TYPE)
        request = request_byte.decode()
        return json.load(request)

    def get_response(self, code, message):
        """
        Generate bytes from json

        Args:
            code (int): http code
            message (str): response message

        Returns:
            bytes: client message in bytes format

        Raises:
            TypeError: If message is not instance of str
        """
        if not isinstance(message, str):
            raise TypeError(self.WRONG_MESSAGE_TYPE)
        response = {'code': code, 'message': message}
        response_dump = json.dump(response)
        return response_dump.encode(self.encode)


class Handler(socketserver.BaseRequestHandler):
    """
    Client request handler
    """

    def handle(self):
        data = self.request.recv(1024).strip()
        self.logger.info("{} wrote: {}".format(self.client_address[0], data))
        if JIM.unpack(data):
            self.request.sendall(JimResponse.status_200())
