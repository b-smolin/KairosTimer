from PySide6.QtWidgets import QLineEdit, QPushButton, \
    QVBoxLayout, QDialog, QWidget, QLabel
from timer import Period
from PySide6.QtCore import Slot, Signal
from typing import List


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
        self.layout.addWidget(self.addIntervalButton)
        self.layout.addWidget(self.submitButton)
        self.submitButton.clicked.connect(self.submitTimer)
        self.addIntervalButton.clicked.connect(self.addInterval)
        self.intervals = []

    @Slot()
    def submitTimer(self) -> None:
        tst = self.intervals
        self.sendTimer.emit(tst)

    @Slot()
    def addInterval(self) -> None:
        t = int(self.timeBox.text())
        s = self.labelBox.text()
        self.intervals.append(Period(t, s))
        print(self.intervals)
