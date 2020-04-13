#!/usr/bin/python3
'''cd to where script is located then run this command: venv/bin/python3 Weekly_Stats.py '''


import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from datetime import timedelta
import seaborn as sns
import sys


#Adding gridlines to Plot
sns.set(style="whitegrid")
tips = sns.load_dataset("tips")



exclude_time = []
rec_s = []
rec_e = []
rec = []


def week():
    global sunday, saturday, url_csv_retrieval
    sunday = str(input('Enter date for the Sunday the week began on in this format: YYYY,MM,DD: '))
    saturday = str(input('Enter date for the Saturday the week ended on in this format: YYYY,MM,DD: '))

    url_archiver = 'http://vm-archiver-02.clsi.ca:17668/retrieval/ui/viewer/archViewer.html?pv=PCT1402-01:mA:fbk&from={}T00:00:00&to={}T23:59:59&binSize=30' \
        .format(sunday.replace(',', '-'), saturday.replace(',', '-'))

    print('Click this link to show data archiver plot:' ,'\n', url_archiver)

    sun = tuple(map(int, sunday.split(',')))
    sun = datetime.datetime(*sun)
    sat = saturday + ',23,59,59'
    sat = tuple(map(int, sat.split(',')))
    sat = datetime.datetime(*sat)

    sun = sun + timedelta(hours=6)
    sat = sat + timedelta(hours=6)

    url_csv_retrieval = 'http://vm-archiver-02.clsi.ca:17668/retrieval/data/getData.csv?pv=PCT1402-01%3AmA%3Afbk&from={}T{}%3A{}%3A{}Z&to={}T{}%3A{}%3A{}Z'\
        .format(sun.strftime('%Y-%m-%d'), sun.strftime('%H'), sun.strftime('%M'),
        sun.strftime('%S'), sat.strftime('%Y-%m-%d'), sat.strftime('%H'),
        sat.strftime('%M'), sat.strftime('%S'))



def exclusions():
    num_of_exclusions_list = []
    num_of_exclusions = int(input('How many shifts do you want to exclude from this week? ie: Maintenance and/or Development: '))
    for i in range(num_of_exclusions):
        num_of_exclusions_list.append(i)
    exc_time_s = []
    exc_time_e = []
    for i in num_of_exclusions_list:

        date_exclusion_start_i = str(input('Enter start date and time of the exclusion in this format: YYYY,MM,DD,HH,MM,SS: '))
        date_exclusion_start_i = tuple(map(int, date_exclusion_start_i.split(',')))
        date_exclusion_start_i = datetime.datetime(*date_exclusion_start_i)
        date_exclusion_end_i = date_exclusion_start_i + timedelta(hours=8)
        exc_time_s.append(date_exclusion_start_i)
        exc_time_e.append(date_exclusion_end_i)

    for i in range(num_of_exclusions):
        global exclude_time
        exclude_time = list(map(list, zip(exc_time_s, exc_time_e)))
        return exclude_time


def recovery_times():
    df = pd.read_csv(url_csv_retrieval)
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


def trip_times():
    trip_recovery_times = []
    num_of_trips = []
    trip_list = list(map(list, zip(rec_s, rec)))

    # Script to save output file
    # path = "/home/richart/AOD/Weekly_Stats_Docs/" # Linux Path
    path = "H:\Documents\Projects\Weekly_Stats_Docs" # Windows Path
    filename = "{}_{} Document.txt".format(sunday.replace(',', '-'), saturday.replace(',''', '-'))
    file = path + filename
    sys.stdout = open(file, "w")


    for i in range(0, len(trip_list)):
        print('Trip #:', i+1, 'start time', trip_list[i][0])
        print('Trip #:', i+1, 'end time', trip_list[i][1])
        trip_time_i = pd.Timedelta(trip_list[i][1] - trip_list[i][0]).seconds / 60
        trip_time_i = round(trip_time_i, 1)
        print('This is Trip #', i + 1, 'recovery time', '\n', trip_time_i, 'Minutes')
        trip_recovery_times.append(trip_time_i)
        num_of_trips.append(i+1)


    print('This is a list of all trip times:' ,'\n', trip_recovery_times)
    print("Total trip time for this period in Minutes is :", sum(trip_recovery_times))



    # Setting the figure size
    fig = plt.figure(figsize=(10, 7))

    y_pos = np.arange(len(num_of_trips))
    plt.bar(y_pos, trip_recovery_times, width = 0.5, color= 'red')

    # adding label to the top of each bars
    for x, y in zip(y_pos, trip_recovery_times,):
        label = "{:.1f}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y), # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center', fontsize = 15, fontweight = 'bold')  # horizontal alignment (ha) can be left, right or center


    # Add title and axis names
    plt.title('Trip Weekly Stat ({}_{})' .format(sunday.replace(',', '-'),saturday.replace(',''', '-'), fontsize=17))
    plt.xlabel('Number of Trips', fontsize=15)
    plt.ylabel('Trip Recovery Time (Minutes)', fontsize=15)


    #Limits for the Y axis2
    plt.ylim(0, max(trip_recovery_times) + 10)

    # Create names
    plt.xticks(y_pos, num_of_trips,)

    # Saving the plot as an image
    # path = "/home/richart/AOD/Weekly_Stats_Docs/" # Linux Path
    path = "H:\Documents\Projects\Weekly_Stats_Docs"  # Windows Path
    filename = "{}_{} Graph.png".format(sunday.replace(',', '-'), saturday.replace(',''', '-'))
    file = path + filename
    fig.savefig(file, bbox_inches=None, dpi=None)
    
    # Show graphic
    plt.show()
    sys.stdout.close() # Close text file




def main():
    week()
    exclusions()
    recovery_times()
    print('This is a list of all trip time starts:' , '\n', rec_s)
    print('This is a list of all trip time ends:' , '\n', rec)
    trip_times()


if __name__ == '__main__':
    main()




