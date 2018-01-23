# coding=utf-8

import pytest
from geekmessenger.app import app
from geekmessenger.app.server import Server


class TestServer(object):

    CODE_200 = 200
    CODE_404 = 404
    CODE_500 = 500

    MESSAGE = "some message"

    REQUEST = {'action': 'echo', 'message': 'some message'}
    REQUEST_STR = "{'action':'echo', 'message': 'some message'}"
    REQUEST_BYTES = b"{'action':'echo', 'message': 'some message'}"

    RESPONSE = {'code': 200, 'message': 'some message'}
    RESPONSE_BYTES = b"{'code': 200, 'message': 'some message'}"

    WRONG_ACTION_REQUEST = "{'action': 'wrong', 'message': 'some message'}"
    WRONG_REQUEST = b"some wrong message"

    def setup_method(self, method):
        self.server = Server(app)

    def teardown_method(self, method):
        del self.server

    def test_server_config(self):
        assert isinstance(self.server, Server)

    def test_server_run(self):
        pass

    def test_handel_request(self):
        # code, message = self.server.handel_request(self.REQUEST_STR)
        # assert code, self.CODE_200
        pass

    def test_handel_wrong_action_request(self):
        # code, message = self.server.handel_request(self.WRONG_ACTION_REQUEST)
        # assert code, self.CODE_404
        pass

    def test_handel_wrong_request(self):
        # code, message = self.server.handel_request(self.WRONG_REQUEST)
        # assert code, self.CODE_500
        pass

    def test_server_can_receive_message(self):
        pass

    def test_server_can_send_message(self):
        pass
