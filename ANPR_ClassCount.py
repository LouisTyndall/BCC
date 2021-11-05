import requests
from passwords import *
import pandas as pd

url = f'https://www.tfwm.onl/AWS_ClassCount.json?ApiKey={key}&earliest=22/09/2021&latest=23/09/2021'
result = requests.get(url).json()
df = pd.DataFrame(result['AWS_ClassCount']['kids'][n]['kids'] for n in result['AWS_ClassCount']['kids'])
df['class_Count'] = df['class_Count'].astype(int)

t = df['class'].tolist()
vehicle_type=list(set(t))

df_new = df.loc[df['camera_name']== 'BW A457 Summer Hill Rd IB (City Centre)']

for i in vehicle_type:
    x = df_new.loc[df_new['class'] == i]
    num = x['class_Count'].sum()
    if num > 0:
        print(f'There are {num} of type {i}')
