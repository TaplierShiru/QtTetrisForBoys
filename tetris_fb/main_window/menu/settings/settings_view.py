from tetris_fb.main_window.utils import PATH_IMAGE_BACK_NEDDLE

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QIcon
import json


class SettingsView(QWidget):

    SETTINGS = 2
    TRANSLATED = 'translated'
    VALUE = 'value'
    SETTINGS_PATH = 'main_window/menu/settings/game_settings.json'
    DEFAULT_SETTINGS_PATH = 'main_window/menu/settings/default_game_settings.json'

    def __init__(self, signalController):
        super().__init__()
        self.signalController = signalController

        self.__create_default_settings(self.DEFAULT_SETTINGS_PATH)
        self.initUI()
    
    def initUI(self):
        """
        Init widget

        """
        grid = QGridLayout()
        hbox = QHBoxLayout()
        hbox.addSpacing(2)

        self._buttonBack = QPushButton(QIcon(PATH_IMAGE_BACK_NEDDLE), "", self)
        self._buttonBack.clicked.connect(self.signalController.back2menu)
        hbox.addWidget(self._buttonBack, 0, QtCore.Qt.AlignLeft)

        self.label = QLabel("SettingsView")
        hbox.addWidget(self.label, 1, QtCore.Qt.AlignCenter)

        grid.addLayout(hbox, 0, 0, QtCore.Qt.AlignTop)

        jsonDataSettings = self.get_settings(None)

        # TODO: Possibility to change settings via this widget
        #self._labels_settings = []

        counter = 1

        for name in jsonDataSettings:
            single = jsonDataSettings[name]

            translated = single[self.TRANSLATED]
            value = single[self.VALUE]

            newLabel = QLabel(name.replace('_', ' '))
            if translated:
                secondLabel = QLabel(QKeySequence(value).toString())
            else:
                secondLabel = QLabel(str(value))

            grid.addWidget(newLabel, counter, 0, QtCore.Qt.AlignLeft)
            grid.addWidget(secondLabel, counter, 1, QtCore.Qt.AlignRight)

            counter += 1

        self.setLayout(grid)
        self.setWindowTitle("Game settings")
    
    def switcher(self):
        """
        Emit signal that menu should be switched to SETTINGS widget

        """
        self.signalController.sgn2stacked.emit(int(self.SETTINGS))

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

    def __create_default_settings(self, pathSave: str):
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

        with open(pathSave, 'w') as rf:
            json.dump(dict_data, rf)

