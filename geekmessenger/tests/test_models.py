# -*- coding:utf-8 -*-v

import pytest

from geekmessenger.app import db
from geekmessenger.app.common.models import User
from geekmessenger.app.common.models import Dialog
from geekmessenger.app.common.models import Message
from geekmessenger.app.common.models import AssociationUsersDialogs


class TestUser(object):

    def setup_method(self, method):
        db.drop_tables()
        db.create_tables()

        sess = db.session
        user1 = User("User1", "user1@email.com", "Password1")
        user2 = User("User2", "user2@email.com", "Password2")
        user3 = User("User3", "user3@email.com", "Password3")
        sess.add(user1)
        sess.add(user2)
        sess.add(user3)
        sess.commit()

    def teardown_method(self, method):
        db.drop_tables()

    def test_create_user(self):
        sess = db.session
        user = User("User", "user@email.com", "Password")
        sess.add(user)
        sess.commit()
        assert user.name == "User"
        assert user.email == "user@email.com"

    def test_correct_password(self):
        sess = db.session
        user = User("User", "user@email.com", "Password")
        sess.add(user)
        sess.commit()
        assert user.correct_password("Password")

    def test_get_user_by_name(self):
        sess = db.session
        user1 = sess.query(User).filter_by(id=1).first()
        assert user1.name == "User1"

    def test_get_user_by_email(self):
        sess = db.session
        user2 = sess.query(User).filter_by(email="user2@email.com").first()
        assert user2.name == "User2"

    def test_remove_user(self):
        sess = db.session
        user3 = sess.query(User).filter_by(id=3).first()
        assert user3.name == "User3"
        sess.delete(user3)
        sess.commit()
        user3 = sess.query(User).filter_by(id=3).first()
        assert user3 is None

    def test_user_change_password(self):
        sess = db.session
        user2 = sess.query(User).filter_by(email="user2@email.com").first()
        assert user2.correct_password("Password2")
        user2.password = "NewPassword2"
        sess.commit()
        assert user2.correct_password("NewPassword2")

    def test_validate_email(self):
        sess = db.session
        user1 = sess.query(User).filter_by(id=1).first()
        with pytest.raises(AssertionError):
            user1.email = "Wrong email"

    def test_get_all_users_list(self):
        sess = db.session
        users = sess.query(User).all()
        assert len(users) == 3


class TestDialog(object):

    def setup_method(self, method):
        db.drop_tables()
        db.create_tables()

        sess = db.session
        sess.commit()

    def teardown_method(self, method):
        db.drop_tables()

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
        """
            Перед вводом в эксплуатацию нужно создать таблици в БД
            """
        db.drop_tables()
        db.create_tables()

        sess = db.session

        user1 = User("User1", "user1@email.com", "Password1")
        user2 = User("User2", "user2@email.com", "Password2")
        user3 = User("User3", "user3@email.com", "Password3")
        sess.add(user1)
        sess.add(user2)
        sess.add(user3)
        sess.commit()

        dialog1 = Dialog()
        dialog2 = Dialog()
        sess.add(dialog1)
        sess.add(dialog2)
        sess.commit()

        """
        Создаем диалог между пользователями user1 и user2
        """
        user1.dialogs.append(dialog1)
        user2.dialogs.append(dialog1)

        """
        Создаем диалог между пользователями user1 и user3
        """
        user1.dialogs.append(dialog2)
        user3.dialogs.append(dialog2)

        sess.commit()

        message1 = Message("Hello world 1", dialog1, user1)
        message2 = Message("Hello world 2", dialog1, user2)
        message3 = Message("Hello world 3", dialog2, user1)
        message4 = Message("Hello world 3", dialog2, user3)
        sess.add(message1)
        sess.add(message2)
        sess.add(message3)
        sess.add(message4)
        sess.commit()

    def teardown_method(self, method):
        db.drop_tables()

    def test_create_message(self):
        sess = db.session
        user1 = sess.query(User).filter_by(id=1).first()
        user2 = sess.query(User).filter_by(id=2).first()
        user3 = sess.query(User).filter_by(id=3).first()
        dialog3 = Dialog()
        user1.dialogs.append(dialog3)
        user2.dialogs.append(dialog3)
        user3.dialogs.append(dialog3)
        message1 = Message("Hello new world", dialog3, user1)
        sess.add(dialog3)
        sess.add(message1)
        sess.commit()
        assert message1.message == "Hello new world"

    def test_remove_message(self):
        sess = db.session
        message1 = sess.query(Message).filter_by(id=1).first()
        assert message1.message == "Hello world 1"
        sess.delete(message1)
        sess.commit()
        message1 = sess.query(Message).filter_by(id=1).first()
        assert message1 is None

    def test_get_all_messages_from_dialog(self):
        sess = db.session
        messages = sess.query(Message).filter_by(dialog_id=1).all()
        assert len(messages) == 2

    def test_get_all_messages_from_dialog_from_user(self):
        sess = db.session
        messages = sess.query(Message).filter_by(dialog_id=1, user_id=1).all()
        assert len(messages) == 1

    def test_get_all_messages_by_user_and_date(self):
        pass
