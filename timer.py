import sys
from typing import List
from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtWidgets import QWidget, QApplication, \
    QPushButton, QLabel, QVBoxLayout


class TimerWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.timeText = QLabel("Time left")
        self.labelText = QLabel("Timer section name")
        self.timeText.setStyleSheet("font-size: 20px")
        self.labelText.setStyleSheet("font-size: 18px")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelText)
        self.layout.addWidget(self.timeText)


class Period(object):

    def __init__(self, duration=15, label="test", color="red") -> None:
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
                self.widget.labelText.setText(self.periods[self.position]
                                              .label)
        self.remaining -= 0.2
        if self.isRunning:
            remainStr = '{:02d}m {:02d}s'.format(*divmod(int(self.remaining),
                                                         60))
            self.widget.timeText.setText(remainStr)
            QTimer.singleShot(200, self.runTimer)
        else:
            print("paused")


class ControlWidget(QWidget):

    def __init__(self, timer: Timer) -> None:
        super().__init__()
        self.timer = timer
        self.button = QPushButton("Start Timer")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.timer.widget)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.button.clicked.connect(self.start)
        self.timer.widget.show()
        self.button.show()

    @Slot()
    def start(self):
        if not self.timer.isRunning:
            self.timer.isRunning = True
            self.timer.runTimer()
            self.button.setText("Pause timer")
        else:
            self.timer.isRunning = False
            self.button.setText("Start Timer")


def buildTestTimerWidget() -> ControlWidget:
    test_timer = Timer()
    test_timer.addInterval(Period(10, "clap your hands", "red"))
    test_timer.addInterval(Period(12, "shout", "blue"))
    test_timer.addInterval(Period(8, "say hi", "purple"))
    countdown = TimerWidget()
    test_timer.widget = countdown
    wrapper = ControlWidget(test_timer)
    return wrapper


def main():
    app = QApplication(sys.argv)
    test = buildTestTimerWidget()
    test.resize(300, 100)
    test.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# http://john.maloney.org/Programming/pythontimer.htm
