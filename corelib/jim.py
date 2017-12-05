import json


class JIM:

    @classmethod
    def pack(cls, dict_msg):
        """
        Создание сообщения, пригодного для отправки через TCP
        :param dict_msg: dict
        :return: str
        """
        str_msg = json.dumps(dict_msg)
        return str_msg.encode("utf8")

    @classmethod
    def unpack(cls, bt_str):
        """
        Распаквка полученного сообщения
        :param bt_str: str
        :return: dict
        """
        str_decoded = bt_str.decode('utf-8')
        return json.loads(str_decoded)


class JimMessage(JIM):
    pass


class JimResponse(JIM):

    @classmethod
    def status_200(cls):
        msg = {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        }
        return cls.pack(msg)

    @classmethod
    def status_402(cls):
        msg = {
            "response": 402,
            "error": "This could be wrong password or no account with that name"
        }
        return cls.pack(msg)

    @classmethod
    def status_409(cls):
        msg = {
            "response": 409,
            "alert": "Someone is already connected with the given user name"
        }
        return cls.pack(msg)
