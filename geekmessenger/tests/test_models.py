# coding=utf-8

import pytest
from geekmessenger.app import db
from geekmessenger.app.common.models import User
from geekmessenger.app.common.models import Dialog
from geekmessenger.app.common.models import Message
from sqlalchemy.orm import Session


class TestUser(object):

    def setup_method(self, method):
        sess = db.session
        user1 = User("User1", "user1@email.com", "Password1")
        user2 = User("User2", "user2@email.com", "Password2")
        user3 = User("User3", "user3@email.com", "Password3")
        sess.add(user1)
        sess.add(user2)
        sess.add(user3)
        sess.commit()

    def teardown_method(self, method):
        pass

    def test_create_user(self):
        user = User("User", "user@email.com", "Password")
        assert user.name == "User"
        assert user.email == "user@email.com"

    def test_correct_password(self):
        user = User("User", "user@email.com", "Password")
        assert user.correct_password("Password")

    def test_get_user_by_name(self):
        sess = Session()
        user1 = sess.query(User).filter_by(id=1).first()
        assert user1.name == "User1"

    def test_get_user_by_email(self):
        pass

    def test_remove_user(self):
        sess = Session()
        sess.delete(user1)
        sess.commit()
        pass

    def test_user_change_password(self):
        pass

    def test_get_user_information(self):
        pass



    def test_get_users_list(self):
        pass


class TestDialog(object):

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_create_dialog(self):
        pass

    def test_remove_dialog(self):
        pass

    def test_get_user_dialogs(self):
        pass

    def test_all_users_from_dialog(self):
        pass


class TestMessage(object):

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

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

