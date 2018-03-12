#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from quamash import QEventLoop
from gbcore.config import make_config
from gbcore.logger import make_logger
from gbclient.image_editor_dialog import ImageEditorDialog
from gbclient.templates.client_window import Ui_client_window
import aiohttp
import asyncio
from gbclient.models import Db


class MainWindow(QMainWindow):

    def __init__(self, client, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.client = client
        self.ui = Ui_client_window()
        self.setupUi()

    def setupUi(self):
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
        self.ui.setupUi(self)
        # Set icons for font buttons
        self.ui.tb_b.setIcon(QIcon(os.path.join(
            self.client.config.root_path, 'app', 'client', 'templates', 'imgs', 'b.jpg')))
        self.ui.tb_i.setIcon(QIcon(os.path.join(
            self.client.config.root_path, 'app', 'client', 'templates', 'imgs', 'i.jpg')))
        self.ui.tb_u.setIcon(QIcon(os.path.join(
            self.client.config.root_path, 'app', 'client', 'templates', 'imgs', 'u.jpg')))
        # Set icons for smile buttons
        self.ui.tb_smile_1.setIcon(QIcon(self.client.path_img_ab))
        self.ui.tb_smile_2.setIcon(QIcon(self.client.path_img_ac))
        self.ui.tb_smile_3.setIcon(QIcon(self.client.path_img_ai))
        # Set icon for image edit dialog
        self.ui.tb_smile_4.setIcon(
            QIcon(os.path.join(
                self.client.config.root_path, 'app', 'client', 'templates', 'imgs', 'open.png')))
        # Connect up the buttons.
        self.ui.send_button.clicked.connect(self.client.action_send_button_clicked)
        # Connect up the font buttons.
        self.ui.tb_b.clicked.connect(lambda: self._insert_html_tag('b'))
        self.ui.tb_i.clicked.connect(lambda: self._insert_html_tag('i'))
        self.ui.tb_u.clicked.connect(lambda: self._insert_html_tag('u'))
        # Connect up smile buttons
        self.ui.tb_smile_1.clicked.connect(lambda: self._insert_image(self.path_img_ab))
        self.ui.tb_smile_2.clicked.connect(lambda: self._insert_image(self.path_img_ac))
        self.ui.tb_smile_3.clicked.connect(lambda: self._insert_image(self.path_img_ai))
        # Image edit dialog
        self.ui.tb_smile_4.clicked.connect(self.client.action_image_edit)

    def closeEvent(self, event):
        asyncio.ensure_future(self.client.close_ws(), loop=self.client.loop)


class Client(object):

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        self.config = make_config(
            os.path.join('config', 'env.json'))
        self.logger = make_logger(self.config)
        self.port = self.config['CLIENT']['PORT']
        self.host = self.config['CLIENT']['HOST']
        self.encode = self.config['CLIENT']['ENCODE']
        self.path_img_ab = os.path.join(self.config.root_path, 'app', 'client', 'templates', 'imgs', 'ab.gif')
        self.path_img_ac = os.path.join(self.config.root_path, 'app', 'client', 'templates', 'imgs', 'ac.gif')
        self.path_img_ai = os.path.join(self.config.root_path, 'app', 'client', 'templates', 'imgs', 'ai.gif')
        self.window = MainWindow(self)
        self.ui = self.window.ui
        self.ie_dialog = ImageEditorDialog(self.config)
        self.font = QFont()
        asyncio.ensure_future(self.check_connection(), loop=self.loop)
        self.ws = None
        asyncio.ensure_future(self.listen_server(), loop=self.loop)
        # TODO тестовые данные пользователей
        self.display_users()
        self.db = Db(self.loop, self.config)
        asyncio.ensure_future(self.db.make_tables(), loop=self.loop)
        asyncio.ensure_future(self.create_users(), loop=self.loop)
        asyncio.ensure_future(self.get_user(), loop=self.loop)
        self.user = None

    def run(self):
        self.window.show()
        self.loop.run_forever()

    def display_users(self):
        users = ['client_user_1', 'client_user_2']
        for user in users:
            icon = QIcon(os.path.join(self.config.root_path, '..', 'upload', user + '.jpg'))
            item = QListWidgetItem(user)
            item.setIcon(icon)
            self.ui.dialogs_list.addItem(item)

    async def create_users(self):
        await self.db.create_user('client_user_1', 'client_user_1@mail.ru', 'client_user_1')
        await self.db.create_user('client_user_2', 'client_user_2@mail.ru', 'client_user_2')

    async def get_user(self):
        self.user = await self.db.get_user('client_user_1')
        print(self.user)

    def action_send_button_clicked(self):
        message_text = self.ui.messanger_edit.toPlainText()
        asyncio.ensure_future(self.send_message(message_text), loop=self.loop)
        self.ui.messanger_edit.clear()

    async def send_message(self, message):
        await self.ws.send_str(message)

    async def listen_server(self):
        session = aiohttp.ClientSession()
        self.ws = await session.ws_connect('http://{host}:{port}/send'.format(host=self.host, port=self.port))
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                self.display_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    async def close_ws(self):
        await self.ws.close()

    async def check_connection(self):
        async with aiohttp.ClientSession() as session:
            url = 'http://{host}:{port}/'.format(host=self.host, port=self.port)
            async with session.get(url) as resp:
                if resp.status == 200:
                    self.logger.info("{} | {}".format(__name__, 'Server online ...'))
                else:
                    self.logger.info("{} | {}".format(__name__, 'Connection error ...'))

    async def signup(self):
        pass

    async def signin(self):
        pass

    async def signout(self):
        pass

    def display_message(self, message):
        self.ui.messanges_list.addItem(message)
        asyncio.ensure_future(self.db.create_message(self.user, message), loop=self.loop)
        print('Received from server: {}'.format(message))

    def action_image_edit(self):
        self.ie_dialog.exec_()

    def _insert_html_tag(self, tag_name):
        text_cursor = self.ui.messanger_edit.textCursor()
        selected_text = text_cursor.selectedText()
        self.ui.messanger_edit.insertHtml("<{tag}>{text}</{tag}>".format(tag=tag_name, text=selected_text))

    def _insert_image(self, image_path):
        self.ui.messanger_edit.insertHtml('<img src="{image_path}" />'.format(image_path=image_path))
