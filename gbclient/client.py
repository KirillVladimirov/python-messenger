#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import asyncio

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

from gbcore.message import Message
from gbclient.image_editor_dialog import ImageEditorDialog
from gbclient.templates.client_window import Ui_client_window


class Client(object):
    """
    Client application class
    """

    def __init__(self, base_app):
        self.base_app = base_app
        self.host = base_app.config['CLIENT']['HOST']
        self.port = base_app.config['CLIENT']['PORT']
        self.encode = base_app.config['CLIENT']['ENCODE']

        self.path_img_ab = os.path.join(base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ab.gif')
        self.path_img_ac = os.path.join(base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ac.gif')
        self.path_img_ai = os.path.join(base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ai.gif')

        self.gui_app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = self.init_ui()
        self.ie_dialog = ImageEditorDialog(self.base_app)
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
        ui.tb_b.setIcon(QIcon(os.path.join(self.base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'b.jpg')))
        ui.tb_i.setIcon(QIcon(os.path.join(self.base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'i.jpg')))
        ui.tb_u.setIcon(QIcon(os.path.join(self.base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'u.jpg')))
        # Set icons for smile buttons
        ui.tb_smile_1.setIcon(QIcon(self.path_img_ab))
        ui.tb_smile_2.setIcon(QIcon(self.path_img_ac))
        ui.tb_smile_3.setIcon(QIcon(self.path_img_ai))
        # Set icon for image edit dialog
        ui.tb_smile_4.setIcon(
            QIcon(os.path.join(self.base_app.config.root_path, 'app', 'client', 'templates', 'imgs', 'open.png')))
        # Connect up the buttons.
        ui.send_button.clicked.connect(self.action_send_button_clicked)
        # Connect up the font buttons.
        ui.tb_b.clicked.connect(lambda: self._insert_html_tag('b'))
        ui.tb_i.clicked.connect(lambda: self._insert_html_tag('i'))
        ui.tb_u.clicked.connect(lambda: self._insert_html_tag('u'))
        # Connect up smile buttons
        ui.tb_smile_1.clicked.connect(lambda: self._insert_image(self.path_img_ab))
        ui.tb_smile_2.clicked.connect(lambda: self._insert_image(self.path_img_ac))
        ui.tb_smile_3.clicked.connect(lambda: self._insert_image(self.path_img_ai))
        # Image edit dialog
        ui.tb_smile_4.clicked.connect(self.action_image_edit)
        return ui

    def create_users(self):
        users = ['cnn', 'egor', 'bobr']
        for user in users:
            icon = QIcon(os.path.join(self.base_app.config.root_path, '..', 'upload', user + '.jpg'))
            item = QListWidgetItem(user)
            item.setIcon(icon)
            self.ui.dialogs_list.addItem(item)

    def action_send_button_clicked(self):
        text = self.ui.messanger_edit.toPlainText()
        self.send(text)
        item = QListWidgetItem(text)
        self.ui.messanges_list.addItem(item)
        self.ui.messanger_edit.clear()

    def action_image_edit(self):
        self.ie_dialog.exec_()

    def _insert_html_tag(self, tag_name):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<{tag}>{text}</{tag}>".format(tag=tag_name, text=selected_text))

    def _insert_image(self, image_path):
        self.ui.messanger_edit.insertHtml('<img src="{image_path}" />'.format(image_path=image_path))

    def send(self, message):
        # sess = db.session
        # TODO for test
        # user = User("User", "user@email.com", "Password")
        # sess.add(user)
        # sess.commit()
        #
        # message = Message(message, 1)
        # sess.add(message)
        # sess.commit()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message_to_server(message, loop))
        loop.close()

    async def send_message_to_server(self, message, loop):
        reader, writer = await asyncio.open_connection(
            host=app.config['CLIENT']['HOST'],
            port=app.config['CLIENT']['PORT'],
            loop=loop
        )
        message = str(message)
        print('Send: %r' % message)
        writer.write(message.encode())
        data = await reader.read(100)
        print('Received: %r' % data.decode())
        print('Close the socket')
        writer.close()

    # TODO сделать авторизацию на сервере
    def __auth(self):
        pass
