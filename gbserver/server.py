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
        self.setup_routes()
        self.setup_middlewares()

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

    def setup_routes(self):
        self._web_app.router.add_route('GET', '/', self.root_handler)
        self._web_app.router.add_route('GET', '/registration', self.registration_handler)
        self._web_app.router.add_route('GET', '/{user_id}/', self.user_handler)
        self._web_app.router.add_route('GET', '/{user_id}/message', self.user_update_handler)

    def setup_middlewares(self):
        error_middleware = self.error_pages({
            404: self.handle_404,
            500: self.handle_500
        })
        self._web_app.middlewares.append(error_middleware)

    async def root_handler(self, request):
        """
        First request from client after start.
        Handler is intended only for check server is online
        :return: None
        """
        text = "Successful connection!"
        self._logger.info("{} | {}".format(__name__, text))
        return web.Response(body=text.encode(self._encode))

    async def registration_handler(self, request):
        text = "Registration completed successfully!"
        self._logger.info("{} | {}".format(__name__, text))
        return web.Response(body=text.encode(self._encode))

    async def user_handler(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        self._logger.info("{} | {}".format(__name__, text))
        return web.Response(body=text.encode(self._encode))

    async def user_update_handler(request):
        pass

    def error_pages(self, overrides):
        async def middleware(app, handler):
            async def middleware_handler(request):
                try:
                    response = await handler(request)
                    override = overrides.get(response.status)
                    if override is None:
                        return response
                    else:
                        return await override(request, response)
                except web.HTTPException as ex:
                    override = overrides.get(ex.status)
                    if override is None:
                        raise
                    else:
                        return await override(request, ex)

            return middleware_handler

        return middleware

    async def handle_404(self, request, response):
        text = '404 error'
        return web.Response(body=text.encode(self._encode))

    async def handle_500(self, request, response):
        text = '500 error'
        return web.Response(body=text.encode(self._encode))

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
