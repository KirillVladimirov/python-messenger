# coding=utf-8

import datetime
import socket
import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

from geekmessenger.app import app
from geekmessenger.app.common.jim import JIM
from geekmessenger.app.client.templates.client_window import Ui_client_window


class Client(object):
    """
    Client application class
    """

    def __init__(self):
        self.host = app.config['CLIENT']['HOST']
        self.port = app.config['CLIENT']['PORT']
        self.encode = app.config['CLIENT']['ENCODE']
        self.gui_app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.init_ui()

    def run(self):
        """
        Run main gui application loop
        """
        self.window.show()
        sys.exit(self.gui_app.exec_())

    def init_ui(self):
        """
        Инициализация UI.

        Компоненты UI:
            dialogs_list - список контактов
            send_button - кнопка отправки сообщения выбранному контакту
            messanges_list - переписка, список сообщений переписки с выбранным контактом
            messanger_edit - строка редактирования сообщения
        """
        ui = Ui_client_window()
        ui.setupUi(self.window)
        # Connect up the buttons.
        ui.send_button.clicked.connect(self.send_button_clicked)
        # self.ui.cancelButton.clicked.connect(self.reject)

    def send_button_clicked(self):
        print("Кнопка нажата. Функция on_clicked")

    def send(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
        except socket.error as err:
            print("Connection error: {}".format(err))
            sys.exit(2)
        print("create socket...")
        msg = self.__auth()
        sock.sendall(msg)
        print("send message...")

        try:
            msg = sock.recv(1024)
            print(JIM.unpack(msg))
        except socket.timeout:
            print("Close connection by timeout.")

        if not msg:
            print("No response")

        sock.close()
        print("client close...")

    def __auth(self):
        user = self.__get_user()
        time = datetime.datetime.now()
        msg = {
            "action": "authenticate",
            "time": time.isoformat(),
            "user": {
                "account_name": user.name,
                "password": user.password,
            },
        }
        return JIM.pack(msg)
