import requests
from passwords import *
import pandas as pd
from datetime import timedelta
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

start = datetime.datetime.strptime('2022-2-26', '%Y-%m-%d')
end= start+datetime.timedelta(days=14)
loc= '1 - A38 City Centre to City Centre - IB'
vehicle = 'PETROL CAR'
url = 'http://www.tfwm.onl/AWS_RoutesAnalysis.json?'
params = {'ApiKey':key,
         'earliest':start,
         'latest':end,
         'Segment_ID':loc,
        'Class':vehicle,
}

result = requests.get(url, params=params).json()
df = pd.DataFrame(result['AWS_RoutesAnalysis']['kids'][n]['kids'] for n in result['AWS_RoutesAnalysis']['kids'])
df['BIN'] =pd.to_datetime(df['BIN'])
df.set_index('BIN', inplace=True)
df['Time_Taken'] = df['Time_Taken'].astype(int)
df = df.resample('30min').mean()
rng = pd.date_range(start, end, freq='30min')
d2 = pd.DataFrame(index=pd.date_range(start,end, freq='15T'))
df = df.join(d2,how='right')
df = df.resample('30min').mean()
df = df.iloc[:-1,:]
df['Time_Taken'] = df['Time_Taken'].fillna(0)
time = df['Time_Taken'].tolist()
diff = np.array_split(time, 14)
date = pd.date_range(start,end-timedelta(days=1),freq='d').strftime('%Y-%m-%d').tolist()
df = pd.DataFrame(data=diff, columns=rng[:48].strftime('%H-%M-%S'), index=[date])
df['time'] = date
df['time'] =pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
df = df.resample('1D').mean()
df.replace(0, np.nan, inplace=True)

fig, ax = plt.subplots(figsize=(13,10)) 
heat = sns.heatmap(df, cbar_kws={'label': 'Time (seconds)', 'orientation': 'horizontal'},mask=df.isnull(),cmap="YlGnBu")
heat
