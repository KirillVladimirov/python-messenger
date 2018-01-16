# coding=utf-8

import unittest
from app import Application


class TestApplication(unittest.TestCase):

    def test_create_app(self):
        app = Application()
        self.assertEqual(app.name(), 'python_messenger')

    def test_available_requirements(self):
        pass

    def test_make_config(self):
        pass

    def test_set_def_env(self):
        pass

    def test_set_prod_env(self):
        pass

    def test_set_test_env(self):
        pass

    def test_logging(self):
        pass


if __name__ == '__main__':
    unittest.main()
