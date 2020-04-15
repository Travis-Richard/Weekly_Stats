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

        # Need to add 6 hours of time to our inputs as the CSV file takes into account the timezone, we will covert back later on

        sunday = sunday + timedelta(hours=6)
        saturday = saturday + timedelta(hours=6)

        self.url_csv_retrieval = 'http://vm-archiver-02.clsi.ca:17668/retrieval/data/getData.csv?pv=PCT1402-01%3AmA%3Afbk' \
                                 '&from={}T{}%3A{}%3A{}Z&to={}T{}%3A{}%3A{}Z' \
            .format(sunday.strftime('%Y-%m-%d'), sunday.strftime('%H'), sunday.strftime('%M'),
                    sunday.strftime('%S'), saturday.strftime('%Y-%m-%d'), saturday.strftime('%H'),
                    saturday.strftime('%M'), saturday.strftime('%S'))
        # print(self.url_csv_retrieval)

    def excludeTimes(self):
        exc_time_s = []
        exc_time_e = []
        day_of_week = ['sun', 'mon', 'tues', 'wed', 'thur', 'fri', 'sat']


        # This loop creates two lists of a start and end time for the exclusion times from the self.dates list. There will be 3 start and end times per day, for a total
        # of 21 items in each list. Start times will be 00, 08, and 16 for each day, End times will be 07:59:59, 15:59:59 and 23:59:59

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


        # exec_time is a list of two lists, start and end exclusion times, this way this new list will have a format of [[mon_1st_shift_start, mon_1st_shift_end], ...]
        # exc_time will have a length of 21, with 2 elements per item.

        exc_time = list(map(list, zip(exc_time_s, exc_time_e)))

        # this list is a boolean list of true or false, depending if the button is selected or not. True if it is

        bool_list_btns = [self.sun_1st_btn.isChecked(), self.sun_2nd_btn.isChecked(), self.sun_3rd_btn.isChecked(),
                          self.mon_1st_btn.isChecked(), self.mon_2nd_btn.isChecked(), self.mon_3rd_btn.isChecked(),
                          self.tues_1st_btn.isChecked(), self.tues_2nd_btn.isChecked(), self.tues_3rd_btn.isChecked(),
                          self.wed_1st_btn.isChecked(), self.wed_2nd_btn.isChecked(), self.wed_3rd_btn.isChecked(),
                          self.thur_1st_btn.isChecked(), self.thur_2nd_btn.isChecked(), self.thur_3rd_btn.isChecked(),
                          self.fri_1st_btn.isChecked(), self.fri_2nd_btn.isChecked(), self.fri_3rd_btn.isChecked(),
                          self.sat_1st_btn.isChecked(), self.sat_2nd_btn.isChecked(), self.sat_3rd_btn.isChecked()]

        # btn_exc_time creates a list of lists, in which the of lists is an item and a list of lists, or a True or False, then followed by the items in exc_time
        # corresponding to the true or false, eg: [[True, [mon_1st_shift_start, mon_1st_shift_end]], [False, [mon_2nd_shift_start, mon_2nd_shift_end]]...]
        # the above is the case if the first shift in monday is selected and the second shift is not. And it will produce these results for all days in the week,
        # again this list will have a length of 21

        btn_exc_time = list(map(list, zip(bool_list_btns, exc_time)))

        # this loop goes from 0 to 20 as an index, and looks to see if the value associated with btn_exc_time[i][0], or the boolean value, is True. If it is true,
        # self.exclude_time list appends the value associated with btn_exc_time[i][1], which a list of dates and times corresponding to the start of the shift that
        # was selected and the end of that same shift. This list will be of varying length depending on how many shifts need to be excluded

        for i in range(0, len(btn_exc_time)):
            if btn_exc_time[i][0]:
                self.exclude_time.append(btn_exc_time[i][1])

    def clear(self):
        # this function is called when the clear button on the GUI is pressed. It should only be pressed if dates and times were selected to be excluded but a mistake
        # was made. In that case the exclude_time list can be cleared and the dates can be re selected
        self.exclude_time.clear()

    def getData(self):
        # this function is called when the Get Data button on the GUI is pressed. It retrieves the csv file, reads it, parses the data, returns a graph of the trip
        # times and saves this graph as well as a text document that includes the information about the trips


        sns.set(style="whitegrid")
        tips = sns.load_dataset("tips")

        # the code below is reading the csv from the self.url_csv_retrieval link that we created in the weekSelection function, it then transforms it into a
        # pandas dataframe. With this datafram we set the column names and drop the columns we do not want, lettered A, B ... We then change the Time column
        # to a time object and subtract the 6 hours we had to add earlier to the csv link for timezone. We then trim the current column to get a readable number
        # and then convert it to a numeric object. Set the index to Time and resample to 10 seconds to change from ~600,000 data points to ~60,00, reset index back
        # to normal. Create a Current_S column to compare Current to its next value. Trip column is created based on the Current value being above 10 mA, and
        # Current_S value being below 1. This will be a True value. Create a Recover column where Current_S is greater than Current, ie: filling SR, and Current_S
        # is greater than 220 mA, ie: stored.

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

        # With the index set as Time we can parse out some information that we want to exclude, ie: exclusion times. This loop goes over the length of the
        # self.exclude_time list and sets the start value = self.exclude_time[i][0], first value, and end time to [i][1], second value. We can then use these
        # values in the df.loc method to remove any times that are within each range of the exclude_time list.

        for i in range(0, len(self.exclude_time)):
            s = pd.to_datetime(self.exclude_time[i][0])
            e = pd.to_datetime(self.exclude_time[i][1])
            df = df.loc[(df.index < s) | (df.index > e)]

        # reset index to normal and create a column Time_shift based on Time next value. Create a new column Time_Subtract that subtracts Time from Tme_shift.
        # we then convert to a readable values of hours only.

        df.reset_index(inplace=True)
        df['Time_shift'] = df['Time'].shift(-1)
        df['Time_Subtract'] = ((df['Time_shift'] - df['Time']).dt.seconds / 3600 +
                               (df['Time_shift'] - df['Time']).dt.days * 24)

        # Using the Time_Subtract column we loop over the entire df looking for values where Time_Subtract is greater than 7 hours, ie: Maint/Dev shift
        # If the current at that location is less than 1, we want to set the Recovery equal to True, That way at location i we are entering an exclusion shift,
        # if trip has yet to be recovered, we want to indicated that this is a recovery so we can have an accurate amount of downtime. If the Current at the
        # i location plus 1, ie coming out of a shift is less than 1 then we want to set the Trip equal to true so we can again account for downtime that isn't
        # necessarily a trip

        for i in range(0, len(df)):
            if df['Time_Subtract'][i] > 7:
                if df['Current'][i] < 1:
                    df.loc[i, 'Recover'] = True
                if df['Current'][i + 1] < 1:
                    df.loc[i + 1, 'Trip'] = True

        # These two if statements look at the beginning and end of the week. Since we are always starting at Sunday 00:00:00, we may have started with a trip from
        # the previous week and thats why we need to set the Trip equal to True, to account for downtime. Likewise, if the Current in the last row is still less than
        # 1 we need to set the Recovery equal to True so we can have an accurate account of downtime even if we haven't recovered

        if df['Current'][0] < 1:
            df.loc[0, 'Trip'] = True
        last_row = len(df) - 1
        if df['Current'][last_row] < 1:
            df.loc[last_row, 'Recover'] = True

        # This loop will create two lists one for the start time of the recovery and one for the end time of the recovery(kind of). The start time for the trips
        # is going to be correct due to the conditions we have. However, the recovery takes all accounts where current is increasing and above 220 so we will have
        # a lot of values in this list.

        for i in range(0, len(df)):
            if df['Trip'][i] == True:
                rec_s.append(pd.to_datetime(df['Time'][i]))
            if df['Recover'][i] == True:
                rec_e.append(pd.to_datetime(df['Time'][i]))

        # This loop fixes the above problem, it first loops over rec_s list, for the value in rec_s it loops over rec_e, if the value in rec_e is greater than the
        # value in rec_s, it appends this value to a new list rec. It the breaks the inner for loop and goes to the next value in rec_s. This will allow us to have
        # the same number of items in each list and we will have lists that have a start and end time

        for i in rec_s:
            for v in rec_e:
                if v > i:
                    rec.append(v)
                    break

        trip_recovery_times = []
        num_of_trips = []

        # trip_list is a list of lists that has a start and end time from the lists rec_s and rec

        trip_list = list(map(list, zip(rec_s, rec)))

        # This loop calculates each trip time we have and assigns a number to each trip, 1,2,3,... it appends these values to trip_recovery_times and num_of_trips
        # respectively

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
        # path = "/home/richart/AOD/Weekly_Stats_Docs/"  # Linux Path
        path = r'H:\Documents\Projects\Weekly_Stats_Docs/'  # Windows Path
        filename = "{}_{}-Graph.png".format(self.sun, self.sat)
        file = path + filename
        fig.savefig(file, bbox_inches=None, dpi=None)

        # Script to save output file
        # path = "/home/richart/AOD/Weekly_Stats_Docs/"  # Linux Path
        path = r"H:\Documents\Projects\Weekly_Stats_Docs/"  # Windows Path
        filename = "{}_{}-Document.txt".format(self.sun, self.sat)
        file = path + filename
        sys.stdout = open(file, "w")

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
