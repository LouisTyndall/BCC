import requests
from passwords import *
import pandas as pd

url = f'https://www.tfwm.onl/AWS_ClassCount.json?ApiKey={key}&earliest=22/09/2021&latest=23/09/2021'
result = requests.get(url).json()
df = pd.DataFrame(result['AWS_ClassCount']['kids'][n]['kids'] for n in result['AWS_ClassCount']['kids'])
df['class_Count'] = df['class_Count'].astype(int)
dfs = dict(tuple(df.groupby('camera_name')))
y = df['camera_name'].tolist()
y=list(set(y))

values=[]
for i in y:
    value = dfs[i]
    values.append(value)

df1 = {}
keys = range(len(y))
for i in keys:
        df1[i] = values[i]

#print(df1[1])
t = df['class'].tolist()
vehicle_type=list(set(t))

loc = df1[1]['camera_name'].iloc[1]

print(f'For {loc}:')
for i in vehicle_type:
    x = df1[0].loc[df1[0]['class'] == i]
    num = x['class_Count'].sum()
    if num > 0:
        print(f'There are {num} of type {i}')
