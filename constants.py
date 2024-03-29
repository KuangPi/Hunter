#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from enum import Enum


class WindowType(Enum):
    INIT = 0  # Also used for the situation when changing window.
    LOGIN = 1
    MAIN = 2
    LOCK = 3
    SELECT = 4
    CD = 5


class Importance(Enum):
    IMMEDIATELY = -1
    EARLY = 1
    NORMAL = 2
    LATER = 4
    ANY_TIME = 10

