#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from PyQt5.QtWidgets import QApplication
import sys


class Manager:
    """
    This objects manages everything.
    Draw widgets on the screen, manipulates the logic and widgets relationship.
    Receive operations and present the needed screen.
    """
    def __init__(self):
        # Create the application
        self.application = QApplication(sys.argv)
        # todo Login
        pass
        # todo delete the test code below.
        self.window = Window()

        self.simple_button = Buttons("Test", self.window)
        self.quit_button = ButtonQuit(self.window)
        self.quit_button.setGeometry(200, 200, 200, 200)

        self.window.show()
        sys.exit(self.application.exec_())


if __name__ == "__main__":
    test = Manager()
