import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
from passwords import key

start=input('Enter date (YYYY-MM-DD)')
#datatype=input('Enter dataset (Total, AverageSpeed, Car, HGV, LGV, Bus)')
site=input('Enter site code')
numday=input('Number of days to search for')
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))

url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df=pd.DataFrame(result)

df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
df.Date = pd.to_datetime(df.Date)
df['Total']=df['Total'].astype(int)
df.set_index('Date',inplace=True)
new = df.resample('D').sum()
new.drop(index=df.index[-1],axis = 0, inplace=True)

plt.bar(new.index, new['Total'], label='count')
plt.xlabel('Date')
plt.ylabel('Number of vehicles')
plt.title(f'Number of vehicles on {site} over time')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(40, 15)
plt.show()
