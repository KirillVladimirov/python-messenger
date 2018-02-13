#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import socket
import sys
import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

from geekmessenger.app import app
from geekmessenger.app import db
from geekmessenger.app.common.models import Message
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
        self.ui = self.init_ui()
        self.font = QFont()

    def run(self):
        """
        Run main gui application loop
        """
        self.window.show()
        self.create_users()
        sys.exit(self.gui_app.exec_())

    def init_ui(self):
        """
        Инициализация UI.

        Компоненты UI:
            dialogs_list - список контактов
            messanges_list - переписка, список сообщений переписки с выбранным контактом
            messanger_edit - строка редактирования сообщения

            send_button - кнопка отправки сообщения выбранному контакту
            tb_i - кнопка, курсив
            tb_b - кнопка, жирный
            tb_u - кнопка, подчеркнутый
            tb_smile_1 - кнопка, смаил 1
            tb_smile_2 - кнопка, смаил 2
            tb_smile_3 - кнопка, смаил 3
            tb_smile_4 - кнопка, смаил 4
        """
        ui = Ui_client_window()
        ui.setupUi(self.window)
        # Set icons
        ui.tb_b.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'b.jpg')))
        ui.tb_i.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'i.jpg')))
        ui.tb_u.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'u.jpg')))
        # Connect up the buttons.
        ui.send_button.clicked.connect(self.action_send_button_clicked)
        ui.tb_b.clicked.connect(self.action_bold)
        ui.tb_i.clicked.connect(self.action_italic)
        ui.tb_u.clicked.connect(self.action_underlined)
        # self.ui.cancelButton.clicked.connect(self.reject)
        return ui

    def create_users(self):
        users = ['cnn', 'egor', 'bobr']
        for user in users:
            icon = QIcon(os.path.join(app.config.root_path, '..', 'upload', user + '.jpg'))
            item = QListWidgetItem(user)
            item.setIcon(icon)
            self.ui.dialogs_list.addItem(item)

    def action_send_button_clicked(self):
        text = self.ui.messanger_edit.toPlainText()
        item = QListWidgetItem(text)
        self.ui.messanges_list.addItem(item)
        self.ui.messanger_edit.setText('')

    def action_bold(self):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<b>" + selected_text + "</b>")

    def action_italic(self):
        self.myFont.setItalic(True)
        self.textEdit.setFont(self.myFont)

    def action_underlined(self):
        self.myFont.setUnderline(True)
        self.textEdit.setFont(self.myFont)

    def send_message(self, request):
        sess = db.session
        message = Message(request.message, request.dialog, request.user)
        sess.add(message)
        sess.commit()
        return self.send(message)

    def send(self, message):
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
