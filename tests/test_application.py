# coding=utf-8

from unittest import TestCase, main

from app import Application
from app import app
from app import db


class TestApplication(TestCase):

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


if __name__ == '__main__':
    main()
