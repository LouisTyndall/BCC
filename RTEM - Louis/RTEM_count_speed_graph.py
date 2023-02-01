import datetime
import pandas as pd
from datetime import date
import requests
from passwords import key,password
import matplotlib.pyplot as plt

#Set up search parameters, including date and the number of days to search for.
start = input('Date:')
start = datetime.datetime.strptime(start, '%Y-%m-%d')
day = input('Number of days:')
end = start + datetime.timedelta(days=int(day))
sites= ['R0101L1',]#'R0101L2']

dfs=[]
for site in sites:
    #Get request for each site, check that the response is 200
    url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
    result=requests.get(url)
    if result.status_code != 200:
        print('400 error')
        continue
    result = result.json()
    if len(result['RTEM_CSVs']) == 1:
        ('Empty data frame')
        continue
    #if there is data, format and resample to 1H bins.
    df=pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
    df['Date'] =pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['Total'] = df['Total'].astype(float)
    df['AverageSpeed'] = df['AverageSpeed'].astype(float)
    df = df.resample('1H').mean()
    dfs.append(df)

#Combine the dataframes, and add a new column for the mean speed.
df = pd.concat(dfs)
df.loc['mean'] = df.mean()
mean = df.values[-1].tolist()
df = df.iloc[:-1,:]

plt.figure(figsize=(35,20))
fig, ax1 = plt.subplots()

#Plot the graph
ax2 = ax1.twinx()
ax1.bar(df.index,df['Total'],color='red',align='edge', width=(df.index[1]-df.index[0])*0.8)
ax2.plot(df.index,df['AverageSpeed'], linestyle="",marker="o")

ax1.set_xlabel('Date')
ax1.set_ylabel('Count', color='r')
ax2.set_ylabel('Average Speed')
fig.set_size_inches(18.5, 10.5)
plt.show()
