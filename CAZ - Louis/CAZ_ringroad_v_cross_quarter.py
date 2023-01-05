import requests
import pandas as pd

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

#Remove camera captures from the city centre
internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

#Identify the cameras that facing the 'wrong' way and switch the direction
reverse = ['CAZ005','CAZ060','CAZ061','CAZ062','CAZ006','CAZ008','CAZ022','CAZ064','CAZ037','CAZ038','CAZ039','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ057','CAZ047']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

#List of the quarters and their corrosponding cameras, then create a new column in the df with the quarter name
know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006','CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']
bound = ['CAZ028','CAZ029','CAZ030','CAZ031','CAZ038','CAZ039','CAZ040','CAZ046','CAZ047']

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

    
#Identify the unique trips that satisfy the requirements, ie 4 trips entering and
#leaving 2 different quarters, or 2 trips entering one quarter and leaving another.
vrn = set(df['Hashed VRN'].tolist())
df_1=[]
df_2=[]
for i in vrn:
    df1 = df.loc[df['Hashed VRN'] == i]
    if len(df1) == 4:
        df1.sort_values(by='Capture Date', inplace=True)
        if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
            if (df1['Direction of Travel'].iloc[2] == 'Inbound') & (df1['Direction of Travel'].iloc[3] == 'Outbound'):
                if (df1['Location'].iloc[0] == df1['Location'].iloc[1]) & (df1['Location'].iloc[2] == df1['Location'].iloc[3]):
                    if (df1['Location'].iloc[0] != df1['Location'].iloc[2]):
                        df_1.append(df1)
    if len(df1) == 2:
        df1.sort_values(by='Capture Date', inplace=True)
        if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
            if (df1['Location'].iloc[0] != df1['Location'].iloc[1]):
                df_2.append(df1)                
        
#Count the number of each trip type        
df = pd.concat(df_1)
df1 = pd.concat(df_2)
print('The number of cross quarter movements are:')
print(len(df1)/2)
print('The number of dual quarter movements are:')
print(len(df)/4)
