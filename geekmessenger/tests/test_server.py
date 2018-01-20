# coding=utf-8

from unittest import TestCase, main
from app import app
from app.server import Server


class TestServer(TestCase):
    CODE_200 = 200

    CODE_404 = 404

    CODE_500 = 500

    REQUEST = {'action': 'echo', 'message': 'some message'}
    REQUEST_NOT_BYTE = "{'action':'echo', 'message': 'some message'}"
    REQUEST_BYTES = b"{'action':'echo', 'message': 'some message'}"

    MESSAGE = "some message"

    RESPONSE = {'code': 200, 'message': 'some message'}
    RESPONSE_BYTES = b"{'code': 200, 'message': 'some message'}"

    def test_server_config(self):
        server = Server(app)
        self.assertEqual(server)

    def test_server_run(self):
        pass

    def test_server_shutdown(self):
        pass

    def test_server_can_receive_message(self):
        pass

    def test_server_can_send_message(self):
        pass


if __name__ == '__main__':
    main()
