
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUiType
import mysql.connector
from mysql.connector import Error
from PyQt5.QtGui import QIntValidator


login, _ = loadUiType('login.ui')
MainUI , _ = loadUiType('main.ui')


class login(QMainWindow, login):
    def __init__(self, parent=None):
        super(login, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handel_login)
        self.window2 = None

    def handel_login(self):
        # self.connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=.\SQLEXPRESS;DATABASE=Cars_DB;')
        # self.cursor = self.connection.cursor()
        # sql = "SELECT User_Name , Password FROM tbl_Users"
        # for row in self.cursor.execute(sql):
        #
        #     if row[0] == self.lineEdit.text() and row[1] == self.lineEdit_2.text() :
        #         user_profile.append(self.lineEdit.text())
        #         user_profile.append(self.lineEdit_2.text())
        #         print(user_profile)
        self.window2 = Main(self)
        self.close()
        self.window2.setWindowTitle('Hotel App')
        self.window2.setWindowIcon(QIcon('icon.png'))
        self.window2.setFixedSize(1221, 791)
        self.window2.show()



        # else:
        #     print('error')
        #     self.label_3.setText("حدث خطأ.. يرجي التأكد من اسم المستخدم وكلمة المرور الخاصة بك ")



class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.Handel_Button()
        self.Ui_Changes()
        self.updateTime()
        self.int_vaildator()
        self.get_room_numbers()


