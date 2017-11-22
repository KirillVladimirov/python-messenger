import pytest
import manager


class TestManagerDB(object):

    def setup_method(self, method):
        self._manager = manager.ManagerDB()

    def teardown_method(self, method):
        pass

    def test_get_index(self):
        pass

    def test_get_all_items(self):
        pass

    def test_get_connection(self):
        pass


class TestManagerGUI(object):

    def setup_method(self, method):
        self._manager = manager.ManagerGUI()

    def teardown_method(self, method):
        pass

    def test_render(self):
        pass
