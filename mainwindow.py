import sys
from timer import Timer, TimerWidget, Period, ControlWidget
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    test_timer = Timer()
    test_timer.addInterval(Period(90, "jump up and down"))
    countdown = TimerWidget()
    test_timer.widget = countdown
    wrapper = ControlWidget(test_timer)
    wrapper.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
