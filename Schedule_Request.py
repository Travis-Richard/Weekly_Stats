import requests
import pandas as pd

response = requests.get("https://user.lightsource.ca/api/v1/schedule/30/modes/").json()
df = pd.json_normalize(response)
df = df.drop(columns=['id', 'tags', 'cancelled', 'rendering', 'display', 'kind', 'description', 'tentative'])


df = df[df.name != 'N']
df = df[df.name != 'NS']

df['start'] = pd.to_datetime(df['start']) - pd.Timedelta(hours = 6)
df['start'] = df['start'].dt.tz_localize(None)

df['end'] = pd.to_datetime(df['end']) - pd.Timedelta(hours = 6,seconds = 1)
df['end'] = df['end'].dt.tz_localize(None)

df = df.sort_values(by = 'start')
