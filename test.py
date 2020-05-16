import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()

        # Uncomment if you want to change the language
        # self.setLocale(QtCore.QLocale(QtCore.QLocale.Spanish, QtCore.QLocale.Peru))
        self.verticalLayout = QVBoxLayout(self)
        self.dateEdit = QDateEdit(self)
        self.dateEdit.setDisplayFormat("MMM dd yyyy")
        self.verticalLayout.addWidget(self.dateEdit)
        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setDisplayFormat("hh:mm:ss AP")
        self.verticalLayout.addWidget(self.timeEdit)
        self.updateTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def updateTime(self):
        current = QtCore.QDateTime.currentDateTime()
        self.dateEdit.setDate(current.date())
        self.timeEdit.setTime(current.time())


def main():
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()