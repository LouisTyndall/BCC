import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

#Create parameters for the search
headers = {
    'Earliest':'2022-11-14 00:00:00',
    'Latest':'2022-11-14 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

#Get request and transformation to a data frame
result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

#Remove the cameras in the city centre
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

#Select cameras of interest, or all cameras
#cams = set(df['RSE Id'].tolist())
cams = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005']

#Create a dataframe that shows the number of captures for a specific camera, 
#resampled to per hour. Can be changed to per 5 min, 15 min, etc.
dfs = []
for x in cams:
    df1 = df[df['RSE Id'] == x]
    df1.set_index('Capture Date', inplace=True)
    df1.index = pd.to_datetime(df1.index)
    df1['Lane'] = df1['Lane'].astype(int)
    df1 = df1[['Lane']]
    df1 = df1.resample('1H').sum()
    df1.rename(columns={'Lane': x}, inplace=True)
    dfs.append(df1)

#Print the data frame showing number of captures per hour.
dfc = pd.concat(dfs, axis=1)
print(dfc)
dfc.to_excel('caz_per_hour.xlsx')

#Plot a graph to show captures per hour, can select which camera you want to look at
ax = plt.plot(dfc.index,dfc['CAZ002'], label='CAZ002 count');
plt.legend(loc="upper left")
plt.title("Inbound-Outbound Count (DATE)")
plt.xlabel("Time")
plt.ylabel("Number of vehicles")
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.show
