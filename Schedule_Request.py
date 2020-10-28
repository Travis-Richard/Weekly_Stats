import requests
import pandas as pd
import os

path = r'C:\Users\richart\Documents\Projects\Weekly_Stats_Documents/'
# filename = 'Exclusion_Shifts_Master.csv'
filename = 'Exclusion_Shifts_Master_NO_NS.csv'
file = path + filename

# using cycle 30, 31 and 32 in link below to create list

response = requests.get("https://user.lightsource.ca/api/v1/schedule/32/modes/").json()
exclusions = pd.json_normalize(response)
exclusions = exclusions.drop(columns=['id', 'tags', 'cancelled', 'rendering', 'display', 'kind', 'description', 'tentative'])


exclusions = exclusions[exclusions.name != 'N']
# exclusions = exclusions[exclusions.name != 'NS']

exclusions['start'] = pd.to_datetime(exclusions['start']) - pd.Timedelta(hours = 6)
exclusions['start'] = exclusions['start'].dt.tz_localize(None)

# exclusions['end'] = pd.to_datetime(exclusions['end']) - pd.Timedelta(hours = 6,seconds = 1)
exclusions['end'] = pd.to_datetime(exclusions['end']) - pd.Timedelta(hours = 6)
exclusions['end'] = exclusions['end'].dt.tz_localize(None)

exclusions = exclusions.sort_values(by = 'start')
exclusions.reset_index(inplace=True)
exclusions=exclusions.drop(columns=['index', 'name'])



multi_shift_exc_start = []
multi_shift_exc_end = []



for i in range(len(exclusions)):
    if exclusions['end'][i] - pd.Timedelta(hours=8) != exclusions['start'][i]:
        exc_range = pd.date_range(start=exclusions['start'][i], end=exclusions['end'][i], freq='8H')
        exclusions.drop(i, inplace=True)

        for i in range(len(exc_range[:-1])):
            multi_shift_exc_start.append(exc_range[i])
            multi_shift_exc_end.append(exc_range[i] + pd.Timedelta(hours=8))

start = exclusions['start'].tolist()
end = exclusions['end'].tolist()

for i in multi_shift_exc_start:
    start.append(i)

for i in multi_shift_exc_end:
    end.append(i)

exclusions = pd.DataFrame(list(zip(start, end)), columns=['Start', 'End'])
exclusions = exclusions.sort_values(by = 'Start')
exclusions['End'] = exclusions['End'] - pd.Timedelta(seconds=1)



if os.path.isfile(file):
    exclusions.to_csv(file, mode='a', header=None, index=False)
#
#
#     # exclusions = pd.read_csv(file)
#     # exclusions.columns = ['start', 'end', 'shift']
#     # exclusions['start'] = pd.to_datetime(exclusions['start'])
#     # exclusions = exclusions.sort_values(by='start')
#     # exclusions.to_csv(file, header=None, index=False)
#
else:
    exclusions.to_csv(file, header=None, index=False)
