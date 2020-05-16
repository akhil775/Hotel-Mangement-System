import getpass
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os.path
import time
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
# from main import Ui_MainWindow
from PyQt5.uic import loadUiType


MainUI , _ = loadUiType('main.ui')




class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.DB_Connect()
        self.Handel_Button()
        self.Ui_Changes()

#############################
    def Ui_Changes(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_2.tabBar().setVisible(False)
        table1 = self.tableWidget.horizontalHeader()
        table2 = self.tableWidget_2.horizontalHeader()
        table3 = self.tableWidget_2.horizontalHeader()
        table1.setSectionResizeMode(0, QHeaderView.Stretch)
        table1.setSectionResizeMode(1, QHeaderView.Stretch)
        table1.setSectionResizeMode(2, QHeaderView.Stretch)
        table1.setSectionResizeMode(3, QHeaderView.Stretch)
        table1.setSectionResizeMode(4, QHeaderView.Stretch)
        table2.setSectionResizeMode(2, QHeaderView.Stretch)
        table2.setSectionResizeMode(3, QHeaderView.Stretch)
        table2.setSectionResizeMode(4, QHeaderView.Stretch)
        table3.setSectionResizeMode(2, QHeaderView.Stretch)
        table3.setSectionResizeMode(3, QHeaderView.Stretch)
        table3.setSectionResizeMode(4, QHeaderView.Stretch)
        self.groupBox.hide()


    # def DB_Connect(self):
    #     self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='toor', db='crypto')
    #     self.cur = self.db.cursor()
    #     print("conection accepted")

    def Handel_Button(self):
        ##########################################################
        ''' OPEN Tabs'''
        self.pushButton.clicked.connect(self.open_check_in)
        self.pushButton_3.clicked.connect(self.open_check_out)
        self.pushButton_6.clicked.connect(self.open_free_rooms)
        self.pushButton_7.clicked.connect(self.open_current_guest)
        self.pushButton_12.clicked.connect(self.open_today)
        self.pushButton_18.clicked.connect(self.open_update_reserve)
        ##########################################################
        ''' Back to Home'''
        self.pushButton_53.clicked.connect(self.back_to_home)
        self.pushButton_54.clicked.connect(self.back_to_home)
        self.pushButton_55.clicked.connect(self.back_to_home)
        self.pushButton_56.clicked.connect(self.back_to_home)
        self.pushButton_57.clicked.connect(self.back_to_home)
        self.pushButton_58.clicked.connect(self.back_to_home)
        self.pushButton_59.clicked.connect(self.back_to_home)

        ##########################################################
        ''' SET IMAGES TO UI'''
        # self.label_9.setPixmap(QtGui.QPixmap('lock1.png'))

##########################################################################################################
##########################################################################################################
##########################################################################################################
    #############################
    '''Open Tabs '''
    ############################
    def open_check_in(self):
        self.tabWidget.setCurrentIndex(1)
    def open_check_out(self):
        self.tabWidget.setCurrentIndex(2)
    def open_free_rooms(self):
        self.tabWidget.setCurrentIndex(3)
    def open_current_guest(self):
        self.tabWidget.setCurrentIndex(4)
    def open_today(self):
        self.tabWidget.setCurrentIndex(5)
    def open_update_reserve(self):
        self.tabWidget.setCurrentIndex(6)
    def back_to_home(self):
        self.tabWidget.setCurrentIndex(0)



#######################################################
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle('Ecryption App')
    window.setWindowIcon(QIcon('lock1.png'))
    window.setFixedSize(1221,791)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
