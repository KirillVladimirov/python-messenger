pyuic5 messanger_window.ui -o messanger_window.py

python -m http.server 8888

python -m SimpleHTTPServer 8888

class TestApplication(TestCase):
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))