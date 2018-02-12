#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Тестирование протокола jim для обмена данными слиент/сервер
import pytest
from geekmessenger.app.common import jim
import geekmessenger.app.client
import geekmessenger.app.server


class TestJIMFormat(object):

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_create_jim_from_message(self):
        pass

    def test_create_message_from_jim(self):
        pass

    def test_create_auth_jim(self):
        pass

    def test_create_error_jim(self):
        pass


class TestServerApi(object):

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_auth_user(self):
        pass

    def test_wrong_auth_user(self):
        pass

    def test_user_search_other_users(self):
        pass

    def test_user_create_dialog(self):
        pass

    def test_user_send_message(self):
        pass

    def test_user_delete_dialog(self):
        pass

    def test_user_send_wrong_format_message(self):
        pass

    def test_user_invite_other_to_dialog(self):
        pass

    def test_user_get_agree_from_other(self):
        pass

    def test_user_get_rejection_from_other(self):
        pass
