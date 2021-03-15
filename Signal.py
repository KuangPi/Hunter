#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from PyQt5 import QtCore


class SignalObjects(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super(SignalObjects, self).__init__()

    def run(self):
        self.signal.emit()


class ChangeSignalMainScreen(SignalObjects):
    def __init__(self):
        super(ChangeSignalMainScreen, self).__init__()


class ChangeSignalSideScreen(SignalObjects):
    def __init__(self):
        super(ChangeSignalSideScreen, self).__init__()


class ChangeSignalSettingScreen(SignalObjects):
    def __init__(self):
        super(ChangeSignalSettingScreen, self).__init__()


class ChangeSignalNewMissionScreen(SignalObjects):
    def __init__(self):
        super(ChangeSignalNewMissionScreen, self).__init__()


class ChangeSignalCountDownScreen(SignalObjects):
    def __init__(self):
        super(ChangeSignalCountDownScreen, self).__init__()


class CloseSignalMainScreen(SignalObjects):
    def __init__(self):
        super(CloseSignalMainScreen, self).__init__()
