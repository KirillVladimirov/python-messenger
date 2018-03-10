#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gbserver.handlers import Test, TestDbSave, TestDbRead, SignUp, SignIn, SignOut, SocketWorker

# Registration, SignIn, SignOut
# from auth.views import Login, SignIn, SignOut

routes = [
    # ('GET', '/', ChatList, 'main'),
    ('GET', '/test', Test, 'test'),
    ('GET', '/testdbsave', TestDbSave, 'test_db_save'),
    ('GET', '/testdbread', TestDbRead, 'test_db_read'),

    ('POST', '/signup', SignUp, 'signup'),
    ('POST', '/signin', SignIn, 'signin'),
    ('POST', '/signout', SignOut, 'signout'),
    # ('GET', '/', ChatList, 'main'),
    # ('GET', '/', ChatList, 'main'),
    ('POST', '/send', SocketWorker, 'socket_worker'),

]
