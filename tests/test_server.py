import pytest
from aiohttp import web
from gbserver.server import Server
from gbcore.application import Application


async def test_hello(test_client):
    app = Application("config/env.json")
    app.logger.info("{} | Application start ...".format(__name__))

    server = Server(app)
    client = await test_client(server.get_web_app())
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text

# async def previous(request):
#     if request.method == 'POST':
#         request.app['value'] = (await request.post())['value']
#         return web.Response(body=b'thanks for the data')
#     return web.Response(
#         body='value: {}'.format(request.app['value']).encode('utf-8'))

# @pytest.fixture
# def cli(loop, aiohttp_client):
#     app = web.Application()
#     app.router.add_get('/', previous)
#     app.router.add_post('/', previous)
#     return loop.run_until_complete(aiohttp_client(app))


# async def test_set_value(cli):
#     resp = await cli.post('/', data={'value': 'foo'})
#     assert resp.status == 200
#     assert await resp.text() == 'thanks for the data'
#     assert cli.server.app['value'] == 'foo'
#
#
# async def test_get_value(cli):
#     cli.server.app['value'] = 'bar'
#     resp = await cli.get('/')
#     assert resp.status == 200
#     assert await resp.text() == 'value: bar'


# class TestServer(object):
#
#     CODE_200 = 200
#     CODE_404 = 404
#     CODE_500 = 500
#
#     MESSAGE = "some message"
#
#     REQUEST = {'action': 'echo', 'message': 'some message'}
#     REQUEST_STR = "{'action':'echo', 'message': 'some message'}"
#     REQUEST_BYTES = b"{'action':'echo', 'message': 'some message'}"
#
#     RESPONSE = {'code': 200, 'message': 'some message'}
#     RESPONSE_BYTES = b"{'code': 200, 'message': 'some message'}"
#
#     WRONG_ACTION_REQUEST = "{'action': 'wrong', 'message': 'some message'}"
#     WRONG_REQUEST = b"some wrong message"
#
#     def setup_method(self, method):
#         self.server = Server(app)
#
#     def teardown_method(self, method):
#         del self.server
#
#     def test_server_config(self):
#         assert isinstance(self.server, Server)
#
#     def test_server_run(self):
#         pass
#
#     def test_handel_request(self):
#         # code, message = self.server.handel_request(self.REQUEST_STR)
#         # assert code, self.CODE_200
#         pass
#
#     def test_handel_wrong_action_request(self):
#         # code, message = self.server.handel_request(self.WRONG_ACTION_REQUEST)
#         # assert code, self.CODE_404
#         pass
#
#     def test_handel_wrong_request(self):
#         # code, message = self.server.handel_request(self.WRONG_REQUEST)
#         # assert code, self.CODE_500
#         pass
#
#     def test_server_can_receive_message(self):
#         pass
#
#     def test_server_can_send_message(self):
#         pass
