#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

"""
This script manipulates the GUI of the application. Using pyqt5 and creates all kinds application required.
"""

from PyQt5.QtCore import QThread, QCoreApplication, Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, \
    QPushButton, QLabel, QDesktopWidget, QMessageBox, QLineEdit, QFrame, QComboBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QMouseEvent
from constants import Importance
import time
import sys


"""
The below lines are the basic inheritance of the Needed part of the PyQt5. 
"""


class Window(QWidget):
    """
    This class is the parent of windows of all kinds.
    """
    def __init__(self):
        super(Window, self).__init__()
        # Here are some basic settings of the screen. Alter it later on your purpose with dot commands for each child.
        # Size
        self.resize(1080, 720)
        # Centralize at the user's screen
        self.setWindowIcon(QIcon("./images/hunter_logo.png"))
        self.center()
        self.setStyleSheet("Window{background-color: #1f2623;}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_size(self, width, height):
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    def hide_window(self):
        """
        Minimize the window.
        :return:
        """
        self.setWindowState(Qt.WindowMinimized)


class Labels(QLabel):
    """
    The label that used to put on a place with content given.
    """
    def __init__(self, content="Blank"):
        super(Labels, self).__init__()
        self.content = str(content)
        self.setText(self.content)
        self.setStyleSheet("Labels{color: white;}")

    def reset_text(self, text, color="ffffff"):
        self.content = str(text)
        self.setText(self.content)
        self.setStyleSheet(f"color: #{color};")  # Coupling problem here. Set color should be in another method.
        self.repaint()

    def __str__(self):
        return self.content


class Buttons(QPushButton):
    """
    There are many buttons in this programs. All of them are child of this class.
    """
    def __init__(self, content="Button", click_event=None):
        super(Buttons, self).__init__(content)
        self.content = content  # Please remember that this will not be update if the text on the button is changed.
        self.connect_event(click_event)

    def connect_event(self, click_event=None):
        if click_event is None:
            self.clicked.connect(self.click_event)
        else:
            self.clicked.connect(click_event)

    def click_event(self):
        """
        Rewrite this function to bind any event to this button.
        When rewriting, simply build the attempted commands and it will run as needed.
        """
        print(f"{self} is clicked! ")

    def set_button_name(self, new_name):
        self.content = new_name

    def __str__(self):
        return f"Button with {self.content}"

    def set_size(self, width, height):
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)


class ImageButtons(QLabel):
    clicked = pyqtSignal()

    def __init__(self, content="Buttons", click_event=None):
        super(ImageButtons, self).__init__()

    def connect_event(self, click_event=None):
        if click_event is None:
            self.clicked.connect(self.click_event)
        else:
            self.clicked.connect(click_event)

    def click_event(self):
        print(f"{self} is clicked! ")

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.clickd.emit()


class InputLine(QLineEdit):
    """
    Yet has no difference with QLineEdit, there will be.
    """
    def __init__(self, initial_content=""):
        super(InputLine, self).__init__()
        self.setText(initial_content)


class Line(QFrame):
    def __init__(self, h=True):
        super(Line, self).__init__()
        if h:
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)
        self.setStyleSheet("QFrame{color: white}")


class ListWindow(QListWidget):
    # This window is a 250 * 500 area.
    def __init__(self, widgets):
        super(ListWindow, self).__init__()
        self.setFixedSize(250, 500)
        for widget in widgets:
            items = QListWidgetItem()
            items.setSizeHint(QSize(200, 50))
            self.addItem(items)
            self.setItemWidget(items, widget)
        self.setStyleSheet("ListWindow{background-color: #2b312c; }")


class NumberComboBox(QComboBox):
    """
    A number box that has choice from 1 to 9
    """
    first_choice = "1"
    other_choices = ["2", "3", "4", "5", "6", "7", "8", "9"]

    def __init__(self):
        super(NumberComboBox, self).__init__()
        self.addItem(self.first_choice)
        self.addItems(self.other_choices)


class ImportanceComboBox(QComboBox):
    """
    A number box that has choice from not important to immediately.
    """
    choices = [Importance.IMMEDIATELY, Importance.EARLY, Importance.NORMAL, Importance.LATER, Importance.ANY_TIME]

    def __init__(self):
        super(ImportanceComboBox, self).__init__()
        temp = list()
        for i in self.choices:
            temp.append(i.name.capitalize())

        self.addItems(temp)

        self.setCurrentIndex(2)

    def currentValue(self):
        return self.choices[self.currentIndex()].value


if __name__ == '__main__':
    print("The below is for test only. If you do not wish to test, you shouldn't see this piece of code. Go debug pls!")
