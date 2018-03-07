#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiohttp import web
from gbserver.message import Message


class Test(web.View):

    async def get(self):
        text = 'Hello, world. Test view.'
        return web.Response(body=text.encode('utf8'))


class TestDbSave(web.View):

    async def get(self):
        message = Message(self.request.db)
        result = await message.save(user='test_user', msg='test_content')
        return web.json_response({'messages': str(result)})


class TestDbRead(web.View):

    async def get(self):
        message = Message(self.request.db)
        messages = await message.get_messages()
        return web.json_response({'messages': messages})

#
# class Registration(web.View):
#
#     async def get(self):
#         text = "Registration completed successfully!"
#         # self._logger.info("{} | {}".format(__name__, text))
#         return web.Response(body=text.encode(self._encode))
#
#
# class Login(web.View):
#
#     async def get(self):
#         session = await get_session(self.request)
#         if session.get('user'):
#             url = request.app.router['main'].url()
#             raise web.HTTPFound(url)
#         return b'Please enter login or email'
#
#
# class Login(web.View):
#
#     async def get(self):
#         session = await get_session(self.request)
#         if session.get('user'):
#             url = request.app.router['main'].url()
#             raise web.HTTPFound(url)
#         return b'Please enter login or email'
#
#
# class Login(web.View):
#
#     async def get(self):
#         session = await get_session(self.request)
#         if session.get('user'):
#             url = request.app.router['main'].url()
#             raise web.HTTPFound(url)
#         return b'Please enter login or email'
#
#     async def _handler(self, request):
#         text = "Registration completed successfully!"
#         self._logger.info("{} | {}".format(__name__, text))
#         return web.Response(body=text.encode(self._encode))

# async def user_handler(self, request):
#     name = request.match_info.get('name', "Anonymous")
#     text = "Hello, " + name
#     self._logger.info("{} | {}".format(__name__, text))
#     return web.Response(body=text.encode(self._encode))
#
# async def synchronization_handler(self, request):
#     data = await request.post()
#     self._logger.info("{} | {}".format(__name__, data))
#     self._logger.info("{} | {}".format(__name__, data))
#     return web.Response(body=text.encode(self._encode))
#
# async def user_message_handler(self, request):
#     data = await request.post()
#     self._logger.info("{} | {}".format(__name__, data))
#     return web.Response(body=text.encode(self._encode))
