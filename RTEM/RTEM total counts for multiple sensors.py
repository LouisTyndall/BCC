import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
from passwords import key

#Set up parameters for the search. The date and the number of days to search for.
start=input('Enter date (YYYY-MM-DD)')
numday=input('Number of days to search for')
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))

#The sites list contains all the sites that will be searched for
#inner-city
#sites= ['R0101L1','R0101L2','R0101L3','R0101L4','R3012L1','R3012L2','R3012L3','R0613L1','R0613L2','R0105L1','R0105L2','R0105L3','R0105L4','R7545L1','R7545L2','R7545L3','R7545L4','R7545L5','R7545L6']

#ring-road
sites=['R4012L1','R4012L2','R4012L3','R4012L4','R4012L5','R4012L6','R3156L1','R3156L2','R0821L1','R0821L2','R0821L3','R0815L1','R0815L2','R0815L3','R0815L4','R0815L5','R0815L6','R0511L1','R0511L2','R0511L3']

#This creates a list of dataframes for each of the sites. 
dfs=[]
for site in sites:
    url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start1)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
    result=requests.get(url).json()
    df=pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
    dfs.append(df)

#Here, the dataframe is formatted to set the index as the time series so it can be resampled. It is possible to change the resample, for example to hourly, daily, weekly. 
#The name of the location is selected using iloc and the last row is dropped. Finally, the data is saved as an excel sheet for analysis.
for df in dfs:
    loc = df.iloc[-1]['SCN']['value']
    df.Date = pd.to_datetime(df.Date)
    df.reset_index(drop=True,inplace=True)
    df.set_index('Date',inplace=True)
    df['Total'] = df['Total'].astype(int)
    new = df.resample('1D').sum()
    new.drop(new.tail(1).index,inplace=True)
    print(f'{loc} is {new}')
    new.to_excel(f'{loc} output.xlsx')
