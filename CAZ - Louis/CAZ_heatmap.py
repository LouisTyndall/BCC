import requests
from password import *
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#set up parameters for the date range

day = input('ENTER START DATE:')
dt = datetime.strptime(day, '%Y-%m-%d')
mon = dt.date()
tues = (dt + timedelta(days=1)).date()
weds = (dt + timedelta(days=2)).date()
thurs = (dt + timedelta(days=3)).date()
fri = (dt + timedelta(days=4)).date()
sat = (dt + timedelta(days=5)).date()
sun = (dt + timedelta(days=6)).date()

days = [mon, tues, weds, thurs, fri, sat, sun]

#retrive data from the API for each day

total = []
for day in days:
    headers = {
        'Earliest':f'{day} 00:00:00',
        'Latest':f'{day} 23:59:59',
        'ApiKey':'HDMWDFKB8IB64BFQ3351251166261'
    }
    url='http://opendata.onl/caz.json?'

    #get request, then convert the data to a data frame
    
    result = requests.get(url, headers = headers).json()
    df = pd.DataFrame(result['CAZ']['kids']['Data'])
    df = pd.json_normalize(df['kids'])

    df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                    'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
                   'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)
    
    #removing the cameras that are inside the centre
    internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
    df = df[~df['RSE Id'].isin(internal)]
    
    #Identifying cameras that are facing the 'wrong' way (Facing towards the city centre so approaching would be departing,
    #then reversing the direction.
    reverse = ['CAZ003','CAZ004','CAZ005','CAZ006','CAZ008','CAZ015','CAZ016','CAZ018','CAZ022','CAZ026','CAZ030','CAZ031',
          'CAZ035','CAZ037','CAZ038','CAZ039','CAZ041','CAZ047','CAZ053','CAZ060','CAZ061','CAZ064']

    df_filtered = df[(df["RSE Id"].isin(reverse))]
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
    df_2 = df[~df['RSE Id'].isin(reverse)]
    df = pd.concat([df_filtered,df_2])

    df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
    df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'
    
    con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
    know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006',
            'CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
    east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
    south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
    west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
    jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']
    
    #Optional filter to select specific cameras of interest
    lookup = ['CAZ035']
    df = df[df['RSE Id'].isin(lookup)]
    
    #Optional filters to select direction of interest
    #df = df.loc[df['Direction of Travel'] == 'Outbound']
    df = df.loc[df['Direction of Travel'] == 'Inbound']
    
    #Creating an index with a date to allow for resampling in 15 minute bins,
    #resampling using Lane gives the number of captures as each capture has a '1'
    df['Capture Date'] =pd.to_datetime(df['Capture Date'])
    df.set_index('Capture Date', inplace=True)
    
    df['Lane'] = df['Lane'].astype(int)
    df = df.resample('15 Min').sum()
    df = df[['Lane']]
    total.append(df)

#Create one dataframe from each day searched
df = pd.concat(total)
df.sort_values(by='Capture Date', ascending=True, inplace=True)

#Create a variable for day 1 and day 7 of the search, then create a list of 5 minute 
#intervals between these dates.
start = datetime.strptime(str(mon), '%Y-%m-%d')
days = 7
end = start+timedelta(days=days)
rng = pd.date_range(start, end, freq='5 min')

#Create a list of the capture number, then create an array for each day
time = df['Lane'].tolist()
diff = np.array_split(time, days)

#Create a date range for the 7 days of interest, then create an empty data frame using 
#the days and the arrays.
date = pd.date_range(start,end-timedelta(days=1),freq='d').strftime('%Y-%m-%d').tolist()
df = pd.DataFrame(data=diff, columns=rng[:96].strftime('%H-%M-%S'), index=[date])

#Add the date range to the dataframe as a new column, and resample by day
df['Date'] = date
df['Date'] =pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.resample('1D').mean()
df.replace(0, np.nan, inplace=True)

#Create a figure with the x-axis as 15 minute intervals
fig, ax = plt.subplots(figsize=(20,15)) 
x_axis_labels = ["00:00:00", "00:15:00", "00:30:00", "00:45:00", "01:00:00", "01:15:00", "01:30:00", "01:45:00",
                 "02:00:00", "02:15:00", "02:30:00", "02:45:00", "03:00:00", "03:15:00", "03:30:00", "03:45:00", 
                 "04:00:00", "04:15:00", "04:30:00", "04:45:00", "05:00:00", "05:15:00", "05:30:00", "05:45:00", 
                 "06:00:00", "06:15:00", "06:30:00", "06:45:00", "07:00:00", "07:15:00", "07:30:00", "07:45:00", 
                 "08:00:00", "08:15:00", "08:30:00", "08:45:00", "09:00:00", "09:15:00", "09:30:00", "09:45:00", 
                 "10:00:00", "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", "11:30:00", "11:45:00", 
                 "12:00:00", "12:15:00", "12:30:00", "12:45:00", "13:00:00", "13:15:00", "13:30:00", "13:45:00", 
                 "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00", "15:15:00", "15:30:00", "15:45:00", 
                 "16:00:00", "16:15:00", "16:30:00", "16:45:00", "17:00:00", "17:15:00", "17:30:00", "17:45:00", 
                 "18:00:00", "18:15:00", "18:30:00", "18:45:00", "19:00:00", "19:15:00", "19:30:00", "19:45:00", 
                 "20:00:00", "20:15:00", "20:30:00", "20:45:00", "21:00:00", "21:15:00", "21:30:00", "21:45:00", 
                 "22:00:00", "22:15:00", "22:30:00", "22:45:00", "23:00:00", "23:15:00", "23:30:00", "23:45:00"]

#Plot a heatmap using the dataframe and the figure created above
ax = sns.heatmap(df, cbar_kws={'label': 'Count', 'orientation': 'horizontal'},
                   mask=df.isnull(),cmap="YlGnBu", xticklabels=x_axis_labels, ax = ax)

plt.title('CAZ Traffic Count', fontsize = 20)
plt.xlabel('Time', fontsize = 15)
plt.ylabel('Date', fontsize = 15)

plt.show()
