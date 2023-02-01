import datetime
import pandas as pd
import numpy as np
from datetime import date
import requests
import password as p

#create a variable of todays date
key=p.key
today = date.today()
end= today+datetime.timedelta(days=1)
print(today)

#Get request with todays date and the desired location
site=input('Enter site code')
url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(today)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
df.Date = pd.to_datetime(df.Date)
df['AverageSpeed']=df['AverageSpeed'].astype(int)

#create a variable for the latest time stamp and the latest speed
Speed = df.iloc[-1]['AverageSpeed']
when = df.iloc[-1]['Date']

#Option to only print the variable if the speed is a certain level
#if 0< Speed <9

#Print the result
print('The latest average speed recorded was',Speed,'kmph at',when)
