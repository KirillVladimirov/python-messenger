#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import socket
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

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
        self.path_img_ab = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ab.gif')
        self.path_img_ac = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ac.gif')
        self.path_img_ai = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ai.gif')
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
        # Set icons for font buttons
        ui.tb_b.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'b.jpg')))
        ui.tb_i.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'i.jpg')))
        ui.tb_u.setIcon(QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'u.jpg')))
        # Set icons for smile buttons
        ui.tb_smile_1.setIcon(QIcon(self.path_img_ab))
        ui.tb_smile_2.setIcon(QIcon(self.path_img_ac))
        ui.tb_smile_3.setIcon(QIcon(self.path_img_ai))
        # Connect up the buttons.
        ui.send_button.clicked.connect(self.action_send_button_clicked)
        # Connect up the font buttons.
        ui.tb_b.clicked.connect(self.action_bold)
        ui.tb_i.clicked.connect(self.action_italic)
        ui.tb_u.clicked.connect(self.action_underlined)
        # Connect up smile buttons
        ui.tb_smile_1.clicked.connect(self.action_smile)
        ui.tb_smile_2.clicked.connect(self.action_melancholy)
        ui.tb_smile_3.clicked.connect(self.action_surprise)
        # Image edit dialog
        ui.tb_smile_4.clicked.connect(self.action_image_edit)
        return ui

    def create_users(self):
        users = ['cnn', 'egor', 'bobr']
        for user in users:
            icon = QIcon(os.path.join(app.config.root_path, '..', 'upload', user + '.jpg'))
            item = QListWidgetItem(user)
            item.setIcon(icon)
            self.ui.dialogs_list.addItem(item)

    def action_send_button_clicked(self):
        text = self.ui.messanger_edit.toHtml()
        item = QListWidgetItem()
        self.ui.messanges_list.addItem(item)
        self.ui.messanger_edit.clear()

    def action_bold(self):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<b>" + selected_text + "</b>")

    def action_italic(self):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<i>" + selected_text + "</i>")

    def action_underlined(self):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<u>" + selected_text + "</u>")

    def action_smile(self):
        self.ui.messanger_edit.insertHtml('<img src="%s" />' % self.path_img_ab)

    def action_melancholy(self):
        self.ui.messanger_edit.insertHtml('<img src="%s" />' % self.path_img_ac)

    def action_surprise(self):
        self.ui.messanger_edit.insertHtml('<img src="%s" />' % self.path_img_ai)

    def action_image_edit(self):
        # image = Image.open("image.jpg")
        # draw = ImageDraw.Draw(image)
        # width = image.size[0]
        # height = image.size[1]
        # pix = image.load()
        #
        # for i in range(width):
        #     for j in range(height):
        #         a = pix[i, j][0]
        #         b = pix[i, j][1]
        #         c = pix[i, j][2]
        #         draw.point((i, j), (255 - a, 255 - b, 255 - c))
        #
        # img_tmp = ImageQt(image.convert('RGBA'))

        # pixmap = QPixmap.fromImage(img_tmp)

        # lbl.setPixmap(pixmap)

        dialog = QDialog()
        lbl = QLabel()
        bt_return = QPushButton("ok")
        hbox = QHBoxLayout()
        hbox.addWidget(lbl)
        hbox.addWidget(bt_return)
        dialog.setLayout(hbox)
        dialog.setWindowTitle('Image Editor')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

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
