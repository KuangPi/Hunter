#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from QtEasy import *
from DbEasy import *
from constants import *
from Signal import *

from PyQt5.QtWidgets import QApplication, QLCDNumber, QMessageBox, QSpacerItem, QFrame, QListWidget
from PyQt5.QtCore import Qt, QDate, QThread, QTime
from PyQt5.QtGui import QMouseEvent, QWindowStateChangeEvent

import sys
import hashlib
import time


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
        self.current_mission = None
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
        self.slot_new_window_transfer = ChangeSignalNewMissionScreen()
        self.slot_new_window_transfer.signal.connect(self.show_new)
        self.slot_count_down_window_transfer = ChangeSignalCountDownScreen()
        self.slot_count_down_window_transfer.signal.connect(self.to_count_down)

        self.tag = WindowType.INIT
        self.to_login()

    def to_login(self):
        self.reset_window()
        self.window = LoginWindow(self)
        self.set_tag(WindowType.LOGIN)
        self.window.show()

    def to_main(self):
        self.reset_window()
        self.current_user.pull_information()
        self.window = MainWindow(self)
        self.set_tag(WindowType.MAIN)
        self.window.show()
        self.show_side()

    def to_count_down(self):
        self.reset_window()
        self.window = CountDownWindow(self.current_mission.mission_name)
        self.window.completed.connect(self.mission_completed)
        self.window.closing.connect(self.to_main)
        self.set_tag(WindowType.CD)
        self.window.show()

    def show_side(self):
        self.side_window = SideWindow(self.window)
        self.side_window.show()

    def show_settings(self):
        self.setting_window = SettingWindow(self)
        self.setting_window.show()

    def show_new(self):
        self.new_window = NewMissionMessageBox(self)
        self.new_window.show()

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
        self.window.is_reset = True
        self.window.close()

    def mission_completed(self):
        mission = self.current_mission
        if mission is not None:
            # Add the record to local device.
            today = QDate.currentDate().toString()
            records = open(f"records/{today}_{self.get_username()}.txt", mode="a")
            records.write(f"{mission.__repr__()}/{today}\n")
            records.close()

            # Add the record to database.
            username = self.get_username()
            update_existing_in_database(username,
                                        "UserName",
                                        [str(int(search_in_database(username,
                                                                    "UserName",
                                                                    "UserInformation",
                                                                    "UserMissionAccomplished")[0][0])+1),
                                         str(int(search_in_database(username,
                                                                    "UserName",
                                                                    "UserInformation",
                                                                    "UserMoney")[0][0]) + 1)
                                         ],
                                        ["UserMissionAccomplished", "UserMoney"],
                                        "UserInformation")
            # Remove the mission completed from the mission.
            delete_records_in_database(mission.mission_id, "MissionID", "Mission")
            self.current_mission = None


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
        if temp is None or password != temp[0][1]:
            self.set_login_message(False, True)
        else:
            print(f"User '{username}' logging into the system...")
            self.set_login_message(True, True)
            self.manager.slot_main_window_transfer.run()

    def register_button_event(self):
        username, password = self.user_information()
        if username == "" or password == sha256(""):
            self.set_login_message(False, False, True)
        else:
            self.set_user(username)
            reply = QMessageBox.question(self, 'Register check',
                                         f"Are you sure to register with '{username}' as your username? ",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if search_in_database(username, "UserName", "Login") is None:
                    insert_into_database([username, password], "Login")
                    insert_into_database([username, None], "UserInformation",
                                         ["UserName", "UserPreferredName"])
                    self.set_login_message(True, False)
                else:
                    self.set_login_message(False, False)

    def set_login_message(self, is_correct, is_login, is_waitting_register=False):
        if is_waitting_register:
            self.tag_hint_message.set_content("Enter information above to register")
            self.tag_hint_message.set_color("c02c38")
        else:
            if is_login:
                if not is_correct:
                    self.tag_hint_message.set_content("Wrong Username or Password! ")
                    self.tag_hint_message.set_color("c02c38")  # red
                else:
                    self.tag_hint_message.set_content(f"Welcome {self.get_username()}. Logging you in.")
                    self.tag_hint_message.set_color("248067")  # Green
            else:
                if not is_correct:
                    self.tag_hint_message.set_content("Registration failed! The username has already been taken! ")
                    self.tag_hint_message.set_color("c02c38")
                else:
                    self.tag_hint_message.set_content("Registration succeeded! Now press 'login' to login ")
                    self.tag_hint_message.set_color("248067")

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
    moved = QtCore.pyqtSignal()
    mission_moved = QtCore.pyqtSignal()
    user_info_changed = QtCore.pyqtSignal()

    def __init__(self, manager):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Hunter: Mission Selection")
        self.set_size(780, 720)

        self._manager = manager

        a, b = self.recommended_mission()

        self.missions = [MissionButtons(a), MissionButtons(b), NewMissionButtons(self._manager)]
        self.stores = [StoreButtons(), StoreButtons(), StoreButtons()]
        self.update_store()
        self.store_mission(False)

        self.missions[0].connect_event(lambda: self.mission_clicked(self.missions[0].mission))
        self.missions[1].connect_event(lambda: self.mission_clicked(self.missions[1].mission))

        for prizes in self.stores:
            prizes.consume.connect(self.prize_consumed)

        self.mission_board_buttons = FunctionalButtons("./images/mission_board_button.png",
                                                       "./images/mission_board_button_pressed.png",
                                                       self.show_missions)
        self.store_button = FunctionalButtons("./images/store_button.png",
                                              "./images/store_button_pressed.png",
                                              self.show_store)
        self.settings_button = FunctionalButtons("./images/settings_button.png",
                                                 "./images/settings_button_pressed.png",
                                                 self.show_settings_window)

        self.mission_moved.connect(self.mission_update)

        layout_missions = QHBoxLayout()
        layout_missions.addStretch(2)
        layout_missions.addWidget(self.stores[0])
        layout_missions.addWidget(self.missions[0])
        layout_missions.addWidget(self.stores[1])
        layout_missions.addWidget(self.missions[1])
        layout_missions.addWidget(self.stores[2])
        layout_missions.addWidget(self.missions[2])
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
        self.mission_moved.emit()
        self.update_store()
        self.store_mission(False)

    def update_store(self):
        self.get_user().pull_information()
        prizes_names = self.get_user().prizes
        prizes_cost = self.get_user().prizes_cost
        if prizes_names[0] is not None and prizes_cost[0] is not None:
            length = 3
            if length == len(prizes_cost) and length == len(prizes_names):
                for i in range(length):
                    self.stores[i].update_prize(prizes_names[i], prizes_cost[i])

    def show_store(self):
        self.update_store()
        self.store_mission(True)

    def closeEvent(self, event):
        if self.is_reset:
            self.is_reset = False
            self._manager.slot_main_window_closer.run()
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self._manager.slot_main_window_closer.run()
                event.accept()
            else:
                event.ignore()

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
        :return: A list of 2 Mission type object
        """
        self.get_user().pull_information()
        temp = self.get_user().mission
        weighted_values = list()
        for mission in temp:
            weighted_values.append(mission.value())

        a, b = find_2_smallest(weighted_values)
        if a is None:
            if b is None:
                return None, None
            else:
                return None, temp[b]
        else:
            if b is None:
                return temp[a], None
            else:
                return temp[a], temp[b]

    def mission_update(self):
        a, b = self.recommended_mission()
        self.missions[0].update_content(a)
        self.missions[1].update_content(b)

        self.update_store()

        self.update()

    def get_user(self):
        return self._manager.get_user()

    def prize_consumed(self, cost):
        if self.get_user().currency is not None and int(self.get_user().currency) >= cost:
            self.get_user().currency = str(int(self.get_user().currency) - cost)
            self.get_user().update_information_to_db()
            self.user_info_changed.emit()

    def mission_clicked(self, mission):
        if mission is not None:
            self._manager.current_mission = mission
            self._manager.slot_count_down_window_transfer.run()

    def changeEvent(self, event):
        super(MainWindow, self).changeEvent(event)
        self.moved.emit()  # Moved event does not run every time. The signal should be at a higher level.
        # Consider rewrite the window moving event.
        if isinstance(event, QWindowStateChangeEvent):
            if self.isMinimized():
                self.minimized.emit()
            else:
                self.maximized.emit()

    def mouseMoveEvent(self, e):
        super(MainWindow, self).mousePressEvent(e)
        self.moved.emit()
        # There's still some problem that cause the side window' position cannot be immediately updated after main's
        # moving. It might need to rewrite more complex event to achieve that feature.


class SideWindow(Window):
    def __init__(self, owner):
        super(SideWindow, self).__init__()
        self.setWindowTitle("Hunter: Profile")
        self.owner_window = owner
        self.owner_window.minimized.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        self.owner_window.maximized.connect(lambda: self.setWindowState(Qt.WindowNoState))
        self.owner_window.moved.connect(self.set_location)
        self.owner_window.user_info_changed.connect(self.update_self)
        self.set_location()
        self.setFixedSize(300, 742)

        overall_layout = QVBoxLayout()

        information_layout = QHBoxLayout()
        hints_layout = QVBoxLayout()
        datas_layout = QVBoxLayout()

        username_tag = Labels("Username: ")
        currency_tag = Labels("Currency: ")
        finished_mission_tag = Labels("Mission Accomplished: ")
        unit_time_tag = Labels("1 unit time: ")

        hints_layout.addWidget(username_tag)
        hints_layout.addWidget(currency_tag)
        hints_layout.addWidget(finished_mission_tag)
        hints_layout.addWidget(unit_time_tag)

        self.username_data = Labels(self.get_user().get_nickname())
        self.success_rate_data = Labels(self.get_user().get_other_information("CU"))
        self.finished_mission_data = Labels(self.get_user().get_other_information("MA"))
        self.unit_time_data = Labels(self.get_user().get_other_information("UT"))

        datas_layout.addWidget(self.username_data)
        datas_layout.addWidget(self.success_rate_data)
        datas_layout.addWidget(self.finished_mission_data)
        datas_layout.addWidget(self.unit_time_data)

        information_layout.addLayout(hints_layout)
        information_layout.addLayout(datas_layout)

        finished_missions = RecordedFinishedMission(self.owner_window.get_user().get_username())
        overall_layout.addLayout(information_layout)
        overall_layout.addWidget(Line())
        overall_layout.addWidget(finished_missions)
        self.setLayout(overall_layout)

        self.setWindowFlag(Qt.FramelessWindowHint)

    def set_location(self):
        self.setGeometry(self.owner_window.x() + self.owner_window.width(),
                         self.owner_window.y(), 300, 740)
        self.updateGeometry()

    def closeEvent(self, event):
        event.accept()

    def get_user(self):
        return self.owner_window.get_user()

    def update_self(self):
        self.get_user().pull_information()
        self.username_data.set_content(self.get_user().get_nickname())
        self.success_rate_data.set_content(self.get_user().get_other_information("CU"))
        self.finished_mission_data.set_content(self.get_user().get_other_information("MA"))
        self.unit_time_data.set_content(self.get_user().get_other_information("UT"))


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
        self.nick_name_holder.setText(f"{self._manager.get_user().get_other_information('NN')}")
        self.unit_time_holder = InputLine()
        self.unit_time_holder.setText(f"{self._manager.get_user().get_other_information('UT')}")
        values.addWidget(self.nick_name_holder)
        values.addWidget(self.unit_time_holder)

        sum_layout.addLayout(hint)
        sum_layout.addStretch(1)
        sum_layout.addLayout(values)
        overall_layout.addLayout(sum_layout)
        line = Line()
        overall_layout.addWidget(line)

        prizes_hint = Labels("You may set your prizes below: ")
        self.prizes_name_holder1 = InputLine()
        self.prizes_name_holder2 = InputLine()
        self.prizes_name_holder3 = InputLine()
        self.prizes_cost_holder1 = InputLine()
        self.prizes_cost_holder2 = InputLine()
        self.prizes_cost_holder3 = InputLine()
        self.set_prize_original()

        prizes_layout_overall = QVBoxLayout()
        prizes1_layout = QHBoxLayout()
        prizes2_layout = QHBoxLayout()
        prizes3_layout = QHBoxLayout()
        prizes1_layout.addWidget(self.prizes_name_holder1)
        prizes1_layout.addWidget(Labels(": "))
        prizes1_layout.addWidget(self.prizes_cost_holder1)
        prizes2_layout.addWidget(self.prizes_name_holder2)
        prizes2_layout.addWidget(Labels(": "))
        prizes2_layout.addWidget(self.prizes_cost_holder2)
        prizes3_layout.addWidget(self.prizes_name_holder3)
        prizes3_layout.addWidget(Labels(": "))
        prizes3_layout.addWidget(self.prizes_cost_holder3)
        prizes_layout_overall.addLayout(prizes1_layout)
        prizes_layout_overall.addLayout(prizes2_layout)
        prizes_layout_overall.addLayout(prizes3_layout)
        prizes_layout_overall.setAlignment(Qt.AlignTop)

        overall_layout.addWidget(prizes_hint)
        overall_layout.addLayout(prizes_layout_overall)

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
        if self._manager.set_tag() is WindowType.MAIN:
            prize_names = [self.prizes_name_holder1.text(), self.prizes_name_holder2.text(), self.prizes_name_holder3.text()]
            prize_costs = [self.prizes_cost_holder1.text(), self.prizes_cost_holder2.text(), self.prizes_cost_holder3.text()]
            self._manager.get_user().prizes = prize_names
            self._manager.get_user().prizes_cost = prize_costs

            self._manager.get_user().update_local_information([self.nick_name_holder.text(),
                                                               self.unit_time_holder.text(),
                                                               None],
                                                              True)

            self.username_tag.setText("Successfully update the settings! ")

    def cancel_event(self):
        if self._manager.set_tag() is WindowType.MAIN:
            self._manager.window.mission_moved.emit()
        self.close()

    def set_prize_original(self):
        temp1 = self._manager.get_user().prizes
        temp2 = self._manager.get_user().prizes_cost
        self.prizes_name_holder1.setText(temp1[0])
        self.prizes_name_holder2.setText(temp1[1])
        self.prizes_name_holder3.setText(temp1[2])
        self.prizes_cost_holder1.setText(temp2[0])
        self.prizes_cost_holder2.setText(temp2[1])
        self.prizes_cost_holder3.setText(temp2[2])


class NewMissionMessageBox(Window):
    def __init__(self, manager):
        super(NewMissionMessageBox, self).__init__()
        self.setWindowTitle("Hunter: NewMission")
        self.setFixedSize(300, 400)
        self.center()
        self._manager = manager

        overall_layout = QVBoxLayout()   # Overall > sum
        self.username_tag = Labels(f"Hello {self._manager.get_user().get_nickname()}! \n"
                                   f"Please enter information below.")
        overall_layout.addWidget(self.username_tag)

        sum_layout = QHBoxLayout()  # Overall > sum

        hint = QVBoxLayout()
        mission_name_tag = Labels("Mission Name: ")
        mission_duration_tag = Labels("Mission Duration: ")
        # todo Thinking about using a calender to input the ddl.
        mission_ddl_tag = Labels("Mission Deadline: ")
        mission_importance_tag = Labels("Mission Importance: ")

        hint.addWidget(mission_name_tag)
        hint.addWidget(mission_duration_tag)
        hint.addWidget(mission_ddl_tag)
        hint.addWidget(mission_importance_tag)
        values = QVBoxLayout()
        self.mission_name_holder = InputLine("Mission Name")
        self.mission_duration_holder = NumberComboBox()
        temp = QDate.currentDate().toString(Qt.ISODate)
        temp = temp.replace("-", "")
        print(temp)
        self.mission_ddl_holder = InputLine(temp)
        self.mission_importance_holder = ImportanceComboBox()
        values.addWidget(self.mission_name_holder)
        values.addWidget(self.mission_duration_holder)
        values.addWidget(self.mission_ddl_holder)
        values.addWidget(self.mission_importance_holder)

        sum_layout.addLayout(hint)
        sum_layout.addStretch(1)
        sum_layout.addLayout(values)
        overall_layout.addLayout(sum_layout)

        buttons_layout = QHBoxLayout()
        self.buttons_ok = Buttons("OK", self.ok_event)
        self.buttons_cancel = Buttons("Cancel", self.cancel_event)
        buttons_layout.addWidget(self.buttons_cancel)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.buttons_ok)

        overall_layout.addLayout(buttons_layout)

        self.setLayout(overall_layout)

    def ok_event(self):
        insert_into_database([None,
                              self._manager.get_user().get_username(),
                              self.mission_name_holder.text(),
                              self.mission_ddl_holder.text(),
                              self.mission_duration_holder.currentText(),
                              self.mission_importance_holder.currentValue()],
                             "Mission")
        self.username_tag.setText("Mission is successfully added! \nClose the window now or"
                                  "edit information \nto add another mission")

    def keyPressEvent(self, key):
        if key.key() == Qt.Key_Enter or key.key() == Qt.Key_Return:
            self.ok_event()
            self.cancel_event()

    def cancel_event(self):
        self.close()

    def closeEvent(self, event):
        self._manager.window.mission_moved.emit()


class CountDownWindow(Window):
    completed = pyqtSignal()
    closing = pyqtSignal()

    def __init__(self, mission_name="Mission", unit_time=25):
        super(CountDownWindow, self).__init__()
        self.mission_name = mission_name
        self.label_mission_name = Labels(self.mission_name)
        self.label_mission_name.set_font_size(24)
        self.label_mission_name.setAlignment(Qt.AlignHCenter)
        self.lcd = QLCDNumber()
        self.lcd.setFixedSize(300, 200)
        self.lcd.overflow.connect(self.too_many_time)
        self.lcd.setNumDigits(2)
        self.quit_button = Buttons("Quit")
        self.quit_button.setFixedSize(100, 100)
        self.quit_button.connect_event(self.quit_before_done)
        self.finished_early_button = Buttons("Finished \nEarly")
        self.finished_early_button.connect_event(self.mission_accomplished)
        self.finished_early_button.setFixedSize(100, 100)
        self.finished_message = Labels("Congradulations! Will turn back to the main window in 1 minute.")
        self.finished_message.hide()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.quit_button)
        button_layout.addWidget(self.finished_early_button)

        overall_layout = QVBoxLayout()
        overall_layout.addStretch(6)
        overall_layout.addWidget(self.label_mission_name)
        overall_layout.addStretch(2)
        overall_layout.addWidget(self.lcd)
        overall_layout.addStretch(1)
        overall_layout.addWidget(self.finished_message)
        overall_layout.addStretch(1)
        overall_layout.addLayout(button_layout)
        overall_layout.addStretch(6)
        overall_layout.setAlignment(Qt.AlignHCenter)

        self.setLayout(overall_layout)

        self.timer = CountDownThread(unit_time)
        self.timer.passed_a_minute.connect(self.time_passed)
        self.timer.completed.connect(self.mission_accomplished)
        self.timer.close_valid.connect(self.close_self)
        self.timer.start()

    def time_passed(self, current_time):
        self.lcd.display(current_time)

    def too_many_time(self):
        print("Time set is higher than expected. ")
        self.lcd.display("Err")

    def mission_accomplished(self):
        self.completed.emit()

        self.finished_early_button.setEnabled(False)
        self.finished_message.show()

        self.is_reset = True

        self.timer.quit()

    def close_self(self):
        self.close()
        self.closing.emit()

    def quit_before_done(self):
        self.close()
        self.closing.emit()


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
    def __init__(self, mission=None):
        super(MissionButtons, self).__init__()
        labels = QVBoxLayout()
        self.mission = mission
        if mission is None:
            self.mission_name = Labels("You Are Free! Enjoy! ")
            self.mission_duration = Labels(f"{0} unit time")
            self.mission_ddl = Labels("U R Free")
        else:
            self.mission_name = Labels(mission.mission_name)
            self.mission_duration = Labels(f"{mission.mission_duration} unit time")
            self.mission_ddl = Labels(mission.mission_ddl.toString())

        labels.addWidget(self.mission_name)
        labels.addWidget(self.mission_duration)
        labels.addWidget(self.mission_ddl)
        labels.setAlignment(Qt.AlignHCenter)

        self.setLayout(labels)

    def update_content(self, new_mission):
        if new_mission is None:
            self.mission_name.setText("You Are Free! Enjoy! ")
            self.mission_duration.setText(f"{0} unit time")
            self.mission_ddl.setText("U R Free")
        else:
            self.mission = new_mission
            self.mission_name.setText(new_mission.mission_name)
            self.mission_duration.setText(f"{new_mission.mission_duration} unit time")
            self.mission_ddl.setText(new_mission.mission_ddl.toString())
        self.update()


class StoreButtons(CardsButton):
    consume = pyqtSignal(int)

    def __init__(self, prize_name="prize", prize_cost=1):
        super(StoreButtons, self).__init__()

        labels = QVBoxLayout()
        self.prize_cost_data = prize_cost
        self.prize_name = Labels(prize_name)
        self.prize_cost = Labels(f"Costs: {prize_cost}")
        labels.addWidget(self.prize_name)
        labels.addWidget(self.prize_cost)
        labels.setAlignment(Qt.AlignHCenter)

        self.setLayout(labels)

    def update_prize(self, prize_name="prize", prize_cost=1):
        self.prize_name.set_content(prize_name)
        self.prize_cost.set_content(prize_cost)
        self.prize_cost_data = prize_cost

    def click_event(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Click yes to complete the buying", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.consume.emit(int(self.prize_cost_data))
        else:
            pass


class NewMissionButtons(CardsButton):
    def __init__(self, manager):
        super(NewMissionButtons, self).__init__()
        self._manager = manager
        new_labels = Labels("+")
        new_labels.setStyleSheet("Labels{font-size: 30px; color: white; }")
        layout = QVBoxLayout()
        layout.addWidget(new_labels)
        layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(layout)

    def click_event(self):
        self._manager.slot_new_window_transfer.run()


class RecordedFinishedMission(ListWindow):
    def __init__(self, user):
        self.user = user
        temp = self.read_local_records()
        widgets = list()

        if temp is None:
            self.empty = True
            widgets.append(Labels("Go Do Something at this new day! "))
        else:
            self.empty = False
            for i in range(len(temp)):
                widgets.append(FinishedMissions({"Number": f"{i+1}", "Name": temp[i][0], "Time": temp[i][1]}))
        super(RecordedFinishedMission, self).__init__(widgets)

    def read_local_records(self):
        try:
            file = open(f"records/{QDate.currentDate().toString()}_{self.user}.txt", "r")
        except FileNotFoundError:
            return None
        temp = file.read()
        if temp == "":
            return None
        else:
            temp = temp.split("\n")
            temp.remove("")
            result = list()
            for element in temp:
                result.append(element.split("/"))
            return result


class FinishedMissions(QWidget):
    def __init__(self, information):
        super(FinishedMissions, self).__init__()
        self.number = Labels(information["Number"])
        self.mission_name = Labels(information["Name"])
        self.mission_finished_time = Labels(information["Time"])

        all_layout = QHBoxLayout()
        all_layout.addWidget(self.number)
        all_layout.addWidget(Line(False))
        other_layout = QVBoxLayout()
        other_layout.addWidget(self.mission_name)
        other_layout.addWidget(self.mission_finished_time)
        all_layout.addLayout(other_layout)
        all_layout.setAlignment(Qt.AlignLeft)
        self.setLayout(all_layout)


class CountDownThread(QThread):
    passed_a_minute = pyqtSignal(str)
    completed = pyqtSignal()
    close_valid = pyqtSignal()

    def __init__(self, excepted=25):
        super(CountDownThread, self).__init__()
        self.sum_minutes = excepted

    def run(self):
        for i in range(self.sum_minutes):
            self.passed_a_minute.emit(str(self.sum_minutes - i))
            time.sleep(1)
        self.passed_a_minute.emit(str(0))
        self.completed.emit()
        time.sleep(1)
        self.close_valid.emit()


class User:
    def __init__(self, username="Have not logged in"):
        self.username = username

        # The following information are empty when init.
        # They will be update later.
        self.nick_name = None
        self.unit_time = None
        self.mission_accomplished = None
        self.prizes = None
        self.prizes_cost = None
        self.currency = None
        self.mission = list()

    def get_username(self):
        return self.username

    def pull_information(self):
        temp = search_in_database(self.username, "UserName", "UserInformation")[0]
        self.pull_mission()
        if temp is not None:
            self.username = temp[0]
            self.nick_name = temp[1]
            self.unit_time = temp[2]
            self.mission_accomplished = temp[3]
            if temp[4] and temp[5] is not None:
                self.prizes = temp[4].split(", ")
                self.prizes_cost = temp[5].split(", ")
            else:
                self.prizes = [temp[4]]
                self.prizes_cost = [temp[5]]
            self.currency = temp[6]
            return True
        else:
            return False

    def pull_mission(self):
        temp = search_in_database(self.username, "BelongUserName", "Mission")
        if temp is not None:
            temp_result = list()
            for information in temp:
                temp_result.append(Mission(information))
            self.mission = temp_result
        else:
            self.mission = []

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
        if self.prizes_cost is not None and self.prizes is not None:
            temp1 = ""
            temp2 = ""
            for i in self.prizes:
                temp1 += str(i) + ", "
            for i in self.prizes_cost:
                temp2 += str(i) + ", "
            temp1 = temp1[0:-2]
            temp2 = temp2[0:-2]
            update_existing_in_database(self.username, "UserName",
                                        [str(self.nick_name), str(self.unit_time),
                                         temp1, temp2,
                                         str(self.mission_accomplished), str(self.currency)],
                                        ["UserPreferredName", "UserUnitTime",
                                         "UserPrizeNames", "UserPrizeTimes",
                                         "UserMissionAccomplished", "UserMoney"],
                                        "UserInformation")
        else:
            update_existing_in_database(self.username, "UserName",
                                        [str(self.nick_name), str(self.unit_time),
                                         str(self.mission_accomplished), str(self.currency)],
                                        ["UserPreferredName", "UserUnitTime",
                                         "UserMissionAccomplished", "UserMoney"],
                                        "UserInformation")

    def get_other_information(self, name):
        if name == "NN":  # Nick Name
            return self.nick_name
        elif name == "UT":  # Unit Time
            return self.unit_time
        elif name == "MA":  # Mission Accomplished
            return self.mission_accomplished
        elif name == "CU":  # Currency
            return self.currency
        else:
            raise KeyError("Wrong user 'Name' is given when using 'get_other_information' method! ")

    def get_nickname(self):
        if self.nick_name is not None:
            return self.nick_name
        else:
            return self.get_username()


class Mission:
    def __init__(self, information):
        self.mission_id = information[0]
        self.belong_user = information[1]
        self.mission_name = information[2]
        temp = information[3]
        self.mission_ddl = QDate(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))
        self.mission_duration = information[4]
        self.mission_importance = information[5]

    def value(self):
        delta_date = self.mission_ddl.daysTo(QDate.currentDate())
        if delta_date >= 0:
            delta_date += 1
        duration = self.mission_duration

        # The equation used here could be improved.
        # One way to make it better is to find the user's preference on mission.
        # Besides, it also could be combined with the user data recorded.
        return delta_date * 8 // duration * self.mission_importance

    def __str__(self):
        return f"The mission {self.mission_name} has a deadline on {self.mission_ddl.toString(Qt.ISODate)} and " \
               f"will take you {self.mission_duration} * 25 min to finish it. "

    def __repr__(self):
        return f"{self.mission_name}"


def sha256(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def find_2_smallest(unsorted_list):
    smallest1 = 100000000
    smallest2 = 100000000
    smallest1_index = None
    smallest2_index = None

    for i in range(len(unsorted_list)):
        test = unsorted_list[i]
        if test < smallest1:
            smallest2 = smallest1
            smallest2_index = smallest1_index
            smallest1 = test
            smallest1_index = i
        elif unsorted_list[i] < smallest2:
            smallest2 = test
            smallest2_index = i
    return smallest1_index, smallest2_index


if __name__ == "__main__":
    app = Application()
    print()