#############################################
    def Ui_Changes(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_2.tabBar().setVisible(False)
        self.radioButton.setChecked(True)
        table1 = self.tableWidget.horizontalHeader()
        table2 = self.tableWidget_2.horizontalHeader()
        table3 = self.tableWidget_3.horizontalHeader()
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


    def DB_Connect(self):
        try:
            self.db= mysql.connector.connect(host='localhost',
                                                 database='hotel',
                                                 user='root',
                                                 password='toor')
            self.cur = self.db.cursor()
            self.statusBar().showMessage('Database Connected Successfully')
        except Error as e:
            self.statusBar().showMessage('Failed To Connect To Database')


    def Handel_Button(self):
        ##########################################################
        ''' Room Mangement'''
        self.radioButton.toggled.connect(self.add_new_room)
        self.radioButton_2.toggled.connect(self.edit_room)
        self.pushButton_51.clicked.connect(self.save_new_room)
        self.pushButton_52.clicked.connect(self.save_edited_room)



        ##########################################################
        ''' OPEN Tabs'''
        self.pushButton.clicked.connect(self.open_check_in)
        self.pushButton_3.clicked.connect(self.open_check_out)
        self.pushButton_6.clicked.connect(self.open_free_rooms)
        self.pushButton_7.clicked.connect(self.open_current_guest)
        self.pushButton_12.clicked.connect(self.open_today)
        self.pushButton_18.clicked.connect(self.open_update_reserve)
        self.pushButton_4.clicked.connect(self.open_add_update_room)
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


        ##########################################################
        ''' Room Mangement'''
    def int_vaildator (self) :
        validator = QIntValidator(0, 10000, self)
        self.lineEdit_27.setValidator(validator)
        self.lineEdit_28.setValidator(validator)
        self.lineEdit_34.setValidator(validator)

    def add_new_room(self):
        new_room = self.sender()
        if new_room.isChecked() :
            self.tabWidget_2.setCurrentIndex(0)
    def edit_room(self):
        edit_room = self.sender()
        if edit_room.isChecked() :
            self.tabWidget_2.setCurrentIndex(1)
            self.comboBox_4.currentIndexChanged.connect(self.retrive_room_data)

    def save_new_room(self):
        try:
            room_number = self.lineEdit_27.text()
            room_type = self.comboBox_3.currentText()
            room_price = self.lineEdit_28.text()
            hotel_id = self.lineEdit_34.text()

            if  room_number!=""  and room_price != "" and hotel_id != "":
                self.cur.execute('''INSERT INTO rooms (room_number , Room_type , room_price , hotel_id) VALUES  ( %s ,%s,%s,%s)''',(room_number , room_type , room_price , hotel_id))
                self.db.commit()
                self.statusBar().showMessage('Room Add Successfully' )
                self.get_room_numbers()
                self.lineEdit_27.clear()
                self.lineEdit_28.clear()
                self.lineEdit_34.clear()
            else :
                self.statusBar().showMessage('Enter All Data' )
        except Exception as m :
            print(m)

    def retrive_room_data(self):
        try :
            room_number = self.comboBox_4.currentText()
            self.cur.execute('''SELECT Room_type , room_price , hotel_id FROM rooms WHERE room_number = %s ''' , (room_number,))
            room_data = self.cur.fetchone()
            if room_data[0] == "Delux" :
                self.comboBox_5.setCurrentIndex(0)
            elif room_data[0] == "Full Deulx" :
                self.comboBox_5.setCurrentIndex(1)
            elif room_data[0] == "Genral" :
                self.comboBox_5.setCurrentIndex(2)
            elif room_data[0] == "Joint" :
                self.comboBox_5.setCurrentIndex(3)
            self.lineEdit_30.setEnabled(True)
            self.lineEdit_33.setEnabled(True)
            self.lineEdit_30.setText(str(room_data[1]))
            self.lineEdit_33.setText(str(room_data[2]))

        except Exception as m :
            print(m)
    def save_edited_room(self):
        try:
            room_number = self.comboBox_4.currentText()
            room_type = self.comboBox_5.currentText()
            room_price = self.lineEdit_30.text()
            hotel_id = self.lineEdit_33.text()
            self.cur.execute('''UPDATE rooms set Room_type = %s , room_price = %s , hotel_id = %s WHERE room_number = %s''',( room_type , room_price , hotel_id , room_number))
            self.db.commit()
            self.statusBar().showMessage('Room Updated Successfully' )
            self.lineEdit_30.clear()
            self.lineEdit_33.clear()
        except Exception as m :
            print(m)
##########################################################################################################
##########################################################################################################
    '''Get_room_numbers'''
    def get_room_numbers(self):
        try :
            self.comboBox_4.clear()
            self.cur.execute('''SELECT room_number FROM rooms''')
            room_numbers = self.cur.fetchall()
            for room in room_numbers :
                self.comboBox_4.addItem(str(room[0]))
        except Exception as m :
            print(m)
##########################################################################################################
    #############################
    '''Open Tabs '''
    ############################
    def open_check_in(self):
        self.tabWidget.setCurrentIndex(1)
        self.statusBar().showMessage('')
    def open_check_out(self):
        self.tabWidget.setCurrentIndex(2)
        self.statusBar().showMessage('')
    def open_free_rooms(self):
        self.tabWidget.setCurrentIndex(3)
        self.statusBar().showMessage('')
    def open_current_guest(self):
        self.tabWidget.setCurrentIndex(4)
        self.statusBar().showMessage('')
    def open_today(self):
        self.tabWidget.setCurrentIndex(5)
        self.statusBar().showMessage('')
    def open_update_reserve(self):
        self.tabWidget.setCurrentIndex(6)
        self.statusBar().showMessage('')
    def back_to_home(self):
        self.tabWidget.setCurrentIndex(0)
        self.statusBar().showMessage('')
    def open_add_update_room(self):
        self.tabWidget.setCurrentIndex(7)
        self.statusBar().showMessage('')

##########################################################################################################
#############################
        '''Current Time '''
        ############################

    def updateTime(self):
        try :
            current = QDateTime.currentDateTime()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateTime)
            self.timer.start(1000)
            self.dateTimeEdit.setDisplayFormat("dd MM yyyy hh:mm:ss AP")
            # self.timeEdit.setDisplayFormat("hh:mm:ss AP")
            self.dateTimeEdit.setDateTime(current.currentDateTime())
        except Exception as m :
            print(m)

#######################################################
'''App Exicution'''


def main():
    app = QApplication(sys.argv)
    window = login()
    window.setWindowTitle('Hotel App')
    window.setWindowIcon(QIcon('icon.png'))
    window.setFixedSize(605, 360)
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
