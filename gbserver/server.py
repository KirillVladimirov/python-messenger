#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Server processes requests from some clients in multithreading mode

Todo:
    * Протестировать обработку сообщений
    * Протестировать конвертацию в json
    * Протестировать генерацию ответа

"""
import asyncio
from aiohttp import web
# from gbcore import db
# from gbcore.common.message import Message
# from gbcore.common.user import User


class Server(object):
    """Server application class"""

    def __init__(self, base_app):
        # setup config server
        self._encode = base_app.config['SERVER']['ENCODE']
        self._logger = base_app.logger
        self._loop = asyncio.get_event_loop()
        self._port = base_app.config['SERVER']['PORT']
        self._host = base_app.config['SERVER']['HOST']

        # init web app
        self._web_app = web.Application(loop=self._loop)

        # # add the routes
        # web_app.router.add_route('GET', '/', self.root_handler)
        # web_app.router.add_route('GET', '/registration', self.registration_handler)
        # web_app.router.add_route('GET', '/{user_id}/', self.user_handler)
        # web_app.router.add_route('GET', '/{user_id}/message', self.user_update_handler)

    def start(self):
        """
        Run server and event loop
        :return:
        """
        self._logger.info("{} | Server start!".format(__name__))
        web.run_app(
            self._web_app,
            host=self._host,
            port=self._port
        )

    @asyncio.coroutine
    def root_handler(self):
        """
        First request from client after start.
        Handler is intended only for check server is online
        :return: None
        """
        text = "Successful connection!"
        return web.Response(body=text.encode(self._encode))

    @asyncio.coroutine
    def registration_handler(self, request):
        text = "Registration completed successfully!"
        return web.Response(body=text.encode(self._encode))

    # option 2: auth at a higher level?
    # set user_id and allowed in the wsgi handler
    @asyncio.coroutine
    def user_handler(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(body=text.encode(self._encode))

    # option 3: super low
    # wsgi doesn't do anything
    @asyncio.coroutine
    def user_update_handler(request):
        # identity, asked_permission
        user_id = yield from identity_policy.identify(request)
        identity = yield from auth_policy.authorized_user_id(user_id)
        allowed = yield from request.auth_policy.permits(
            identity, asked_permission
        )
        if not allowed:
            # how is this pluggable as well?
            # ? return NotAllowedStream()
            raise NotAllowedResponse()

        update_user()

    # async def save_message(self, message):
    #     print('-----------> print message: {}'.format(message))
    #     sess = db.session
    #     message = Message.load(message)
    #     user = sess.query(User).filter_by(id=message.user_id).first()
    #     if user is None:
    #         return False
    #     sess.add(message)
    #     sess.commit()
    #     return True
