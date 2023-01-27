from datetime import datetime, timedelta
import pandas as pd
import requests
from password import key,password
import time
import smtplib

last_15 = datetime.now() - timedelta(minutes = 15)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')

def check_speed():
	url='http://bcc.opendata.onl/UTMC%20RTEM.json?ApiKey='+key
	result=requests.get(url).json()
	df = pd.DataFrame(result['RTEMS']['kids'][n]['kids'] for n in result['RTEMS']['kids'])
	df = df.drop('SCN',axis=1).join(pd.DataFrame(df.SCN.values.tolist()))
	df['Speed']=df['Speed'].astype(int)
	df.Date = pd.to_datetime(df.Date)
	df.set_index('Date',inplace=True)
	df=df[(df.index > last_15)]
	df=df[(df['Speed'] < 15)]
	df=df[(df['Speed']>0)]
	df['Sensor']=df['value']
	first_check = df['Sensor'].tolist()
	df = df[['Sensor','Speed','Direction','Lane','Vehicles']]
	return df,first_check

df1,first_check=check_speed()
print(df1, first_check)

time.sleep(1200)

df2, second_check=check_speed()
print(df2,second_check)

duplicates = [x for x in second_check if x in first_check]

df3 = df2.loc[df2['Sensor'].isin(duplicates)]

print(f'duplicates{duplicates}')
print(df3)

df1, first_check=check_speed()
