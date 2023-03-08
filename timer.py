from doctest import FAIL_FAST
import sys
from typing import List
from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtWidgets import QWidget, QApplication, \
    QPushButton, QLabel, QHBoxLayout


class Period(object):

    def __init__(self, duration=15, label="test", color=QColor(0, 125, 255)) -> None:
        self.label = label
        self.duration = duration
        self.color = color

    def __str__(self) -> str:
        return (str(self.label) + " " +
                str(self.duration) + " " +
                str(self.color))


class Timer(QWidget):

    def __init__(self, periods: List[Period] = [], isRunning: bool = False) -> None:
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.palette = QPalette()
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        self.timeText = QLabel("")
        self.labelText = QLabel("")
        self.timeText.setFont(QFont("Bahnschrift", 18, QFont.Bold))
        self.labelText.setFont(QFont("Bahnschrift", 18, QFont.Bold))
        self.button = QPushButton("Start Timer")
        self.button.clicked.connect(self.press)
        self.layout.addWidget(self.labelText)
        self.layout.addWidget(self.timeText)
        self.layout.addWidget(self.button)
        self.periods = periods
        self.isRunning = isRunning
        self.remaining = -1
        self.position = -1
        if isRunning:
            self.runTimer()

    def render(self) -> None:
        self.timeText.show()
        self.labelText.show()
        self.button.show()

    @Slot()
    def press(self) -> None:
        if not self.isRunning:
            self.isRunning = True
            self.runTimer()
            self.button.setText("Pause Timer")
        else:
            self.isRunning = False
            self.button.setText("Run timer")

    def __str__(self) -> str:
        fin = ""
        for word in self.periods:
            fin += str(word)
            fin += " : "
        return fin

    def addInterval(self, interval: Period) -> None:
        self.periods.append(interval)

    def runTimer(self) -> None:
        if len(self.periods) == 0:
            return
            # should probably exception handle this
        if self.remaining <= 0.05:
            self.position += 1
            # timer is over at this point, should handle in special case
            if self.position >= len(self.periods):
                return
            else:
                self.remaining = self.periods[self.position].duration
                self.labelText.setText(self.periods[self.position].label)
                self.palette.setColor(
                    QPalette.Window, self.periods[self.position].color)
                self.palette.setColor(QPalette.WindowText, Qt.white)
                self.setPalette(self.palette)
        self.remaining -= 0.2
        if self.isRunning:
            remainStr = '{:02d}m {:02d}s'.format(*divmod(int(self.remaining),
                                                         60))
            self.timeText.setText(remainStr)
            QTimer.singleShot(200, self.runTimer)
        else:
            print("paused")


def buildTestTimerWidget() -> Timer:
    test = Timer()
    test.addInterval(Period())
    test.addInterval(Period(5, "fee fi fo fum"))
    return test


def main():
    app = QApplication(sys.argv)
    test = buildTestTimerWidget()
    test.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# http://john.maloney.org/Programming/pythontimer.htm
