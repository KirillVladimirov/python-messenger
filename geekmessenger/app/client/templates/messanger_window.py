# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'messanger_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_messanger_window_2(object):
    def setupUi(self, messanger_window_2):
        messanger_window_2.setObjectName("messanger_window_2")
        messanger_window_2.resize(648, 600)
        self.messanger_window = QtWidgets.QWidget(messanger_window_2)
        self.messanger_window.setMinimumSize(QtCore.QSize(648, 600))
        self.messanger_window.setObjectName("messanger_window")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.messanger_window)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.messanger_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QtCore.QSize(150, 16777215))
        self.listWidget.setLineWidth(1)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.messanges_list = QtWidgets.QListWidget(self.messanger_window)
        self.messanges_list.setLineWidth(2)
        self.messanges_list.setObjectName("messanges_list")
        self.verticalLayout.addWidget(self.messanges_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.messanger_edit = QtWidgets.QTextEdit(self.messanger_window)
        self.messanger_edit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.messanger_edit.setObjectName("messanger_edit")
        self.horizontalLayout.addWidget(self.messanger_edit)
        self.send_button = QtWidgets.QPushButton(self.messanger_window)
        self.send_button.setMinimumSize(QtCore.QSize(50, 0))
        self.send_button.setMaximumSize(QtCore.QSize(16777215, 50))
        self.send_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../imgs/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_button.setIcon(icon)
        self.send_button.setObjectName("send_button")
        self.horizontalLayout.addWidget(self.send_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.messanges_list.raise_()
        self.listWidget.raise_()
        self.listWidget.raise_()
        messanger_window_2.setCentralWidget(self.messanger_window)
        self.actionsend = QtWidgets.QAction(messanger_window_2)
        self.actionsend.setIcon(icon)
        self.actionsend.setObjectName("actionsend")

        self.retranslateUi(messanger_window_2)
        QtCore.QMetaObject.connectSlotsByName(messanger_window_2)

    def retranslateUi(self, messanger_window_2):
        _translate = QtCore.QCoreApplication.translate
        messanger_window_2.setWindowTitle(_translate("messanger_window_2", "Messanger Client"))
        self.actionsend.setText(_translate("messanger_window_2", "send"))

