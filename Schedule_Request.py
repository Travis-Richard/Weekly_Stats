import requests
import pandas as pd
import os

path = r'C:\Users\richart\Documents\Projects\Weekly_Stats_Documents/'
filename = 'Exclusion_Shifts_Master.csv'
file = path + filename

# using cycle 30, 31 and 32 in link below to create list

response = requests.get("https://user.lightsource.ca/api/v1/schedule/32/modes/").json()
exclusions = pd.json_normalize(response)
exclusions = exclusions.drop(columns=['id', 'tags', 'cancelled', 'rendering', 'display', 'kind', 'description', 'tentative'])


exclusions = exclusions[exclusions.name != 'N']
exclusions = exclusions[exclusions.name != 'NS']

exclusions['start'] = pd.to_datetime(exclusions['start']) - pd.Timedelta(hours = 6)
exclusions['start'] = exclusions['start'].dt.tz_localize(None)

exclusions['end'] = pd.to_datetime(exclusions['end']) - pd.Timedelta(hours = 6,seconds = 1)
exclusions['end'] = exclusions['end'].dt.tz_localize(None)

exclusions = exclusions.sort_values(by = 'start')



if os.path.isfile(file):
    exclusions.to_csv(file, mode='a', header=False, index=False)
    exclusions = pd.read_csv(file)
    exclusions['start'] = pd.to_datetime(exclusions['start'])
    exclusions = exclusions.sort_values(by='start')
    exclusions.to_csv(file, index=False)

else:
    exclusions.to_csv(file, index=False)
