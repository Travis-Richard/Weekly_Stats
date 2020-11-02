from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np
from datetime import timedelta, datetime
import seaborn as sns
import sys
import traceback
import os


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class WeeklyStats(QtWidgets.QWidget):
    def __init__(self):
        super(WeeklyStats, self).__init__()
        uic.loadUi('Weekly_Stats_Application_New.ui', self)
        self.show()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        self.exclude_time = []
        self.rec_s = []
        self.rec_e = []
        self.rec = []
        self.dates = []
        self.trip_recovery_times = []
        self.num_of_trips = []
        self.trip_start_time = []
        self.trip_end_time = []
        # self.path = "/home/richart/AOD/Weekly_Stats_Docs/Cycle_32/"  # Linux Path
        # self.path = "/home/richart/Documents/"  # Linux Path
        self.path = r'C:\Users\richart\Documents\Projects\Weekly_Stats_Docs/'  # Windows Path

        self.ok_btn.clicked.connect(self.week_selection_thread)
        self.get_data_btn.clicked.connect(self.get_data_thread)

    def week_selection_thread(self):
        week_list = [self.week_selection, self.exclude_times]
        for i in week_list:
            worker = Worker(i)  # Any other args, kwargs are passed to the run function
            # worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

    def get_data_thread(self):
        # print('starting get data thread')
        worker = Worker(self.get_data)  # Any other args, kwargs are passed to the run function
        worker.signals.finished.connect(self.save_files_thread)
        # Execute
        self.threadpool.start(worker)

    def save_files_thread(self):
        # Pass the function to execute
        save_files_list = [self.get_info, self.save_weekly_csv, self.save_weekly_graph, self.save_total_csv,
                           self.save_total_graph, self.display_figures]
        for i in save_files_list:
            worker = Worker(i)  # Any other args, kwargs are passed to the run function
            # worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

    def week_selection(self):
        sunday = self.week_start.dateTime().toPyDateTime()
        saturday = self.week_end.dateTime().toPyDateTime()
        self.sun = sunday.strftime('%Y-%m-%d')
        self.sat = saturday.strftime('%Y-%m-%d')
        url_archiver = 'http://vm-archiver-02.clsi.ca:17668/retrieval/ui/viewer/archViewer.html?pv=PCT1402-01:mA:fbk' \
                       '&from={}T00:00:00&to={}T23:59:59&binSize=30' \
            .format(self.sun, self.sat)
        print('Click this link to show data archiver plot:', '\n', url_archiver)
        print()
        print()

        # Need to add 6 hours of time to our inputs as the CSV file takes into account the timezone, we will covert
        # back later on

        sunday = sunday + timedelta(hours=6)
        saturday = saturday + timedelta(hours=6)

        self.url_csv_retrieval = 'http://vm-archiver-02.clsi.ca:17668/retrieval/data/getData.csv?pv=PCT1402-01%3AmA' \
                                 '%3Afbk&from={}T{}%3A{}%3A{}Z&to={}T{}%3A{}%3A{}Z' \
            .format(sunday.strftime('%Y-%m-%d'), sunday.strftime('%H'), sunday.strftime('%M'),
                    sunday.strftime('%S'), saturday.strftime('%Y-%m-%d'), saturday.strftime('%H'),
                    saturday.strftime('%M'), saturday.strftime('%S'))

        # print(self.url_csv_retrieval)

    def exclude_times(self):
        exc_s = []
        exc_e = []
        week_s = self.week_start.dateTime().toPyDateTime()
        week_e = self.week_end.dateTime().toPyDateTime()
        week_range = pd.date_range(start=week_s, end=week_e, freq='H')

        dates = pd.read_csv(self.path + 'Exclusion_Times_Cycle32.csv', header=None)
        dates.columns = ['Date']
        dates['Date'] = pd.to_datetime(dates['Date'])

        for i in dates['Date']:
            if i in week_range:
                exc_s.append(i)
                exc_e.append(i + timedelta(hours=7, minutes=59, seconds=59))

        self.exclude_time = list(map(list, zip(exc_s, exc_e)))

        print("The following shifts will be excluded:")
        print()

        for i in range(0, len(self.exclude_time)):
            print(self.exclude_time[i][0].isoformat(), 'to', self.exclude_time[i][1].isoformat())

        print()
        print("If this is correct hit the Get Data button to collect trip data for the week.")
        print()
        print()

    def get_data(self):

        print(
            "Collecting Data, please wait and do not close program. A graph will be displayed when finished, "
            "you can then exit the program. All data will be saved to: home/AOD/Weekly_Stats_Docs")
        print()

        # this function is called when the Get Data button on the GUI is pressed. It retrieves the csv file,
        # reads it, parses the data, returns a graph of the trip times and saves this graph as well as a text
        # document that includes the information about the trips

        # the code below is reading the csv from the self.url_csv_retrieval link that we created in the weekSelection
        # function, it then transforms it into a pandas dataframe. With this datafram we set the column names and
        # drop the columns we do not want, lettered A, B ... We then change the Time column to a time object and
        # subtract the 6 hours we had to add earlier to the csv link for timezone. We then trim the current column to
        # get a readable number and then convert it to a numeric object. Set the index to Time and resample to 10
        # seconds to change from ~600,000 data points to ~60,00, reset index back to normal. Create a Current_S
        # column to compare Current to its next value. Trip column is created based on the Current value being above
        # 10 mA, and Current_S value being below 1. This will be a True value. Create a Recover column where
        # Current_S is greater than Current, ie: filling SR, and Current_S is greater than 220 mA, ie: stored.

        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        df = pd.read_csv(self.url_csv_retrieval)
        df.columns = ['Time', 'Current', 'A', 'B', 'C']
        df = df.drop(columns=['A', 'B', 'C'])
        df['Time'] = pd.to_datetime(df['Time'], unit='s') - pd.Timedelta(hours=6)
        # df['Current'] = df['Current'].map(lambda y: str(y)[:5])
        df['Current'] = pd.to_numeric(df['Current'])
        # df = df.set_index(['Time'])
        # df = df.resample('10S').max()
        # df.reset_index(inplace=True)
        df['Current_S'] = df['Current'].shift(-1)
        df['Trip'] = (df['Current'] > 10) & (df['Current_S'] < 10)
        df['Recover'] = (df['Current_S'] > df['Current']) & (df['Current_S'] > 220)

        df = df.set_index(['Time'])

        # With the index set as Time we can parse out some information that we want to exclude, ie: exclusion times.
        # This loop goes over the length of the self.exclude_time list and sets the start value = self.exclude_time[
        # i][0], first value, and end time to [i][1], second value. We can then use these values in the df.loc method
        # to remove any times that are within each range of the exclude_time list.

        for i in range(0, len(self.exclude_time)):
            s = pd.to_datetime(self.exclude_time[i][0])
            e = pd.to_datetime(self.exclude_time[i][1])
            df = df.loc[(df.index < s) | (df.index > e)]

        # reset index to normal and create a column Time_shift based on Time next value. Create a new column
        # Time_Subtract that subtracts Time from Tme_shift. we then convert to a readable values of hours only.

        df.reset_index(inplace=True)
        df['Time_shift'] = df['Time'].shift(-1)
        df['Time_Subtract'] = ((df['Time_shift'] - df['Time']).dt.seconds / 3600 +
                               (df['Time_shift'] - df['Time']).dt.days * 24)

        # Using the Time_Subtract column we loop over the entire df looking for values where Time_Subtract is greater
        # than 7 hours, ie: Maint/Dev shift If the current at that location is less than 1, we want to set the
        # Recovery equal to True, That way at location i we are entering an exclusion shift, if trip has yet to be
        # recovered, we want to indicated that this is a recovery so we can have an accurate amount of downtime. If
        # the Current at the i location plus 1, ie coming out of a shift is less than 1 then we want to set the Trip
        # equal to true so we can again account for downtime that isn't necessarily a trip

        for i in range(0, len(df) - 1):
            if df['Time_Subtract'][i] > 7:
                if df['Current'][i] < 130:
                    df.loc[i, 'Recover'] = True
                if df['Current'][i + 1] < 130:
                    df.loc[i + 1, 'Trip'] = True

        # This loop goes over the length of df, looks for a condition in where we are filling, If that condition is true
        # it then looks to see if the next current falls below 1 mA, if this happens then we have another trip before
        # we have fully recovered. Therefore we need to set a recovery time to just before the trip happened at i-1
        # Did not go with above method as it was too difficult to track changes over 1 second intervals, The way below
        # goes over the length of the dataframe and finds wherever there is a trip, once that is found it sets the
        # previous line to recover and this solves our problem

        for i in range(1, len(df)):
            if df['Trip'][i]:
                df.loc[i - 1, 'Recover'] = True

        # for i in range(0, len(df)-1):
        #     if df['Current_S'][i] > df['Current'][i]:
        #         if df['Current'][i+1]

        # for i in range(1, len(df)):
        #     if df['Current'][i - 1] > 10 and df['Current_S'][i - 1] > df['Current'][i - 1]:
        #         if df['Current_S'][i] < 1:
        #             df.loc[i - 1, 'Recover'] = True

        # if 10 < df['Current'][i - 1] < df['Current_S'][i - 1]:
        #     if df['Current_S'][i] < 1:
        #         df.loc[i - 1, 'Recover'] = True

        # These two if statements look at the beginning and end of the week. Since we are always starting at Sunday
        # 00:00:00, we may have started with a trip from the previous week and thats why we need to set the Trip
        # equal to True, to account for downtime. Likewise, if the Current in the last row is still less than 1 we
        # need to set the Recovery equal to True so we can have an accurate account of downtime even if we haven't
        # recovered

        if df['Current'][0] < 130:
            df.loc[0, 'Trip'] = True
        last_row = len(df) - 1
        if df['Current'][last_row] < 130:
            df.loc[last_row, 'Recover'] = True

        # This loop will create two lists one for the start time of the recovery and one for the end time of the
        # recovery(kind of). The start time for the trips is going to be correct due to the conditions we have.
        # However, the recovery takes all accounts where current is increasing and above 220 so we will have a lot of
        # values in this list.

        for i in range(0, len(df)):
            if df['Trip'][i]:
                self.rec_s.append(pd.to_datetime(df['Time'][i]))
            if df['Recover'][i]:
                self.rec_e.append(pd.to_datetime(df['Time'][i]))

        # This loop fixes the above problem, it first loops over rec_s list, for the value in rec_s it loops over
        # rec_e, if the value in rec_e is greater than the value in rec_s, it appends this value to a new list rec.
        # It the breaks the inner for loop and goes to the next value in rec_s. This will allow us to have the same
        # number of items in each list and we will have lists that have a start and end time

        for i in self.rec_s:
            for v in self.rec_e:
                if v > i:
                    self.rec.append(v)
                    break
        QtWidgets.QApplication.restoreOverrideCursor()
        print('Data is collected, the files will now be saved')
        print()

    def get_info(self):

        self.trip_list = list(map(list, zip(self.rec_s, self.rec)))

        if len(self.trip_list) > 0:

            for i in range(0, len(self.trip_list)):
                print('Trip #{} start time:'.format(i+1), '\n', self.trip_list[i][0])
                print('Trip #{} end time:'.format(i+1), '\n', self.trip_list[i][1])
                trip_time_i = pd.Timedelta(self.trip_list[i][1] - self.trip_list[i][0]).seconds / 60
                trip_time_i = round(trip_time_i, 1)
                print('Trip #{} recovery time:'.format(i+1), '\n', '{} Minutes'.format(trip_time_i))
                self.trip_recovery_times.append(trip_time_i)
                self.num_of_trips.append(i + 1)
                print()

            print('This is a list of all trip times:', '\n', self.trip_recovery_times)
            print()
            print("Total trip time for this period in Minutes is:", '\n', sum(self.trip_recovery_times))

            for i in range(0, len(self.trip_list)):
                self.trip_start_time.append(self.trip_list[i][0])
                self.trip_end_time.append(self.trip_list[i][1])

            self.total_downtime = sum(self.trip_recovery_times)

            self.trip_stats_dict = {'Trip #': self.num_of_trips,
                                    'Trip Start Time': self.trip_start_time,
                                    'Trip End Time': self.trip_end_time,
                                    'Recovery Time': self.trip_recovery_times,
                                    'Total Downtime': self.total_downtime}

        else:

            self.total_downtime = 0
            self.trip_recovery_times = [0]

        return

    def save_weekly_csv(self):

        if len(self.trip_list) > 0:

            filename = "{}_{}-CSV.csv".format(self.sun, self.sat)
            file = self.path + filename
            trip_stats = pd.DataFrame(self.trip_stats_dict, columns=['Trip #', 'Trip Start Time', 'Trip End Time',
                                                                     'Recovery Time', 'Total Downtime'])
            trip_stats.to_csv(file, index=False)

        else:

            return

    def save_weekly_graph(self):

        if len(self.trip_list) > 0:
            # sns.set(style="whitegrid")
            # tips = sns.load_dataset("tips")

            # Setting the figure size
            fig = plt.figure(figsize=(10, 7))

            y_pos = np.arange(len(self.num_of_trips))
            plt.bar(y_pos, self.trip_recovery_times, width=0.5, color='red')

            # adding label to the top of each bars
            for x, y in zip(y_pos, self.trip_recovery_times, ):
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
            plt.ylim(0, max(self.trip_recovery_times) + 10)

            # Create names
            plt.xticks(y_pos, self.num_of_trips, )

            filename = "{}_{}-Graph.png".format(self.sun, self.sat)
            file = self.path + filename
            fig.savefig(file, bbox_inches=None, dpi=None)

        else:

            return

    def save_total_csv(self):

        total_wk_time = 10080 - len(self.exclude_time) * 480
        percentage_up_time = ((total_wk_time - self.total_downtime) / total_wk_time) * 100
        mean_time_to_recover = self.total_downtime / len(self.trip_recovery_times)
        mean_time_between_failures = (total_wk_time / 60) / len(self.trip_recovery_times)
        date_wk_end = self.sat

        # cycle_31 = pd.date_range(start='2020-01-01', end='2020-06-28')
        # cycle_32 = pd.date_range(start='2020-07-01', end='2020-12-31')
        #
        # if self.sun in cycle_31:
        #     self.cycle = 'cycle_31'
        # elif self.sun in cycle_32:
        #     self.cycle = 'cycle_32'

        self.cycle = 'cycle_32'

        totals_dict = {'Date Week End': date_wk_end,
                       'Number of Trips': self.num_of_trips,
                       'Total Week Time': total_wk_time,
                       'Total Trip Time': self.total_downtime,
                       'Percentage Up Time': percentage_up_time,
                       'Mean Time To Recover': mean_time_to_recover,
                       'Mean Time Between Failures': mean_time_between_failures}

        filename = '{}.csv'.format(self.cycle)
        file = self.path + filename

        if os.path.isfile(file):
            totals = pd.read_csv(file)
            if date_wk_end in totals['Date Week End'].values:
                totals.drop(totals.loc[totals['Date Week End'].values == date_wk_end].index, inplace=True)
                totals.to_csv(file, index=False)
                totals = pd.DataFrame(totals_dict, columns=['Date Week End',
                                                            'Number of Trips'
                                                            'Total Week Time',
                                                            'Total Trip Time',
                                                            'Percentage Up Time',
                                                            'Mean Time To Recover',
                                                            'Mean Time Between Failures'], index=[0])
                totals.to_csv(file, mode='a', header=False, index=False)
                totals = pd.read_csv(file)
                totals['Date Week End'] = pd.to_datetime(totals['Date Week End'])
                totals = totals.sort_values(by=['Date Week End'])
                totals.to_csv(file, index=False)

            else:
                totals = pd.DataFrame(totals_dict, columns=['Date Week End',
                                                            'Number of Trips'
                                                            'Total Week Time',
                                                            'Total Trip Time',
                                                            'Percentage Up Time',
                                                            'Mean Time To Recover',
                                                            'Mean Time Between Failures'], index=[0])
                totals.to_csv(file, mode='a', header=False, index=False)
                totals = pd.read_csv(file)
                totals['Date Week End'] = pd.to_datetime(totals['Date Week End'])
                totals = totals.sort_values(by=['Date Week End'])
                totals.to_csv(file, index=False)

        else:
            totals = pd.DataFrame(totals_dict, columns=['Date Week End',
                                                            'Number of Trips'
                                                            'Total Week Time',
                                                            'Total Trip Time',
                                                            'Percentage Up Time',
                                                            'Mean Time To Recover',
                                                            'Mean Time Between Failures'], index=[0])
            totals.to_csv(file, index=False)

    def save_total_graph(self):

        filename = '{}.csv'.format(self.cycle)
        file = self.path + filename
        running_total = pd.read_csv(file)
        percentage_up_time = running_total['Percentage Up Time'].tolist()
        mean_time_to_recover = running_total['Mean Time To Recover'].tolist()
        date_week_end = running_total['Date Week End'].tolist()
        mean_time_between_failures = running_total['Mean Time Between Failures'].tolist()

        print(mean_time_between_failures)

        # Plotting the variables
        fig = plt.figure(figsize=(10, 4))

        # Data
        x = date_week_end
        y1 = percentage_up_time
        y2 = mean_time_to_recover

        # create figure and axis objects with subplots()
        fig, ax = plt.subplots()

        # make a plot
        plot1 = ax.plot(x, y1, linewidth=2, color="orange", marker="o", label='Percentage up time')

        # set x-axis label
        ax.set_xlabel("Date Week End", fontsize=13)

        # set y-axis label
        ax.set_ylabel("percentage up time (%)", color="orange", fontsize=13)

        # twin object for two different y-axis on the sample plot
        ax2 = ax.twinx()

        # make a plot with different y-axis using second axis object
        plot2 = ax2.plot(x, y2, linewidth=2, color="blue", marker="o", label='mean time to recover')
        ax2.set_ylabel("mean time to recover (mins)", color="blue", fontsize=13)
        plt.title('Trip Weekly Stat', fontsize=13)

        # Add legend
        lns = plot1 + plot2
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.40),
                  fancybox=True, shadow=True, ncol=5)
        fig.autofmt_xdate(rotation=45)  # line to slant the xtick labels

        # Saving cumulative weekly file to directory
        filename = '{}-Graph.png'.format(self.cycle)
        file = self.path + filename
        fig.savefig(file, bbox_inches='tight', dpi=200)

    def display_figures(self):
        graph_list = ["{}_{}-Graph.png".format(self.sun, self.sat), '{}-Graph.png'.format(self.cycle)]
        for graph in graph_list:
            file = self.path + graph
            if os.path.isfile(file):
                img = Image.open(file)
                img.show()
            else:
                print()
                print('There were not any trips this week, so no weekly graph will be saved')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = WeeklyStats()
    app.exec_()
