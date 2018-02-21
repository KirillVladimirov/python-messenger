#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import random
import asyncio

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL.ImageQt import ImageQt

from geekmessenger.app import app
from geekmessenger.app.common.message import Message
from geekmessenger.app.common.user import User
from geekmessenger.app.common.image import Image
from geekmessenger.app.common.jim import JIM
from geekmessenger.app.client.templates.client_window import Ui_client_window

import datetime

from geekmessenger.app import db


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
        self.ie_dialog = ImageEditorDialog()
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
        # Set icon for image edit dialog
        ui.tb_smile_4.setIcon(
            QIcon(os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'open.png')))
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
            icon = QIcon(os.path.join(app.config.root_path, '..', 'upload', user + '.jpg'))
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
        sess = db.session
        # TODO for test
        # user = User("User", "user@email.com", "Password")
        # sess.add(user)
        # sess.commit()
        #
        message = Message(message, 1)
        sess.add(message)
        sess.commit()

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


class ImageEditorDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.path_img_ab = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ab.gif')
        self.path_img_ac = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ac.gif')
        self.path_img_ai = os.path.join(app.config.root_path, 'app', 'client', 'templates', 'imgs', 'ai.gif')
        self.canvas = QLabel(self)
        self.canvas.setObjectName('canvas')
        self.init_ie_dialog()

    def init_ie_dialog(self):
        negative = QToolButton(self)
        negative.setIcon(QIcon(self.path_img_ab))
        negative.clicked.connect(self.action_negative)
        noise = QToolButton(self)
        noise.setIcon(QIcon(self.path_img_ac))
        noise.clicked.connect(self.action_noise)
        gray = QToolButton(self)
        gray.setIcon(QIcon(self.path_img_ai))
        gray.clicked.connect(self.action_gray)

        bt_return = QPushButton("ok")
        bt_return.clicked.connect(self.accept)
        tool_box = QHBoxLayout()
        tool_box.addWidget(negative)
        tool_box.addWidget(noise)
        tool_box.addWidget(gray)
        vbox = QVBoxLayout()
        vbox.addLayout(tool_box)
        vbox.addWidget(self.canvas)
        vbox.addWidget(bt_return)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        tool_box.addItem(spacer_item)
        self.setLayout(vbox)
        self.setWindowTitle('Image Editor')
        self.setWindowModality(Qt.ApplicationModal)

    def safe_image(self, image):
        sess = db.session
        message = Image()
        sess.add(message)
        sess.commit()
        return self.send(message)

    def open_image(self, image_name):
        try:
            return PILImage.open(os.path.join(app.config.root_path, '..', 'upload', image_name))
        except FileNotFoundError:
            print("Wrong file or file path for: {}".format(image_name))
            self.reject()

    def action_negative(self):
        image = self.open_image('bobr.jpg')
        draw = PILImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255 - a, 255 - b, 255 - c))

        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.canvas.setPixmap(pixmap)
        self.move_to_center()

    def action_noise(self):
        image = self.open_image('bobr.jpg')
        draw = PILImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        max_noise = 100
        min_noise = -100
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + random.randint(min_noise, max_noise)
                b = pix[i, j][1] + random.randint(min_noise, max_noise)
                c = pix[i, j][2] + random.randint(min_noise, max_noise)

                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255

                if a < 0:
                    a = 0
                if b < 0:
                    b = 0
                if c < 0:
                    c = 0

                draw.point((i, j), (a, b, c))

        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.canvas.setPixmap(pixmap)
        self.move_to_center()

    def action_gray(self):
        image = self.open_image('bobr.jpg')
        draw = PILImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                draw.point((i, j), (S, S, S))

        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.canvas.setPixmap(pixmap)
        self.move_to_center()

    def move_to_center(self):
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())


class ImageEditor:

    def __init__(self, image):
        self.image = image
        self.image_draw = PILImageDraw.Draw(image)

    def filter(self, filter_name):
        if self.image_draw:
            method = getattr(self.image_draw, filter_name)
            return self.method()

        return None

    def filter_gray(self):
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                self.image_draw.point((i, j), (S, S, S))

        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.canvas.setPixmap(pixmap)
        self.move_to_center()

    def filter_noise(self):
        pass

    def filter_negative(self):
        pass

    def cut_image(self):
        pass

    def scaling(self):
        pass
