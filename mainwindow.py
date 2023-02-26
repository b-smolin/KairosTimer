import sys
# from timer import Timer, Period
from timerBox import TimerBox
from timerDialog import TimerDialog
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.timerWindow = TimerBox()
        self.newTimerButton = QPushButton("New Timer")
        self.loadTimerButton = QPushButton("Load Timer")
        self.newTimerButton.clicked.connect(self.newTimerDialog)
        self.layout.addWidget(self.newTimerButton)
        self.layout.addWidget(self.loadTimerButton)
        self.layout.addWidget(self.timerWindow)
        self.setWindowTitle("Kairos Timer")
        self.newTimerButton.show()
        self.loadTimerButton.show()
        self.timerWindow.show()
        self.timerDialog = None

    @Slot()
    def newTimerDialog(self, s):
        self.timerDialog = TimerDialog()
        self.timerDialog.sendTimer.connect(self.timerWindow.createTimer)
        print("clicked", s)
        self.timerDialog.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
