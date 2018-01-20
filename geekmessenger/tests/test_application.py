# coding=utf-8

import pytest

from geekmessenger.app import Application
from geekmessenger.app import app
from geekmessenger.app import db


class TestApplication(object):

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_create_app(self):
        application = Application()
        self.assertMultiLineEqual(application.name, 'python_messenger')

    def test_get_ready_app_object(self):
        self.assertMultiLineEqual(app.name, 'python_messenger')

    def test_bd_connection(self):
        self.assertTrue(db.check_connection())

    def test_make_config(self):
        self.assertEqual(app.config["SERVER"]["HOST"], "127.0.0.1")
        self.assertEqual(app.config["SERVER"]["PORT"], 8010)

    def test_set_config_attr(self):
        app.config['GEEK_HOST'] = "https://geekbrains.ru"
        self.assertEqual(app.config["GEEK_HOST"], "https://geekbrains.ru")
