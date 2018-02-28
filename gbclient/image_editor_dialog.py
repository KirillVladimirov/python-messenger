#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

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
from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL.ImageQt import ImageQt


class ImageEditorDialog(QDialog):

    def __init__(self, gui_app, base_app):
        QDialog.__init__(self, gui_app)
        self.base_app = base_app
        self.image = None
        # self.ui = self.init_ie_dialog()

    def init_ie_dialog(self):
        ui = Ui_dialog(self)
        path_img_ab = os.path.join(self.base_app.config.root_path, 'templates', 'imgs', 'ab.gif')
        path_img_ac = os.path.join(self.base_app.config.root_path, 'templates', 'imgs', 'ac.gif')
        path_img_ai = os.path.join(self.base_app.config.root_path, 'templates', 'imgs', 'ai.gif')
        self.canvas = QLabel(self)
        self.canvas.setObjectName('canvas')

        negative = QToolButton(self)
        negative.setIcon(QIcon(path_img_ab))
        negative.clicked.connect(self.action_negative)
        noise = QToolButton(self)
        noise.setIcon(QIcon(path_img_ac))
        noise.clicked.connect(self.action_noise)
        gray = QToolButton(self)
        gray.setIcon(QIcon(path_img_ai))
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
        return ui

    def safe_image(self, image):
        # sess = db.session
        # message = Image()
        # sess.add(message)
        # sess.commit()
        # return self.send(message)
        pass

    def open_image(self, image_name):
        try:
            return PILImage.open(os.path.join(self.base_app.config.root_path, '..', 'upload', image_name))
        except FileNotFoundError:
            print("Wrong file or file path for: {}".format(image_name))
            self.reject()

    def filter_image(self, fltr):
        pixmap = QPixmap.fromImage(fltr(self))
        self.canvas.setPixmap(pixmap)
        self.move_to_center()

    def move_to_center(self):
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())


class UiDialog(object):

    def setup_ui(self, client_window):
        client_window.setObjectName("client_window")
        client_window.resize(648, 600)
        self.messanger_window = QtWidgets.QWidget(client_window)
        self.messanger_window.setMinimumSize(QtCore.QSize(648, 600))

        self.retranslate_ui(client_window)
        QtCore.QMetaObject.connectSlotsByName(client_window)

    def retranslate_ui(self, client_window):
        _translate = QtCore.QCoreApplication.translate
        client_window.setWindowTitle(_translate("client_window", "Messanger Client"))
        self.tb_b.setText(_translate("client_window", "..."))
        self.tb_i.setText(_translate("client_window", "..."))
        self.tb_u.setText(_translate("client_window", "..."))
        self.tb_smile_1.setText(_translate("client_window", "..."))
        self.tb_smile_2.setText(_translate("client_window", "..."))
        self.tb_smile_3.setText(_translate("client_window", "..."))
        self.tb_smile_4.setText(_translate("client_window", "..."))
        self.send_button.setText(_translate("client_window", "Отправить"))
        self.actionsend.setText(_translate("client_window", "send"))
