import pandas as pd
import requests

#set up search parameters
headers = {
    'Earliest':'2022-11-15 00:00:00',
    'Latest':'2022-11-15 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

#Get request and convert data to a data frame
result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

#Print the total number of captures, and the number of captures classified as Parking
print('Total captures:',len(df))
print('Total Parking',len(df.loc[df['Direction of Travel'] == 'Parking']))

#Remove captures in the city centre
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

#Print the total number of inbound and outbound captures
print('Total Inbound',len(df.loc[df['Direction of Travel'] == 'Inbound']))
print('Total Outbound',len(df.loc[df['Direction of Travel'] == 'Outbound']))

#Create a list of unique vehicles and then print the number of unique vehicles
vrn = set(df['Hashed VRN'].tolist())
print('Total unique captures:',len(vrn))
