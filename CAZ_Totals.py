import pandas as pd
import requests

headers = {
    'Earliest':'2022-09-12 00:00:00',
    'Latest':'2022-09-12 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

print('Total captures:',len(df))

internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

reverse = ['CAZ003','CAZ004','CAZ005','CAZ006','CAZ008','CAZ015','CAZ016','CAZ018','CAZ022','CAZ026','CAZ030','CAZ031',
          'CAZ035','CAZ037','CAZ038','CAZ039','CAZ041','CAZ047','CAZ053','CAZ060','CAZ061','CAZ064']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])


know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006','CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']

bound = ['CAZ028','CAZ029','CAZ030','CAZ031','CAZ038','CAZ039','CAZ040','CAZ046','CAZ047']

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

print(df.iloc[-1]['Capture Date'])

print('Total Inbound',len(df.loc[df['Direction of Travel'] == 'Inbound']))
print('Total Outbound',len(df.loc[df['Direction of Travel'] == 'Outbound']))

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

cams = set(df['RSE Id'].tolist())

vrn = set(df['Hashed VRN'].tolist())

print('Total unique captures:',len(vrn))

#print('average capture confidence',df['ANPR Confidence'].mean())

d = df.loc[df['Direction of Travel'] == 'Inbound']
print('In bound',len(d.loc[d['Location'] == 'Bound']))

p = df.loc[df['Direction of Travel'] == 'Outbound']
print('Out bound',len(p.loc[p['Location'] == 'Bound']))

places = ['Bound','Jewel','East','West','South','Con','Know']

# for i in cams:
#     d = df.loc[df['Direction of Travel'] == 'Inbound']
#     print(f'In {i}',len(d.loc[d['RSE Id'] == i]))

#     p = df.loc[df['Direction of Travel'] == 'Outbound']
#     print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))

for i in places:
    b = df.loc[df['Location'] == i]
    #print(f'average capture confidence for {i}',b['ANPR Confidence'].mean())
    d = df.loc[df['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(d.loc[d['Location'] == i]))

    p = df.loc[df['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['Location'] == i]))
