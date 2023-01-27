import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import requests
import numpy as np
import password as p

key=p.key

start=input('Enter date (YYYY-MM-DD)')
#datatype=input('Enter dataset (Total, AverageSpeed, Car, HGV, LGV, Bus)')
site=input('Enter site code')
numday=input('Number of days to search for')
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))

url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df=pd.DataFrame(result)

df2=df.iloc[:,0:40]
df2.count()

a = [[datetime.datetime.strptime(result['RTEM_CSVs']['kids'][n]['kids']['Date'],"%Y-%m-%d %H:%M:%S"),int(result['RTEM_CSVs']['kids'][n]['kids']['Total'])] for n in result['RTEM_CSVs']['kids']]
Car=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['Car']) for n in result['RTEM_CSVs']['kids'])
Bus=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['Bus']) for n in result['RTEM_CSVs']['kids'])
HGV=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['HGV']) for n in result['RTEM_CSVs']['kids'])
LGV=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['LGV']) for n in result['RTEM_CSVs']['kids'])
Motorcycle=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['MotorBike']) for n in result['RTEM_CSVs']['kids'])
Total=sum(int(result['RTEM_CSVs']['kids'][n]['kids']['Total']) for n in result['RTEM_CSVs']['kids'])

print('The total car count is',Car)
print('The total bus count is',Bus)
print('The total HGV count is',HGV)
print('The total LGV count is',LGV)
print('The total Motorcycle count is',Motorcycle)
print('The total count is',Total)


ax = plt.plot([n[0] for n in a],[m[1] for m in a]);
fig1=plt.gcf()
plt.xticks(rotation = '25')
fig1.set_size_inches(18.5,10.5)
plt.show
