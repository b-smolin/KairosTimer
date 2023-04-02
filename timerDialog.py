from PySide6.QtWidgets import QLineEdit, QPushButton, \
    QVBoxLayout, QGridLayout, QWidget, QLabel, QCheckBox, \
    QHBoxLayout
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
        self.setStyleSheet('background-color: {hex};'.format(hex=color))


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


class TimeEntryWidget(QWidget):

    def __init__(self, text):
        super().__init__()
        self.layout = QGridLayout(self)
        self.upTen = QPushButton("Add 10")
        self.upTen.setMaximumWidth(50)
        self.upOne = QPushButton("Add 1")
        self.upOne.setMaximumWidth(50)
        self.entryBox = QLineEdit("0")
        self.label = QLabel(text)
        self.downTen = QPushButton("Down 10")
        self.downTen.setMaximumWidth(50)
        self.downOne = QPushButton("Down 1")
        self.downOne.setMaximumWidth(50)
        self.value = 0
        self.upTen.clicked.connect(self.addTen)
        self.upOne.clicked.connect(self.addOne)
        self.downTen.clicked.connect(self.subTen)
        self.downOne.clicked.connect(self.subOne)
        self.layout.addWidget(self.upTen, 0, 0)
        self.layout.addWidget(self.upOne, 0, 1)
        self.layout.addWidget(self.entryBox, 1, 0, 1, 2)
        self.layout.addWidget(self.label, 1, 2)
        self.layout.addWidget(self.downTen, 2, 0)
        self.layout.addWidget(self.downOne, 2, 1)

    def addTen(self):
        self.value += 10
        self.entryBox.setText(str(self.value))
    
    def addOne(self):
        self.value += 1
        self.entryBox.setText(str(self.value))
    
    def subTen(self):
        self.value = 0 if self.value < 10 else self.value - 10
        self.entryBox.setText(str(self.value))
    
    def subOne(self):
        self.value = 0 if self.value <= 1 else self.value - 1
        self.entryBox.setText(str(self.value))
    
    def getValue(self):
        t = self.value
        self.value = 0
        self.entryBox.setText(str(self.value))
        return t

class TimerDialog(QWidget):
    sendTimer = Signal(type(List[Period]), bool)

    def __init__(self) -> None:
        super().__init__()
        self.labelText = QLabel("Enter label: ")
        self.labelBox = QLineEdit()
        self.timeText = QLabel("Enter time: ")
        self.addIntervalButton = QPushButton("Add time interval")
        self.submitButton = QPushButton("Add Timer")
        self.runOnSubmit = QCheckBox("Run on start?")
        self.entryArea = QHBoxLayout()
        self.secEntry = TimeEntryWidget("s")
        self.minEntry = TimeEntryWidget("m")
        self.hourEntry = TimeEntryWidget("h")
        self.entryArea.addWidget(self.hourEntry)
        self.entryArea.addWidget(self.minEntry)
        self.entryArea.addWidget(self.secEntry)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelText)
        self.layout.addWidget(self.labelBox)
        self.layout.addWidget(self.timeText)
        self.layout.addLayout(self.entryArea)
        self.colorGrid = _ColorGrid()
        self.layout.addWidget(self.colorGrid)
        self.layout.addWidget(self.runOnSubmit)
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
        self.sendTimer.emit(self.intervals, self.runOnSubmit.isChecked())
        self.hide()

    @Slot()
    def addInterval(self) -> None:
        t = self.secEntry.getValue() + (60 * self.minEntry.getValue()) + (3600 * self.hourEntry.getValue())
        s = self.labelBox.text()
        self.intervals.append(Period(t, s, QColor(self.currentColor)))
        print(self.intervals)
