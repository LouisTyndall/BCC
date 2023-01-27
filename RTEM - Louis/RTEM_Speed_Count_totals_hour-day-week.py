import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import requests
import numpy as np
from password import key


start=input('Enter date (YYYY-MM-DD)')
numday=input('Number of days to search for')
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))
datatype= 'Total'

#inner-city
#sites=['R0101L1','R0101L2','R0101L3','R0101L4','R3012L1','R3012L2','R23012L3','R0613L1','R0613L2','R0105L1','R0105L2','R0105L3','R0105L4','R7545L1','R7545L2','R7545L3','R7545L4','R7545L5','R7545L6']
sites=['R0101L1','R0101L2','R0101L3','R0101L4']

#ring-road
#sites=['R4012L1','R4012L2','R4012L3','R4012L4','R4012L5','R3156L1','R3156L2','R0821L1','R0821L2','R0821L3','R0511L1','R0511L2','R0511L3']

urls=[]
for site in sites:
    url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start1)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
    result=requests.get(url).json()
    df=pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
    urls.append(df)


for df in urls:
    df.Date = pd.to_datetime(df.Date)
    df.reset_index(drop=True,inplace=True)
    df.set_index('Date',inplace=True)
    df['AverageSpeed'] = df['AverageSpeed'].astype(int)
    df['Total'] = df['Total'].astype(int)
    new = df.resample('1H').mean()
    loc = df.iloc[-1]['SCN']['value']
    new.to_excel(f"{loc}.xlsx") 
    print(loc)
    print(new)
