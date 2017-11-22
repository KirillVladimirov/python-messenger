class User:
    """
    A simple user class
    """

    def __init__(self, name, password):
        self._name = name
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password
