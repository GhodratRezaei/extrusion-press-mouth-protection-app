# Importing Packages
import sys
import cv2
import numpy as np  
import time
import os
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QCommandLinkButton, QTabWidget, QPushButton, QVBoxLayout, QDialog, QLabel, QSizePolicy, QWidget, QLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTimer, Qt, QSize   
from PyQt5.uic import loadUi


# # Defining the plc 
from pycomm3 import LogixDriver 
import snap7
import socket

#******************************************************************************************************************************************************************************************************

class MouthProtectionApp():
    
    defined_plc_types = ["TiaPortal", "Rockwell"]
    def __init__(self, video_dir, fps, plc_type):
        self.video_dir = video_dir
        self.fps = fps  
        self.plc_type = plc_type

        
        self.ToPlc_Watchdog = False
        self.FromPlc_Watchdog = False
        self.WatchdogFromPlcMem = False   
        self.watchdog_counter = 0
        self.ToPlc_Result = 0                
        self.Plc_Jetson_Communication = False 

        self.danieli_logo_image = cv2.imread("resources\logo.jpg")
        self.danieli_icon =  "READ the ICON HERE."
        
    #     self.initCommunication()  
          



    # def initCommunication(self):         
    #     assert (self.plc_type in MouthProtectionApp.defined_plc_types) , "Plc Type inserted {} is not among the defined plc variables; {}. please insert the verified plc type.".format(self.plc_type, MouthProtectionApp.defined_plc_types) 
    #     if (self.plc_type == "TiaPortal"):    
    #         self.client = snap7.client.Client()
    #         self.client.connect("PLC IP ADDRESS", 0, 1) 
            
            
             
    
    def initUI(self,mouthProtectionWinow):
        
        
        # Main Window
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
        self.footer_title.setGeometry(QtCore.QRect(670, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.footer_title.sizePolicy().hasHeightForWidth())
        self.footer_title.setSizePolicy(sizePolicy)
        font1 = QtGui.QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(19)
        font1.setBold(False)
        font1.setUnderline(True)
        font1.setWeight(50)
        self.footer_title.setFont(font1)
        self.footer_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.footer_title.setAlignment(Qt.AlignCenter)
        self.textEdit = QtWidgets.QTextEdit(self.footer_widget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QtCore.QRect(30, 46, 1541, 46))
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"font: 10pt \"Segoe UI\";\n"
"border-color: rgb(0, 0, 0);")
        
        
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.footer_widget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QtCore.QRect(1410, 48, 161, 43))
        font2 = QtGui.QFont()
        font2.setFamily(u"MS Shell Dlg 2")
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(50)
        self.dateTimeEdit.setFont(font2)
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
        self.record_label.setGeometry(QtCore.QRect(170, 630, 471, 51))
        self.record_label.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.save_pushButton = QPushButton(self.video_widget)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setGeometry(QtCore.QRect(190, 640, 75, 31))
        font2 = QtGui.QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(9)
        self.save_pushButton.setFont(font2)
        self.save_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"")
        self.start_pushButton = QPushButton(self.video_widget)
        self.start_pushButton.setObjectName(u"start_pushButton")
        self.start_pushButton.setGeometry(QtCore.QRect(310, 640, 75, 31))
        self.start_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        self.stop_pushButton = QPushButton(self.video_widget)
        self.stop_pushButton.setObjectName(u"stop_pushButton")
        self.stop_pushButton.setGeometry(QtCore.QRect(550, 640, 75, 31))
        self.stop_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        self.pause_pushButton = QPushButton(self.video_widget)
        self.pause_pushButton.setObjectName(u"pause_pushButton")
        self.pause_pushButton.setGeometry(QtCore.QRect(430, 640, 75, 31))
        self.pause_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        
        
        
        # Seeting_widget
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
        self.setting_frame.setGeometry(QtCore.QRect(10, 50, 771, 641))
        self.setting_frame.setStyleSheet(u"border-color: rgb(220, 220, 240);")
        self.setting_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setting_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraUrl_label = QLabel(self.setting_frame)
        self.cameraUrl_label.setObjectName(u"cameraUrl_label")
        self.cameraUrl_label.setGeometry(QtCore.QRect(20, 26, 731, 31))
        font3 = QtGui.QFont()
        font3.setPointSize(15)
        self.cameraUrl_label.setFont(font3)
        self.cameraUrl_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.cameraUrl_label.setAlignment(Qt.AlignCenter)
        self.cameraUrl_line = QtWidgets.QLineEdit(self.setting_frame)
        self.cameraUrl_line.setObjectName(u"cameraUrl_line")
        self.cameraUrl_line.setGeometry(QtCore.QRect(20, 60, 731, 30))
        font4 = QtGui.QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setWeight(50)
        self.cameraUrl_line.setFont(font4)
        self.cameraUrl_line.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.prmRecPath_text = QtWidgets.QLineEdit(self.setting_frame)
        self.prmRecPath_text.setObjectName(u"prmRecPath_text")
        self.prmRecPath_text.setGeometry(QtCore.QRect(20, 144, 731, 30))
        self.prmRecPath_text.setFont(font4)
        self.prmRecPath_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.prmRecPath_text_2 = QLabel(self.setting_frame)
        self.prmRecPath_text_2.setObjectName(u"prmRecPath_text_2")
        self.prmRecPath_text_2.setGeometry(QtCore.QRect(20, 110, 731, 31))
        self.prmRecPath_text_2.setFont(font3)
        self.prmRecPath_text_2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.prmRecPath_text_2.setAlignment(Qt.AlignCenter)
        self.plcIp_text = QtWidgets.QLineEdit(self.setting_frame)
        self.plcIp_text.setObjectName(u"plcIp_text")
        self.plcIp_text.setGeometry(QtCore.QRect(20, 344, 731, 30))
        self.plcIp_text.setFont(font4)
        self.plcIp_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_label = QLabel(self.setting_frame)
        self.secRecPath_label.setObjectName(u"secRecPath_label")
        self.secRecPath_label.setGeometry(QtCore.QRect(20, 196, 731, 31))
        self.secRecPath_label.setFont(font3)
        self.secRecPath_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.secRecPath_label.setAlignment(Qt.AlignCenter)
        self.plcIp_label = QLabel(self.setting_frame)
        self.plcIp_label.setObjectName(u"plcIp_label")
        self.plcIp_label.setGeometry(QtCore.QRect(20, 310, 731, 31))
        self.plcIp_label.setFont(font3)
        self.plcIp_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plcIp_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.extrusionTag_text.setObjectName(u"extrusionTag_text")
        self.extrusionTag_text.setGeometry(QtCore.QRect(20, 514, 731, 30))
        self.extrusionTag_text.setFont(font4)
        self.extrusionTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartbeatTag_label = QLabel(self.setting_frame)
        self.heartbeatTag_label.setObjectName(u"heartbeatTag_label")
        self.heartbeatTag_label.setGeometry(QtCore.QRect(20, 566, 731, 31))
        self.heartbeatTag_label.setFont(font3)
        self.heartbeatTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartbeatTag_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.mouthDoorTag_text.setObjectName(u"mouthDoorTag_text")
        self.mouthDoorTag_text.setGeometry(QtCore.QRect(20, 430, 731, 30))
        self.mouthDoorTag_text.setFont(font4)
        self.mouthDoorTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.MouthDoorTag_label = QLabel(self.setting_frame)
        self.MouthDoorTag_label.setObjectName(u"MouthDoorTag_label")
        self.MouthDoorTag_label.setGeometry(QtCore.QRect(20, 396, 731, 31))
        self.MouthDoorTag_label.setFont(font3)
        self.MouthDoorTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.MouthDoorTag_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_label = QLabel(self.setting_frame)
        self.extrusionTag_label.setObjectName(u"extrusionTag_label")
        self.extrusionTag_label.setGeometry(QtCore.QRect(20, 480, 731, 31))
        self.extrusionTag_label.setFont(font3)
        self.extrusionTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTag_label.setAlignment(Qt.AlignCenter)
        self.heartbeatTag_text = QtWidgets.QLineEdit(self.setting_frame)
        self.heartbeatTag_text.setObjectName(u"heartbeatTag_text")
        self.heartbeatTag_text.setGeometry(QtCore.QRect(20, 600, 731, 30))
        self.heartbeatTag_text.setFont(font4)
        self.heartbeatTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_text = QtWidgets.QTextEdit(self.setting_frame)
        self.secRecPath_text.setObjectName(u"secRecPath_text")
        self.secRecPath_text.setGeometry(QtCore.QRect(20, 230, 730, 61))
        self.secRecPath_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";")
        
        
        
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
        font5 = QtGui.QFont()
        font5.setFamily(u"Arial")
        font5.setPointSize(28)
        font5.setBold(True)
        font5.setUnderline(False)
        font5.setWeight(75)
        self.header_title.setFont(font5)
        self.header_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.danieli_label = QLabel(self.header_widget)
        self.danieli_label.setObjectName(u"danieli_label")
        self.danieli_label.setGeometry(QtCore.QRect(-2, 0, 141, 81))
        self.danieli_label.setStyleSheet(u"border-color: rgb(220, 220, 240);\n")
        
        
        self.danieli_label.setText("")
        self.danieli_label.setObjectName("danieli_label")
        
        print(self.danieli_logo_image.shape)
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
        
        
        # Initialize the QDateTimeEdit with the current date and time
        current_datetime = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(current_datetime)  
        
        # Updating frames within loop
        self.timer = QTimer(mouthProtectionWinow)      
        if (self.plc_type == "TiaPortal"):
            self.timer.timeout.connect(self.update_video_tiaPortalPlc)
            self.timer.start(1000 // self.fps)     
        elif (self.plc_type == "Rockwell"):
            self.timer.timeout.connect(self.update_video_RockwellPlc)  
            self.timer.start(1000 // self.fps)         





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", u"MainWindow", None))
        self.header_title.setText(_translate("MainWindow", u"DANIELI PRESS MOUTH PROTECTION", None))
        self.danieli_label.setText("")
        self.footer_title.setText(_translate("MainWindow", u"System Logs", None))
        self.textEdit.setHtml(_translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sdsdsd<br />sdsdsd</p></body></html>", None))
        self.video_title.setText(_translate("MainWindow", u"Live View", None))
        self.video_label.setText(_translate("MainWindow", u"put here the live video frame", None))
        self.record_label.setText("")
        self.save_pushButton.setText(_translate("MainWindow", u"Save", None))
        self.start_pushButton.setText(_translate("MainWindow", u"Start", None))
        self.stop_pushButton.setText(_translate("MainWindow", u"Stop", None))
        self.pause_pushButton.setText(_translate("MainWindow", u"Pause", None))
        self.setting_title.setText(_translate("MainWindow", u"Settings", None))
        self.cameraUrl_label.setText(_translate("MainWindow", u"Camera URL", None))
        self.cameraUrl_line.setText("")
        self.prmRecPath_text.setText("")
        self.prmRecPath_text_2.setText(_translate("MainWindow", u"Primary recording path", None))
        self.plcIp_text.setText("")
        self.secRecPath_label.setText(_translate("MainWindow", u"Secondary recording path (local only)", None))
        self.plcIp_label.setText(_translate("MainWindow", u"PLC IP address", None))
        self.extrusionTag_text.setText("")
        self.heartbeatTag_label.setText(_translate("MainWindow", u"Heartbeat tag", None))
        self.mouthDoorTag_text.setText("")
        self.MouthDoorTag_label.setText(_translate("MainWindow", u"Mouth door tag", None))
        self.extrusionTag_label.setText(_translate("MainWindow", u"Extrusion tag", None))
        self.heartbeatTag_text.setText("")
        self.secRecPath_text.setHtml(_translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sddsdsdsd<br />hjhjhj</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ukjjojkuj,</p></body></html>", None))
    # retranslateUi




    ### Live Video Stream Analyser 
    def update_video_tiaPortalPlc(self):
        # updating the time and date
        current_datetime = QDateTime.currentDateTime()   
        self.dateTimeEdit.setDateTime(current_datetime)
        ret, frame = self.video_capture.read()
        ipcamera_ret, ipcamera_frame = ret, frame
        if (ret) & (ipcamera_ret):
            print("---------------------------------------------------------------------------------------------------------------")
            image, reference_time, Plc_Jetson_Communication = self.process_frame_tiaPortalPlc(frame)                            
            # Display the processed frame and variables in the GUI   
            self.display_frame(image)     
            self.display_variables(reference_time, Plc_Jetson_Communication)       



    def update_video_RockwellPlc(self):
        with LogixDriver(self.plc_ip_address) as plc:
            self.plc = plc
            # updating the time and date
            current_datetime = QDateTime.currentDateTime()      
            self.dateTimeEdit.setDateTime(current_datetime)
            ret, frame = self.video_capture.read()  
            # ipcamera_ret, ipcamera_frame = self.video_capture_ipcamera.read()
            ipcamera_ret, ipcamera_frame = ret, frame
            if (ret) & (ipcamera_ret):
                print("---------------------------------------------------------------------------------------------------------------")
                image, reference_time, Plc_Jetson_Communication = self.process_frame_RockwellPlc(frame)                            
                # Display the processed frame and variables in the GUI   
                self.display_frame(image)     
                self.display_variables(reference_time, Plc_Jetson_Communication)       
              
                

    def process_frame_tiaPortalPlc(self, frame):                                                                        
        # Reading variables from the plc
        self.FromPlc_Watchdog = self.FromPlc_Watchdog_Node.get_value()  
        self.FromPlc_ResultAck = self.FromPlc_ResultAck_Node.get_value()
        self.FromPlc_Pressure = self.FromPlc_Pressure_Node.get_value()
        self.FromPlc_Speed = self.FromPlc_Speed_Node.get_value()
        start_time = time.time()   
        

        # Watchdog Management 
        if self.FromPlc_Watchdog == self.WatchdogFromPlcMem:    
            self.watchdog_counter += 1
        else:
            self.watchdog_counter = 0  
            
        if self.watchdog_counter > 100:
            print("Communication Error!")  
            self.Plc_Jetson_Communication = False
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))   # set the jetson-plc-communication cell font to gray rgb (128,128,128) 
            brush.setStyle(QtCore.Qt.NoBrush)
            comm_item = self.visionVariables_widget_table.item(1, 0)
            comm_item.setForeground(brush)
        else:
            print("Communication Okay!")        
            self.Plc_Jetson_Communication = True
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))   # set the jetson-plc-communication cell font to gray rgb (128,128,128) 
            brush.setStyle(QtCore.Qt.NoBrush)
            comm_item = self.visionVariables_widget_table.item(1, 0)
            comm_item.setForeground(brush)
        self.WatchdogFromPlcMem = self.FromPlc_Watchdog    
        self.ToPlc_Watchdog = self.FromPlc_Watchdog       
        

        image = cv2.resize(frame, (691, 641))   # resize to the defined image_size
        #   Wrinting output to PLC    
        self.ToPlc_Watchdog_Node.set_value(ua.DataValue(ua.Variant(self.ToPlc_Watchdog, ua.VariantType.Boolean))) 
        end_time = time.time()      

        # Modify the frame and calculate result and reference_time as needed
        reference_time = "Reference Time:                {:.3f} (seconds)".format(end_time - start_time )  # Replace with actual reference time
        return image, reference_time, self.Plc_Jetson_Communication
    
    
    
    def process_frame_RockwellPlc(self, frame):  
        # Reading variables from the plc    
        self.FromPlc_Watchdog = (self.plc.read("JETSON_TO_Watchdog")).value
        self.FromPlc_ResultAck = (self.plc.read("JETSON_TO_ResultAck")).value
        self.FromPlc_Pressure = (self.plc.read("JETSON_TO_Pressure")).value
        self.FromPlc_Speed = (self.plc.read("JETSON_TO_Speed")).value 
        start_time = time.time()      
        # counter(s)   
        self.counter += 1    
        self.command_init_counter += 1  
        self.sleep_new_command_counter += 1

        # Watchdog Management 
        if self.FromPlc_Watchdog == self.WatchdogFromPlcMem:    
            self.watchdog_counter += 1
        else:
            self.watchdog_counter = 0  
            
        if self.watchdog_counter > 100:
            print("Communication Error!")  
            self.Plc_Jetson_Communication = False
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))   # set the jetson-plc-communication cell font to gray rgb (128,128,128) 
            brush.setStyle(QtCore.Qt.NoBrush)
            comm_item = self.visionVariables_widget_table.item(1, 0)
            comm_item.setForeground(brush)
        else:
            print("Communication Okay!")        
            self.Plc_Jetson_Communication = True
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))   # set the jetson-plc-communication cell font to gray rgb (128,128,128) 
            brush.setStyle(QtCore.Qt.NoBrush)
            comm_item = self.visionVariables_widget_table.item(1, 0)
            comm_item.setForeground(brush)
        self.WatchdogFromPlcMem = self.FromPlc_Watchdog    
        self.ToPlc_Watchdog = self.FromPlc_Watchdog       
        
            
        image = cv2.resize(frame, (691, 641))   # resize to the defined image_size
                             

        #   Wrinting output to PLC   
        self.plc.write('JETSON_FROM_Watchdog', self.ToPlc_Watchdog) 
        end_time = time.time()          
        # Modify the frame and calculate result and reference_time as needed
        reference_time = "Reference Time:                {:.3f} (seconds)".format(end_time - start_time)  # Replace with actual reference time
        return image, reference_time, self.Plc_Jetson_Communication
    
    
    
    # display the opencv BGR image into the defined lables in Qt Designer.
    def display_frame(self, frame):  
        height, width, channel = frame.shape   
        bytes_per_line = 3 * width
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)   


        

    # Display variables Function 
    def display_variables(self, result_symbol, reference_time, detected_glove_pairs, Plc_Jetson_Communication, movement_type, pressure ,speed):        
        self.loglist_widget_textBrowser.setText(f"------------------------------------------------------------------------------------------------------------------------------------------------------------------\n. {reference_time}\n. Detected glove pair(s) per frame:   {str(detected_glove_pairs)} \n. PLC ({self.plc_type}:{self.plc_ip_address}) and Nvidia Jetson Nano ({self.device_eth0_ip_address}) communication:   {str(Plc_Jetson_Communication)} \n------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        self.command_widget_result.setText(movement_type)              
        item1 = self.visionVariables_widget_table.item(0, 0)  
        item1.setText(str(detected_glove_pairs))
        item2 = self.visionVariables_widget_table.item(1, 0)               
        item2.setText(str(Plc_Jetson_Communication))  
        item3 = self.visionVariables_widget_table.item(2, 0)   
        item3.setText(str(result_symbol))  
        pressure_item = self.plcVariables_widget_table.item(0, 0)
        pressure_item.setText(str(pressure))
        speed_item = self.plcVariables_widget_table.item(1, 0)                        
        speed_item.setText(str(speed))


    
    # pop-up message box    
    def showpopup(self):
        msg = QMessageBox()    
        msg.setWindowTitle("Operator Guidance") 
        msg.resize(4000, 2000)
        with open(self.Glove_Movements_Symbols_dir, "rb") as txt_file:
            lines = [(line.rstrip()).decode()  for line in txt_file]     # line.rstrip:   removes the spaces from the end of the line.
        msg.setText(f"Please read the below explanation of how to use the software.\n\n***  The software is only sensitive toward two glove movements.\n\n***  Movements of the Gloves either vertically or horizantally should not have Intersection.\n\n\nMovements: \n\n{lines[0]}\n{lines[1]}\n{lines[2]}\n{lines[3]}\n{lines[4]}\n\n\n")
        # msg.setText("Please read the below explanation of how to use the software.\n\n***  The software is only sensitive toward two glove movements.\n\n***  Movements of the Gloves either vertically or horizantally should not have Intersection.\n\n\nMovements: \n\n1. Extrusion-Start................................................................      ⇗.⇙\n2. Extrusion-Stop............................................................      ⇙.⇗\n3. Press-Clamp-Close.................................................      --->.<---\n4. Press-Mouth-Open...................................................      <---.--->\n5. Puller-Extrusion-Start...................................................      ↑.↑\n6. command1........................................................................      ↓.↓\n\n\n")
        # msg.setText("Please read the below explanation of how to use the software.\n\n***  The software is only sensitive toward two glove movements.\n\n***  Movements of the Gloves either vertically or horizantally should not have Intersection.\n\n\nMovements: \n\n1. Extrusion-Start................................................................      ↑.↑\n2. Extrusion-Stop............................................................      ↓.↓\n3. Press-Clamp-Close-&-Start.......................................      --->.<---\n4. Press-Mouth-Open...................................................      <---.--->\n\n\n")
        msg.setIcon(QMessageBox.Information)  
        x = msg.exec_()
        
        
        
    def closeEvent(self, event):  
        self.video_capture.release()
        event.accept()      


#***********************************************************************************************************************************************************************************************************
def main():
    
    video_dir = "" 
    fps = 30  
    plc_type = "TiaPortal"   # TiaPortal or Rockwell   


                                                                            
    app = QApplication(sys.argv)                       
    mouthProtectionWinow = QtWidgets.QMainWindow()  
    mouthProtection = MouthProtectionApp(video_dir, fps, plc_type)
    mouthProtection.initUI(mouthProtectionWinow)
    mouthProtectionWinow.show()    
    sys.exit(app.exec_())  

if     __name__ == "__main__":                                      
    main()
    
    
    
    
          
    
    





