# coding=utf-8

# Тестирование Пользовательского интерфейса клиента
import pytest
import sys
from PyQt5.QtWidgets  import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from geekmessenger.app.client.templates.client_window import Ui_client_window

class TestGui(object):

    def setup_method(self, method):
        """Create the GUI"""
        self.app = QApplication(sys.argv)
        self.form = Ui_client_window()
        self.window = QMainWindow()
        self.form.setupUi(self.window)

    def teardown_method(self, method):
        pass

    def test_gui_default_run(self):
        """Test the GUI in its default state"""
        assert self.form.send_button.text() == "Отправить"
        assert self.window.windowTitle() == "Messanger Client"
        QTest.mouseClick(self.form.send_button, Qt.LeftButton)

        # self.assertEqual(self.form.ui.tequilaScrollBar.value(), 8)
        # self.assertEqual(self.form.ui.tripleSecSpinBox.value(), 4)
        # self.assertEqual(self.form.ui.limeJuiceLineEdit.text(), "12.0")
        # self.assertEqual(self.form.ui.iceHorizontalSlider.value(), 12)
        # self.assertEqual(self.form.ui.speedButtonGroup.checkedButton().text(), "&Karate Chop")
        #
        # # Class is in the default state even without pressing OK
        # self.assertEqual(self.form.jiggers, 36.0)
        # self.assertEqual(self.form.speedName, "&Karate Chop")
        #
        # # Push OK with the left mouse button
        # okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        # QTest.mouseClick(okWidget, Qt.LeftButton)
        # self.assertEqual(self.form.jiggers, 36.0)
        # self.assertEqual(self.form.speedName, "&Karate Chop")

    # def test_dialogs_scrollbar(self):
    #     """Test the tequila scroll bar"""
    #     self.setFormToZero()
    #
    #     # Test the maximum. This one goes to 11.
    #     self.form.ui.tequilaScrollBar.setValue(12)
    #     self.assertEqual(self.form.ui.tequilaScrollBar.value(), 11)
    #
    #     # Test the minimum of zero.
    #     self.form.ui.tequilaScrollBar.setValue(-1)
    #     self.assertEqual(self.form.ui.tequilaScrollBar.value(), 0)
    #
    #     self.form.ui.tequilaScrollBar.setValue(5)
    #
    #     # Push OK with the left mouse button
    #     okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
    #     QTest.mouseClick(okWidget, Qt.LeftButton)
    #     self.assertEqual(self.form.jiggers, 5)
    #
    # def test_mouse_click(self):
    #     okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
    #     QTest.mouseClick(okWidget, Qt.LeftButton)
    #     self.assertEqual(self.form.jiggers, 5)
    #
    # def test_edit_lineedit(self):
    #     """
    #     Test the lime juice line edit.
    #     Testing the minimum and maximum is left as an exercise for the reader.
    #     """
    #     self.setFormToZero()
    #     # Clear and then type "3.5" into the lineEdit widget
    #     self.form.ui.limeJuiceLineEdit.clear()
    #     QTest.keyClicks(self.form.ui.limeJuiceLineEdit, "3.5")
    #
    #     # Push OK with the left mouse button
    #     okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
    #     QTest.mouseClick(okWidget, Qt.LeftButton)
    #     self.assertEqual(self.form.jiggers, 3.5)

    def test_show_current_user(self):
        pass

    def test_show_dialogs_list_for_user(self):
        pass

    def test_show_messages_for_select_dialog(self):
        pass

    def test_create_new_dialog(self):
        pass

    def test_send_message(self):
        pass

    def test_receive_message(self):
        pass
