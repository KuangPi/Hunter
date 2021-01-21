#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

"""
This script manipulates the GUI of the application. Using pyqt5 and creates all kinds application required.
"""

from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon
import time
import sys


"""
The below lines are the basic inheritance of the Needed part of the PYQT5. 
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
        self.center()

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


class Labels(QLabel):
    """
    The label that used to put on a place with content given.
    """
    def __init__(self, content="Blank"):
        super(Labels, self).__init__()
        self.setText(f"{content}")


class Buttons(QPushButton):
    """
    There are many buttons in this programs. All of them are child of this class.
    """
    def __init__(self, content, window):
        super(Buttons, self).__init__(content, window)
        self.content = content  # Please remember that this will not be update if the text on the button is changed.
        self.clicked.connect(self.click_event)

    def click_event(self):
        """
        Rewrite this function to bind any event to this button.
        When rewriting, simply build the attempted commands and it will run as needed.
        """
        print(f"{self} is clicked! ")

    def __str__(self):
        return f"Button with {self.content}"


class ButtonQuit(Buttons):
    def __init__(self, window):
        super(ButtonQuit, self).__init__("Quit", window)

    def click_event(self):
        # todo Call the close event when quit.
        # This is a temporary solution, which directly copies the code from close event.
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QCoreApplication.instance().quit()
        else:
            pass


if __name__ == '__main__':
    print("The below is for test only. If you do not wish to test, you shouldn't see this piece of code. Go debug pls!")
