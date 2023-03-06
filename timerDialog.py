from PySide6.QtWidgets import QLineEdit, QPushButton, \
    QVBoxLayout, QGridLayout, QWidget, QLabel
from timer import Period
from PySide6.QtGui import QColor
from PySide6.QtCore import Slot, Signal, QSize
from typing import List
import sys

COLOR_OPTIONS = ['#05878a', '#074e67', '#5a175d', '#67074e',
                 '#1c222e', '#41533b', '#006666', '#493267',
                 '#cc0101', '#940000', '#e37448', '#5167a3']

class _ColorButton(QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(28, 28))
        self.color = color
        self.setStyleSheet('background-color: {hex};'.format(hex = color))


class _ColorWrapper(QWidget):

    selected = Signal(object)

    def _emit_color(self, color):
        self.selected.emit(color)

class _ColorGrid(_ColorWrapper):

    def __init__(self) -> None:
        super().__init__()
        palette = QGridLayout()
        row, col = 0, 0

        for c in COLOR_OPTIONS:
            btn = _ColorButton(c)
            btn.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(btn, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
        self.setLayout(palette)

class TimerDialog(QWidget):
    sendTimer = Signal(type(List[Period]))

    def __init__(self) -> None:
        super().__init__()
        self.labelText = QLabel("Enter label: ")
        self.labelBox = QLineEdit()
        self.timeText = QLabel("Enter time: ")
        self.timeBox = QLineEdit()
        self.addIntervalButton = QPushButton("Add time interval")
        self.submitButton = QPushButton("Add Timer")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelText)
        self.layout.addWidget(self.labelBox)
        self.layout.addWidget(self.timeText)
        self.layout.addWidget(self.timeBox)
        self.colorGrid = _ColorGrid()
        self.layout.addWidget(self.colorGrid)
        self.layout.addWidget(self.addIntervalButton)
        self.layout.addWidget(self.submitButton)
        self.colorGrid.selected.connect(self.changeColor)
        self.submitButton.clicked.connect(self.submitTimer)
        self.addIntervalButton.clicked.connect(self.addInterval)
        self.currentColor = '#05878a'
        self.intervals = []


    @Slot()
    def changeColor(self, color):
        self.currentColor = color

    @Slot()
    def submitTimer(self) -> None:
        self.sendTimer.emit(self.intervals)
        self.hide()

    @Slot()
    def addInterval(self) -> None:
        t = int(self.timeBox.text())
        s = self.labelBox.text()
        self.intervals.append(Period(t, s, QColor(self.currentColor)))
        print(self.intervals)
