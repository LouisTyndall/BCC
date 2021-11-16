import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
from passwords import key

#Set search parameters, date, datatype and number of days to search for
start=input('Enter date (YYYY-MM-DD)')
datatype=input('Enter dataset (Total, AverageSpeed, Car, HGV, LGV, Bus)')
site=input('Enter site code')
numday=input('Number of days to search for')
vehicle_types=['Car','Bus','HGV','LGV','MotorBike','Total']
start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
end = start1 + datetime.timedelta(days=int(numday))

#Retrieve data and convert to dataframe
url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 
result=requests.get(url).json()
df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
df['Date'] = pd.to_datetime(df['Date'])

#Firstly, change vehicle data to int. Secondly, provide a count for each type of vehicle. Commit this to a list and print.
vehicles_total=[]
for vehicle_type in vehicle_types:
	df[vehicle_type] = df[vehicle_type].astype(int)
	vehicle_count = sum(int(result['RTEM_CSVs']['kids'][n]['kids'][i]) for n in result['RTEM_CSVs']['kids'])
	vehicle_type_count=f'The total {vehicle_type} count is {vehicle_count}'
	vehicles_total.append(vehicle_type_count)

for i in vehicles_total:
	print(i)

#Plot graph of selected datatype throughout the specified time period.
plt.plot(df['Date'],df[f'{datatype}'], marker='o',linestyle='none', label= f'{datatype} count');
plt.xticks(rotation = '25')
plt.xlabel('Date')
plt.ylabel(f'{datatype} Count')
plt.title(f'{numday} Day Count for {datatype} at site {site} ({start})')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(40, 15)
plt.show()



