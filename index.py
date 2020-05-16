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

    # def DB_Connect(self):
    #     self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='toor', db='crypto')
    #     self.cur = self.db.cursor()
    #     print("conection accepted")

    def Handel_Button(self):

        ##########################################################
        ''' OPEN FILES DIALOG'''
        ##########################################################
        ''' SET IMAGES TO UI'''
        # self.label_9.setPixmap(QtGui.QPixmap('lock1.png'))

##########################################################################################################
##########################################################################################################
##########################################################################################################
    #############################
    '''GET USER CHOICES FILES '''
    ############################


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
