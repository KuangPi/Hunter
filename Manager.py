#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from DbEasy import *
from constants import *
from Signal import *

from PyQt5.QtWidgets import QApplication, QLCDNumber, QMessageBox, QSpacerItem, QFrame
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QWindowStateChangeEvent

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
        self.side_window = Window()
        self.side_window.hide()
        self.setting_window = Window()
        self.setting_window.hide()

        # For connect the events with the slots
        self.slot_main_window_transfer = ChangeSignalMainScreen()
        self.slot_main_window_transfer.signal.connect(self.to_main)
        self.slot_side_window_transfer = ChangeSignalSideScreen()
        self.slot_side_window_transfer.signal.connect(self.show_side)
        self.slot_setting_window_transfer = ChangeSignalSettingScreen()
        self.slot_setting_window_transfer.signal.connect(self.show_settings)
        self.slot_main_window_closer = CloseSignalMainScreen()
        self.slot_main_window_closer.signal.connect(self.close_side)

        self.tag = WindowType.INIT
        self.to_login()

    def to_login(self):
        self.reset_window()
        self.window = LoginWindow(self)
        self.set_tag(WindowType.LOGIN)
        self.window.show()

    def to_main(self):
        self.reset_window()
        self.window = MainWindow(self)
        self.set_tag(WindowType.MAIN)
        self.window.show()
        self.show_side()
        self.current_user.pull_information()

    def show_side(self):
        self.side_window = SideWindow(self.window)
        self.side_window.show()

    def show_settings(self):
        self.setting_window = SettingWindow(self)
        self.setting_window.show()

    def close_side(self):
        self.side_window.close()

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
        return self.current_user.get_username()

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

        tag_notification = Labels("The  Hunter")
        tag_notification.setStyleSheet("QLabel{color: red; font-size:60px;}")
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
    minimized = QtCore.pyqtSignal()
    maximized = QtCore.pyqtSignal()

    def __init__(self, manager):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Hunter: Mission Selection")
        self.set_size(780, 720)

        self._manager = manager
        self.list_mission = list()
        self.load_mission()

        self.missions = [MissionButtons(), MissionButtons(), NewMissionButtons()]
        self.stores = [StoreButtons(), StoreButtons(), StoreButtons(), StoreButtons()]
        self.store_mission(False)

        self.mission_board_buttons = FunctionalButtons("./images/mission_board_button.png",
                                                       "./images/mission_board_button_pressed.png",
                                                       self.show_missions)
        self.store_button = FunctionalButtons("./images/store_button.png",
                                              "./images/store_button_pressed.png",
                                              lambda: self.store_mission(True))
        self.settings_button = FunctionalButtons("./images/settings_button.png",
                                                 "./images/settings_button_pressed.png",
                                                 self.show_settings_window)

        layout_missions = QHBoxLayout()
        layout_missions.addStretch(2)
        layout_missions.addWidget(self.stores[0])
        layout_missions.addWidget(self.missions[0])
        layout_missions.addWidget(self.stores[1])
        layout_missions.addWidget(self.missions[1])
        layout_missions.addWidget(self.stores[2])
        layout_missions.addWidget(self.missions[2])
        layout_missions.addWidget(self.stores[3])
        layout_missions.addStretch(2)

        layout_functional_buttons = QVBoxLayout()
        layout_functional_buttons.addStretch(2)
        layout_functional_buttons.addWidget(self.mission_board_buttons)
        layout_functional_buttons.addStretch(1)
        layout_functional_buttons.addWidget(self.store_button)
        layout_functional_buttons.addStretch(1)
        layout_functional_buttons.addWidget(self.settings_button)
        layout_functional_buttons.addStretch(2)

        layout_all = QHBoxLayout()
        layout_all.addStretch(1)
        layout_all.addLayout(layout_functional_buttons)
        layout_all.addStretch(1)
        layout_all.setSizeConstraint(1)
        layout_all.addLayout(layout_missions)
        layout_all.addStretch(1)

        self.setLayout(layout_all)

    def show_side_window(self):
        self._manager.slot_side_window_transfer.run()

    def show_settings_window(self):
        self._manager.slot_setting_window_transfer.run()

    def show_missions(self):
        self.store_mission(False)
        self.show_side_window()

    def show_store(self):
        self.store_mission(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self._manager.slot_main_window_closer.run()
            event.accept()
        else:
            event.ignore()

    def load_mission(self):
        temp = search_in_database(self._manager.get_user().get_username(), "BelongUserName", "Mission")
        for elements in temp:
            self.list_mission.append(Mission(elements))

    def store_mission(self, show_store):
        if show_store:
            for elements in self.missions:
                elements.setVisible(False)
            for elements in self.stores:
                elements.setVisible(True)
        else:
            for elements in self.missions:
                elements.setVisible(True)
            for elements in self.stores:
                elements.setVisible(False)
        self.show()

    def recommended_mission(self):
        """
        This method must be called after at least after one mission is created.
        :return:
        """
        if len(self.list_mission) > 1:
            pass
        else:
            pass

    def get_user(self):
        return self._manager.get_user()

    def changeEvent(self, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self.isMinimized():
                self.minimized.emit()
            else:
                self.maximized.emit()


class SideWindow(Window):
    def __init__(self, owner):
        super(SideWindow, self).__init__()
        self.setWindowTitle("Hunter: Profile")
        self.owner_window = owner
        self.owner_window.minimized.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        self.owner_window.maximized.connect(lambda: self.setWindowState(Qt.WindowNoState))
        self.setGeometry(self.owner_window.x() + self.owner_window.width(),
                         self.owner_window.y(), 300, 740)  # A weired way to solve a weired bug. The location of
        # The bug is because the system hint bar, the way to solve it is to hide the bar, but it will cause extra work.
        self.setFixedSize(300, 742)

        overall_layout = QVBoxLayout()

        information_layout = QHBoxLayout()
        hints_layout = QVBoxLayout()
        datas_layout = QVBoxLayout()

        username_tag = Labels("Username: ")
        success_rate_tag = Labels("Success Rate: ")
        finished_mission_tag = Labels("Mission Accomplished: ")
        unit_time_tag = Labels("1 unit time: ")

        hints_layout.addWidget(username_tag)
        hints_layout.addWidget(success_rate_tag)
        hints_layout.addWidget(finished_mission_tag)
        hints_layout.addWidget(unit_time_tag)

        self.username_data = Labels(self.get_user().get_username())
        self.success_rate_data = Labels()
        self.finished_mission_data = Labels()
        self.unit_time_data = Labels()

        datas_layout.addWidget(self.username_data)
        datas_layout.addWidget(self.success_rate_data)
        datas_layout.addWidget(self.finished_mission_data)
        datas_layout.addWidget(self.unit_time_data)

        information_layout.addLayout(hints_layout)
        information_layout.addLayout(datas_layout)

        todos_layout = QVBoxLayout()

        overall_layout.addLayout(information_layout)
        overall_layout.addLayout(todos_layout)
        self.setLayout(overall_layout)

        self.setWindowFlag(Qt.FramelessWindowHint)

    def closeEvent(self, event):
        event.accept()

    def get_user(self):
        return self.owner_window.get_user()


class SettingWindow(Window):
    def __init__(self, manager):
        super(SettingWindow, self).__init__()
        self.setWindowTitle("Hunter: Settings")
        self.setFixedSize(300, 400)
        self.center()
        self._manager = manager

        overall_layout = QVBoxLayout()   # Overall > sum
        self.username_tag = Labels(f"Hello {self._manager.get_user().get_username()}! \n"
                              f"Please make your settings here.")
        # todo If user has a nick name, use it to replace it here.
        overall_layout.addWidget(self.username_tag)

        sum_layout = QHBoxLayout()  # Overall > sum

        hint = QVBoxLayout()
        nick_name_tag = Labels("Nick Name: ")
        unit_time_tag = Labels("1 Unit Time: ")
        hint.addWidget(nick_name_tag)
        hint.addWidget(unit_time_tag)
        values = QVBoxLayout()
        self.nick_name_holder = InputLine()
        self.nick_name_holder.setText(f"{self._manager.get_user().get_other_information('nick_name')}")
        self.unit_time_holder = InputLine()
        self.unit_time_holder.setText(f"{self._manager.get_user().get_other_information('unit_time')}")
        values.addWidget(self.nick_name_holder)
        values.addWidget(self.unit_time_holder)

        sum_layout.addLayout(hint)
        sum_layout.addStretch(1)
        sum_layout.addLayout(values)
        overall_layout.addLayout(sum_layout)
        line = Line()
        overall_layout.addWidget(line)

        prizes_hint = Labels("You may set your prizes below: ")

        overall_layout.addWidget(prizes_hint)

        buttons_layout = QHBoxLayout()
        self.buttons_ok = Buttons("OK", self.ok_event)
        self.buttons_cancel = Buttons("Cancel", self.cancel_event)
        buttons_layout.addWidget(self.buttons_cancel)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.buttons_ok)

        overall_layout.addLayout(buttons_layout)

        self.setLayout(overall_layout)

    def closeEvent(self, event):
        event.accept()

    def ok_event(self):
        self._manager.get_user().update_local_information([self.nick_name_holder.text(),
                                                           self.unit_time_holder.text(),
                                                           None],
                                                          True)
        self.username_tag.setText("Successfully update the settings! ")

    def cancel_event(self):
        self.close()


# ############ Window Class Finishes here ################# #

class FunctionalButtons(Buttons):
    def __init__(self, image_on, image_off, event=None):
        super(FunctionalButtons, self).__init__("", event)
        self.set_size(100, 100)
        self.image_on = image_on
        self.image_off = image_off
        self._released()  # This is a function for button event, but its function is suitable for init the button.

        self.pressed.connect(self._pressed)
        self.released.connect(self._released)

    def _pressed(self):
        self.setStyleSheet(f"QPushButton{{border-image: url({self.image_off})}}")

    def _released(self):
        self.setStyleSheet(f"QPushButton{{border-image: url({self.image_on})}}")


class CardsButton(QFrame):
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super(CardsButton, self).__init__()
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(10)
        self.pressed = False

        self.setFixedSize(200, 400)

        self.connect_event()

    def mouseReleaseEvent(self, ev: QMouseEvent):
        if self.pressed:
            self.clicked.emit()
            self.setFrameShadow(QFrame.Raised)
            self.pressed = False

    def mousePressEvent(self, ev: QMouseEvent):
        self.setFrameShadow(QFrame.Sunken)
        self.pressed = True

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


class MissionButtons(CardsButton):
    def __init__(self, mission_name="mission", mission_duration=1, mission_ddl="00000000"):
        super(MissionButtons, self).__init__()

        labels = QVBoxLayout()
        self.mission_name = Labels(mission_name)
        mission_duration = Labels(f"{mission_duration} unit time")
        mission_ddl = Labels(mission_ddl)
        labels.addWidget(self.mission_name)
        labels.addWidget(mission_duration)
        labels.addWidget(mission_ddl)
        labels.setAlignment(Qt.AlignHCenter)

        self.setLayout(labels)

    def click_event(self):
        """
        Rewrite this function to bind any event to this button.
        When rewriting, simply build the attempted commands and it will run as needed.
        """
        print(f"Start mission {self.mission_name}! ")


class StoreButtons(CardsButton):
    def __init__(self, prize_name="prize", prize_duration=1, prize_cost=1):
        super(StoreButtons, self).__init__()
        self.setMinimumSize(150, 400)

        labels = QVBoxLayout()
        self.mission_name = Labels(prize_name)
        mission_duration = Labels(f"{prize_duration} unit time")
        mission_ddl = Labels(f"Costs: {prize_cost}")
        labels.addWidget(self.mission_name)
        labels.addWidget(mission_duration)
        labels.addWidget(mission_ddl)
        labels.setAlignment(Qt.AlignHCenter)

        self.setLayout(labels)


class NewMissionButtons(CardsButton):
    def __init__(self):
        super(NewMissionButtons, self).__init__()
        new_labels = Labels("New")
        layout = QVBoxLayout()
        layout.addWidget(new_labels)
        layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(layout)


class User:
    def __init__(self, username="Have not logged in"):
        self.username = username

        # The following information are empty when init.
        # They will be update later.
        self.nick_name = None
        self.unit_time = None
        self.mission_accomplished = None
        self.prizes = None
        self.prizes_times = None

    def get_username(self):
        return self.username

    def pull_information(self):
        temp = search_in_database(self.username, "UserName", "UserInformation")
        try:
            self.username = temp[0][0]
        except IndexError:
            return False
        try:
            self.nick_name = temp[0][1]
        except IndexError:
            return False
        try:
            self.unit_time = temp[0][2]
        except IndexError:
            return False
        try:
            self.mission_accomplished = temp[0][3]
        except IndexError:
            return False
        try:
            self.prizes = temp[0][4].split(", ")
        except IndexError:
            return False
        try:
            self.prizes_times = temp[0][5].split(", ")
        except IndexError:
            return False
        return True

    def update_local_information(self, values, directly_to_db):
        self.nick_name = values[0]
        failed_update = 0
        try:
            self.unit_time = int(values[1])
        except TypeError:
            failed_update += 1
        try:
            self.mission_accomplished = int(values[2])
        except TypeError:
            failed_update += 1

        if directly_to_db:
            self.update_information_to_db()

    def update_information_to_db(self):
        update_existing_in_database(self.username, "UserName",
                                    [self.nick_name, self.unit_time, self.mission_accomplished],
                                    ["UserPreferredName", "UserUnitTime", "UserMissionAccomplished"],
                                    "UserInformation")

    def get_other_information(self, name):
        if name == "nick_name":
            return self.nick_name
        elif name == "unit_time":
            return self.unit_time
        elif name == "mission_accomplished":
            return self.mission_accomplished
        else:
            raise KeyError("Wrong user 'Name' is given when using 'get_other_information' method! ")


class Mission:
    def __init__(self, information):
        self.mission_id = information[0]
        self.belong_user = information[1]
        self.mission_name= information[2]
        self.mission_ddl = information[3]
        self.mission_duration = information[4]

    def __str__(self):
        return f"The mission {self.mission_name} has a deadline on {self.mission_ddl} and " \
               f"will take you {self.mission_duration} * 25 min to finish it. "

    def __repr__(self):
        return self.__str__()


def sha256(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def find_2_largest(unsorted_list):
    largest1 = - 100000
    largest2 = - 100000
    largest1_index = None
    largest2_index = None

    for i in range(len(unsorted_list)):
        test = unsorted_list[i]
        if test > largest1:
            largest2 = largest1
            largest2_index = largest1_index
            largest1 = test
            largest1_index = i
        elif unsorted_list[i] > largest2:
            largest2 = test
            largest2_index = i
    return largest1_index, largest2_index


def quick_sort(unsorted_list):
    pivot = unsorted_list[0]
    for i in range(len(unsorted_list)):
        if unsorted_list[i] < pivot:
            temp = unsorted_list
        else:  # Case of the same value is considered to be here
            pass


if __name__ == "__main__":
    app = Application()
