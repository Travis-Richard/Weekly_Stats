from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from datetime import timedelta, datetime
import seaborn as sns
import sys

exclude_time = []
rec_s = []
rec_e = []
rec = []
dates = []


class Ui_Weekly_Stats_Application(object):

    def __init__(self):
        self.exclude_time = exclude_time
        self.rec_s = rec_s
        self.rec_e = rec_e
        self.rec = rec
        self.dates = dates

    def setupUi(self, Weekly_Stats_Application):
        Weekly_Stats_Application.setObjectName("Weekly_Stats_Application")
        Weekly_Stats_Application.resize(1042, 312)
        Weekly_Stats_Application.setToolTipDuration(-5)
        self.gridLayoutWidget = QtWidgets.QWidget(Weekly_Stats_Application)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(480, 10, 551, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.Week_Selection = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.Week_Selection.setContentsMargins(0, 0, 0, 0)
        self.Week_Selection.setObjectName("Week_Selection")
        self.week_end = QtWidgets.QDateEdit(self.gridLayoutWidget)
        # Setting the date to today's date
        self.week_end.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime(23, 59, 59)))
        self.week_end.setMaximumDate(QtCore.QDate(2050, 12, 31))
        self.week_end.setMinimumDate(QtCore.QDate(2018, 1, 1))
        self.week_end.setCalendarPopup(True)
        self.week_end.setDate(QtCore.QDate.currentDate())
        self.week_end.setObjectName("week_end")
        self.Week_Selection.addWidget(self.week_end, 1, 1, 1, 1)
        self.week_end_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.week_end_label.setObjectName("week_end_label")
        self.Week_Selection.addWidget(self.week_end_label, 1, 0, 1, 1)
        self.week_start = QtWidgets.QDateEdit(self.gridLayoutWidget)
        # Setting the date to today's date
        self.week_start.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime(0, 0, 0)))
        self.week_start.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2050, 12, 31), QtCore.QTime(23, 59, 59)))
        self.week_start.setMaximumDate(QtCore.QDate(2050, 12, 31))
        self.week_start.setMinimumDate(QtCore.QDate(2018, 1, 1))
        self.week_start.setCalendarPopup(True)
        self.week_start.setDate(QtCore.QDate.currentDate())
        self.week_start.setObjectName("week_start")
        self.Week_Selection.addWidget(self.week_start, 0, 1, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ok_btn.setObjectName("ok_btn")
        self.Week_Selection.addWidget(self.ok_btn, 2, 1, 1, 1)
        self.week_start_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.week_start_label.setObjectName("week_start_label")
        self.Week_Selection.addWidget(self.week_start_label, 0, 0, 1, 1)
        self.ok_btn_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ok_btn_label.setObjectName("ok_btn_label")
        self.Week_Selection.addWidget(self.ok_btn_label, 2, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Weekly_Stats_Application)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 120, 1021, 185))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.Exclusion_Dates = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.Exclusion_Dates.setContentsMargins(0, 0, 0, 0)
        self.Exclusion_Dates.setObjectName("Exclusion_Dates")
        self.sun_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sun_label.setFont(font)
        self.sun_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sun_label.setObjectName("sun_label")
        self.Exclusion_Dates.addWidget(self.sun_label, 1, 0, 1, 1)
        self.get_data_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.get_data_btn.setObjectName("get_data_btn")
        self.Exclusion_Dates.addWidget(self.get_data_btn, 7, 5, 1, 2)
        self.save_exc_dates_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.save_exc_dates_btn.setObjectName("save_exc_dates_btn")
        self.Exclusion_Dates.addWidget(self.save_exc_dates_btn, 6, 5, 1, 2)
        self.thur_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.thur_label.setFont(font)
        self.thur_label.setAlignment(QtCore.Qt.AlignCenter)
        self.thur_label.setObjectName("thur_label")
        self.Exclusion_Dates.addWidget(self.thur_label, 1, 4, 1, 1)
        self.sat_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sat_label.setFont(font)
        self.sat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sat_label.setObjectName("sat_label")
        self.Exclusion_Dates.addWidget(self.sat_label, 1, 6, 1, 1)
        self.fri_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.fri_label.setFont(font)
        self.fri_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fri_label.setObjectName("fri_label")
        self.Exclusion_Dates.addWidget(self.fri_label, 1, 5, 1, 1)
        self.mon_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mon_label.setFont(font)
        self.mon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mon_label.setObjectName("mon_label")
        self.Exclusion_Dates.addWidget(self.mon_label, 1, 1, 1, 1)
        self.tues_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tues_label.setFont(font)
        self.tues_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tues_label.setObjectName("tues_label")
        self.Exclusion_Dates.addWidget(self.tues_label, 1, 2, 1, 1)
        self.wed_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.wed_label.setFont(font)
        self.wed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wed_label.setObjectName("wed_label")
        self.Exclusion_Dates.addWidget(self.wed_label, 1, 3, 1, 1)
        self.sun_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sun_1st_btn.setCheckable(True)
        self.sun_1st_btn.setObjectName("sun_1st_btn")
        self.Exclusion_Dates_btns = QtWidgets.QButtonGroup(Weekly_Stats_Application)
        self.Exclusion_Dates_btns.setObjectName("Exclusion_Dates_btns")
        self.Exclusion_Dates_btns.setExclusive(False)
        self.Exclusion_Dates_btns.addButton(self.sun_1st_btn)
        self.Exclusion_Dates.addWidget(self.sun_1st_btn, 3, 0, 1, 1)
        self.mon_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.mon_1st_btn.setCheckable(True)
        self.mon_1st_btn.setObjectName("mon_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.mon_1st_btn)
        self.Exclusion_Dates.addWidget(self.mon_1st_btn, 3, 1, 1, 1)
        self.tues_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.tues_1st_btn.setCheckable(True)
        self.tues_1st_btn.setObjectName("tues_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.tues_1st_btn)
        self.Exclusion_Dates.addWidget(self.tues_1st_btn, 3, 2, 1, 1)
        self.sat_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sat_1st_btn.setCheckable(True)
        self.sat_1st_btn.setObjectName("sat_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.sat_1st_btn)
        self.Exclusion_Dates.addWidget(self.sat_1st_btn, 3, 6, 1, 1)
        self.fri_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.fri_1st_btn.setCheckable(True)
        self.fri_1st_btn.setObjectName("fri_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.fri_1st_btn)
        self.Exclusion_Dates.addWidget(self.fri_1st_btn, 3, 5, 1, 1)
        self.thur_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.thur_1st_btn.setCheckable(True)
        self.thur_1st_btn.setObjectName("thur_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.thur_1st_btn)
        self.Exclusion_Dates.addWidget(self.thur_1st_btn, 3, 4, 1, 1)
        self.wed_1st_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.wed_1st_btn.setCheckable(True)
        self.wed_1st_btn.setObjectName("wed_1st_btn")
        self.Exclusion_Dates_btns.addButton(self.wed_1st_btn)
        self.Exclusion_Dates.addWidget(self.wed_1st_btn, 3, 3, 1, 1)
        self.wed_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.wed_2nd_btn.setCheckable(True)
        self.wed_2nd_btn.setObjectName("wed_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.wed_2nd_btn)
        self.Exclusion_Dates.addWidget(self.wed_2nd_btn, 4, 3, 1, 1)
        self.tues_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.tues_2nd_btn.setCheckable(True)
        self.tues_2nd_btn.setObjectName("tues_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.tues_2nd_btn)
        self.Exclusion_Dates.addWidget(self.tues_2nd_btn, 4, 2, 1, 1)
        self.tues_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.tues_3rd_btn.setCheckable(True)
        self.tues_3rd_btn.setObjectName("tues_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.tues_3rd_btn)
        self.Exclusion_Dates.addWidget(self.tues_3rd_btn, 5, 2, 1, 1)
        self.mon_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.mon_3rd_btn.setCheckable(True)
        self.mon_3rd_btn.setObjectName("mon_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.mon_3rd_btn)
        self.Exclusion_Dates.addWidget(self.mon_3rd_btn, 5, 1, 1, 1)
        self.mon_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.mon_2nd_btn.setCheckable(True)
        self.mon_2nd_btn.setObjectName("mon_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.mon_2nd_btn)
        self.Exclusion_Dates.addWidget(self.mon_2nd_btn, 4, 1, 1, 1)
        self.sun_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sun_2nd_btn.setCheckable(True)
        self.sun_2nd_btn.setObjectName("sun_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.sun_2nd_btn)
        self.Exclusion_Dates.addWidget(self.sun_2nd_btn, 4, 0, 1, 1)
        self.sun_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sun_3rd_btn.setCheckable(True)
        self.sun_3rd_btn.setObjectName("sun_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.sun_3rd_btn)
        self.Exclusion_Dates.addWidget(self.sun_3rd_btn, 5, 0, 1, 1)
        self.fri_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.fri_2nd_btn.setCheckable(True)
        self.fri_2nd_btn.setObjectName("fri_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.fri_2nd_btn)
        self.Exclusion_Dates.addWidget(self.fri_2nd_btn, 4, 5, 1, 1)
        self.sat_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sat_2nd_btn.setCheckable(True)
        self.sat_2nd_btn.setObjectName("sat_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.sat_2nd_btn)
        self.Exclusion_Dates.addWidget(self.sat_2nd_btn, 4, 6, 1, 1)
        self.fri_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.fri_3rd_btn.setCheckable(True)
        self.fri_3rd_btn.setObjectName("fri_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.fri_3rd_btn)
        self.Exclusion_Dates.addWidget(self.fri_3rd_btn, 5, 5, 1, 1)
        self.sat_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sat_3rd_btn.setCheckable(True)
        self.sat_3rd_btn.setObjectName("sat_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.sat_3rd_btn)
        self.Exclusion_Dates.addWidget(self.sat_3rd_btn, 5, 6, 1, 1)
        self.wed_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.wed_3rd_btn.setCheckable(True)
        self.wed_3rd_btn.setObjectName("wed_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.wed_3rd_btn)
        self.Exclusion_Dates.addWidget(self.wed_3rd_btn, 5, 3, 1, 1)
        self.thur_2nd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.thur_2nd_btn.setCheckable(True)
        self.thur_2nd_btn.setObjectName("thur_2nd_btn")
        self.Exclusion_Dates_btns.addButton(self.thur_2nd_btn)
        self.Exclusion_Dates.addWidget(self.thur_2nd_btn, 4, 4, 1, 1)
        self.thur_3rd_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.thur_3rd_btn.setCheckable(True)
        self.thur_3rd_btn.setObjectName("thur_3rd_btn")
        self.Exclusion_Dates_btns.addButton(self.thur_3rd_btn)
        self.Exclusion_Dates.addWidget(self.thur_3rd_btn, 5, 4, 1, 1)
        self.desc_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.desc_label.setFont(font)
        self.desc_label.setAlignment(QtCore.Qt.AlignCenter)
        self.desc_label.setObjectName("desc_label")
        self.Exclusion_Dates.addWidget(self.desc_label, 0, 0, 1, 7)
        self.save_exc_dates_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.save_exc_dates_label.setObjectName("save_exc_dates_label")
        self.Exclusion_Dates.addWidget(self.save_exc_dates_label, 6, 3, 1, 2)
        self.get_data_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.get_data_label.setObjectName("get_data_label")
        self.Exclusion_Dates.addWidget(self.get_data_label, 7, 3, 1, 2)
        self.clear_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.clear_btn.setObjectName("clear_btn")
        self.Exclusion_Dates.addWidget(self.clear_btn, 7, 0, 1, 2)
        self.clear_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.clear_label.setObjectName("clear_label")
        self.Exclusion_Dates.addWidget(self.clear_label, 6, 0, 1, 3)
        self.textBrowser = QtWidgets.QTextBrowser(Weekly_Stats_Application)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 461, 101))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Weekly_Stats_Application)
        QtCore.QMetaObject.connectSlotsByName(Weekly_Stats_Application)

        self.ok_btn.clicked.connect(self.weekSelection)
        self.save_exc_dates_btn.clicked.connect(self.excludeTimes)
        self.clear_btn.clicked.connect(self.clear)
        self.get_data_btn.clicked.connect(self.getData)

    def retranslateUi(self, Weekly_Stats_Application):
        _translate = QtCore.QCoreApplication.translate
        Weekly_Stats_Application.setWindowTitle(_translate("Weekly_Stats_Application", "Weekly_Stats_Application"))
        self.week_end_label.setText(_translate("Weekly_Stats_Application", "Week End"))
        self.ok_btn.setText(_translate("Weekly_Stats_Application", "OK"))
        self.week_start_label.setText(_translate("Weekly_Stats_Application", "Week Start"))
        self.ok_btn_label.setText(_translate("Weekly_Stats_Application", "Press OK to use selected dates"))
        self.sun_label.setText(_translate("Weekly_Stats_Application", "Sun"))
        self.get_data_btn.setText(_translate("Weekly_Stats_Application", "Get Data"))
        self.save_exc_dates_btn.setText(_translate("Weekly_Stats_Application", "Save Exclusion Dates"))
        self.thur_label.setText(_translate("Weekly_Stats_Application", "Thur"))
        self.sat_label.setText(_translate("Weekly_Stats_Application", "Sat"))
        self.fri_label.setText(_translate("Weekly_Stats_Application", "Fri"))
        self.mon_label.setText(_translate("Weekly_Stats_Application", "Mon"))
        self.tues_label.setText(_translate("Weekly_Stats_Application", "Tues"))
        self.wed_label.setText(_translate("Weekly_Stats_Application", "Wed"))
        self.sun_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.mon_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.tues_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.sat_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.fri_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.thur_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.wed_1st_btn.setText(_translate("Weekly_Stats_Application", "00:00"))
        self.wed_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.tues_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.tues_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.mon_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.mon_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.sun_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.sun_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.fri_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.sat_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.fri_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.sat_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.wed_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.thur_2nd_btn.setText(_translate("Weekly_Stats_Application", "08:00"))
        self.thur_3rd_btn.setText(_translate("Weekly_Stats_Application", "16:00"))
        self.desc_label.setText(_translate("Weekly_Stats_Application",
                                           "Select shifts to be excluded from the above week, ie Maintenance or Development"))
        self.save_exc_dates_label.setText(
            _translate("Weekly_Stats_Application", "Press this button to have the excluded dates saved"))
        self.clear_btn.setText(_translate("Weekly_Stats_Application", "Clear"))
        self.clear_label.setText(
            _translate("Weekly_Stats_Application", "Clear Exclusion Dates if mistake was made and btn pressed"))
        self.get_data_label.setText(
            _translate("Weekly_Stats_Application", "Press this button to get trip data for week"))
        self.textBrowser.setHtml(_translate("Weekly_Stats_Application",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To use this application first select the date the week started on, then select the date the week ended on. Hit the OK button. Select all shifts that you want excluded from the week. These can be maintenance or development shifts. Select all that apply to that week then hit the Save Exclusion Dates button, that will allow the script to save these dates to be excluded. Once you are satisfied with everything, hit the Get Data button to get the trip data for the week.</p></body></html>"))

    def weekSelection(self):
        sunday = self.week_start.dateTime().toPyDateTime()
        saturday = self.week_end.dateTime().toPyDateTime()
        self.sun = sunday.strftime('%Y-%m-%d')
        self.sat = saturday.strftime('%Y-%m-%d')
        url_archiver = 'http://vm-archiver-02.clsi.ca:17668/retrieval/ui/viewer/archViewer.html?pv=PCT1402-01:mA:fbk' \
                       '&from={}T00:00:00&to={}T23:59:59&binSize=30' \
            .format(self.sun, self.sat)
        print('Click this link to show data archiver plot:', '\n', url_archiver)

        self.dates = [sunday + timedelta(days=x) for x in range((saturday - sunday).days + 1)]
        # print(self.dates)

        sunday = sunday + timedelta(hours=6)
        saturday = saturday + timedelta(hours=6)

        self.url_csv_retrieval = 'http://vm-archiver-02.clsi.ca:17668/retrieval/data/getData.csv?pv=PCT1402-01%3AmA%3Afbk' \
                                 '&from={}T{}%3A{}%3A{}Z&to={}T{}%3A{}%3A{}Z' \
            .format(sunday.strftime('%Y-%m-%d'), sunday.strftime('%H'), sunday.strftime('%M'),
                    sunday.strftime('%S'), saturday.strftime('%Y-%m-%d'), saturday.strftime('%H'),
                    saturday.strftime('%M'), saturday.strftime('%S'))
        print(self.url_csv_retrieval)

    def excludeTimes(self):
        exc_time_s = []
        exc_time_e = []
        days_shifts = ['sun_1st_s', 'sun_1st_e', 'sun_2nd_s', 'sun_2nd_e', 'sun_3rd_s', 'sun_3rd_e']
        day_of_week = ['sun', 'mon', 'tues', 'wed', 'thur', 'fri', 'sat']

        for i in range(0, len(day_of_week)):
            for v in range(3):
                if v == 0:
                    exc_time_s.append(self.dates[i])
                    exc_time_e.append(self.dates[i] + timedelta(hours=7, minutes=59, seconds=59))

                if v == 1:
                    exc_time_s.append(self.dates[i] + timedelta(hours=8))
                    exc_time_e.append(self.dates[i] + timedelta(hours=15, minutes=59, seconds=59))

                if v == 2:
                    exc_time_s.append(self.dates[i] + timedelta(hours=16))
                    exc_time_e.append(self.dates[i] + timedelta(hours=23, minutes=59, seconds=59))

        exc_time = list(map(list, zip(exc_time_s, exc_time_e)))

        bool_list_btns = [self.sun_1st_btn.isChecked(), self.sun_2nd_btn.isChecked(), self.sun_3rd_btn.isChecked(),
                          self.mon_1st_btn.isChecked(), self.mon_2nd_btn.isChecked(), self.mon_3rd_btn.isChecked(),
                          self.tues_1st_btn.isChecked(), self.tues_2nd_btn.isChecked(), self.tues_3rd_btn.isChecked(),
                          self.wed_1st_btn.isChecked(), self.wed_2nd_btn.isChecked(), self.wed_3rd_btn.isChecked(),
                          self.thur_1st_btn.isChecked(), self.thur_2nd_btn.isChecked(), self.thur_3rd_btn.isChecked(),
                          self.fri_1st_btn.isChecked(), self.fri_2nd_btn.isChecked(), self.fri_3rd_btn.isChecked(),
                          self.sat_1st_btn.isChecked(), self.sat_2nd_btn.isChecked(), self.sat_3rd_btn.isChecked()]
        btn_exc_time = list(map(list, zip(bool_list_btns, exc_time)))

        for i in range(0, len(btn_exc_time)):
            if btn_exc_time[i][0]:
                self.exclude_time.append(btn_exc_time[i][1])

    def clear(self):
        self.exclude_time.clear()

    def getData(self):
        sns.set(style="whitegrid")
        tips = sns.load_dataset("tips")

        df = pd.read_csv(self.url_csv_retrieval)
        df.columns = ['Time', 'Current', 'A', 'B', 'C']
        df = df.drop(columns=['A', 'B', 'C'])
        df['Time'] = pd.to_datetime(df['Time'], unit='s') - pd.Timedelta(hours=6)
        df['Current'] = df['Current'].map(lambda y: str(y)[:5])
        df['Current'] = pd.to_numeric(df['Current'])
        df = df.set_index(['Time'])
        df = df.resample('10S').max()
        df.reset_index(inplace=True)
        df['Current_S'] = df['Current'].shift(-1)
        df['Trip'] = (df['Current'] > 10) & (df['Current_S'] < 1)
        df['Recover'] = (df['Current_S'] > df['Current']) & (df['Current_S'] > 220)

        df = df.set_index(['Time'])

        for i in range(0, len(exclude_time)):
            s = pd.to_datetime(exclude_time[i][0])
            e = pd.to_datetime(exclude_time[i][1])
            df = df.loc[(df.index < s) | (df.index > e)]

        df.reset_index(inplace=True)
        df['Time_shift'] = df['Time'].shift(-1)
        df['Time_Subtract'] = ((df['Time_shift'] - df['Time']).dt.seconds / 3600 +
                               (df['Time_shift'] - df['Time']).dt.days * 24)

        for i in range(0, len(df)):
            if df['Time_Subtract'][i] > 7:
                if df['Current'][i] < 1:
                    df.loc[i, 'Recover'] = True
                if df['Current'][i + 1] < 1:
                    df.loc[i + 1, 'Trip'] = True

        if df['Current'][0] < 1:
            df.loc[0, 'Trip'] = True
        last_row = len(df) - 1
        if df['Current'][last_row] < 1:
            df.loc[last_row, 'Recover'] = True

        for i in range(0, len(df)):
            if df['Trip'][i] == True:
                rec_s.append(pd.to_datetime(df['Time'][i]))
            if df['Recover'][i] == True:
                rec_e.append(pd.to_datetime(df['Time'][i]))

        for i in rec_s:
            for v in rec_e:
                if v > i:
                    rec.append(v)
                    break

        trip_recovery_times = []
        num_of_trips = []
        trip_list = list(map(list, zip(rec_s, rec)))

        # Script to save output file
        path = "/home/richart/AOD/Weekly_Stats_Docs/"  # Linux Path
        # path = r"H:\Documents\Projects\Weekly_Stats_Docs/"  # Windows Path
        filename = "{}_{}-Document.txt".format(self.sun, self.sat)
        file = path + filename
        sys.stdout = open(file, "w")

        for i in range(0, len(trip_list)):
            print('Trip #:', i + 1, 'start time', trip_list[i][0])
            print('Trip #:', i + 1, 'end time', trip_list[i][1])
            trip_time_i = pd.Timedelta(trip_list[i][1] - trip_list[i][0]).seconds / 60
            trip_time_i = round(trip_time_i, 1)
            print('This is Trip #', i + 1, 'recovery time', '\n', trip_time_i, 'Minutes')
            trip_recovery_times.append(trip_time_i)
            num_of_trips.append(i + 1)

        print('This is a list of all trip times:', '\n', trip_recovery_times)
        print("Total trip time for this period in Minutes is :", sum(trip_recovery_times))

        # Setting the figure size
        fig = plt.figure(figsize=(10, 7))

        y_pos = np.arange(len(num_of_trips))
        plt.bar(y_pos, trip_recovery_times, width=0.5, color='red')

        # adding label to the top of each bars
        for x, y in zip(y_pos, trip_recovery_times, ):
            label = "{:.1f}".format(y)

            plt.annotate(label,  # this is the text
                         (x, y),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center', fontsize=15,
                         fontweight='bold')  # horizontal alignment (ha) can be left, right or center

        # Add title and axis names
        plt.title(
            'Trip Weekly Stat ({}_{})'.format(self.sun, self.sat, fontsize=17))
        plt.xlabel('Number of Trips', fontsize=15)
        plt.ylabel('Trip Recovery Time (Minutes)', fontsize=15)

        # Limits for the Y axis2
        plt.ylim(0, max(trip_recovery_times) + 10)

        # Create names
        plt.xticks(y_pos, num_of_trips, )

        # Saving the plot as an image
        path = "/home/richart/AOD/Weekly_Stats_Docs/"  # Linux Path
        # path = r'H:\Documents\Projects\Weekly_Stats_Docs/'  # Windows Path
        filename = "{}_{}-Graph.png".format(self.sun, self.sat)
        file = path + filename
        fig.savefig(file, bbox_inches=None, dpi=None)

        # Show graphic
        plt.show()
        sys.stdout.close()  # Close text file


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Weekly_Stats_Application = QtWidgets.QWidget()
    ui = Ui_Weekly_Stats_Application()
    ui.setupUi(Weekly_Stats_Application)
    Weekly_Stats_Application.show()
    sys.exit(app.exec_())
