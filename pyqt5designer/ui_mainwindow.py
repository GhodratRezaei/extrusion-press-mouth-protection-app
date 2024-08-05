# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindoweSgiSX.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1680, 1050)
        MainWindow.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(43, 39, 56);\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.header_widget = QWidget(self.centralwidget)
        self.header_widget.setObjectName(u"header_widget")
        self.header_widget.setGeometry(QRect(40, 20, 1601, 81))
        self.header_widget.setStyleSheet(u"border: 1px solid white;\n"
"border-color: rgb(220, 220, 240);\n"
"background-color: rgb(220, 220, 240);")
        self.header_title = QLabel(self.header_widget)
        self.header_title.setObjectName(u"header_title")
        self.header_title.setGeometry(QRect(300, 24, 1000, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_title.sizePolicy().hasHeightForWidth())
        self.header_title.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(28)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.header_title.setFont(font)
        self.header_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.header_title.setAlignment(Qt.AlignCenter)
        self.danieli_label = QLabel(self.header_widget)
        self.danieli_label.setObjectName(u"danieli_label")
        self.danieli_label.setGeometry(QRect(-2, 0, 141, 81))
        self.danieli_label.setStyleSheet(u"border-color: rgb(220, 220, 240);\n"
"")
        self.border_widget = QWidget(self.centralwidget)
        self.border_widget.setObjectName(u"border_widget")
        self.border_widget.setGeometry(QRect(29, 10, 1621, 941))
        self.border_widget.setStyleSheet(u"border: 1px solid white;\n"
"")
        self.footer_widget = QWidget(self.border_widget)
        self.footer_widget.setObjectName(u"footer_widget")
        self.footer_widget.setGeometry(QRect(10, 830, 1601, 101))
        self.footer_widget.setStyleSheet(u"border: 1px solid white;\n"
"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        self.footer_title = QLabel(self.footer_widget)
        self.footer_title.setObjectName(u"footer_title")
        self.footer_title.setGeometry(QRect(670, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.footer_title.sizePolicy().hasHeightForWidth())
        self.footer_title.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(19)
        font1.setBold(False)
        font1.setUnderline(True)
        font1.setWeight(50)
        self.footer_title.setFont(font1)
        self.footer_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.footer_title.setAlignment(Qt.AlignCenter)
        self.textEdit = QTextEdit(self.footer_widget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 46, 1541, 46))
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"font: 10pt \"Segoe UI\";\n"
"border-color: rgb(0, 0, 0);")
        self.video_widget = QWidget(self.border_widget)
        self.video_widget.setObjectName(u"video_widget")
        self.video_widget.setGeometry(QRect(10, 110, 791, 701))
        self.video_widget.setStyleSheet(u"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        self.video_title = QLabel(self.video_widget)
        self.video_title.setObjectName(u"video_title")
        self.video_title.setGeometry(QRect(260, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.video_title.sizePolicy().hasHeightForWidth())
        self.video_title.setSizePolicy(sizePolicy)
        self.video_title.setFont(font1)
        self.video_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.video_title.setAlignment(Qt.AlignCenter)
        self.video_label = QLabel(self.video_widget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(50, 60, 691, 641))
        self.video_label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.record_label = QLabel(self.video_widget)
        self.record_label.setObjectName(u"record_label")
        self.record_label.setGeometry(QRect(170, 630, 471, 51))
        self.record_label.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.save_pushButton = QPushButton(self.video_widget)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setGeometry(QRect(190, 640, 75, 31))
        font2 = QFont()
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
        self.start_pushButton.setGeometry(QRect(310, 640, 75, 31))
        self.start_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        self.stop_pushButton = QPushButton(self.video_widget)
        self.stop_pushButton.setObjectName(u"stop_pushButton")
        self.stop_pushButton.setGeometry(QRect(550, 640, 75, 31))
        self.stop_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        self.pause_pushButton = QPushButton(self.video_widget)
        self.pause_pushButton.setObjectName(u"pause_pushButton")
        self.pause_pushButton.setGeometry(QRect(430, 640, 75, 31))
        self.pause_pushButton.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 75 12pt \"Arial\";\n"
"border-color: rgb(0, 0, 0);")
        self.setting_widget = QWidget(self.border_widget)
        self.setting_widget.setObjectName(u"setting_widget")
        self.setting_widget.setGeometry(QRect(820, 110, 791, 701))
        self.setting_widget.setStyleSheet(u"background-color: rgb(220, 220, 240);\n"
"border-color: rgb(220, 220, 240);")
        self.setting_title = QLabel(self.setting_widget)
        self.setting_title.setObjectName(u"setting_title")
        self.setting_title.setGeometry(QRect(270, 8, 271, 31))
        sizePolicy.setHeightForWidth(self.setting_title.sizePolicy().hasHeightForWidth())
        self.setting_title.setSizePolicy(sizePolicy)
        self.setting_title.setFont(font1)
        self.setting_title.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.setting_title.setAlignment(Qt.AlignCenter)
        self.setting_frame = QFrame(self.setting_widget)
        self.setting_frame.setObjectName(u"setting_frame")
        self.setting_frame.setGeometry(QRect(10, 50, 771, 641))
        self.setting_frame.setStyleSheet(u"border-color: rgb(220, 220, 240);")
        self.setting_frame.setFrameShape(QFrame.StyledPanel)
        self.setting_frame.setFrameShadow(QFrame.Raised)
        self.cameraUrl_label = QLabel(self.setting_frame)
        self.cameraUrl_label.setObjectName(u"cameraUrl_label")
        self.cameraUrl_label.setGeometry(QRect(20, 26, 731, 31))
        font3 = QFont()
        font3.setPointSize(15)
        self.cameraUrl_label.setFont(font3)
        self.cameraUrl_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.cameraUrl_label.setAlignment(Qt.AlignCenter)
        self.cameraUrl_line = QLineEdit(self.setting_frame)
        self.cameraUrl_line.setObjectName(u"cameraUrl_line")
        self.cameraUrl_line.setGeometry(QRect(20, 60, 731, 30))
        font4 = QFont()
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
        self.prmRecPath_text = QLineEdit(self.setting_frame)
        self.prmRecPath_text.setObjectName(u"prmRecPath_text")
        self.prmRecPath_text.setGeometry(QRect(20, 144, 731, 30))
        self.prmRecPath_text.setFont(font4)
        self.prmRecPath_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.prmRecPath_text_2 = QLabel(self.setting_frame)
        self.prmRecPath_text_2.setObjectName(u"prmRecPath_text_2")
        self.prmRecPath_text_2.setGeometry(QRect(20, 110, 731, 31))
        self.prmRecPath_text_2.setFont(font3)
        self.prmRecPath_text_2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.prmRecPath_text_2.setAlignment(Qt.AlignCenter)
        self.plcIp_text = QLineEdit(self.setting_frame)
        self.plcIp_text.setObjectName(u"plcIp_text")
        self.plcIp_text.setGeometry(QRect(20, 344, 731, 30))
        self.plcIp_text.setFont(font4)
        self.plcIp_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_label = QLabel(self.setting_frame)
        self.secRecPath_label.setObjectName(u"secRecPath_label")
        self.secRecPath_label.setGeometry(QRect(20, 196, 731, 31))
        self.secRecPath_label.setFont(font3)
        self.secRecPath_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.secRecPath_label.setAlignment(Qt.AlignCenter)
        self.plcIp_label = QLabel(self.setting_frame)
        self.plcIp_label.setObjectName(u"plcIp_label")
        self.plcIp_label.setGeometry(QRect(20, 310, 731, 31))
        self.plcIp_label.setFont(font3)
        self.plcIp_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.plcIp_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_text = QLineEdit(self.setting_frame)
        self.extrusionTag_text.setObjectName(u"extrusionTag_text")
        self.extrusionTag_text.setGeometry(QRect(20, 514, 731, 30))
        self.extrusionTag_text.setFont(font4)
        self.extrusionTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.heartbeatTag_label = QLabel(self.setting_frame)
        self.heartbeatTag_label.setObjectName(u"heartbeatTag_label")
        self.heartbeatTag_label.setGeometry(QRect(20, 566, 731, 31))
        self.heartbeatTag_label.setFont(font3)
        self.heartbeatTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.heartbeatTag_label.setAlignment(Qt.AlignCenter)
        self.mouthDoorTag_text = QLineEdit(self.setting_frame)
        self.mouthDoorTag_text.setObjectName(u"mouthDoorTag_text")
        self.mouthDoorTag_text.setGeometry(QRect(20, 430, 731, 30))
        self.mouthDoorTag_text.setFont(font4)
        self.mouthDoorTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.MouthDoorTag_label = QLabel(self.setting_frame)
        self.MouthDoorTag_label.setObjectName(u"MouthDoorTag_label")
        self.MouthDoorTag_label.setGeometry(QRect(20, 396, 731, 31))
        self.MouthDoorTag_label.setFont(font3)
        self.MouthDoorTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.MouthDoorTag_label.setAlignment(Qt.AlignCenter)
        self.extrusionTag_label = QLabel(self.setting_frame)
        self.extrusionTag_label.setObjectName(u"extrusionTag_label")
        self.extrusionTag_label.setGeometry(QRect(20, 480, 731, 31))
        self.extrusionTag_label.setFont(font3)
        self.extrusionTag_label.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-color: rgb(220, 220, 240);")
        self.extrusionTag_label.setAlignment(Qt.AlignCenter)
        self.heartbeatTag_text = QLineEdit(self.setting_frame)
        self.heartbeatTag_text.setObjectName(u"heartbeatTag_text")
        self.heartbeatTag_text.setGeometry(QRect(20, 600, 731, 30))
        self.heartbeatTag_text.setFont(font4)
        self.heartbeatTag_text.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.secRecPath_text = QTextEdit(self.setting_frame)
        self.secRecPath_text.setObjectName(u"secRecPath_text")
        self.secRecPath_text.setGeometry(QRect(20, 230, 730, 61))
        self.secRecPath_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"Segoe UI\";")
        self.video_widget.raise_()
        self.setting_widget.raise_()
        self.footer_widget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.border_widget.raise_()
        self.header_widget.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1680, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.header_title.setText(QCoreApplication.translate("MainWindow", u"DANIELI PRESS MOUTH PROTECTION", None))
        self.danieli_label.setText("")
        self.footer_title.setText(QCoreApplication.translate("MainWindow", u"System Logs", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sdsdsd<br />sdsdsd</p></body></html>", None))
        self.video_title.setText(QCoreApplication.translate("MainWindow", u"Live View", None))
        self.video_label.setText(QCoreApplication.translate("MainWindow", u"put here the live video frame", None))
        self.record_label.setText("")
        self.save_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.start_pushButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_pushButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pause_pushButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.setting_title.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.cameraUrl_label.setText(QCoreApplication.translate("MainWindow", u"Camera URL", None))
        self.cameraUrl_line.setText("")
        self.prmRecPath_text.setText("")
        self.prmRecPath_text_2.setText(QCoreApplication.translate("MainWindow", u"Primary recording path", None))
        self.plcIp_text.setText("")
        self.secRecPath_label.setText(QCoreApplication.translate("MainWindow", u"Secondary recording path (local only)", None))
        self.plcIp_label.setText(QCoreApplication.translate("MainWindow", u"PLC IP address", None))
        self.extrusionTag_text.setText("")
        self.heartbeatTag_label.setText(QCoreApplication.translate("MainWindow", u"Heartbeat tag", None))
        self.mouthDoorTag_text.setText("")
        self.MouthDoorTag_label.setText(QCoreApplication.translate("MainWindow", u"Mouth door tag", None))
        self.extrusionTag_label.setText(QCoreApplication.translate("MainWindow", u"Extrusion tag", None))
        self.heartbeatTag_text.setText("")
        self.secRecPath_text.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sddsdsdsd<br />hjhjhj</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ukjjojkuj,</p></body></html>", None))
    # retranslateUi

