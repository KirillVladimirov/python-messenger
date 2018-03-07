#!/usr/bin/python3
# -*- coding: utf-8 -*-


import asyncio
import os
from aiohttp import web
from gbserver.routes import routes
from gbcore.config import make_config
from gbcore.logger import make_logger
from motor import motor_asyncio as ma

# from gbcore import db
# from gbcore.common.message import Message
# from gbcore.common.user import User


class Server(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.app = web.Application(loop=self.loop)
        self.app['config'] = make_config(
            os.path.join('config', 'env.json'))
        self.encode = self.app['config']['SERVER']['ENCODE']
        self.logger = make_logger(self.app['config'])
        self.port = self.app['config']['SERVER']['PORT']
        self.host = self.app['config']['SERVER']['HOST']
        self.setup_routes()
        self.setup_middlewares()
        self.app.client = ma.AsyncIOMotorClient(self.app['config']['SERVER']['MONGO_HOST'])
        self.app.db = self.app.client[self.app['config']['SERVER']['MONGO_DB_NAME']]
        self.logger.info("Hello! Server application init.")

    def start(self):
        self.logger.info("Server start!")
        web.run_app(self.app, host=self.host, port=self.port)

    async def stop(self):
        self.app.client.close()
        await self.app.shutdown()
        await self.app.cleanup()
        self.loop.close()

    def setup_routes(self):
        for route in routes:
            self.app.router.add_route(route[0], route[1], route[2], name=route[3])

    def setup_middlewares(self):
        error_middleware = self.error_pages_middleware({
            404: self.handle_404,
            500: self.handle_500
        })
        self.app.middlewares.append(error_middleware)
        # self.app.middlewares.append(self.authorize_middleware())
        self.app.middlewares.append(self.db_handler_middleware)

    def error_pages_middleware(self, overrides):
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
        return web.Response(body=text.encode(self.encode))

    async def handle_500(self, request, response):
        text = '500 error'
        return web.Response(body=text.encode(self.encode))

    # async def authorize_middleware(self, handler):
    #     async def middleware(request):
    #         def check_path(path):
    #             result = True
    #             for r in ['/login', '/signin', '/signout']:
    #                 if path.startswith(r):
    #                     result = False
    #             return result
    #
    #         session = await get_session(request)
    #         if session.get("user"):
    #             return await handler(request)
    #         elif check_path(request.path):
    #             url = request.app.router['login'].url()
    #             raise web.HTTPFound(url)
    #             return handler(request)
    #         else:
    #             return await handler(request)
    #
    #     return middleware

    async def db_handler_middleware(self, app, handler):
        async def middleware(request):
            request.db = app.db
            response = await handler(request)
            return response

        return middleware

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
