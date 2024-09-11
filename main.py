## Importing Packages
# Built-in standard packages
import sys
import datetime
import time
import os

# opencv package
import cv2

# PyQT5 Packages
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QMessageBox, QCommandLinkButton, QTabWidget, QPushButton, QVBoxLayout, QDialog, QLabel, QSizePolicy, QWidget, QLayout, QGraphicsBlurEffect, QInputDialog, QLineEdit
from PyQt5.QtGui import QImage, QPixmap, QPainter, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTimer, Qt, QSize   
from PyQt5.uic import loadUi

# Defining the plc communication packages
from pycomm3 import LogixDriver 
from pycomm3.exceptions import CommError
import snap7 
from snap7 import *
from snap7.util import *
from snap7.types import *




class MouthProtectionApp():                  
                                            
    defined_plc_types = ["Siemens", "AllenBradly"]
    def __init__(self, fps):
            
        # video recorder parameters    
        self.fps = fps  
        self.folder_dir = ""
        self.record_timer_limit = 300  # 5 (min) = 300 (s) 
        self.first_auto_record_img = True
        self.recording = False

        # Plc Communication 
        self.plc_type = "Siemens"
        self.plc_connection = False
        assert (self.plc_type in MouthProtectionApp.defined_plc_types) , "Plc Type inserted {} is not among the defined plc variables; {}. please insert the verified plc type.".format(self.plc_type, MouthProtectionApp.defined_plc_types) 
        
        # Manual Push buttons to manage records
        self.manl_start_record = False
        self.manl_stop_record = False
        self.manl_pause_record = False
        self.manl_continue_record = False
        
        # Automatic record managing
        self.auto_start_record = False
        self.auto_stop_record = False

        # save configurations 
        self.save_configuration = False
        
        # Logo and icon
        self.danieli_logo_image = cv2.imread("resources\logo.jpg")
        self.danieli_icon =  "READ the ICON HERE."
        

    def __initCommunication(self):    
        self.plc_type = str(self.comboBox.currentText())
        self.plc_ip_address = self.plcIp_text.text()   

        # Siemens PLC 
        if (self.plc_type == "Siemens"):  
            try:  
                self.client = snap7.client.Client()
                self.client.connect(self.plcIp_text.text(), 0, 1) 
                print("Connection to Siemens PLC is okay!")
                self.plc_connection = True
            except Exception as err:
                self.__plc_show_warning_messagebox(str(err), str(self.plc_type))
        else: 
            try:
                self.client = LogixDriver(self.plcIp_text.text())
                self.client.__enter__()  # Explicitly enter the context
                print("Connection to AllenBradly PLC is okay!")
                self.plc_connection = True
            except CommError as err:
                self.__plc_show_warning_messagebox(str(err), str(self.plc_type))    
             
             
        
    def initUI(self,mouthProtectionWinow):
        ## Fonts:
        # font0: Header
        font0 = QtGui.QFont()
        font0.setFamily(u"Arial")
        font0.setPointSize(28)
        font0.setBold(True)
        font0.setUnderline(False)
        font0.setWeight(75)
        # font1: Titles
        font1 = QtGui.QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(19)
        font1.setBold(False)
        font1.setUnderline(True)
        font1.setWeight(50)
        # font2
        font2 = QtGui.QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(9)
        #font3
        font3 = QtGui.QFont()
        font3.setFamily(u"MS Shell Dlg 2")
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setWeight(50)
        #font4: combobox
        font4 = QtGui.QFont()
        font4.setPointSize(10)
        #font5: checkbox
        font5 = QtGui.QFont()
        font5.setBold(True)
        font5.setWeight(75)
        #font6: Logger Text
        font6 = QtGui.QFont()
        font6.setFamily(u"Arial")
        font6.setPointSize(7)
        font6.setBold(False)
        font6.setItalic(False)
        font6.setWeight(9)
        #font7:
        font7 = QtGui.QFont()
        font7.setFamily(u"MS Shell Dlg 2")
        font7.setPointSize(10)
        font7.setBold(False)
        font7.setItalic(False)
        #font8:
        font8 = QtGui.QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(8)
        font8.setBold(False)
        font8.setItalic(False)
        
        # Blur effect for the pushbutton
        self.blur_effect_record = QGraphicsBlurEffect()
        self.blur_effect_record.setBlurRadius(2)
        self.blur_effect_continue = QGraphicsBlurEffect()
        self.blur_effect_continue.setBlurRadius(2)
        self.blur_effect_pause = QGraphicsBlurEffect()
        self.blur_effect_pause.setBlurRadius(2)
        self.blur_effect_stop = QGraphicsBlurEffect()
        self.blur_effect_stop.setBlurRadius(2)
        
        # Blur effect for the setting frame
        self.blur_effect_setting_frame = QGraphicsBlurEffect()
        self.blur_effect_setting_frame.setBlurRadius(2)
        
                
        ## Main Window
        mouthProtectionWinow.setWindowIcon(QtGui.QIcon("resources/favicon.ico"))
        mouthProtectionWinow.setObjectName(u"mouthProtectionWinow")
        mouthProtectionWinow.resize(1680, 1050)
        mouthProtectionWinow.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(43, 39, 56);\n"
