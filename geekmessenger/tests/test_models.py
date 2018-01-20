# coding=utf-8

from unittest import TestCase, main
from app.common import User
from app.common import Dialog
from app.common import Message


class TestUser(TestCase):

    def test_create_user(self):
        user = User("User", "Password")
        assert user.name == "User"
        assert user.password == "Password"

    def test_remove_user(self):
        pass

    def test_user_change_password(self):
        pass

    def test_get_user_information(self):
        pass

    def test_get_user_by_name(self):
        pass

    def test_get_user_by_login(self):
        pass

    def test_get_user_by_email(self):
        pass

    def test_get_users_list(self):
        pass


class TestDialog(TestCase):

    def test_create_dialog(self):
        pass

    def test_remove_dialog(self):
        pass

    def test_get_user_dialogs(self):
        pass

    def test_all_users_from_dialog(self):
        pass


class TestMessage(TestCase):

    def test_create_message(self):
        pass

    def test_remove_message(self):
        pass

    def test_get_all_messages_from_dialog(self):
        pass

    def test_get_all_messages_from_dialog_from_user(self):
        pass

    def test_get_all_messages_by_user_and_date(self):
        pass


if __name__ == '__main__':
    main()
