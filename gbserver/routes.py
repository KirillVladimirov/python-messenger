#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbserver.handlers import Test, TestDbSave, TestDbRead

# Registration, SignIn, SignOut
# from auth.views import Login, SignIn, SignOut

routes = [
    # ('GET', '/', ChatList, 'main'),
    ('GET', '/test', Test, 'test'),
    ('GET', '/testdbsave', TestDbSave, 'test_db_save'),
    ('GET', '/testdbread', TestDbRead, 'test_db_read'),
    # ('GET', '/registration', Registration, 'login'),
    # ('GET', '/signin', SignIn, 'signin'),
    # ('GET', '/signout', SignOut, 'signout'),
    # ('GET', '/', ChatList, 'main'),
    # ('GET', '/', ChatList, 'main'),
    # ('GET', '/ws', WebSocket, 'chat'),

]
