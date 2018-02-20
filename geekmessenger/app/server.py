#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Server processes requests from some clients in multithreading mode

Todo:
    * Протестировать обработку сообщений
    * Протестировать конвертацию в json
    * Протестировать генерацию ответа

"""
import json
import os
import sys
import asyncio
import logging
import concurrent.futures
import socketserver

from geekmessenger.app.common.jim import JIM, JimResponse


class Server(object):
    """Server application class"""

    WRONG_MESSAGE_TYPE = "Wrong message type."

    def __init__(self, base_app, loop=None):
        self._encode = base_app.config['SERVER']['ENCODE']
        self._logger = base_app.logger
        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(
            self.handle_connection,
            host=base_app.config['SERVER']['HOST'],
            port=base_app.config['SERVER']['PORT']
        )

    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        self._logger.info('Listening established on {0}'.format(self._server.sockets[0].getsockname()))
        if and_loop:
            self._loop.run_forever()

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        peer_name = writer.get_extra_info('peername')
        self._logger.info('Accepted connection from {}'.format(peer_name))
        while not reader.at_eof():
            try:
                data = yield from asyncio.wait_for(reader.read(100), timeout=10.0)
                message = data.decode()
                self._logger.info('Received {} from {}'.format(message, peer_name))
                writer.write(data)
                writer.drain()
            except concurrent.futures.TimeoutError:
                break
        writer.close()


if __name__ == '__main__':
    server = EchoServer('127.0.0.1', 2007)
    try:
        server.start()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.stop()
