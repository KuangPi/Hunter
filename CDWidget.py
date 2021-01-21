#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from PyQt5.QtWidgets import *


class CountDownWidget(Window):
    def __init__(self, mission_name):
        super(CountDownWidget, self).__init__()

        # Init window
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle("CountDown")

        # Init Ui
        self.name_of_mission_name = QLabel("Ongoing Mission: ")
        self.mission_name = QLabel(str(mission_name))
        # self.seperation_line =
        self.lcd_left_text = QLabel("You have")
        # todo time setting
        self.lcd =QLCDNumber(self)
        self.lcd_right_text = QLabel("Minutes Left")
        self.early_finished_button = Buttons("If you finished early, click me!", self)
        self.early_finished_button.set_button_name("Early finished button")

        # lcd format setting
        self.lcd.setDigitCount(8)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setStyleSheet("border: 2px solid black; color: red; background: silver;")

        # Ui Layout

        mission_hbox = QHBoxLayout()
        mission_hbox.addStretch(2)
        mission_hbox.addWidget(self.name_of_mission_name)
        mission_hbox.addStretch(1)
        mission_hbox.addWidget(self.mission_name)
        mission_hbox.addStretch(2)

        lcd_hbox = QHBoxLayout()
        lcd_hbox.addStretch(2)
        lcd_hbox.addWidget(self.lcd_left_text)
        lcd_hbox.addWidget(self.lcd)
        lcd_hbox.addWidget(self.lcd_right_text)
        lcd_hbox.addStretch(2)

        early_finished_button_layout = QHBoxLayout()
        early_finished_button_layout.addStretch(2)
        early_finished_button_layout.addWidget(self.early_finished_button)
        early_finished_button_layout.addStretch(2)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(mission_hbox)
        vbox.addStretch(1)
        vbox.addLayout(lcd_hbox)
        vbox.addStretch(1)
        vbox.addLayout(early_finished_button_layout)
        vbox.addStretch(2)

        self.setLayout(vbox)

        self.show()
