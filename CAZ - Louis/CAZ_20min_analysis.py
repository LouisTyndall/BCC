import pandas as pd
from datetime import timedelta
pd.options.mode.chained_assignment = None
import numpy as np
import requests

#Set up parameters of the search
headers = {
    'Earliest':'2022-11-07 00:00:00',
    'Latest':'2022-11-07 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

#get request, then convert the data to a data frame
result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

#Option to limit the search to certain hours of the day
# mask = (df['Capture Date'] > '2022-07-20 13:00:00') & (df['Capture Date'] <= '2022-07-20 14:00:00')
# df = df.loc[mask]

#Remove cameras in the city centre
internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

#Identifying cameras that are facing the 'wrong' way (Facing towards the city centre so approaching would be departing,
#then reversing the direction.
reverse = ['CAZ005','CAZ060','CAZ061','CAZ006','CAZ008','CAZ022','CAZ064','CAZ035','CAZ037','CAZ038','CAZ039','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ047']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

#Select cameras of interest
lookup = ['CAZ035','CAZ003']
df = df[df['RSE Id'].isin(lookup)]

#Set up lists for locations and their corrosponding cameras
know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006','CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']
bound = ['CAZ028','CAZ029','CAZ030','CAZ031','CAZ038','CAZ039','CAZ040','CAZ046','CAZ047']

#Create new column with the location name for each capture
for cam in know:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Know'

for cam in east:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'East'

for cam in west:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'West'

for cam in south:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'South'

for cam in con:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Con'

for cam in jewel:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Jewel' 
    
for cam in bound:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Bound'

#Create a unique list of cameras and VRNs
cams = set(df['RSE Id'].tolist())
vrn = set(df['Hashed VRN'].tolist())

#Identify the trips that had an even number of captures (ie X in and X out)
#Create data frames for the first pair of in and outs, second pair of in and outs etc.
single = []
one = []
two = []
three = []
four = []
five = []
for i in vrn:
    df1 = df.loc[df['Hashed VRN'] == i]
    if len(df1) == 2:
        df1.sort_values(by='Capture Date', inplace=True)
        single.append(df1)
    elif len(df1) == 4:
        df1.sort_values(by='Capture Date', inplace=True)
        df_one = df1.head(2)
        one.append(df_one)
        df_two = df1.tail(2)
        two.append(df_two)
    elif len(df1) == 6:
        df1.sort_values(by='Capture Date', inplace=True)
        df__1 = df1.iloc[0:2]
        df__2 = df1.iloc[2:4]
        df__3 = df1.iloc[4:6]
        one.append(df__1)
        two.append(df__2)
        three.append(df__3)
    elif len(df1) == 8:
        df1.sort_values(by='Capture Date', inplace=True)
        df__1 = df1.iloc[0:2]
        df__2 = df1.iloc[2:4]
        df__3 = df1.iloc[4:6]
        df__4 = df1.iloc[6:8]
        one.append(df__1)
        two.append(df__2)
        three.append(df__3)
        four.append(df__4)
    elif len(df1) == 10:
        df1.sort_values(by='Capture Date', inplace=True)
        df__1 = df1.iloc[0:2]
        df__2 = df1.iloc[2:4]
        df__3 = df1.iloc[4:6]
        df__4 = df1.iloc[6:8]
        df__5 = df1.iloc[8:10]
        one.append(df__1)
        two.append(df__2)
        three.append(df__3)
        four.append(df__4)
        five.append(df__5)
    else:
        continue
dfs = []  
if len(single) >1:
    df_1 = pd.concat(single)
    dfs.append(df_1)
if len(one) >1:
    df_2 = pd.concat(one)
    dfs.append(df_2)
if len(two) >1:
    df_3 = pd.concat(two)
    dfs.append(df_3)
if len(three) >1:
    df_4 = pd.concat(three)
    dfs.append(df_4)
if len(four) >1:
    df_5 = pd.concat(four)
    dfs.append(df_5)
if len(five) >1:
    df_6 = pd.concat(five)
    dfs.append(df_6)
if len(dfs) == 0:
    print('end')   

#Identify each individual trip that satisfies the requirements of line 168,
#this can be specific cameras or quarters. Then find the difference in time between
#the first and second capture. Create a list of these time differences.
time = []
for df in dfs:
    for i in vrn:
        df1 = df.loc[df['Hashed VRN'] == i]
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        if len(df1) == 2:
            #if (df1['Location'].iloc[0] == 'Know') & (df1['Location'].iloc[1] == 'Bound'):
            if (df1['RSE Id'].iloc[0] == 'CAZ035') & (df1['RSE Id'].iloc[1] == 'CAZ003'):
                if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                    if df1.empty == True:
                        continue
                    else:
                        df1['Capture Date'] =pd.to_datetime(df1['Capture Date'])
                        diff = (df1['Capture Date'].iloc[1]) - (df1['Capture Date'].iloc[0])
                        time.append(diff)
                else:
                    continue
            else:
                continue
        else:
            continue

#From the list of time differences create a data frame and format the data into seconds.
df2 = pd.DataFrame({'col':time})
if len(df2) >= 1:
    df2['col'] = df2['col'] / np.timedelta64(1, 's')

#Print the total number of trips. Create a new data frame for time period of interest.
#For example, a data frame of all trips under 20 minutes. Then find the percentage of trips
#under 20 minutes. 
first = len(df2)
print('Number of trips:',first)
#df3 = df2.loc[df2['col'] > 21600]
#df4 = df3.loc[df3['col'] < 28800]
df4 = df2.loc[df2['col'] < 1200]
print('Number under 20 mins:',len(df4))
second = len(df4)
print('Percent under 20 mins:',second/first*100)