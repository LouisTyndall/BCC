###Data every 5 minutes
import datetime
from datetime import timedelta
import pandas as pd
import requests
import numpy as np
from passwords import key


#start=input('Enter date (YYYY-MM-DD)')
start = '2021-1-1'
#numday=input('Number of days to search for')
#site =input('Enter site')
site = 'R0101L1'
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(365))

url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start1)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df=pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])

df.Date = pd.to_datetime(df.Date)
df.reset_index(drop=True,inplace=True)
df.set_index('Date',inplace=True)
df['Total'] = df['Total'].astype(int)
df['AverageSpeed'] = df['AverageSpeed'].astype(float)

df = df[['AverageSpeed']]
df.drop(df.tail(1).index,inplace=True)
df =df.resample('5Min').mean()

df = df['AverageSpeed'].to_frame()
df['SMA24'] = df['AverageSpeed'].ewm(span = 288).mean()

df['difference'] = abs(df['SMA24'] - df['AverageSpeed'])

speed = df['AverageSpeed'].tolist()
SMA24 = df['SMA24'].tolist()
difference = df['difference'].tolist()
diff = np.array_split(difference, 365)

lst = [i for i in range(1,288+1)]
lst = [str(x) for x in lst]

date = pd.date_range(start,end-timedelta(days=1),freq='d').strftime('%Y-%m-%d').tolist()
df = pd.DataFrame(data=diff, columns=lst, index=[date])

df['sum']= df.sum(axis=1)


df['total'] = df.select_dtypes(np.number).gt(15).sum(axis=1)
df=df.loc[(df['total'] >= 48)]

dates = df.index.tolist()

print(dates)
