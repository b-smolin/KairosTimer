import sys
from typing import List
from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QWidget, QApplication, \
    QPushButton, QLabel, QVBoxLayout


class TimerWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.text = QLabel("")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)


class Period(object):

    def __init__(self, duration=15, color="red", label="test") -> None:
        self.label = label
        self.duration = duration
        self.color = color

    def __str__(self) -> str:
        return (str(self.label) + " " +
                str(self.duration) + " " +
                str(self.color))


class Timer(object):

    def __init__(self, widget: TimerWidget = None,
                 periods: List[Period] = None, isRunning=None,
                 remaining=None, position=None) -> None:
        self.periods = []
        self.isRunning = False
        self.remaining = -1
        self.position = -1
        self.widget = widget

    def __str__(self) -> str:
        fin = ""
        for word in self.periods:
            fin += str(word)
            fin += " : "
        return fin

    def addInterval(self, interval: Period) -> None:
        self.periods.append(interval)

    def runTimer(self) -> None:
        # should disable the button in this case, should timer exist
        # at this point?
        if len(self.periods) == 0:
            return
        if self.remaining <= 0.05:
            self.position += 1
            # timer is over at this point, should handle in special case
            if self.position >= len(self.periods):
                return
            else:
                self.remaining = self.periods[self.position].duration
        self.remaining -= 0.2
        print(self.remaining)
        if self.isRunning:
            self.widget.text.setText(str(self.remaining))
            QTimer.singleShot(200, self.runTimer)
        else:
            print("paused")


class ControlWidget(QWidget):

    def __init__(self, timer: Timer) -> None:
        super().__init__()
        self.timer = timer
        self.button = QPushButton("Start Timer")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.timer.widget)
        self.button.clicked.connect(self.start)
        self.button.show()
        self.timer.widget.show()

    @Slot()
    def start(self):
        if not self.timer.isRunning:
            self.timer.isRunning = True
            self.timer.runTimer()
            self.button.setText("Pause timer")
        else:
            self.timer.isRunning = False
            self.button.setText("Start Timer")


def buildTestWidget() -> ControlWidget:
    test_timer = Timer()
    test_timer.addInterval(Period(10))
    test_timer.addInterval(Period(12))
    test_timer.addInterval(Period(8))
    countdown = TimerWidget()
    test_timer.widget = countdown
    wrapper = ControlWidget(test_timer)
    return wrapper


def main():
    app = QApplication(sys.argv)
    test = buildTestWidget()
    test.resize(300, 300)
    test.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# http://john.maloney.org/Programming/pythontimer.htm
