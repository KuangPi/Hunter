#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from DbEasy import *
from constants import *
from Signal import *

from PyQt5.QtWidgets import QApplication, QLCDNumber, QMessageBox
from PyQt5.QtCore import Qt

import sys
import hashlib


class Application:
    def __init__(self):
        # Application Running
        application = QApplication(sys.argv)
        self.manager = Manager()
        application.setWindowIcon(QIcon('./images/hunter_logo.png'))

        sys.exit(application.exec_())


class Manager:
    def __init__(self):
        self.current_user = User()
        self.window = Window()

        # For connect the events with the slots
        self.slot_main_window_transfer = ChangeSignalMainScreen()
        self.slot_main_window_transfer.signal.connect(self.to_main)

        self.tag = WindowType.INIT
        self.to_login()

    def to_login(self):
        self.window = LoginWindow(self)
        self.set_tag(WindowType.LOGIN)
        self.window.show()

    def to_main(self):
        self.window = MainWindow()
        self.set_tag(WindowType.MAIN)
        self.window.show()

    def set_tag(self, new=None):
        if new is None:
            return self.tag
        else:
            self.tag = new
            return self.tag

    def get_user(self, user=None):
        if user is not None:
            self.current_user = user
        return self.current_user

    def get_username(self):
        return self.current_user.get_information(1)

    def reset_window(self):
        """
        Always create a new window right after rest it.
        """
        self.window = None


