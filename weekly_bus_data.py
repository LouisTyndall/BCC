import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime

#set up variables to search for 7 days as URL only allows one day searches
search_date=input('What date do want to search for? (YYYY-MM-DD)')
day1 = datetime.datetime.strptime(search_date, '%Y-%m-%d')
day2=day1 + datetime.timedelta(days=1)
day3=day2 + datetime.timedelta(days=1)
day4=day3 + datetime.timedelta(days=1)
day5=day4 + datetime.timedelta(days=1)
day6=day5 + datetime.timedelta(days=1)
day7=day6 + datetime.timedelta(days=1)

days=[day1,day2,day3,day4,day5,day6]

#format date to datetime
d=[]
for day in days:
    d1=day.strftime('%Y-%m-%d')
    d.append(d1)

#creates url for each day
request=[]
for i in d:
    r1=requests.get('https://realjourneytime.azurewebsites.net/index.php?method=Journeys&fromCode=43000219503&toCode=43000414601&dateString='+i)
    request.append(r1)

#cretes dataframe for each day
times=[]
for i in request:
    t=i.json()['JourneyTimes']
    times.append(t)

df=[]
for i in times:
    df1=pd.DataFrame(i)
    df.append(df1)

#turns each dataframe into single dataframe
df_total = pd.concat(df)
df_total.reset_index(drop=True,inplace=True)

df_total[['X','Y']]=df_total.ScheduledDepartureTime.str.split('T',expand=True)
df_total[['time','Z']]=df_total.Y.str.split('Z',expand=True)
df_total['Date']=df_total['X']+ ' '+ df_total['time']

#converts journey time into seconds
def convert(o_clock):
    h,m,s=o_clock.split(':')
    return int(m)*60+int(s)
min_col=[convert(t) for t in df_total['RealJourneyTime']]
df_total['real'] =min_col

y=df_total.iloc[1]['ScheduledJourneyTime']

#convert scheduled time to seconds
def converty(line):
    h,m,s=line.split(':')
    return int(m)*60+int(s)
newline=[converty(y)]

#set up variable to early and late, 1 minute either side of scheduled journey time
newnum = ''.join(str(e) for e in newline)
late = int(newnum)+60
early = int(newnum)-60
ontime= late - early
x=sum(df_total['real']>int(late))
y = sum(df_total['real'] > int(early))

percent = ontime+x+y

latepercent = (x/percent)*100
earlypercent = (y/percent)*100
onpercent = (ontime/percent)*100

#prints number of journeys on time, overtime and under time
print(f'The number of journeys on time was: {ontime}({round(onpercent,1)}%)')
print(f'The number of journeys over the scheduled time was: {x} ({round(latepercent,1)}%)')
print(f'The number of journeys under the scheduled time was: {y}({round(earlypercent,1)}%)')

#plots bar graph of journey times, with a red line indicating the scheduled journey time
plt.bar(df_total['time'],df_total['real'], label='Actual Time')
plt.axhline(newline, color='r', linestyle='--')
plt.xlabel('Depature Time')
plt.ylabel('Journey Time (m)')
plt.title('Bus Journey Time, actual vs predicted')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(40, 15)
plt.show()
