## Importing Packages
# Built-in standard packages
import sys
import datetime
import time
import os

# opencv package
import cv2

# PyQT5 Packages
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QCommandLinkButton, QTabWidget, QPushButton, QVBoxLayout, QDialog, QLabel, QSizePolicy, QWidget, QLayout, QGraphicsBlurEffect, QInputDialog, QLineEdit
from PyQt5.QtGui import QImage, QPixmap, QPainter, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTimer, Qt, QSize   
from PyQt5.uic import loadUi

# Defining the plc communication packages
from pycomm3 import LogixDriver 
import snap7 
from snap7 import *
from snap7.util import *
from snap7.types import *




class MouthProtectionApp():                  
                                            
    defined_plc_types = ["Siemens", "AllenBradly"]
    def __init__(self, video_dir, fps, plc_type):
            
        # video recorder parameters    
        self.fps = fps  
        self.folder_dir = ""
        self.record_timer_limit = 300  # 5 (min) = 300 (s) 
        self.first_auto_record_img = True
        self.recording = False

        # Plc Communication 
        self.plc_type = plc_type
        self.plc_connection = False
        self.ToPlc_Watchdog = False
        self.FromPlc_Watchdog = False
        self.WatchdogFromPlcMem = False   
        self.watchdog_counter = 0
        self.ToPlc_Result = 0                
        self.Plc_Jetson_Communication = False 
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
        

    def initCommunication(self):    
        self.plc_type = str(self.comboBox.currentText())
        self.plc_ip_address = self.plcIp_text.text()   

        # Siemens PLC 
        try:        
            if (self.plc_type == "Siemens"):    
                self.client = snap7.client.Client()
                self.client.connect(self.plcIp_text.text(), 0, 1) 
                print("Connection to Siemens PLC is okay!")
                self.plc_connection = True
            else: 
                self.client = LogixDriver(self.plcIp_text.text())
                self.client.__enter__()  # Explicitly enter the context
                print("Connection to AllenBradly PLC is okay!")
                self.plc_connection = True
        except Exception as e:
            print(f"Error:   {e}")  
             
        # Allen Bradly
        if (self.plc_type == "Allen Bradly"):  
            with LogixDriver(self.plcIp_text.text()) as plc:
                if plc.connected:
                    print("Connection to Allen Bradly PLC is okay!")
                else:
                    print("Failed to connect to the Allen Bradly PLC.")
            
        
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
        # Blur effect for the pushbutton
        self.blur_effect_record = QGraphicsBlurEffect()
        self.blur_effect_record.setBlurRadius(2)
        self.blur_effect_continue = QGraphicsBlurEffect()
        self.blur_effect_continue.setBlurRadius(2)
        self.blur_effect_pause = QGraphicsBlurEffect()
        self.blur_effect_pause.setBlurRadius(2)
        self.blur_effect_stop = QGraphicsBlurEffect()
        self.blur_effect_stop.setBlurRadius(2)
        

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
        # # Connect the checkbox stateChanged signal to the slot
        # self.activtaeRecording_checkBox.stateChanged.connect(self.show_password_dialog)
        
        
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
        self.prmRecPath_text.setFont(font2)
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
        self.plcIp_text.setGeometry(QtCore.QRect(390, 305, 361, 30))
        self.plcIp_text.setFont(font2)
        self.plcIp_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_label = QLabel(self.setting_frame)
        self.secRecPath_label.setObjectName(u"secRecPath_label")
        self.secRecPath_label.setGeometry(QtCore.QRect(20, 141, 731, 31))
        self.secRecPath_label.setFont(font2)
        self.secRecPath_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.secRecPath_label.setAlignment(Qt.AlignCenter)
        self.plcIp_label = QLabel(self.setting_frame)
        self.plcIp_label.setObjectName(u"plcIp_label")
        self.plcIp_label.setGeometry(QtCore.QRect(390, 273, 361, 31))
        self.plcIp_label.setFont(font2)
        self.plcIp_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plcIp_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTag_text.setObjectName(u"extrusionTag_text")
        self.extrusionTag_text.setGeometry(QtCore.QRect(20, 462, 731, 30))
        self.extrusionTag_text.setFont(font2)
        self.extrusionTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartbeatTag_label = QLabel(self.setting_frame)
        self.heartbeatTag_label.setObjectName(u"heartbeatTag_label")
        self.heartbeatTag_label.setGeometry(QtCore.QRect(20, 510, 731, 31))
        self.heartbeatTag_label.setFont(font2)
        self.heartbeatTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartbeatTag_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTag_text.setObjectName(u"mouthDoorTag_text")
        self.mouthDoorTag_text.setGeometry(QtCore.QRect(20, 387, 731, 30))
        self.mouthDoorTag_text.setFont(font2)
        self.mouthDoorTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.MouthDoorTag_label = QLabel(self.setting_frame)
        self.MouthDoorTag_label.setObjectName(u"MouthDoorTag_label")
        self.MouthDoorTag_label.setGeometry(QtCore.QRect(20, 356, 731, 31))
        self.MouthDoorTag_label.setFont(font2)
        self.MouthDoorTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.MouthDoorTag_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_label = QLabel(self.setting_frame)
        self.extrusionTag_label.setObjectName(u"extrusionTag_label")
        self.extrusionTag_label.setGeometry(QtCore.QRect(20, 431, 731, 31))
        self.extrusionTag_label.setFont(font2)
        self.extrusionTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTag_label.setAlignment(Qt.AlignCenter)
        self.heartbeatTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartbeatTag_text.setObjectName(u"heartbeatTag_text")
        self.heartbeatTag_text.setGeometry(QtCore.QRect(20, 540, 731, 30))
        self.heartbeatTag_text.setFont(font2)
        self.heartbeatTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_text = QtWidgets.QTextEdit(self.setting_frame)
        self.secRecPath_text.setObjectName(u"secRecPath_text")
        self.secRecPath_text.setGeometry(QtCore.QRect(20, 171, 621, 61))
        self.secRecPath_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";")
        self.primPath_checkBox = QtWidgets.QCheckBox(self.setting_frame)
        self.primPath_checkBox.setObjectName(u"primPath_checkBox")
        self.primPath_checkBox.setGeometry(QtCore.QRect(640, 101, 111, 30))
        self.primPath_checkBox.setFont(font5)
        self.primPath_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.primPath_checkBox.setChecked(True) 
        self.secondPath_checkBox = QtWidgets.QCheckBox(self.setting_frame)
        self.secondPath_checkBox.setObjectName(u"secondPath_checkBox")
        self.secondPath_checkBox.setGeometry(QtCore.QRect(640, 171, 111, 61))
        self.secondPath_checkBox.setFont(font5)
        self.secondPath_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.secondPath_checkBox.setChecked(False) 
        self.comboBox = QtWidgets.QComboBox(self.setting_frame)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(30, 305, 241, 31))
        self.comboBox.setFont(font4)
        self.comboBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.comboBox.setCurrentText("Siemens") 
        self.plctype_label = QLabel(self.setting_frame)
        self.plctype_label.setObjectName(u"plctype_label")
        self.plctype_label.setGeometry(QtCore.QRect(20, 273, 251, 31))
        self.plctype_label.setFont(font2)
        self.plctype_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plctype_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTagLED = QLabel(self.setting_frame)
        self.mouthDoorTagLED.setObjectName(u"mouthDoorTagLED")
        self.mouthDoorTagLED.setGeometry(QtCore.QRect(680, 387, 71, 30))
        self.extrusionTagLED = QLabel(self.setting_frame)
        self.extrusionTagLED.setObjectName(u"extrusionTagLED")
        self.extrusionTagLED.setGeometry(QtCore.QRect(680, 462, 71, 30))
        self.HeartbeatTagLED = QLabel(self.setting_frame)
        self.HeartbeatTagLED.setObjectName(u"HeartbeatTagLED")
        self.HeartbeatTagLED.setGeometry(QtCore.QRect(680, 540, 71, 30))
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
        self.prmRecPath_text.setText("E:\Danieli Breda\Extrusion Press\Automation\mouth-protection\Recorded_videos")
        self.prmRecPath_label.setText(_translate("Danieli Mouth Protectoion Application", u"Primary recording path", None))
        self.primPath_checkBox.setText(_translate("Danieli Mouth Protectoion Application", u"Check", None))
        self.plcIp_text.setText("192.168.1.1")
        self.secRecPath_label.setText(_translate("Danieli Mouth Protectoion Application", u"Secondary recording path (local only)", None))
        self.secondPath_checkBox.setText(_translate("Danieli Mouth Protectoion Application", u"Check", None))
        self.plcIp_label.setText(_translate("Danieli Mouth Protectoion Application", u"PLC IP address", None))
        self.plctype_label.setText(_translate("Danieli Mouth Protectoion Application", u"PLC Type", None))
        self.comboBox.setItemText(0, _translate("Danieli Mouth Protectoion Application", u"Siemens", None))
        self.comboBox.setItemText(1, _translate("Danieli Mouth Protectoion Application", u"Allen Bradly", None))
        self.extrusionTag_text.setText("")
        self.heartbeatTag_label.setText(_translate("Danieli Mouth Protectoion Application", u"Heartbeat tag", None))
        self.mouthDoorTag_text.setText("")
        self.MouthDoorTag_label.setText(_translate("Danieli Mouth Protectoion Application", u"Mouth door tag", None))
        self.extrusionTag_label.setText(_translate("Danieli Mouth Protectoion Application", u"Extrusion tag", None))
        self.heartbeatTag_text.setText("")
        self.secRecPath_text.setHtml(_translate("Danieli Mouth Protectoion Application", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ukjjojkuj,</p></body></html>", None))
        self.saveCong_pushButton.setText(_translate("Danieli Mouth Protectoion Application", u"Save Configuration", None))
        self.saveConf_label.setText("")
        self.mouthDoorTagLED.setText("")
        self.extrusionTagLED.setText("")
        self.HeartbeatTagLED.setText("")
        

    # def show_password_dialog(self, state):
    #     if state == 2:  # Checkbox is checked
    #         # Show a password input dialog
    #         password, ok = QInputDialog.getText(self, "Enter Password", "Password:")
            
    #         if ok and password:
    #             QMessageBox.information(self, "Password Entered", "Password accepted.")
    #         else:
    #             # Uncheck the checkbox if no password is entered or dialog is cancelled
    #             self.checkbox.setChecked(False)
    #     else:
    #         QMessageBox.information(self, "Checkbox Unchecked", "Checkbox was unchecked.")
                    

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
        self.initCommunication()
        # Defining the recording directory
        if int(self.primPath_checkBox.checkState()) ==  2:   # 2: True, 0: False
                self.folder_dir = self.prmRecPath_text.text()
        elif int(self.secondPath_checkBox.checkState()) ==  2:
                self.folder_dir = self.secRecPath_text.text()
        # Initializing the cap
        self.cap = cv2.VideoCapture(self.url)  
        self.cap.set(cv2.CAP_PROP_FPS, 20)
    
    
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
            
        if self.save_configuration == True:
            if self.plc_type == "Siemens":
                self.update_video_SiemensPlc()
            elif self.plc_type == "Allen Bradly":
                self.update_video_AllenBradlyPlc()
                if not self.client:
                    self.client.__exit__(None, None, None)  # Ensure resources are released
                
            

    
    ### Live Video Stream Analyser: Siemens
    def update_video_SiemensPlc(self):
        start_time = time.time()
        
        # Reading variables from the plc
        self.mouth_door_tag = self.ReadDataBlock(self.client, 63, 0, 2, 1, S7WLBit)
        self.extrusion_tag = self.ReadDataBlock(self.client, 63, 0, 3, 1, S7WLBit)           
        self.heartbeat_tag = self.ReadDataBlock(self.client, 63, 0, 4, 1, S7WLBit) 
        self.dieCode_tag = self.ReadDataBlock(self.client, 63, 2, 0, 4, S7WLDInt) 
        self.billetNumber_tag = self.ReadDataBlock(self.client, 63, 6, 0, 4, S7WLDInt) 
                        
        # Read a frame from the stream 
        ret, frame = self.cap.read()
        if ret:
                print("---------------------------------------------------------------------------------------------------------------")
                image = self.process_frame(frame)                       
                # Display the processed frame and variables in the GUI   
                self.display_frame(image)     
                end_time = time.time()      
                # Modify the frame and calculate result and reference_time as needed
                reference_time = end_time - start_time 
                print("Reference Time:        {:.3f} (seconds)".format(reference_time))
                self.display_variables(reference_time)       



    ### Live Video Stream Analyser: Allen Bradly
    def update_video_AllenBradlyPlc(self):
        start_time = time.time()
        
        # with LogixDriver(self.plc_ip_address) as plc:   // comment this Line
 
        # Reading variables from the plc
        self.mouth_door_tag = (self.client.read('Mouth_Door')).value  
        self.extrusion_tag = (self.client.read('Extrusion_Run')).value  
        self.heartbeat_tag = (self.client.read('Heart_Beat')).value  
        self.dieCode_tag = (self.client.read('Die_Code')).value  
        self.billetNumber_tag = (self.client.read('Billet_Number')).value  
        
        # Read a frame from the stream
        ret, frame = self.cap.read()
        if ret:
                print("---------------------------------------------------------------------------------------------------------------")
                image = self.process_frame(frame)                       
                # Display the processed frame and variables in the GUI   
                self.display_frame(image)     
                end_time = time.time()      
                # Modify the frame and calculate result and reference_time as needed
                reference_time = end_time - start_time 
                print("Reference Time:        {:.3f} (seconds)".format(reference_time))
                self.display_variables(reference_time)        
                
            

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
            self.HeartbeatTagLED.setStyleSheet("background-color: green; border-radius: 15px;")
        else:
            self.HeartbeatTagLED.setStyleSheet("background-color: red; border-radius: 15px;")     
        
        
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

    # Display variables Function 
    def display_variables(self, reference_time):    
        pass        
        self.textEdit.setText(" Reference time:    {:.3f}\n PLC {}:    {} \n " 
                               "Recording Status:    {}".format(reference_time, self.plc_type, self.plc_ip_address, self.recording))
        self.mouthDoorTag_text.setText(str(self.mouth_door_tag))   
        self.extrusionTag_text.setText(str(self.extrusion_tag))           
        self.heartbeatTag_text.setText(str(self.heartbeat_tag))
        

    def closeEvent(self, event):  
        self.video_capture.release()
        event.accept()      


#********************************************************************************************************************************************************
def main():
    
    video_dir = "" 
    fps = 800
    plc_type = "Siemens"   # Siemens or AllenBradly    
                                                          
    app = QApplication(sys.argv)                       
    mouthProtectionWinow = QtWidgets.QMainWindow()   
    mouthProtection = MouthProtectionApp(video_dir, fps, plc_type)
    mouthProtection.initUI(mouthProtectionWinow)
    mouthProtectionWinow.show()    
    sys.exit(app.exec_())  

if __name__ == "__main__":                                      
    main()
    
    
    
    
             
    
    





