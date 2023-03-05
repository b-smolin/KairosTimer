from typing import List
from timer import Timer, Period
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class TimerBox(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.emptyTitle = QLabel("No timers running." +
                                 "Use the buttons up top to start one")
        self.layout.addWidget(self.emptyTitle)
        self.timer = None

    @Slot()
    def createTimer(self, intervals: List[Period]):
        print("time")
        self.timer = Timer(intervals, False)
        self.layout.addWidget(self.timer)
        self.timer.show()
