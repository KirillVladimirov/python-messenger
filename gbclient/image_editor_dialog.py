#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL.ImageQt import ImageQt

from gbcore import app
from gbcore.image import Image


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
