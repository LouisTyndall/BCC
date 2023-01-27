import requests
from password import *
import pandas as pd
from datetime import timedelta
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sites=['R0101L3','R0101L4']
start = datetime.datetime.strptime('2023-1-16', '%Y-%m-%d')
days = 7
end = start+datetime.timedelta(days=days)
url ='http://bcc.bccutc.com/rtem_csv.json?'

print(start, end)

dfs=[]
for site in sites:
    params = {'ApiKey':key,
         'earliest':start,
         'latest':end,
         'SCN':site,
    }
    result=requests.get(url, params=params).json()
    df=pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
    dfs.append(df)

df = pd.concat(dfs)
df.Date = pd.to_datetime(df.Date)
df.reset_index(drop=True,inplace=True)
df.set_index('Date',inplace=True)

df['Total'] = df['Total'].astype(int)
df['AverageSpeed'] = df['AverageSpeed'].astype(float)
df = df.resample('15 Min').mean()
df = df[df.AverageSpeed < 70]

rng = pd.date_range(start, end, freq='5 min')
d2 = pd.DataFrame(index=pd.date_range(start,end, freq='15T'))
df = df.join(d2,how='right')
df = df.resample('15 min').mean()
df = df.iloc[:-1,:]
df['AverageSpeed'] = df['AverageSpeed'].fillna(0)
df['Total'] = df['Total'].fillna(0)
df1 = df
#time = df['AverageSpeed'].tolist()
time = df['Total'].tolist()
diff = np.array_split(time, days)
date = pd.date_range(start,end-timedelta(days=1),freq='d').strftime('%Y-%m-%d').tolist()
df = pd.DataFrame(data=diff, columns=rng[:96].strftime('%H-%M-%S'), index=[date])
df['Date'] = date
df['Date'] =pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.resample('1D').mean()
df.replace(0, np.nan, inplace=True)


df1 = df1.resample('1H').mean()
df2 = df1.resample('1D').sum()
plt.plot(df1.index,df1['Total'])
plt.title("A38 Traffic Count")
plt.xlabel("Time")
plt.ylabel("Number of vehicles")
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.show()

fig, ax = plt.subplots(figsize=(20,15)) 
x_axis_labels = ["00:00:00", "00:15:00", "00:30:00", "00:45:00", "01:00:00", "01:15:00", "01:30:00", "01:45:00",
                 "02:00:00", "02:15:00", "02:30:00", "02:45:00", "03:00:00", "03:15:00", "03:30:00", "03:45:00", 
                 "04:00:00", "04:15:00", "04:30:00", "04:45:00", "05:00:00", "05:15:00", "05:30:00", "05:45:00", 
                 "06:00:00", "06:15:00", "06:30:00", "06:45:00", "07:00:00", "07:15:00", "07:30:00", "07:45:00", 
                 "08:00:00", "08:15:00", "08:30:00", "08:45:00", "09:00:00", "09:15:00", "09:30:00", "09:45:00", 
                 "10:00:00", "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", "11:30:00", "11:45:00", 
                 "12:00:00", "12:15:00", "12:30:00", "12:45:00", "13:00:00", "13:15:00", "13:30:00", "13:45:00", 
                 "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00", "15:15:00", "15:30:00", "15:45:00", 
                 "16:00:00", "16:15:00", "16:30:00", "16:45:00", "17:00:00", "17:15:00", "17:30:00", "17:45:00", 
                 "18:00:00", "18:15:00", "18:30:00", "18:45:00", "19:00:00", "19:15:00", "19:30:00", "19:45:00", 
                 "20:00:00", "20:15:00", "20:30:00", "20:45:00", "21:00:00", "21:15:00", "21:30:00", "21:45:00", 
                 "22:00:00", "22:15:00", "22:30:00", "22:45:00", "23:00:00", "23:15:00", "23:30:00", "23:45:00"]


ax = sns.heatmap(df, cbar_kws={'label': 'Count', 'orientation': 'horizontal'},
                   mask=df.isnull(),cmap="YlGnBu", xticklabels=x_axis_labels, ax = ax)

plt.title(f'A38 Traffic Count Heatmap - Inbound - w/c {start}', fontsize = 20)
plt.xlabel('Time', fontsize = 15)
plt.ylabel('Date', fontsize = 15)

plt.show()