"")
        # Central Widget
        self.centralwidget = QWidget(mouthProtectionWinow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        #### border_widget;  all the widgets comparision are done wrt border_widget  
        self.border_widget = QWidget(self.centralwidget)
        self.border_widget.setObjectName(u"border_widget")
        self.border_widget.setGeometry(QtCore.QRect(29, 10, 1621, 941))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.border_widget.sizePolicy().hasHeightForWidth())
        self.border_widget.setSizePolicy(sizePolicy)
        self.border_widget.setStyleSheet(u"border: 1px solid white;\n"
"")
        
        # Footer_widget:         
        self.footer_widget = QWidget(self.border_widget)
        self.footer_widget.setObjectName(u"footer_widget")
        self.footer_widget.setGeometry(QtCore.QRect(10, 830, 1601, 101))
        self.footer_widget.setStyleSheet(u"border: 1px solid white;\n"
"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        self.footer_title = QLabel(self.footer_widget)
        self.footer_title.setObjectName(u"footer_title")
        self.footer_title.setGeometry(QtCore.QRect(670, -2, 271, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer_title.sizePolicy().hasHeightForWidth())
        self.footer_title.setSizePolicy(sizePolicy)
        self.footer_title.setFont(font1)
        self.footer_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.footer_title.setAlignment(Qt.AlignCenter)
        self.textEdit = QtWidgets.QTextEdit(self.footer_widget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QtCore.QRect(25, 36, 1541, 61))
        self.textEdit.setFont(font6)
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"font: 9pt \"Segoe UI\";\n"
"border-color: rgb(0, 0, 0);")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.footer_widget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QtCore.QRect(1387, 36, 181, 61))
        self.dateTimeEdit.setFont(font3)
        self.dateTimeEdit.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        
        
        # video_widget
        self.video_widget = QWidget(self.border_widget)
        self.video_widget.setObjectName(u"video_widget")
        self.video_widget.setGeometry(QtCore.QRect(10, 110, 791, 701))
        self.video_widget.setStyleSheet(u"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        
        self.video_title = QLabel(self.video_widget)
        self.video_title.setObjectName(u"video_title")
        self.video_title.setGeometry(QtCore.QRect(260, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.video_title.sizePolicy().hasHeightForWidth())
        self.video_title.setSizePolicy(sizePolicy)
        self.video_title.setFont(font1)
        self.video_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.video_title.setAlignment(Qt.AlignCenter)
        self.video_label = QLabel(self.video_widget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QtCore.QRect(50, 60, 691, 641))
        self.video_label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.record_label = QLabel(self.video_widget)
        self.record_label.setObjectName(u"record_label")
        self.record_label.setGeometry(QtCore.QRect(70, 630, 651, 51))
        self.record_label.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.record_pushButton = QPushButton(self.video_widget)
        self.record_pushButton.setObjectName(u"record_pushButton")
        self.record_pushButton.setGeometry(QtCore.QRect(368, 640, 75, 31))
        self.record_pushButton.setFont(font2)
        # Set the style for normal and hover state
        self.record_pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 75 12pt \"Arial\";
                border-color: rgb(0, 0, 0);;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.record_pushButton.clicked.connect(self.__on_record_button)
        # Apply blur effect and disable the button
        self.record_pushButton.setGraphicsEffect(self.blur_effect_record)
        self.record_pushButton.setEnabled(False)

        
        self.continue_pushButton = QPushButton(self.video_widget)
        self.continue_pushButton.setObjectName(u"continue_pushButton")
        self.continue_pushButton.setGeometry(QtCore.QRect(455, 640, 75, 31))
        # Set the style for normal and hover state
        self.continue_pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 75 12pt \"Arial\";
                border-color: rgb(0, 0, 0);;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.continue_pushButton.clicked.connect(self.__on_continue_button)
        # Apply blur effect and disable the button
        self.continue_pushButton.setGraphicsEffect(self.blur_effect_continue)
        self.continue_pushButton.setEnabled(False)


        self.stop_pushButton = QPushButton(self.video_widget)
        self.stop_pushButton.setObjectName(u"stop_pushButton")
        self.stop_pushButton.setGeometry(QtCore.QRect(631, 640, 75, 31))
        # Set the style for normal and hover state
        self.stop_pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 75 12pt \"Arial\";
                border-color: rgb(0, 0, 0);;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.stop_pushButton.clicked.connect(self.__on_stop_button)
        # Apply blur effect and disable the button
        self.stop_pushButton.setGraphicsEffect(self.blur_effect_stop)
        self.stop_pushButton.setEnabled(False)
        
        self.pause_pushButton = QPushButton(self.video_widget)
        self.pause_pushButton.setObjectName(u"pause_pushButton")
        self.pause_pushButton.setGeometry(QtCore.QRect(543, 640, 75, 31))
        # Set the style for normal and hover state
        self.pause_pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 75 12pt \"Arial\";
                border-color: rgb(0, 0, 0);;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.pause_pushButton.clicked.connect(self.__on_pause_button)
        # Apply blur effect and disable the button
        self.pause_pushButton.setGraphicsEffect(self.blur_effect_pause)
        self.pause_pushButton.setEnabled(False)

        
        self.activtaeRecording_checkBox = QtWidgets.QCheckBox(self.video_widget)
        self.activtaeRecording_checkBox.setObjectName(u"activtaeRecording_checkBox")
        self.activtaeRecording_checkBox.setGeometry(QtCore.QRect(90, 640, 181, 31))
        self.activtaeRecording_checkBox.setStyleSheet(u"colo: rgb(0, 0, 0);\n"
"font: 75 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")

        
        # Setting_widget
        self.setting_widget = QWidget(self.border_widget)
        self.setting_widget.setObjectName(u"setting_widget")
        self.setting_widget.setGeometry(QtCore.QRect(820, 110, 791, 701))
        self.setting_widget.setStyleSheet(u"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        self.setting_title = QLabel(self.setting_widget)
        self.setting_title.setObjectName(u"setting_title")
        self.setting_title.setGeometry(QtCore.QRect(270, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.setting_title.sizePolicy().hasHeightForWidth())
        self.setting_title.setSizePolicy(sizePolicy)
        self.setting_title.setFont(font1)
        self.setting_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.setting_title.setAlignment(Qt.AlignCenter)
        self.setting_frame = QtWidgets.QFrame(self.setting_widget)
        self.setting_frame.setObjectName(u"setting_frame")    
        self.setting_frame.setGeometry(QtCore.QRect(10, 50, 771, 591))
        self.setting_frame.setStyleSheet(u"border-color: rgb(220, 220, 240);\n"
"border-color: rgb(0, 0, 0);")
        self.setting_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setting_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.showSettingFrame_checkBox = QtWidgets.QCheckBox(self.setting_widget)
        self.showSettingFrame_checkBox.setObjectName(u"showSettingFrame_checkBox")
        self.showSettingFrame_checkBox.setGeometry(QtCore.QRect(462, 17, 21, 20))
        
        self.cameraUrl_label = QLabel(self.setting_frame)
        self.cameraUrl_label.setObjectName(u"cameraUrl_label")
        self.cameraUrl_label.setGeometry(QtCore.QRect(20, 4, 731, 31))
        self.cameraUrl_label.setFont(font2)
        self.cameraUrl_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.cameraUrl_label.setAlignment(Qt.AlignCenter)
        self.cameraUrl_line = QtWidgets.QLineEdit(self.setting_frame)
        self.cameraUrl_line.setObjectName(u"cameraUrl_line")
        self.cameraUrl_line.setGeometry(QtCore.QRect(20, 31, 731, 30))
        self.cameraUrl_line.setFont(font2)
        self.cameraUrl_line.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")

        self.prmRecPath_text = QtWidgets.QLineEdit(self.setting_frame)
        self.prmRecPath_text.setObjectName(u"prmRecPath_text")
        self.prmRecPath_text.setGeometry(QtCore.QRect(20, 100, 621, 30))
        self.prmRecPath_text.setFont(font5)
        self.prmRecPath_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.prmRecPath_label = QLabel(self.setting_frame)
        self.prmRecPath_label.setObjectName(u"prmRecPath_label")
        self.prmRecPath_label.setGeometry(QtCore.QRect(20, 69, 731, 31))
        self.prmRecPath_label.setFont(font2)
        self.prmRecPath_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.prmRecPath_label.setAlignment(Qt.AlignCenter)
        self.plcIp_text = QtWidgets.QLineEdit(self.setting_frame)
        self.plcIp_text.setObjectName(u"plcIp_text")
        self.plcIp_text.setGeometry(QtCore.QRect(490, 254, 261, 30))
        self.plcIp_text.setFont(font5)
        self.plcIp_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_label = QLabel(self.setting_frame)
        self.secRecPath_label.setObjectName(u"secRecPath_label")
        self.secRecPath_label.setGeometry(QtCore.QRect(20, 140, 731, 31))
        self.secRecPath_label.setFont(font2)
        self.secRecPath_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.secRecPath_label.setAlignment(Qt.AlignCenter)
        self.plcIp_label = QLabel(self.setting_frame)
        self.plcIp_label.setObjectName(u"plcIp_label")
        self.plcIp_label.setGeometry(QtCore.QRect(490, 222, 261, 31))
        self.plcIp_label.setFont(font2)
        self.plcIp_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plcIp_label.setAlignment(Qt.AlignCenter)
        self.primPath_checkBox = QtWidgets.QCheckBox(self.setting_frame)
        self.primPath_checkBox.setObjectName(u"primPath_checkBox")
        self.primPath_checkBox.setGeometry(QtCore.QRect(640, 100, 111, 29))
        self.primPath_checkBox.setFont(font5)
        self.primPath_checkBox.setLayoutDirection(Qt.LeftToRight)
        self.primPath_checkBox.setAutoFillBackground(False)
        self.primPath_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.primPath_checkBox.setTristate(False)
        self.primPath_checkBox.setChecked(True) 
        self.secondPath_checkBox = QtWidgets.QCheckBox(self.setting_frame)
        self.secondPath_checkBox.setObjectName(u"secondPath_checkBox")
        self.secondPath_checkBox.setGeometry(QtCore.QRect(640, 170, 111, 30))
        self.secondPath_checkBox.setFont(font5)
        self.secondPath_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.comboBox = QtWidgets.QComboBox(self.setting_frame)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(20, 254, 201, 31))
        self.comboBox.setFont(font4)
        self.comboBox.setStyleSheet(u"color: rgb(0,0,0);\n"
"")
        self.comboBox.setInputMethodHints(Qt.ImhNone)
        self.plctype_label = QLabel(self.setting_frame)
        self.plctype_label.setObjectName(u"plctype_label")
        self.plctype_label.setGeometry(QtCore.QRect(20, 222, 201, 31))
        self.plctype_label.setFont(font2)
        self.plctype_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plctype_label.setAlignment(Qt.AlignCenter)
        self.secRecPath_text = QtWidgets.QLineEdit(self.setting_frame)
        self.secRecPath_text.setObjectName(u"secRecPath_text")
        self.secRecPath_text.setGeometry(QtCore.QRect(20, 170, 621, 30))
        self.secRecPath_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.billetNumberTagTitle_label = QLabel(self.setting_frame)
        self.billetNumberTagTitle_label.setObjectName(u"billetNumberTagTitle_label")
        self.billetNumberTagTitle_label.setGeometry(QtCore.QRect(2, 550, 121, 21))
        self.billetNumberTagTitle_label.setFont(font2)
        self.billetNumberTagTitle_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.billetNumberTagTitle_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.billetNumberTagBorder1 = QLabel(self.setting_frame)
        self.billetNumberTagBorder1.setObjectName(u"billetNumberTagBorder1")
        self.billetNumberTagBorder1.setGeometry(QtCore.QRect(130, 547, 371, 31))
        self.billetNumberTagBorder1.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.billetNumberTagBorder1.setAlignment(Qt.AlignCenter)
        self.billetNumberTagDB_label = QLabel(self.setting_frame)
        self.billetNumberTagDB_label.setObjectName(u"billetNumberTagDB_label")
        self.billetNumberTagDB_label.setGeometry(QtCore.QRect(143, 552, 121, 20))
        self.billetNumberTagDB_label.setFont(font7)
        self.billetNumberTagDB_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.billetNumberTagDB_label.setAlignment(Qt.AlignCenter)  
        self.billetNumberTagDB_text = QtWidgets.QLineEdit(self.setting_frame)
        self.billetNumberTagDB_text.setObjectName(u"billetNumberTagDB_text")
        self.billetNumberTagDB_text.setGeometry(QtCore.QRect(264, 552, 41, 21))
        self.billetNumberTagDB_text.setFont(font8)
        self.billetNumberTagDB_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.billetNumberTagBit_label = QLabel(self.setting_frame)
        self.billetNumberTagBit_label.setObjectName(u"billetNumberTagBit_label")
        self.billetNumberTagBit_label.setGeometry(QtCore.QRect(407, 554, 41, 20))
        self.billetNumberTagBit_label.setFont(font7)
        self.billetNumberTagBit_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.billetNumberTagBit_label.setAlignment(Qt.AlignCenter)
        self.billetNumberTagByte_text = QtWidgets.QLineEdit(self.setting_frame)
        self.billetNumberTagByte_text.setObjectName(u"billetNumberTagByte_text")
        self.billetNumberTagByte_text.setGeometry(QtCore.QRect(358, 553, 41, 21))
        self.billetNumberTagByte_text.setFont(font8)
        self.billetNumberTagByte_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.billetNumberTagBit_text = QtWidgets.QLineEdit(self.setting_frame)
        self.billetNumberTagBit_text.setObjectName(u"billetNumberTagBit_text")
        self.billetNumberTagBit_text.setGeometry(QtCore.QRect(443, 553, 41, 21))
        self.billetNumberTagBit_text.setFont(font8)
        self.billetNumberTagBit_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.billetNumberTagByte_label = QLabel(self.setting_frame)
        self.billetNumberTagByte_label.setObjectName(u"billetNumberTagByte_label")
        self.billetNumberTagByte_label.setGeometry(QtCore.QRect(324, 553, 31, 20))
        self.billetNumberTagByte_label.setFont(font7)
        self.billetNumberTagByte_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.billetNumberTagByte_label.setAlignment(Qt.AlignCenter)
        self.billetNumberTagBorder2 = QLabel(self.setting_frame)
        self.billetNumberTagBorder2.setObjectName(u"billetNumberTagBorder2")
        self.billetNumberTagBorder2.setGeometry(QtCore.QRect(510, 547, 201, 31))
        self.billetNumberTagBorder2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.billetNumberTagBorder2.setAlignment(Qt.AlignCenter)
        self.billetNumberTagTagName_label = QLabel(self.setting_frame)
        self.billetNumberTagTagName_label.setObjectName(u"billetNumberTagTagName_label")
        self.billetNumberTagTagName_label.setGeometry(QtCore.QRect(515, 553, 71, 20))
        self.billetNumberTagTagName_label.setFont(font7)
        self.billetNumberTagTagName_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.billetNumberTagTagName_label.setAlignment(Qt.AlignCenter)
        self.billetNumberTagTagName_text = QtWidgets.QLineEdit(self.setting_frame)
        self.billetNumberTagTagName_text.setObjectName(u"billetNumberTagTagName_text")
        self.billetNumberTagTagName_text.setGeometry(QtCore.QRect(587, 553, 111, 21))
        self.billetNumberTagTagName_text.setFont(font8)
        self.billetNumberTagTagName_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dieCodeTagTitle_label = QLabel(self.setting_frame)
        self.dieCodeTagTitle_label.setObjectName(u"dieCodeTagTitle_label")
        self.dieCodeTagTitle_label.setGeometry(QtCore.QRect(2, 495, 121, 21))
        self.dieCodeTagTitle_label.setFont(font2)
        self.dieCodeTagTitle_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.dieCodeTagTitle_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dieCodeTagBorder1 = QLabel(self.setting_frame)
        self.dieCodeTagBorder1.setObjectName(u"dieCodeTagBorder1")
        self.dieCodeTagBorder1.setGeometry(QtCore.QRect(130, 492, 371, 31))
        self.dieCodeTagBorder1.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.dieCodeTagBorder1.setAlignment(Qt.AlignCenter)
        self.dieCodeTagDB_label = QLabel(self.setting_frame)
        self.dieCodeTagDB_label.setObjectName(u"dieCodeTagDB_label")
        self.dieCodeTagDB_label.setGeometry(QtCore.QRect(143, 497, 121, 20))
        self.dieCodeTagDB_label.setFont(font7)
        self.dieCodeTagDB_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.dieCodeTagDB_label.setAlignment(Qt.AlignCenter)
        self.dieCodeTagByte_label = QLabel(self.setting_frame)
        self.dieCodeTagByte_label.setObjectName(u"dieCodeTagByte_label")
        self.dieCodeTagByte_label.setGeometry(QtCore.QRect(324, 498, 31, 20))
        self.dieCodeTagByte_label.setFont(font7)
        self.dieCodeTagByte_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.dieCodeTagByte_label.setAlignment(Qt.AlignCenter)
        self.dieCodeTagBit_label = QLabel(self.setting_frame)
        self.dieCodeTagBit_label.setObjectName(u"dieCodeTagBit_label")
        self.dieCodeTagBit_label.setGeometry(QtCore.QRect(407, 499, 41, 20))
        self.dieCodeTagBit_label.setFont(font7)
        self.dieCodeTagBit_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.dieCodeTagBit_label.setAlignment(Qt.AlignCenter)
        self.dieCodeTagDB_text = QtWidgets.QLineEdit(self.setting_frame)
        self.dieCodeTagDB_text.setObjectName(u"dieCodeTagDB_text")
        self.dieCodeTagDB_text.setGeometry(QtCore.QRect(264, 497, 41, 21))
        self.dieCodeTagDB_text.setFont(font8)
        self.dieCodeTagDB_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dieCodeTagBit_text = QtWidgets.QLineEdit(self.setting_frame)
        self.dieCodeTagBit_text.setObjectName(u"dieCodeTagBit_text")
        self.dieCodeTagBit_text.setGeometry(QtCore.QRect(443, 497, 41, 21))
        self.dieCodeTagBit_text.setFont(font8)
        self.dieCodeTagBit_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dieCodeTagByte_text = QtWidgets.QLineEdit(self.setting_frame)
        self.dieCodeTagByte_text.setObjectName(u"dieCodeTagByte_text")
        self.dieCodeTagByte_text.setGeometry(QtCore.QRect(358, 498, 41, 21))
        self.dieCodeTagByte_text.setFont(font8)
        self.dieCodeTagByte_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dieCodeTagBorder2 = QLabel(self.setting_frame)
        self.dieCodeTagBorder2.setObjectName(u"dieCodeTagBorder2")
        self.dieCodeTagBorder2.setGeometry(QtCore.QRect(510, 492, 201, 31))
        self.dieCodeTagBorder2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.dieCodeTagBorder2.setAlignment(Qt.AlignCenter)
        self.dieCodeTagTagName_label = QLabel(self.setting_frame)
        self.dieCodeTagTagName_label.setObjectName(u"dieCodeTagTagName_label")
        self.dieCodeTagTagName_label.setGeometry(QtCore.QRect(515, 498, 71, 20))
        self.dieCodeTagTagName_label.setFont(font7)
        self.dieCodeTagTagName_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.dieCodeTagTagName_label.setAlignment(Qt.AlignCenter)
        self.dieCodeTagTagName_text = QtWidgets.QLineEdit(self.setting_frame)
        self.dieCodeTagTagName_text.setObjectName(u"dieCodeTagTagName_text")
        self.dieCodeTagTagName_text.setGeometry(QtCore.QRect(587, 498, 111, 21))
        self.dieCodeTagTagName_text.setFont(font8)
        self.dieCodeTagTagName_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartBeatTagTitle_label = QLabel(self.setting_frame)
        self.heartBeatTagTitle_label.setObjectName(u"heartBeatTagTitle_label")
        self.heartBeatTagTitle_label.setGeometry(QtCore.QRect(3, 440, 121, 21))
        self.heartBeatTagTitle_label.setFont(font2)
        self.heartBeatTagTitle_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartBeatTagTitle_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.heartBeatTagBorder1 = QLabel(self.setting_frame)
        self.heartBeatTagBorder1.setObjectName(u"heartBeatTagBorder1")
        self.heartBeatTagBorder1.setGeometry(QtCore.QRect(131, 437, 371, 31))
        self.heartBeatTagBorder1.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.heartBeatTagBorder1.setAlignment(Qt.AlignCenter)
        self.heartBeatTagDB_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartBeatTagDB_text.setObjectName(u"heartBeatTagDB_text")
        self.heartBeatTagDB_text.setGeometry(QtCore.QRect(265, 442, 41, 21))
        self.heartBeatTagDB_text.setFont(font8)
        self.heartBeatTagDB_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartBeatTagBit_label = QLabel(self.setting_frame)
        self.heartBeatTagBit_label.setObjectName(u"heartBeatTagBit_label")
        self.heartBeatTagBit_label.setGeometry(QtCore.QRect(408, 444, 41, 20))
        self.heartBeatTagBit_label.setFont(font7)
        self.heartBeatTagBit_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartBeatTagBit_label.setAlignment(Qt.AlignCenter)
        self.heartBeatTagDB_label = QLabel(self.setting_frame)
        self.heartBeatTagDB_label.setObjectName(u"heartBeatTagDB_label")
        self.heartBeatTagDB_label.setGeometry(QtCore.QRect(144, 442, 121, 20))
        self.heartBeatTagDB_label.setFont(font7)
        self.heartBeatTagDB_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartBeatTagDB_label.setAlignment(Qt.AlignCenter)
        self.heartBeatTagByte_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartBeatTagByte_text.setObjectName(u"heartBeatTagByte_text")
        self.heartBeatTagByte_text.setGeometry(QtCore.QRect(359, 443, 41, 21))
        self.heartBeatTagByte_text.setFont(font8)
        self.heartBeatTagByte_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")       
        self.heartBeatTagByte_label = QLabel(self.setting_frame)
        self.heartBeatTagByte_label.setObjectName(u"heartBeatTagByte_label")
        self.heartBeatTagByte_label.setGeometry(QtCore.QRect(325, 443, 31, 20))
        self.heartBeatTagByte_label.setFont(font7)
        self.heartBeatTagByte_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")        
        
        self.heartBeatTagByte_label.setAlignment(Qt.AlignCenter)
        self.heartBeatTagBit_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartBeatTagBit_text.setObjectName(u"heartBeatTagBit_text")
        self.heartBeatTagBit_text.setGeometry(QtCore.QRect(444, 445, 41, 21))
        self.heartBeatTagBit_text.setFont(font8)
        self.heartBeatTagBit_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")     
     
        self.heartBeatTagBorder2 = QLabel(self.setting_frame)
        self.heartBeatTagBorder2.setObjectName(u"heartBeatTagBorder2")
        self.heartBeatTagBorder2.setGeometry(QtCore.QRect(510, 437, 201, 31))
        self.heartBeatTagBorder2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.heartBeatTagBorder2.setAlignment(Qt.AlignCenter)
     
        self.heartBeatTagTagName_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartBeatTagTagName_text.setObjectName(u"heartBeatTagTagName_text")
        self.heartBeatTagTagName_text.setGeometry(QtCore.QRect(588, 443, 111, 21))
        self.heartBeatTagTagName_text.setFont(font8)
        self.heartBeatTagTagName_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartBeatTagTagName_label = QLabel(self.setting_frame)
        self.heartBeatTagTagName_label.setObjectName(u"heartBeatTagTagName_label")
        self.heartBeatTagTagName_label.setGeometry(QtCore.QRect(516, 443, 71, 20))
        self.heartBeatTagTagName_label.setFont(font7)
        self.heartBeatTagTagName_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartBeatTagTagName_label.setAlignment(Qt.AlignCenter)
     
        self.heartBeatTagLED = QLabel(self.setting_frame)
        self.heartBeatTagLED.setObjectName(u"heartBeatTagLED")
        self.heartBeatTagLED.setGeometry(QtCore.QRect(723, 444, 31, 21))
        self.heartBeatTagLED.setStyleSheet(u"")
        
        self.extrusionTagTitle_label = QLabel(self.setting_frame)
        self.extrusionTagTitle_label.setObjectName(u"extrusionTagTitle_label")
        self.extrusionTagTitle_label.setGeometry(QtCore.QRect(3, 383, 121, 21))
        self.extrusionTagTitle_label.setFont(font2)
        self.extrusionTagTitle_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTagTitle_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        
        self.extrusionTagBorder1 = QLabel(self.setting_frame)
        self.extrusionTagBorder1.setObjectName(u"extrusionTagBorder1")
        self.extrusionTagBorder1.setGeometry(QtCore.QRect(131, 380, 371, 31))
        self.extrusionTagBorder1.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.extrusionTagBorder1.setAlignment(Qt.AlignCenter)
        self.extrusionTagDB_label = QLabel(self.setting_frame)
        self.extrusionTagDB_label.setObjectName(u"extrusionTagDB_label")
        self.extrusionTagDB_label.setGeometry(QtCore.QRect(144, 385, 121, 20))
        self.extrusionTagDB_label.setFont(font7)
        self.extrusionTagDB_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTagDB_label.setAlignment(Qt.AlignCenter)

        self.extrusionTagDB_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTagDB_text.setObjectName(u"extrusionTagDB_text")
        self.extrusionTagDB_text.setGeometry(QtCore.QRect(265, 385, 41, 21))
        self.extrusionTagDB_text.setFont(font8)
        self.extrusionTagDB_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")

        self.extrusionTagByte_label = QLabel(self.setting_frame)
        self.extrusionTagByte_label.setObjectName(u"extrusionTagByte_label")
        self.extrusionTagByte_label.setGeometry(QtCore.QRect(325, 386, 31, 20))
        self.extrusionTagByte_label.setFont(font7)
        self.extrusionTagByte_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTagByte_label.setAlignment(Qt.AlignCenter)
        self.extrusionTagBit_label = QLabel(self.setting_frame)
        self.extrusionTagBit_label.setObjectName(u"extrusionTagBit_label")
        self.extrusionTagBit_label.setGeometry(QtCore.QRect(408, 387, 41, 20))
        self.extrusionTagBit_label.setFont(font7)
        self.extrusionTagBit_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTagBit_label.setAlignment(Qt.AlignCenter)

        self.extrusionTagBit_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTagBit_text.setObjectName(u"extrusionTagBit_text")
        self.extrusionTagBit_text.setGeometry(QtCore.QRect(444, 385, 41, 21))
        self.extrusionTagBit_text.setFont(font8)
        self.extrusionTagBit_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")


        self.extrusionTagByte_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTagByte_text.setObjectName(u"extrusionTagByte_text")
        self.extrusionTagByte_text.setGeometry(QtCore.QRect(359, 386, 41, 21))
        self.extrusionTagByte_text.setFont(font8)
        self.extrusionTagByte_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        
        self.extrusionTagBorder2 = QLabel(self.setting_frame)
        self.extrusionTagBorder2.setObjectName(u"extrusionTagBorder2")
        self.extrusionTagBorder2.setGeometry(QtCore.QRect(510, 380, 201, 31))
        self.extrusionTagBorder2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.extrusionTagBorder2.setAlignment(Qt.AlignCenter)

        self.extrusionTagTagName_label = QLabel(self.setting_frame)
        self.extrusionTagTagName_label.setObjectName(u"extrusionTagTagName_label")
        self.extrusionTagTagName_label.setGeometry(QtCore.QRect(516, 386, 71, 20))
        self.extrusionTagTagName_label.setFont(font7)
        self.extrusionTagTagName_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTagTagName_label.setAlignment(Qt.AlignCenter)
        
        self.extrusionTagTagName_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTagTagName_text.setObjectName(u"extrusionTagTagName_text")
        self.extrusionTagTagName_text.setGeometry(QtCore.QRect(588, 386, 111, 21))
        self.extrusionTagTagName_text.setFont(font8)
        self.extrusionTagTagName_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        
        self.extrusionTagLED = QLabel(self.setting_frame)
        self.extrusionTagLED.setObjectName(u"extrusionTagLED")
        self.extrusionTagLED.setGeometry(QtCore.QRect(723, 387, 31, 21))
        self.extrusionTagLED.setStyleSheet(u"")
       
        self.mouthDoorTagTitle_label = QLabel(self.setting_frame)
        self.mouthDoorTagTitle_label.setObjectName(u"mouthDoorTagTitle_label")
        self.mouthDoorTagTitle_label.setGeometry(QtCore.QRect(4, 325, 121, 21))
        self.mouthDoorTagTitle_label.setFont(font2)
        self.mouthDoorTagTitle_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.mouthDoorTagTitle_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        
        self.mouthDoorTagBorder1 = QLabel(self.setting_frame)
        self.mouthDoorTagBorder1.setObjectName(u"mouthDoorTagBorder1")
        self.mouthDoorTagBorder1.setGeometry(QtCore.QRect(132, 322, 371, 31))
        self.mouthDoorTagBorder1.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.mouthDoorTagBorder1.setAlignment(Qt.AlignCenter)
        self.mouthDoorTagDB_label = QLabel(self.setting_frame)
        self.mouthDoorTagDB_label.setObjectName(u"mouthDoorTagDB_label")
        self.mouthDoorTagDB_label.setGeometry(QtCore.QRect(145, 327, 121, 20))
        self.mouthDoorTagDB_label.setFont(font7)
        self.mouthDoorTagDB_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.mouthDoorTagDB_label.setAlignment(Qt.AlignCenter)

        self.mouthDoorTagBit_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTagBit_text.setObjectName(u"mouthDoorTagBit_text")
        self.mouthDoorTagBit_text.setGeometry(QtCore.QRect(444, 327, 41, 21))
        self.mouthDoorTagBit_text.setFont(font8)
        self.mouthDoorTagBit_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.mouthDoorTagByte_label = QLabel(self.setting_frame)
        self.mouthDoorTagByte_label.setObjectName(u"mouthDoorTagByte_label")
        self.mouthDoorTagByte_label.setGeometry(QtCore.QRect(326, 328, 31, 20))
        self.mouthDoorTagByte_label.setFont(font7)
        self.mouthDoorTagByte_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.mouthDoorTagByte_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTagBit_label = QLabel(self.setting_frame)
        self.mouthDoorTagBit_label.setObjectName(u"mouthDoorTagBit_label")
        self.mouthDoorTagBit_label.setGeometry(QtCore.QRect(413, 329, 31, 20))
        self.mouthDoorTagBit_label.setFont(font7)
        self.mouthDoorTagBit_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.mouthDoorTagBit_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTagDB_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTagDB_text.setObjectName(u"mouthDoorTagDB_text")
        self.mouthDoorTagDB_text.setGeometry(QtCore.QRect(265, 329, 41, 21))
        self.mouthDoorTagDB_text.setFont(font8)
        self.mouthDoorTagDB_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.mouthDoorTagByte_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTagByte_text.setObjectName(u"mouthDoorTagByte_text")
        self.mouthDoorTagByte_text.setGeometry(QtCore.QRect(360, 330, 41, 21))
        self.mouthDoorTagByte_text.setFont(font8)
        self.mouthDoorTagByte_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
  
        self.mouthDoorTagBorder2 = QLabel(self.setting_frame)
        self.mouthDoorTagBorder2.setObjectName(u"mouthDoorTagBorder2")
        self.mouthDoorTagBorder2.setGeometry(QtCore.QRect(510, 322, 201, 31))
        self.mouthDoorTagBorder2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.mouthDoorTagBorder2.setAlignment(Qt.AlignCenter)      
        
        self.mouthDoorTagTagName_label = QLabel(self.setting_frame)
        self.mouthDoorTagTagName_label.setObjectName(u"mouthDoorTagTagName_label")
        self.mouthDoorTagTagName_label.setGeometry(QtCore.QRect(514, 327, 71, 20))
        self.mouthDoorTagTagName_label.setFont(font7)
        self.mouthDoorTagTagName_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.mouthDoorTagTagName_label.setAlignment(Qt.AlignCenter)
        
        self.mouthDoorTagTagName_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTagTagName_text.setObjectName(u"mouthDoorTagTagName_text")
        self.mouthDoorTagTagName_text.setGeometry(QtCore.QRect(589, 328, 111, 21))
        self.mouthDoorTagTagName_text.setFont(font8)
        self.mouthDoorTagTagName_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        
        self.mouthDoorTagLED = QLabel(self.setting_frame)
        self.mouthDoorTagLED.setObjectName(u"mouthDoorTagLED")
        self.mouthDoorTagLED.setGeometry(QtCore.QRect(724, 329, 31, 21))
        self.mouthDoorTagLED.setStyleSheet(u"")

        self.saveConf_label = QLabel(self.setting_widget)
        self.saveConf_label.setObjectName(u"saveConf_label")
        self.saveConf_label.setGeometry(QtCore.QRect(290, 651, 201, 41))
        self.saveConf_label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.saveCong_pushButton = QPushButton(self.setting_widget)
        self.saveCong_pushButton.setObjectName(u"saveCong_pushButton")
        self.saveCong_pushButton.setGeometry(QtCore.QRect(300, 660, 181, 21))
        self.saveCong_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        # Set the style for normal and hover state
        self.saveCong_pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 75 12pt \"Arial\";
                border-color: rgb(0, 0, 0);;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.saveCong_pushButton.clicked.connect(self.__on_saveConf_button)
        
        
        
        # Header Widget
        self.header_widget = QWidget(self.border_widget)
        self.header_widget.setObjectName(u"header_widget")
        self.header_widget.setGeometry(QtCore.QRect(10, 10, 1601, 81))
        self.header_widget.setStyleSheet(u"border: 1px solid white;\n"
"border-color: rgb(220, 220, 240);\n"
"background-color: rgb(220, 220, 240);")
        self.header_title = QLabel(self.header_widget)
        self.header_title.setObjectName(u"header_title")
        self.header_title.setGeometry(QtCore.QRect(300, 24, 1000, 31))
        sizePolicy.setHeightForWidth(self.header_title.sizePolicy().hasHeightForWidth())
        self.header_title.setSizePolicy(sizePolicy)
        self.header_title.setFont(font0)
        self.header_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.danieli_label = QLabel(self.header_widget)
        self.danieli_label.setObjectName(u"danieli_label")
        self.danieli_label.setGeometry(QtCore.QRect(-2, 0, 141, 81))
        self.danieli_label.setStyleSheet(u"border-color: rgb(220, 220, 240);\n")
        self.danieli_label.setText("")
        self.danieli_label.setObjectName("danieli_label")
        self.danieli_logo_image = cv2.resize(self.danieli_logo_image, (141, 81))
        logo_height, logo_width, logo_channel = self.danieli_logo_image.shape   
        logo_bytes_per_line = 3 * logo_width
        logo_frame_rgb = cv2.cvtColor(self.danieli_logo_image, cv2.COLOR_BGR2RGB)
        logo_q_img = QImage(logo_frame_rgb.data, logo_width, logo_height, logo_bytes_per_line, QImage.Format_RGB888)
        logo_pixmap = QPixmap.fromImage(logo_q_img)  
        self.danieli_label.setPixmap(logo_pixmap)      
        
        
        
        self.video_widget.raise_()
        self.setting_widget.raise_()
        self.footer_widget.raise_()
        mouthProtectionWinow.setCentralWidget(self.centralwidget)
        self.border_widget.raise_()
        self.header_widget.raise_()
        self.menubar = QtWidgets.QMenuBar(mouthProtectionWinow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1680, 21))
        mouthProtectionWinow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mouthProtectionWinow)
        self.statusbar.setObjectName(u"statusbar")
        mouthProtectionWinow.setStatusBar(self.statusbar)

        self.retranslateUi(mouthProtectionWinow)
        QtCore.QMetaObject.connectSlotsByName(mouthProtectionWinow)
        
        # Initialize the QtWidgets.QDateTimeEdit with the current date and time
        current_datetime = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(current_datetime)  
        self.url = self.cameraUrl_line.text()

        # Updating frames within loop
        self.timer = QTimer(mouthProtectionWinow)      
        self.timer.timeout.connect(self.update_video)
        self.timer.start(5)        # update frame every (1000//(self.ps = 1000)  = 1 ms)   second(s)
     


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Danieli Mouth Protectoion Application", u"Danieli Mouth Protectoion Application", None))
        self.header_title.setText(_translate("Danieli Mouth Protectoion Application", u"DANIELI PRESS MOUTH PROTECTION", None))
        self.danieli_label.setText("")
        self.footer_title.setText(_translate("Danieli Mouth Protectoion Application", u"System Logs", None))
        self.textEdit.setHtml(_translate("Danieli Mouth Protectoion Application", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sdsdsd<br />sdsdsd</p></body></html>", None))
        self.video_title.setText(_translate("Danieli Mouth Protectoion Application", u"Live View", None))
        # self.video_label.setText(_translate("Danieli Mouth Protectoion Application", u"put here the live video frame", None))
        self.record_label.setText("")
        self.record_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Record", None))
        self.continue_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Continue", None))
        self.stop_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Stop", None))
        self.pause_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Pause", None))
        self.activtaeRecording_checkBox.setText(_translate("Danieli Mouth Protectoion Application", u"Activate Manual Recording ", None))
        self.setting_title.setText(_translate("Danieli Mouth Protectoion Application", u"Settings", None))
        self.cameraUrl_label.setText(_translate("Danieli Mouth Protectoion Application", u"Camera URL", None))
        self.cameraUrl_line.setText("rtsp://192.168.1.100:554/stream2")
   
        self.prmRecPath_text.setText("E:\Danieli Breda\Extrusion Press\Automation\Apps\mouth-protection\Recorded_videos")
        self.prmRecPath_label.setText(_translate("Danieli Mouth Protectoion Application", u"Primary recording path", None))
        self.plcIp_text.setText("")
        self.secRecPath_label.setText(_translate("Danieli Mouth Protectoion Application", u"Secondary recording path (local only)", None))
        self.plcIp_label.setText(_translate("Danieli Mouth Protectoion Application", u"PLC IP address", None))
#if QT_CONFIG(tooltip)
        self.primPath_checkBox.setToolTip(_translate("Danieli Mouth Protectoion Application", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.primPath_checkBox.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.primPath_checkBox.setText(_translate("Danieli Mouth Protectoion Application", u"      Select ", None))
#if QT_CONFIG(tooltip)
        self.secondPath_checkBox.setToolTip(_translate("Danieli Mouth Protectoion Application", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.secondPath_checkBox.setText(_translate("Danieli Mouth Protectoion Application", u"      Select ", None))
        self.comboBox.setItemText(0, _translate("Danieli Mouth Protectoion Application", u"Siemens", None))
        self.comboBox.setItemText(1, _translate("Danieli Mouth Protectoion Application", u"Allen Bradly", None))

        self.plctype_label.setText(_translate("Danieli Mouth Protectoion Application", u"PLC Type", None))
        self.secRecPath_text.setText("")
        self.billetNumberTagDB_text.setText("63")
        self.billetNumberTagTitle_label.setText(_translate("Danieli Mouth Protectoion Application", u"Billet No. tag", None))
        self.billetNumberTagBit_label.setText(_translate("Danieli Mouth Protectoion Application", u"Bit:", None))
        self.billetNumberTagByte_text.setText("6")
        self.billetNumberTagBit_text.setText("0")
        self.billetNumberTagTagName_label.setText(_translate("Danieli Mouth Protectoion Application", u"Tag Name:", None))
        self.billetNumberTagDB_label.setText(_translate("Danieli Mouth Protectoion Application", u"Data Block Number:", None))
        self.billetNumberTagByte_label.setText(_translate("Danieli Mouth Protectoion Application", u"Byte:", None))
        self.billetNumberTagTagName_text.setText("Billet_Number")
        # self.billetNumberTagBorder1.setText("")
        self.billetNumberTagBorder2.setText("")
        self.dieCodeTagTitle_label.setText(_translate("Danieli Mouth Protectoion Application", u"Die code tag", None))
        self.dieCodeTagBorder1.setText("")
        self.dieCodeTagDB_label.setText(_translate("Danieli Mouth Protectoion Application", u"Data Block Number:", None))
        self.dieCodeTagTagName_label.setText(_translate("Danieli Mouth Protectoion Application", u"Tag Name:", None))
        self.dieCodeTagByte_label.setText(_translate("Danieli Mouth Protectoion Application", u"Byte:", None))
        self.dieCodeTagBit_label.setText(_translate("Danieli Mouth Protectoion Application", u"Bit:", None))
        self.dieCodeTagDB_text.setText("63")
        self.dieCodeTagBit_text.setText("0")
        self.dieCodeTagByte_text.setText("2")
        self.dieCodeTagBorder2.setText("")
        self.dieCodeTagTagName_text.setText("Die_Code")
        self.heartBeatTagBorder1.setText("")
        self.extrusionTagBorder1.setText("")
        self.extrusionTagDB_label.setText(_translate("Danieli Mouth Protectoion Application", u"Data Block Number:", None))
        self.extrusionTagBorder2.setText("")
        self.mouthDoorTagBorder2.setText("")
        self.heartBeatTagBorder2.setText("")
        self.extrusionTagTagName_label.setText(_translate("Danieli Mouth Protectoion Application", u"Tag Name:", None))
        self.extrusionTagTitle_label.setText(_translate("Danieli Mouth Protectoion Application", u"Exrusion Tag", None))
        self.heartBeatTagTitle_label.setText(_translate("Danieli Mouth Protectoion Application", u"Heartbeat tag", None))
        self.heartBeatTagDB_text.setText("63")
        self.heartBeatTagBit_text.setText("4")
        self.heartBeatTagByte_text.setText("0")
        self.heartBeatTagBit_label.setText(_translate("Danieli Mouth Protectoion Application", u"Bit:", None))
        self.heartBeatTagTagName_text.setText("Heart_Beat")
        self.heartBeatTagTagName_label.setText(_translate("Danieli Mouth Protectoion Application", u"Tag Name:", None))
        self.extrusionTagDB_text.setText("63")
        self.heartBeatTagDB_label.setText(_translate("Danieli Mouth Protectoion Application", u"Data Block Number:", None))
        self.heartBeatTagLED.setText("")
        self.heartBeatTagByte_text.setText("")
        self.extrusionTagByte_label.setText(_translate("Danieli Mouth Protectoion Application", u"Byte:", None))
        self.extrusionTagBit_label.setText(_translate("Danieli Mouth Protectoion Application", u"Bit:", None))
        self.heartBeatTagByte_label.setText(_translate("Danieli Mouth Protectoion Application", u"Byte:", None))
        self.extrusionTagBit_text.setText("3")
        self.extrusionTagByte_text.setText("0")
        self.extrusionTagTagName_text.setText("Extrusion_Run")
        self.heartBeatTagByte_text.setText("0")
        self.heartBeatTagBit_text.setText("4")
        self.extrusionTagLED.setText("")
        self.mouthDoorTagBorder1.setText("")
        self.mouthDoorTagDB_label.setText(_translate("Danieli Mouth Protectoion Application", u"Data Block Number:", None))
        self.mouthDoorTagTitle_label.setText(_translate("Danieli Mouth Protectoion Application", u"Mouth DoorTag", None))
        self.mouthDoorTagLED.setText("")
        self.mouthDoorTagTagName_text.setText("Mouth_Door")
        self.mouthDoorTagBit_text.setText("2")
        self.mouthDoorTagByte_label.setText(_translate("Danieli Mouth Protectoion Application", u"Byte:", None))
        self.mouthDoorTagBit_label.setText(_translate("Danieli Mouth Protectoion Application", u"Bit:", None))
        self.mouthDoorTagDB_text.setText("63")
        self.mouthDoorTagByte_text.setText("0")
        self.mouthDoorTagTagName_label.setText(_translate("Danieli Mouth Protectoion Application", u"Tag Name:", None))
        self.plcIp_text.setText("192.168.1.1")
        
        self.saveCong_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Save Configuration", None))
        self.saveConf_label.setText("")


    # Reading Tags's Values in PLC
    def ReadDataBlock(self, plc, data_block_number, byte, bit, size, data_type):
        """
        plc
        data-block(int): number of Data Block; DB1, DB2, ...
        byte(int): in case of 2.0, byte is 2.
        bit(int): in case of 2.0,bit is 0.
        size(int): The size of the db data to read  
        data_type(variable): S7WLBit, S7WLWord, S7WLReal, S7WLDDword 

        """
        result = plc.db_read(data_block_number, byte, size)
        if data_type == S7WLBit:
            return get_bool(result, 0, bit)
        elif data_type == S7WLByte or data_type == S7WLWord:
            return get_int(result, 0)
        elif data_type == S7WLReal:
            return get_real(result, 0)  
        elif data_type == S7WLDWord:
            return get_word(result, 0)
        elif data_type == S7WLDInt:
            return get_dint(result, 0)
        else:
            return None  


    def __on_record_button(self):
        self.manl_start_record = True
        self.manl_stop_record = False
        # Defining for the Video Recorder   
        self.manl_fourcc = cv2.VideoWriter_fourcc(*'XVID')    
        start_record_time = str(datetime.now()).replace(":", "").replace(" ", "_")  
        print(self.folder_dir + "/" + "Die" + str(self.dieCode_tag) + "_" + "Billet" + str(self.billetNumber_tag) + "_" + start_record_time[:17 ] + ".avi")
        self.manl_video_path = self.folder_dir + "/" + "Die" + str(self.dieCode_tag) + "_" + "Billet" + str(self.billetNumber_tag) + "_" + start_record_time[:17 ] + ".avi"    
        self.manl_out = cv2.VideoWriter(self.manl_video_path,self.manl_fourcc, 20,  (691, 641))

    def __on_stop_button(self):
        self.manl_stop_record = True
        self.manl_start_record = False
        self.manl_pause_record = False
        self.manl_continue_record = False
            
    def __on_continue_button(self):
        self.manl_continue_record = True
        self.manl_pause_record = False
        self.manl_start_record = True
        self.recording = True

    def __on_pause_button(self):
        self.manl_pause_record = True
        self.manl_continue_record = False  
        self.manl_start_record = False
        self.recording = False

    def __on_saveConf_button(self):
        self.save_configuration = True   
        self.__initCommunication()
        # Defining the recording directory
        if int(self.primPath_checkBox.checkState()) ==  2:   # 2: True, 0: False
                self.folder_dir = self.prmRecPath_text.text()
        elif int(self.secondPath_checkBox.checkState()) ==  2:
                self.folder_dir = self.secRecPath_text.text()
        # Initializing the caps
        self.cap = cv2.VideoCapture(self.url)  
        self.cap.set(cv2.CAP_PROP_FPS, 20)
    
    
    def __plc_show_warning_messagebox(self, error_string, plc_type_string): 
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Warning) 
        # setting message for Message Box 
        msg.setText(error_string + "\nPlease check again inserted properties!") 
        # setting Message box window title 
        msg.setWindowTitle(f"{plc_type_string} PLC Connection") 
        # declaring buttons on Message Box 
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
        self.save_configuration = False
        # start the app 
        retval = msg.exec_() 
        

    def __camera_show_warning_messagebox(self):
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Warning) 
        # setting message for Message Box 
        msg.setText("Camera Connection aborted. \nPlease check again inserted properties!") 
        # setting Message box window title 
        msg.setWindowTitle("Camera Connection") 
        # declaring buttons on Message Box 
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
        self.save_configuration = False
        # start the app 
        retval = msg.exec_()     
        
    
    def update_video(self):
        # Activate Manual Recording
        if int(self.activtaeRecording_checkBox.checkState()) ==  2:   # 2: True, 0: False
            self.record_pushButton.setGraphicsEffect(None)
            self.continue_pushButton.setGraphicsEffect(None)
            self.pause_pushButton.setGraphicsEffect(None)
            self.stop_pushButton.setGraphicsEffect(None)
            # Enabling recording pushbuttons
            self.record_pushButton.setEnabled(True)
            self.continue_pushButton.setEnabled(True)
            self.pause_pushButton.setEnabled(True)
            self.stop_pushButton.setEnabled(True)
        # Deactivate Manual Recording     
        else:
            # Blur effect for the pushbutton
            self.blur_effect_record = QGraphicsBlurEffect()
            self.blur_effect_record.setBlurRadius(2)
            self.blur_effect_continue = QGraphicsBlurEffect()
            self.blur_effect_continue.setBlurRadius(2)
            self.blur_effect_pause = QGraphicsBlurEffect()
            self.blur_effect_pause.setBlurRadius(2)
            self.blur_effect_stop = QGraphicsBlurEffect()
            self.blur_effect_stop.setBlurRadius(2)
            self.record_pushButton.setGraphicsEffect(self.blur_effect_record)
            self.continue_pushButton.setGraphicsEffect(self.blur_effect_continue)
            self.pause_pushButton.setGraphicsEffect(self.blur_effect_pause)
            self.stop_pushButton.setGraphicsEffect(self.blur_effect_stop)
            # Disabling recording pushbuttons
            self.record_pushButton.setEnabled(False)
            self.continue_pushButton.setEnabled(False)
            self.pause_pushButton.setEnabled(False)
            self.stop_pushButton.setEnabled(False)

        # Show Setting Frame
        if int(self.showSettingFrame_checkBox.checkState()) ==  2:   # 2: True, 0: False
             self.setting_frame.setDisabled(False)
             self.setting_frame.setGraphicsEffect(None)  

        # Hide Setting Frame
        else:
             self.setting_frame.setDisabled(True)
             self.blur_effect_setting_frame = QGraphicsBlurEffect()
             self.blur_effect_setting_frame.setBlurRadius(2)
             self.setting_frame.setGraphicsEffect(self.blur_effect_setting_frame)

        
        if self.save_configuration == True:
            if self.plc_type == "Siemens":
                self.update_video_SiemensPlc()
            elif self.plc_type == "Allen Bradly":
                self.update_video_AllenBradlyPlc()
                if not self.client:
                    self.client.__exit__(None, None, None)  # Ensure resources are released
                

    ### Live Video Stream Analyser: Siemens
    def update_video_SiemensPlc(self):
        try:
                start_time = time.time()

                # Reading variables from the plc
                self.mouth_door_tag = self.ReadDataBlock(self.client, int(self.mouthDoorTagDB_text.text()), int(self.mouthDoorTagByte_text.text()), int(self.mouthDoorTagBit_text.text()), 1, S7WLBit)
                self.extrusion_tag = self.ReadDataBlock(self.client, int(self.extrusionTagDB_text.text()), int(self.extrusionTagByte_text.text()), int(self.extrusionTagBit_text.text()), 1, S7WLBit)           
                self.heartbeat_tag = self.ReadDataBlock(self.client, int(self.heartBeatTagDB_text.text()), int(self.heartBeatTagByte_text.text()), int(self.heartBeatTagBit_text.text()), 1, S7WLBit) 
                self.dieCode_tag = self.ReadDataBlock(self.client, int(self.dieCodeTagDB_text.text()), int(self.dieCodeTagByte_text.text()), int(self.dieCodeTagBit_text.text()), 4, S7WLDInt) 
                self.billetNumber_tag = self.ReadDataBlock(self.client, int(self.billetNumberTagDB_text.text()), int(self.billetNumberTagByte_text.text()), self.billetNumberTagBit_text.text(), 4, S7WLDInt) 
                                 
                # Read a frame from the stream 
                ret, frame = self.cap.read()
                if ret:
                        print("---------------------------------------------------------------------------------------------------------------")
                        image = self.process_frame(frame)                       
                        # Display the processed frame and variables in the GUI   
                        self.display_frame(image)   
                else:
                        self.__camera_show_warning_messagebox()      
                end_time = time.time()      
                # Modify the frame and calculate result and reference_time as needed
                reference_time = end_time - start_time 
                print("Reference Time:        {:.3f} (seconds)".format(reference_time))
                self.display_variables(reference_time)       
        except Exception as err:
                self.__plc_show_warning_messagebox(str(err), str(self.plc_type))
            


    ### Live Video Stream Analyser: Allen Bradly
    def update_video_AllenBradlyPlc(self):
        try:
            start_time = time.time()
                
            # Reading variables from the plc
            self.mouth_door_tag = (self.client.read(str(self.mouthDoorTagTagName_text.text()))).value  
            self.extrusion_tag = (self.client.read(str(self.extrusionTagTagName_text.text()))).value  
            self.heartbeat_tag = (self.client.read(str(self.heartBeatTagTagName_text.text()))).value  
            self.dieCode_tag = (self.client.read(str(self.dieCodeTagTagName_text.text()))).value  
            self.billetNumber_tag = (self.client.read(str(self.billetNumberTagTagName_text.text()))).value  
            
            
            # Read a frame from the stream
            ret, frame = self.cap.read()
            if ret:
                print("---------------------------------------------------------------------------------------------------------------")
                image = self.process_frame(frame)                       
                # Display the processed frame and variables in the GUI   
                self.display_frame(image)   
            else:
                self.__camera_show_warning_messagebox()            
            end_time = time.time()      
            # Modify the frame and calculate result and reference_time as needed
            reference_time = end_time - start_time 
            print("Reference Time:        {:.3f} (seconds)".format(reference_time))
            self.display_variables(reference_time)        
        except CommError as err:
            self.__plc_show_warning_messagebox(str(err), str(self.plc_type))

            

            

    def process_frame(self, frame):    
        # updating the time and date
        current_datetime = QDateTime.currentDateTime()      
        self.dateTimeEdit.setDateTime(current_datetime)
        
        if self.mouth_door_tag == True:
            self.mouthDoorTagLED.setStyleSheet("background-color: green; border-radius: 15px;")
        else:
            self.mouthDoorTagLED.setStyleSheet("background-color: red; border-radius: 15px;")
        
        if self.extrusion_tag == True:
            self.extrusionTagLED.setStyleSheet("background-color: green; border-radius: 15px;")
        else:
            self.extrusionTagLED.setStyleSheet("background-color: red; border-radius: 15px;")    
        
        if self.heartbeat_tag == True:
            self.heartBeatTagLED.setStyleSheet("background-color: green; border-radius: 15px;")
        else:
            self.heartBeatTagLED.setStyleSheet("background-color: red; border-radius: 15px;")     
        
        
        image = cv2.resize(frame, (691, 641))   # resize to the defined image_size        
        print(f"Manual Start: {self.manl_start_record}, Manual stop: {self.manl_stop_record}")
        print(f"Automatic Start: {self.auto_start_record}, Automatic stop: {self.auto_stop_record}")
        
        # Manual Recording
        if (self.manl_start_record == True) & (self.manl_stop_record == False):
            print("*****************************   Manual Recording is happening ")
            self.recording = True
            print("Writting Enable.") 
            self.manl_out.write(image)
        
        if self.manl_stop_record == True:
            self.manl_out.release()
            self.recording = False
            self.manl_start_record = False
        
        if self.manl_pause_record == True:
            self.recording = False

        if self.manl_continue_record == True:
            self.recording = True

        # Automatic Recording
        if (self.mouth_door_tag == True) & (self.extrusion_tag == True):
            if self.first_auto_record_img == True:
                self.record_timer = time.time()    
                self.auto_start_record = True
                self.auto_stop_record = False
                # Defining for the Video Recorder   
                self.auto_fourcc = cv2.VideoWriter_fourcc(*'XVID')    
                start_record_time = str(datetime.now()).replace(":", "").replace(" ", "_")  
                print(self.folder_dir + "/" + "Die" + str(self.dieCode_tag) + "_" + "Billet" + str(self.billetNumber_tag) + "_" + start_record_time[:17 ] + ".avi")
                self.auto_video_path = self.folder_dir + "/" + "Die" + str(self.dieCode_tag) + "_" + "Billet" + str(self.billetNumber_tag) + "_" + start_record_time[:17 ] + ".avi"     
                self.auto_out = cv2.VideoWriter(self.auto_video_path,self.auto_fourcc, 20,  (691, 641)) 
                self.first_auto_record_img = False
            print("*****************************   Auto Recording is happening ")
            self.recording = True
            print("Writting Enable.") 
            self.auto_out.write(image)     

        if self.auto_start_record:
            if (self.mouth_door_tag == False) | (self.record_timer - (time.time()) > self.record_timer_limit):
                    self.auto_start_record = False     
                    self.auto_stop_record = True
                    self.auto_out.release()
                    self.first_auto_record_img = True
                    self.recording = False
        return image
    
    
    

    # display the opencv BGR image into the defined lables in Qt Designer.
    def display_frame(self, frame):  
        height, width, channel = frame.shape   
        bytes_per_line = 3 * width
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)   

    # Display variables Function .
    def display_variables(self, reference_time):    
        pass        
        self.textEdit.setText(" Reference time:    {:.3f}\n PLC {}:    {} \n " 
                               "Recording Status:    {}".format(reference_time, self.plc_type, self.plc_ip_address, self.recording))
        

    def closeEvent(self, event):  
        self.video_capture.release()
        event.accept()      


#********************************************************************************************************************************************************
def main():
    
    fps = 800
                                                          
    app = QApplication(sys.argv)                       
    mouthProtectionWinow = QtWidgets.QMainWindow()   
    mouthProtection = MouthProtectionApp(fps)
    mouthProtection.initUI(mouthProtectionWinow)
    mouthProtectionWinow.show()    
    sys.exit(app.exec_())  
    

if __name__ == "__main__":                                      
    main()
    
    
    
    
             
    
    





