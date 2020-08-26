from main_window.utils import PATH_IMAGE_BACK_NEDDLE

from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence, QIcon
import json


class Settings(QWidget):

    SETTINGS = 2
    TRANSLATED = 'translated'
    VALUE = 'value'
    SETTINGS_PATH = 'main_window/menu/settings/game_settings.json'

    def __init__(self, signal_controller):
        super().__init__()
        self.signal_controller = signal_controller

        self.__create_default_settings()
        self.initUI()
    
    def initUI(self):
        """
        Init widget

        """
        grid = QGridLayout()
        hbox = QHBoxLayout()
        hbox.addSpacing(2)

        self._button_back = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._button_back.clicked.connect(self.signal_controller.back_to_menu)
        hbox.addWidget(self._button_back, 0, QtCore.Qt.AlignLeft)

        self.label = QLabel("Settings")
        hbox.addWidget(self.label, 1, QtCore.Qt.AlignCenter)

        grid.addLayout(hbox, 0, 0, QtCore.Qt.AlignTop)

        json_data_settings = self.get_settings(None)

        # TODO: Possibility to change settings via this widget
        #self._labels_settings = []

        counter = 1

        for name in json_data_settings:
            single = json_data_settings[name]

            translated = single[self.TRANSLATED]
            value = single[self.VALUE]

            new_label = QLabel(name.replace('_', ' '))
            if translated:
                second_label = QLabel(QKeySequence(value).toString())
            else:
                second_label = QLabel(str(value))

            grid.addWidget(new_label, counter, 0, QtCore.Qt.AlignLeft)
            grid.addWidget(second_label, counter, 1, QtCore.Qt.AlignRight)

            counter += 1

        self.setLayout(grid)
        self.setWindowTitle("Game settings")
    
    def switcher(self):
        """
        Emit signal that menu should be switched to SETTINGS widget

        """
        self.signal_controller.sgn2stacked.emit(int(self.SETTINGS))

    def get_settings(self, key):
        """
        Get settings by key,
        If key is equal to None, all settings will be returned

        """
        with open(self.SETTINGS_PATH, "r") as rf:
            data = json.load(rf)
        if key is None:
            return data

        return data[key][self.VALUE]

    def __create_default_settings(self):
        """
        Create default settings

        """
        dict_data = {}

        dict_data.update({"window_size": {
            self.VALUE: [250, 380],
            self.TRANSLATED: False
            }
        })
        dict_data.update({"board_size": {
            self.VALUE: [10, 22],
            self.TRANSLATED: False
            }
        })

        dict_data.update({"board_speed": {
            self.VALUE: 100,
            self.TRANSLATED: False
            }
        })

        dict_data.update({"rotate_left": {
            self.VALUE: int(Qt.Key_Down),
            self.TRANSLATED: True
            }
        })

        dict_data.update({"rotate_right": {
            self.VALUE: int(Qt.Key_Up),
            self.TRANSLATED: True
            }
        })

        dict_data.update({"move_left": {
            self.VALUE: int(Qt.Key_Left),
            self.TRANSLATED: True
            }
        })

        dict_data.update({"move_right": {
            self.VALUE: int(Qt.Key_Right),
            self.TRANSLATED: True
            }
        })

        dict_data.update({"down": {
            self.VALUE: int(Qt.Key_Space),
            self.TRANSLATED: True
            }
        })

        dict_data.update({"game_pause": {
            self.VALUE: int(Qt.Key_P),
            self.TRANSLATED: True
            }
        })

        with open(self.SETTINGS_PATH, 'w') as rf:
            json.dump(dict_data, rf)

