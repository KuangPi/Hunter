#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from PyQt5.QtWidgets import QApplication, QLCDNumber
import sys
from DbEasy import *
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
        self.current_user = User(0, "DE", "DE")
        self.to_login()

    # Scene changing methods
    def to_login(self):
        self.reset()
        self.application.window.setGeometry(300, 300, 400, 300)
        self.application.window.setWindowTitle("Hunter: Login")
        self.application.window.tag_username = Labels("Username:")
        self.application.window.tag_password = Labels("Password: ")
        self.application.window.tag_hintMessage = Labels("")

        self.application.window.holder_username = InputLine()
        self.application.window.holder_password = InputLine()

        self.application.window.button_login = Buttons("Login", self.button_event_login)
        self.application.window.button_register = Buttons("Register", self.button_event_register)

        layout_username = QHBoxLayout()
        layout_username.addStretch(1)
        layout_username.addWidget(self.application.window.tag_username)
        layout_username.addWidget(self.application.window.holder_username)
        layout_username.addStretch(1)

        layout_password = QHBoxLayout()
        layout_password.addStretch(1)
        layout_password.addWidget(self.application.window.tag_password)
        layout_password.addWidget(self.application.window.holder_password)
        layout_password.addStretch(1)

        layout_error_message = QHBoxLayout()
        layout_error_message.addStretch(1)
        layout_error_message.addWidget(self.application.window.tag_hintMessage)
        layout_error_message.addStretch(1)

        layout_buttons = QHBoxLayout()
        layout_buttons.addStretch(2)
        layout_buttons.addWidget(self.application.window.button_register)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.application.window.button_login)
        layout_buttons.addStretch(2)

        layout_all = QVBoxLayout()
        layout_all.addStretch(2)
        layout_all.addLayout(layout_username)
        layout_all.addLayout(layout_password)
        layout_all.addLayout(layout_error_message)
        layout_all.addLayout(layout_buttons)
        layout_all.addStretch(2)

        self.application.window.setLayout(layout_all)

        self.set_tag(WindowType.LOGIN)

    def to_countdown(self, mission_name="None"):
        self.reset()
        # Init window
        self.application.window.setGeometry(300, 300, 400, 300)
        self.application.window.setWindowTitle("Hunter: Ongoing Mission")

        # Init Ui
        self.application.window.name_of_mission_name = QLabel("Ongoing Mission: ")
        self.application.window.mission_name = QLabel(str(mission_name))
        # self.seperation_line =
        self.application.window.lcd_left_text = QLabel("You have")
        # todo time setting
        self.application.window.lcd = QLCDNumber(self.application.window)
        self.application.window.lcd_right_text = QLabel("Minutes Left")
        self.application.window.early_finished_button = Buttons("If you finished early, click me!")
        self.application.window.early_finished_button.set_button_name("Early finished button")

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

        self.set_tag(WindowType.CD)

        self.application.window.show()  # Update the window changes.

    def to_main(self):
        self.reset()
        # todo UI of the MainWindow

    # Attribute Manipulation Methods
    def reset(self):
        """
        According to the current tag, delete all components in the window.
        :return: 1 when success, 0 when failed for any reason.
        """
        self.application.window = Window()
        self.tag = WindowType.INIT
        self.application.window.show()

    def set_tag(self, new):
        """
        Set the window tag to the parameter. Return the old tag.
        :param new:
        :return:
        """
        if isinstance(new, WindowType):
            old = self.tag
            self.tag = new
            return old
        else:
            raise TypeError("The given parameter is in wrong type! ")

    def set_current_user(self, _id, username, password):
        self.current_user = User(_id, username, password)

    def set_login_message(self, is_correct):
        # todo Generalize this method so that other error message could also use this.
        if not is_correct:
            self.application.window.tag_hintMessage.reset_text("Wrong Username or Password! ", "c02c38")  # red
        else:
            self.application.window.tag_hintMessage.reset_text(f"Welcome {self.current_user.get_username()}. "
                                                               f"Logging you in.")

    # Button Click event
    def button_event_login(self):
        if self.tag is WindowType.LOGIN:
            username = self.application.window.holder_username.text()
            password = self.application.window.holder_password.text()
            temp = search_in_database(username, "UserName", "Login")
            if temp[0] is "NF" or password != temp[0][2]:
                self.set_login_message(False)
            else:
                self.set_current_user(temp[0][0], temp[0][1], temp[0][2])
                self.set_login_message(True)
        else:
            raise TabError("Wrong Page. button_event_check_login() should only be called when at register page! ")

    def button_event_register(self):
        if self.tag is WindowType.LOGIN:
            print("Register! ")
            # todo check the unique of the username.
        else:
            raise TabError("Wrong Page. button_event_check_login() should only be called when at register page! ")


class User:
    def __init__(self, _id, username, password):
        self.user_id = _id
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_id(self):
        return self.user_id


# Several Pure functions
def pf_check_account(self, username):
    return not search_in_database(username, "UserName", "Login")[0] is "NF"


if __name__ == "__main__":
    test = Application()
