#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from PyQt5.QtWidgets import QApplication, QLCDNumber
import sys
from constants import *


class Application:
    """
    The top class.
    """
    def __init__(self):
        application = QApplication(sys.argv)
        self.window = Window()
        self.manager = Manager(self)
        self.window.show()
        sys.exit(application.exec_())


class Manager:
    """
    This objects manages everything.
    Draw widgets on the screen, manipulates the logic and widgets relationship.
    Receive operations and present the needed screen.
    """
    def __init__(self, application):
        self.tag = WindowType.INIT
        self.application = application
        self.to_login()
        self.to_countdown()

    def to_login(self):
        pass

    def to_countdown(self, mission_name="None"):
        # Init window
        self.application.window.setGeometry(300, 300, 400, 300)
        self.application.window.setWindowTitle("CountDown")

        # Init Ui
        self.application.window.name_of_mission_name = QLabel("Ongoing Mission: ")
        self.application.window.mission_name = QLabel(str(mission_name))
        # self.seperation_line =
        self.application.window.lcd_left_text = QLabel("You have")
        # todo time setting
        self.application.window.lcd = QLCDNumber(self.application.window)
        self.application.window.lcd_right_text = QLabel("Minutes Left")
        self.application.window.early_finished_button = Buttons("If you finished early, click me!",
                                                                self.application.window)
        self.application.window.early_finished_button.set_button_name("Early finished button")
        self.application.window.early_finished_button.connect_event(self.destroy)  # todo delete this test code. 

        # lcd format setting
        self.application.window.lcd.setDigitCount(8)
        self.application.window.lcd.setMode(QLCDNumber.Dec)
        self.application.window.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.application.window.lcd.setStyleSheet("border: 2px solid black; color: red; background: silver;")

        # Ui Layout

        mission_hbox = QHBoxLayout()
        mission_hbox.addStretch(2)
        mission_hbox.addWidget(self.application.window.name_of_mission_name)
        mission_hbox.addStretch(1)
        mission_hbox.addWidget(self.application.window.mission_name)
        mission_hbox.addStretch(2)

        lcd_hbox = QHBoxLayout()
        lcd_hbox.addStretch(2)
        lcd_hbox.addWidget(self.application.window.lcd_left_text)
        lcd_hbox.addWidget(self.application.window.lcd)
        lcd_hbox.addWidget(self.application.window.lcd_right_text)
        lcd_hbox.addStretch(2)

        early_finished_button_layout = QHBoxLayout()
        early_finished_button_layout.addStretch(2)
        early_finished_button_layout.addWidget(self.application.window.early_finished_button)
        early_finished_button_layout.addStretch(2)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(mission_hbox)
        vbox.addStretch(1)
        vbox.addLayout(lcd_hbox)
        vbox.addStretch(1)
        vbox.addLayout(early_finished_button_layout)
        vbox.addStretch(2)

        self.application.window.setLayout(vbox)

        self.tag = WindowType.CD

        self.application.window.show()  # Update the window changes.

    def destroy(self):
        """
        According to the current tag, delete all components in the window.
        :return: 1 when success, 0 when failed for any reason.
        """
        self.application.window = Window()
        self.tag = WindowType.INIT
        self.application.window.show()


if __name__ == "__main__":
    test = Application()
