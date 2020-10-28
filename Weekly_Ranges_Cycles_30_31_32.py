import pandas as pd

cycle_range_week_start = pd.date_range(start='6/30/2019T00:00:00', end='12/31/2020', freq='W')
cycle_range_week_end = []

for i in cycle_range_week_start:
    cycle_range_week_end.append(i + pd.Timedelta(days=6, hours=23, minutes=59, seconds=59))

range_dict = {'Week_Start' : cycle_range_week_start, 'Week_End' : cycle_range_week_end}

exclusion_weeks_start_str = ['10/13/2019T00:00:00', '10/20/2019T00:00:00','10/27/2019T00:00:00', '11/3/2019T00:00:00', '11/10/2019T00:00:00', '11/17/2019T00:00:00', '12/29/2019T00:00:00',
                             '3/22/2020T00:00:00', '3/29/2020T00:00:00', '4/5/2020T00:00:00', '4/12/2020T00:00:00', '4/19/2020T00:00:00', '4/26/2020T00:00:00', '5/3/2020T00:00:00',
                             '5/10/2020T00:00:00', '5/17/2020T00:00:00', '5/24/2020T00:00:00', '5/31/2020T00:00:00', '6/7/2020T00:00:00', '6/14/2020T00:00:00', '6/21/2020T00:00:00',
                             '6/28/2020T00:00:00', '7/5/2020T00:00:00', '7/12/2020T00:00:00', '8/16/2020T00:00:00', '10/4/2020T00:00:00', '10/11/2020T00:00:00', '10/18/2020T00:00:00',
                             '10/25/2020T00:00:00', '11/1/2020T00:00:00', '11/8/2020T00:00:00', '11/15/2020T00:00:00', '11/22/2020T00:00:00', '11/29/2020T00:00:00', '12/6/2020T00:00:00',
                             '12/13/2020T00:00:00', '12/20/2020T00:00:00', '12/27/2020T00:00:00']

exclusion_weeks_start_date = [pd.to_datetime(date) for date in exclusion_weeks_start_str]

df = pd.DataFrame(range_dict)

for i in range(len(df)):
    if df['Week_Start'][i] in exclusion_weeks_start_date:
        df.drop(i, inplace=True)

df.to_csv('Weekly_Ranges_Cycles_30_31_32.csv')

