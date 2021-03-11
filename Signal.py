#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from PyQt5 import QtCore


class ChangeSignalMainScreen(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeSignalMainScreen, self).__init__()

    def run(self):
        self.signal.emit()


class ChangeSignalSideScreen(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeSignalSideScreen, self).__init__()

    def run(self):
        self.signal.emit()


class ChangeSignalSettingScreen(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeSignalSettingScreen, self).__init__()

    def run(self):
        self.signal.emit()


class ChangeSignalNewMissionScreen(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeSignalNewMissionScreen, self).__init__()

    def run(self):
        self.signal.emit()


class CloseSignalMainScreen(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(CloseSignalMainScreen, self).__init__()

    def run(self):
        self.signal.emit()
