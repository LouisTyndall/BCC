import datetime
import pandas as pd
import numpy as np
from datetime import date
import requests
import password as p

key=p.key
today = date.today()
end= today+datetime.timedelta(days=1)
print(today)
site=input('Enter site code')
url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(today)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
df.Date = pd.to_datetime(df.Date)
df['AverageSpeed']=df['AverageSpeed'].astype(int)

Speed = df.iloc[-1]['AverageSpeed']
when = df.iloc[-1]['Date']

#if 0< Speed <9

print('The latest average speed recorded was',Speed,'kmph at',when)
