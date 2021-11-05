import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime
from datetime import timedelta

search_date=input('What date do want to search for? (YYYY-MM-DD)')
day1 = datetime.datetime.strptime(search_date, '%Y-%m-%d')
day2=day1 + datetime.timedelta(days=1)
day3=day2 + datetime.timedelta(days=1)
day4=day3 + datetime.timedelta(days=1)
day5=day4 + datetime.timedelta(days=1)
day6=day5 + datetime.timedelta(days=1)
day7=day6 + datetime.timedelta(days=1)

days=[day1,day2,day3,day4,day5,day6]

d=[]
for day in days:
    d1=day.strftime('%Y-%m-%d')
    d.append(d1)

request=[]
for i in d:
    r1=requests.get('https://realjourneytime.azurewebsites.net/index.php?method=Journeys&fromCode=43000219503&toCode=43000414601&dateString='+i)
    request.append(r1)

times=[]
for i in request:
    t=i.json()['JourneyTimes']
    times.append(t)

df=[]
for i in times:
    df1=pd.DataFrame(i)
    df.append(df1)

df = pd.concat(df)
df.reset_index(drop=True,inplace=True)


#set up depature time column 
df[['x','y']]=df.RealDepartureTime.str.split('T',expand=True)
df[['DepartureTime','z']]=df.y.str.split('Z',expand=True)
df = df.sort_values(by='DepartureTime',ascending=True)

def convert(o_clock):
    h,m,s=o_clock.split(':')
    return int(m)*60+int(s)
min_col=[convert(t) for t in df['RealJourneyTime']]
df['RealTime'] =min_col

def convert(o_clock):
    h,m,s=o_clock.split(':')
    return int(m)*60+int(s)
min_col=[convert(t) for t in df['ScheduledJourneyTime']]
df['ScheduledTime'] =min_col

df['ScheduledTimeOver']=df['ScheduledTime'] + 60
df['ScheduledTimeUnder']=df['ScheduledTime'] - 60
df = df[(df['RealTime'] < 1500)]

df_under = df.loc[(df['RealTime']) <= df['ScheduledTimeUnder']]
df_over = df.loc[(df['RealTime']) >= df['ScheduledTimeOver']]

total=len(df)
num_over = len(df_over.index)
num_under = len(df_under.index)
num_ontime= len(df) - num_over - num_under


over_percent = (num_over/total)*100
under_percent = (num_under/total)*100
ontime_percent = (num_ontime/total)*100

df_over['Difference'] = df_over['RealTime'] - df_over['ScheduledTime']
x = df_over['Difference'].mean()

print('Average time over scheduled was', (x/60))
print(f'The total number of journeys was {total}')
print(f'The number of journeys on time was: {round(num_ontime)} ({round(ontime_percent,1)}%)')
print(f'The number of journeys late time was: {round(num_over)} ({round(over_percent,1)}%)')
print(f'The number of journeys early time was: {round(num_under)} ({round(under_percent,1)}%)')

plt.bar(df['DepartureTime'],df['RealTime'], label='Actual Time')
plt.plot(df['DepartureTime'],df['ScheduledTime'],'r', label='Scheduled Time')
plt.xlabel('Depature Time')
plt.ylabel('Journey Time (s)')
plt.title(f'Bus Journey Time, actual vs predicted for w/c {search_date}')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(40, 15)
plt.show()
