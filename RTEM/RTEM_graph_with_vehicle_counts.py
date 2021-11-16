import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import requests
import numpy as np
from passwords import key


start=input('Enter date (YYYY-MM-DD)')
datatype=input('Enter dataset (Total, AverageSpeed, Car, HGV, LGV, Bus)')
site=input('Enter site code')
numday=input('Number of days to search for')
vehicle_types=['Car','Bus','HGV','LGV','MotorBike','Total']
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))

url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df=pd.DataFrame(result)

a = [[datetime.datetime.strptime(result['RTEM_CSVs']['kids'][n]['kids']['Date'],"%Y-%m-%d %H:%M:%S"),\
int(result['RTEM_CSVs']['kids'][n]['kids'][datatype])] for n in result['RTEM_CSVs']['kids']]

vehicles_total=[]
for i in vehicle_types:
	i1 = sum(int(result['RTEM_CSVs']['kids'][n]['kids'][i]) for n in result['RTEM_CSVs']['kids'])
	i=f'The total {i} count is {i1}'
	vehicles_total.append(i)

for i in vehicles_total:
	print(i)

ax = plt.plot([n[0] for n in a],[m[1] for m in a], marker='o',linestyle='none', label=' vehicle count');
plt.xticks(rotation = '25')
plt.xlabel('Date')
plt.ylabel(f'{datatype} Count')
plt.title(f'{numday} Day Count for {datatype} at site {site} ({start})')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(40, 15)
plt.show()