class LoginWindow(Window):
    def __init__(self, manager):
        super(LoginWindow, self).__init__()

        # Attribute set up.
        self.manager = manager

        # Attribute UI set up.
        self.holder_username = InputLine()
        self.holder_password = InputLine()

        # UI set up.
        self.set_size(1080, 720)
        self.center()
        self.setWindowTitle("Hunter: Login")
        self.tag_hint_message = Labels("")

        tag_notification = Labels("Enter below to login or register")
        tag_username = Labels("Username:")
        tag_password = Labels("Password: ")

        button_login = Buttons("Login", self.login_button_event)
        button_register = Buttons("Register", self.register_button_event)

        layout_top_notification = QHBoxLayout()
        layout_top_notification.addStretch(1)
        layout_top_notification.addWidget(tag_notification)
        layout_top_notification.addStretch(1)

        layout_username = QHBoxLayout()
        layout_username.addStretch(1)
        layout_username.addWidget(tag_username)
        layout_username.addWidget(self.holder_username)
        layout_username.addStretch(1)

        layout_password = QHBoxLayout()
        layout_password.addStretch(1)
        layout_password.addWidget(tag_password)
        layout_password.addWidget(self.holder_password)
        layout_password.addStretch(1)

        layout_error_message = QHBoxLayout()
        layout_error_message.addStretch(1)
        layout_error_message.addWidget(self.tag_hint_message)
        layout_error_message.addStretch(1)

        layout_buttons = QHBoxLayout()
        layout_buttons.addStretch(2)
        layout_buttons.addWidget(button_register)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(button_login)
        layout_buttons.addStretch(2)

        layout_all = QVBoxLayout()
        layout_all.addStretch(8)
        layout_all.addLayout(layout_top_notification)
        layout_all.addStretch(4)
        layout_all.addLayout(layout_username)
        layout_all.addLayout(layout_password)
        layout_all.addStretch(1)
        layout_all.addLayout(layout_error_message)
        layout_all.addStretch(1)
        layout_all.addLayout(layout_buttons)
        layout_all.addStretch(8)

        # UI attribute set up.
        self.holder_password.setEchoMode(InputLine.Password)

        # Finish UI setting.
        self.setLayout(layout_all)

    def user_information(self):
        return self.holder_username.text(), sha256(self.holder_password.text())

    # Button click events

    def login_button_event(self):
        username, password = self.user_information()
        self.set_user(username)
        temp = search_in_database(username, "UserName", "Login")
        if temp[0] is "NF" or password != temp[0][1]:
            self.set_login_message(False, True)
        else:
            print(f"User '{username}' logging into the system...")
            self.set_login_message(True, True)
            self.manager.slot_main_window_transfer.run()

    def register_button_event(self):
        username, password = self.user_information()
        self.set_user(username)
        reply = QMessageBox.question(self, 'Register check',
                                     f"Are you sure to register with '{username}' as your username? ",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            if search_in_database(username, "UserName", "Login") == ["NF"]:
                insert_into_database([username, password], "Login")
                self.set_login_message(True, False)
            else:
                self.set_login_message(False, False)

    def set_login_message(self, is_correct, is_login):
        if is_login:
            if not is_correct:
                self.tag_hint_message.reset_text("Wrong Username or Password! ", "c02c38")  # red
            else:
                self.tag_hint_message.reset_text(f"Welcome {self.get_username()}. "
                                                 f"Logging you in.", "248067")
        else:
            if not is_correct:
                self.tag_hint_message.reset_text("Registration failed! "
                                                 "The username has already been taken! ", "c02c38")
            else:
                self.tag_hint_message.reset_text("Registration succeeded! "
                                                 "Now press 'login' to login ", "248067")

    def keyPressEvent(self, key):
        super(LoginWindow, self).keyPressEvent(key)
        if key.key() == Qt.Key_Enter or key.key() == Qt.Key_Return:
            self.login_button_event()

    def set_user(self, username):
        self.manager.get_user(User(username))

    def get_user(self):
        return self.manager.get_user()

    def get_username(self):
        return self.manager.get_username()

    def login_finished(self):
        # Send the signal to jump to the main screen
        pass


class MainWindow(Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Hunter: Mission Selection")
        self.set_size(780, 720)
        self.sideWindow = SideWindow(self)

        self.mission1 = MissionButtons()
        self.mission2 = MissionButtons()
        self.mission_new = NewMissionButtons()

        self.mission_board_buttons = FunctionalButtons(self.show_side_window)
        self.store_button = FunctionalButtons()
        self.settings_button = FunctionalButtons()

        layout_missions = QHBoxLayout()
        layout_missions.addStretch(2)
        layout_missions.addWidget(self.mission1, 1)
        layout_missions.addStretch(1)
        layout_missions.addWidget(self.mission2, 1)
        layout_missions.addStretch(1)
        layout_missions.addWidget(self.mission_new, 1)
        layout_missions.addStretch(2)

        layout_functional_buttons = QVBoxLayout()
        layout_missions.addStretch(1)
        layout_functional_buttons.addWidget(self.mission_board_buttons)
        layout_functional_buttons.addWidget(self.store_button)
        layout_functional_buttons.addWidget(self.settings_button)
        layout_missions.addStretch(1)

        layout_all = QHBoxLayout()
        layout_missions.addStretch(1)
        layout_all.addLayout(layout_functional_buttons)
        layout_missions.addStretch(1)
        layout_all.setSizeConstraint(1)
        layout_all.addLayout(layout_missions)

        self.setLayout(layout_all)
        self.show_side_window()

    def show_side_window(self):
        self.sideWindow = SideWindow(self)
        self.sideWindow.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.sideWindow = None
            event.accept()
        else:
            event.ignore()


class SideWindow(Window):
    def __init__(self, owner):
        super(SideWindow, self).__init__()
        self.setWindowTitle("Hunter: Profile")
        self.owner_window = owner
        self.setGeometry(self.owner_window.x() + self.owner_window.width(),
                         self.owner_window.y() + 22, 300, 720)  # A weired way to solve a weired bug. The location of
        # the side window will be little shorter than the main window.
        # The x() and y() may not have show the true location.
        # todo Check if this happens to Windows also or if it is a special bug for mac.
        self.setFixedSize(300, 720)


# ############ Window Class Finishes here ################# #


class FunctionalButtons(Buttons):
    def __init__(self, event=None):
        super(FunctionalButtons, self).__init__("Functional Buttons", event)
        self.set_size(100, 100)


class MissionButtons(Buttons):
    def __init__(self, mission_name="mission"):
        super(MissionButtons, self).__init__(mission_name)
        self.setMinimumSize(200, 500)


class NewMissionButtons(MissionButtons):
    def __init__(self):
        super(NewMissionButtons, self).__init__("New")


class User:
    def __init__(self, username="Have not logged in"):
        self.username = username
        self.other_information = []
        self.update_information(self.username)

    def get_information(self, n):
        # Search in database for other records.
        return self.other_information[0:n]

    def update_information(self, content):
        self.other_information.append(content)


def sha256(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    app = Application()
