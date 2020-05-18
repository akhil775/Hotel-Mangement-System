
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import datetime
from datetime import timedelta
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
        self.int_vaildator()
        self.get_room_numbers()
        self.to_day_and_tomorow()
        self.show_free_and_reserved_rooms()
        self.retrive_history_data()
#

#############################################
    def Ui_Changes(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_2.tabBar().setVisible(False)
        self.radioButton.setChecked(True)
        self.radioButton_8.setChecked(True)
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
            self.cur = self.db.cursor(buffered=True)
            self.statusBar().showMessage('Database Connected Successfully')
        except Error as e:
            self.statusBar().showMessage('Failed To Connect To Database')


    def Handel_Button(self):
        ##########################################################
        ''' Room Mangement'''
        self.radioButton.toggled.connect(self.add_new_room)
        self.radioButton_2.toggled.connect(self.edit_room)
        self.radioButton_3.toggled.connect(self.get_free_room_numbers)
        self.radioButton_5.toggled.connect(self.get_free_room_numbers)
        self.radioButton_4.toggled.connect(self.get_free_room_numbers)
        self.radioButton_6.toggled.connect(self.get_free_room_numbers)
        self.comboBox_2.activated.connect(self.get_room_price)
        self.pushButton_51.clicked.connect(self.save_new_room)
        self.pushButton_52.clicked.connect(self.save_edited_room)
        ##########################################################
        ''' Check in Mangement'''
        self.pushButton_25.clicked.connect(self.handel_check_in)
        self.spinBox.valueChanged.connect(self.count_date_to_cuurent)
        self.lineEdit_3.textChanged.connect(self.validate_phone_number)
        ##########################################################
        ''' Check Out Mangement'''
        self.lineEdit_10.returnPressed.connect(self.get_check_out_room_data)
        self.pushButton_40.clicked.connect(self.save_guest_check_out)
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
    def validate_phone_number(self , phone_number):
        try :
            return int(phone_number)
        except Exception as m :
            self.statusBar().showMessage('Enter Only numbers')
            self.lineEdit_3.clear()


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
            self.comboBox_2.clear()
            self.cur.execute('''SELECT room_number FROM rooms''')
            room_numbers = self.cur.fetchall()
            for room in room_numbers :
                self.comboBox_4.addItem(str(room[0]))
        except Exception as m :
            print(m)
    def get_free_room_numbers(self):
        self.comboBox_2.clear()
        selected_room_type = ""
        if self.radioButton_3.isChecked():
            selected_room_type = "Delux"
        elif self.radioButton_4.isChecked():
            selected_room_type = "Full Deulx"
        elif self.radioButton_5.isChecked():
            selected_room_type = "Genral"
        elif self.radioButton_6.isChecked():
            selected_room_type = "Joint"
        if selected_room_type :
            self.cur.execute('''SELECT room_number FROM rooms WHERE room_status = 0 AND room_type = %s ''',(selected_room_type,))
            empty_room = self.cur.fetchall()
            if empty_room :
                for room in empty_room:
                    self.comboBox_2.addItem(str(room[0]))
            else:
                self.comboBox_2.addItem("No Free {} Rooms  ".format(selected_room_type))


    def get_room_price (self) :
        room_number =self.comboBox_2.currentText()
        self.cur.execute('''SELECT room_price FROM rooms WHERE room_number =  %s ''',(room_number,))
        room_price = self.cur.fetchone()
        self.label_38.setText(str(room_price[0]))
        self.calcuate_price()

    def test(self):
        print('test')

##########################################################################################################
    #############################
    '''CHECK IN Tab '''
    ############################
    def handel_check_in (self ) :
        name = self.lineEdit.text()
        adress = self.lineEdit_2.text()
        phone = self.lineEdit_3.text()
        room_number = self.comboBox_2.currentText()
        selected_room_type = ""
        payment_method = ""
        today_date = datetime.date.today()
        to_date = self.dateEdit.date().toPyDate()
        total_price = float(self.label_37.text())
        if self.radioButton_3.isChecked():
            selected_room_type = "Delux"
        elif self.radioButton_4.isChecked():
            selected_room_type = "Full Deulx"
        elif self.radioButton_5.isChecked():
            selected_room_type = "Genral"
        elif self.radioButton_6.isChecked():
            selected_room_type = "Joint"
        if self.radioButton_7.isChecked():
            payment_method = "Credit"
        elif self.radioButton_8.isChecked():
            payment_method = "Cash"
        self.save_guest_check_in( name, adress, phone, room_number, selected_room_type, payment_method, today_date,to_date, total_price)

    #############################
    '''SAVE GUSET CHECK IN DATA INTO DATABASE  '''
    ############################
    def save_guest_check_in(self,name , adress , phone , room_number , selected_room_type , payment_method , today_date , to_date , total_price):
        if name != "" and adress != " " and phone != "" and total_price > 0 :
            try:
                self.cur.execute('''INSERT INTO guests (name , adress , phone , room_number , room_type , payment , from_date , to_date , total_price)
                                VALUES (%s , %s, %s, %s, %s, %s, %s, %s, %s)
                                ''',(name , adress , phone , room_number , selected_room_type , payment_method , today_date , to_date , total_price))
                room_status_number = int(room_number)
                self.cur.execute('''UPDATE rooms SET room_status = %s   , reserved_counter = reserved_counter +1 WHERE room_number = %s''',( 1 , room_status_number,))
                self.db.commit()
                self.statusBar().showMessage("Checked In successfully ")
                self.add_history_record(name, room_number, total_price, today_date, to_date, 1)
                self.show_free_and_reserved_rooms()
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.comboBox_2.clear()
                self.label_37.clear()
                self.label_38.clear()
                self.spinBox.clear()
                self.radioButton_3.setChecked(False)
                self.radioButton_4.setChecked(False)
                self.radioButton_5.setChecked(False)
                self.radioButton_6.setChecked(False)
                self.radioButton_8.setChecked(False)
                self.radioButton_7.setChecked(False)
            except Exception as m:
                print(m)
        else :
            self.statusBar().showMessage("Enter Valid Data")

##########################################################################################################
        #############################
        '''CHECK OUT Tab '''
        ############################
    def get_check_out_room_data(self):
        try :
            room_number = self.lineEdit_10.text()
            self.cur.execute('''SELECT guests.name ,rooms.room_status FROM guests JOIN rooms
                                WHERE guests.room_number = rooms.room_number  AND guests.room_number = %s''',(room_number,))
            data = self.cur.fetchone()
            if data[1] == 1 :
                self.lineEdit_15.setText(data[0])
            else:
                self.statusBar().showMessage("Room is Free")
                self.lineEdit_15.setText("Room is Free")
        except Exception as m:
            print(m)
#############################
    '''SAVE GUSET CHECK OUT INTO DATABASE  '''
    ############################
    def save_guest_check_out(self):
        name = self.lineEdit_15.text()
        if name != "Room is Free":
            room_number = self.lineEdit_10.text()
            self.cur.execute('''UPDATE rooms SET room_status =%s  WHERE room_number = %s''',(0 ,room_number ))
            self.cur.execute('''SELECT from_date , to_date FROM guests WHERE name =%s ''',(name,))
            dates = self.cur.fetchone()
            self.add_history_record(name, room_number, 0, dates[0], dates[1], 0)
            self.lineEdit_10.clear()
            self.lineEdit_15.clear()
            self.db.commit()
            self.statusBar().showMessage("Checked Out Successfully")
            self.show_free_and_reserved_rooms()
        else :
            self.statusBar().showMessage("Free Rooms Can Not Check Out")
            self.lineEdit_15.setText("Free Rooms Can Not Check Out")

    ################################################################
    '''ADD GUSETS RECORD INTO HISTORY TABLE '''
    def add_history_record(self,name,room_number,total_price,today_date, to_date, type_):
        try:
            self.cur.execute('''SELECT id FROM guests WHERE name = %s ''',(name,))
            guest_id = self.cur.fetchone()
            self.cur.execute('''INSERT INTO history (guest_id , room_number , room_price , from_ , to_ , type_)
                                VALUES (%s,%s,%s,%s,%s,%s)''',(guest_id[0],room_number,total_price,today_date, to_date, type_))
            self.db.commit()
        except Exception as m:
            print(m)

    def to_day_and_tomorow(self):

        today_date = datetime.date.today()
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setDate(today_date)
        self.label_40.setText(str(today_date))

    def count_date_to_cuurent(self):
        days = self.spinBox.value()
        to_date = datetime.date.today()  + timedelta(days=days)
        self.dateEdit.setDate(to_date)
        self.calcuate_price()
    def calcuate_price(self):
        room_number = self.comboBox_2.currentText()
        if room_number :
            on_day_price = self.label_38.text()
            number_of_dayes = self.spinBox.value()
            totalprice = float(on_day_price) *int(number_of_dayes)
            self.label_37.setText(str(totalprice))

##########################################################################################################
    ######################################
        '''ADD DATA IN HISTORY TAB '''
    ######################################
    def retrive_history_data(self):
        self.cur.execute('''SELECT h.type_ , h.room_number, g.name, h.from_ , h.to_ ,h.room_price FROM history AS h
                        JOIN guests AS g WHERE g.id = h.guest_id
                        ''')
        history_data = self.cur.fetchall()
        print(history_data)
        for row_number , row_data in enumerate(history_data) :
            self.tableWidget_3.insertRow(row_number)
            for column_number , cloumn_data in enumerate(row_data):
                if column_number == 0 :
                    if cloumn_data == "0" :
                        cell = QTableWidgetItem("Check Out")
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_3.setItem(row_number, column_number, cell)
                    else:
                        cell = QTableWidgetItem("Check In")
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_3.setItem(row_number, column_number, cell)
                elif column_number== 5 :
                    if cloumn_data==0.0 :
                        cell = QTableWidgetItem("checkout")
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_3.setItem(row_number, column_number, cell)
                    else :
                        cell = QTableWidgetItem(str(cloumn_data))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_3.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(cloumn_data))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_3.setItem(row_number, column_number, cell)

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

    def show_free_and_reserved_rooms(self):
        try :
            self.cur.execute('''SELECT count(*) as room FROM rooms WHERE room_status =0''')
            free = self.cur.fetchone()
            self.cur.execute('''SELECT count(*) as room FROM rooms WHERE room_status =1''')
            reserved = self.cur.fetchone()
            self.lcdNumber.display(free[0])
            self.lcdNumber_2.display(reserved[0])

        except Exception as m:
            print(m)


##########################################################################################################
#############################
        '''Current Time '''
        ############################



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
