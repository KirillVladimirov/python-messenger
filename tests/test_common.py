from corelib.user import User


def test_create_user():
    user = User("User", "Password")
    assert user.name == "User"
    assert user.password == "Password"