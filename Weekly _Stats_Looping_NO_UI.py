#### Use this file to loop over large amount of weeks ###


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import sys
import traceback
import os


class WeeklyStats():
    def __init__(self):
        self.exclude_time = []
        self.rec_s = []
        self.rec_e = []
        self.rec = []
        self.dates = []
        self.trip_recovery_times = []
        self.num_of_trips = []
        self.trip_start_time = []
        self.trip_end_time = []
        self.path = r'C:\Users\richart\Documents\Projects\Weekly_Stats_Documents/'  # Windows Path
        self.weekly_ranges = pd.read_csv('Weekly_Ranges_Cycles_30_31_32.csv')
        self.exclusion_shifts = pd.read_csv('Exclusion_Shifts_Master_NO_NS.csv', header=None)
        self.loop()

    def loop(self):
        self.weekly_ranges['Week_Start'] = pd.to_datetime(self.weekly_ranges['Week_Start'])
        self.weekly_ranges['Week_End'] = pd.to_datetime(self.weekly_ranges['Week_End'])
        self.exclusion_shifts.columns = ['start', 'end']
        self.exclusion_shifts['start'] = pd.to_datetime(self.exclusion_shifts['start'])
        self.exclusion_shifts['end'] = pd.to_datetime(self.exclusion_shifts['end'])

        for i in range(len(self.weekly_ranges)):
            print('starting ' + str(i+1) + ' of ' + str(len(self.weekly_ranges)))
            self.week_selection(i)
            self.exclude_times(i)
            self.get_data()
            self.get_info()
            self.save_weekly_csv(i)
            self.save_total_csv(i)
            self.clear(i)

    def week_selection(self, i):

        # Need to add 6 hours of time to our inputs as the CSV file takes into account the timezone, we will covert
        # back later on

        sunday = self.weekly_ranges['Week_Start'][i] + timedelta(hours=6)
        saturday = self.weekly_ranges['Week_End'][i] + timedelta(hours=6)

        self.url_csv_retrieval = 'http://vm-archiver-02.clsi.ca:17668/retrieval/data/getData.csv?pv=PCT1402-01%3AmA' \
                                 '%3Afbk&from={}T{}%3A{}%3A{}Z&to={}T{}%3A{}%3A{}Z' \
            .format(sunday.strftime('%Y-%m-%d'), sunday.strftime('%H'), sunday.strftime('%M'),
                    sunday.strftime('%S'), saturday.strftime('%Y-%m-%d'), saturday.strftime('%H'),
                    saturday.strftime('%M'), saturday.strftime('%S'))

        print('Week selection complete')

    def exclude_times(self, i):
        exc_s = []
        exc_e = []
        week_range = pd.date_range(start=self.weekly_ranges['Week_Start'][i], end=self.weekly_ranges['Week_End'][i], freq='H')

        for v in range(len(self.exclusion_shifts)):
            if self.exclusion_shifts['start'][v] in week_range:
                exc_s.append(self.exclusion_shifts['start'][v])
                exc_e.append(self.exclusion_shifts['end'][v])

        self.exclude_time = list(map(list, zip(exc_s, exc_e)))

        print('Exclude times complete')

    def get_data(self):

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

        print('Get data complete')

    def get_info(self):

        self.trip_list = list(map(list, zip(self.rec_s, self.rec)))

        if len(self.trip_list) > 0:

            for i in range(0, len(self.trip_list)):
                trip_time_i = pd.Timedelta(self.trip_list[i][1] - self.trip_list[i][0]).seconds / 60
                trip_time_i = round(trip_time_i, 1)
                self.trip_recovery_times.append(trip_time_i)
                self.num_of_trips.append(i + 1)


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

    def save_weekly_csv(self, i):

        if len(self.trip_list) > 0:

            filename = "{}_{}-CSV.csv".format(str(self.weekly_ranges['Week_Start'][i])[:-9], str(self.weekly_ranges['Week_End'][i])[:-9])
            file = self.path + filename
            trip_stats = pd.DataFrame(self.trip_stats_dict, columns=['Trip #', 'Trip Start Time', 'Trip End Time',
                                                                     'Recovery Time', 'Total Downtime'])
            trip_stats.to_csv(file, index=False)

            print('Weekly csv saved')

        else:

            return

    def save_total_csv(self, i):

        total_wk_time = 10080 - len(self.exclude_time) * 480
        percentage_up_time = ((total_wk_time - self.total_downtime) / total_wk_time) * 100
        mean_time_to_recover = self.total_downtime / len(self.trip_recovery_times)
        mean_time_between_failures = (total_wk_time / 60) / len(self.trip_recovery_times)
        date_wk_end = str(self.weekly_ranges['Week_End'][i])[:-9]

        totals_dict = {'Date Week End': date_wk_end,
                       'Number of Trips': len(self.trip_recovery_times),
                       'Total Week Time': total_wk_time,
                       'Total Trip Time': self.total_downtime,
                       'Percentage Up Time': percentage_up_time,
                       'Mean Time To Recover': mean_time_to_recover,
                       'Mean Time Between Failures': mean_time_between_failures}

        filename = 'Weekly_Stats_Master.csv'
        file = self.path + filename

        if os.path.isfile(file):
            totals = pd.read_csv(file)
            if date_wk_end in totals['Date Week End'].values:
                totals.drop(totals.loc[totals['Date Week End'].values == date_wk_end].index, inplace=True)
                totals.to_csv(file, index=False)
                totals = pd.DataFrame(totals_dict, columns=['Date Week End',
                                                            'Number of Trips',
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
                                                            'Number of Trips',
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
                                                            'Number of Trips',
                                                            'Total Week Time',
                                                            'Total Trip Time',
                                                            'Percentage Up Time',
                                                            'Mean Time To Recover',
                                                            'Mean Time Between Failures'], index=[0])
            totals.to_csv(file, index=False)

        print('Total csv saved')

    def clear(self, i):
        self.exclude_time.clear()
        self.rec_s.clear()
        self.rec_e.clear()
        self.rec.clear()
        self.dates.clear()
        self.trip_list.clear()
        self.trip_recovery_times.clear()
        self.num_of_trips.clear()
        self.trip_start_time.clear()
        self.trip_end_time.clear()
        self.trip_stats_dict.clear()

        print(str(i + 1) + ' of ' + str(len(self.weekly_ranges)) + ' complete')


if __name__ == '__main__':
    WeeklyStats()


