import pandas as pd

#Create parameters for the search
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

#rename column headings
df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

#Remove the cameras in the city centre
internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

"""
Identifying cameras that are facing the 'wrong' way (Facing towards the city centre so approaching would be departing,
then reversing the direction.
"""
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

"""
Create dictionary for each quarter and their corresponding cameras, then turn
it into a dataframe
"""
data = [{'Gun':{'inbound':["CAZ004","CAZ061","CAZ058","CAZ056",'CAZ057','CAZ055'],
    'outbound':['CAZ005','CAZ060','CAZ056','CAZ057','CAZ055']},'Eastside':{'inbound'
    :["CAZ006",'CAZ002','CAZ009','CAZ010','CAZ064','CAZ011','CAZ012','CAZ013',
    'CAZ014','CAZ065'],'outbound':['CAZ008','CAZ007','CAZ009','CAZ010','CAZ064'
    ,'CAZ011','CAZ012','CAZ013','CAZ014','CAZ065']},'Digbeth':{'inbound':['CAZ017'
    ,'CAZ019','CAZ021','CAZ023','CAZ024','CAZ063','CAZ025'],'outbound':['CAZ018'
    ,'CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ063','CAZ025']}, 'Southside':
    {'inbound':['CAZ029','CAZ032','CAZ033','CAZ035','CAZ037','CAZ036'],'outbound':
    ['CAZ031','CAZ032','CAZ033','CAZ034','CAZ037','CAZ036']}, 'Convention':{'inbound':
    ['CAZ040','CAZ041','CAZ042','CAZ062','CAZ043','CAZ044'],'outbound':['CAZ040',
    'CAZ041','CAZ042','CAZ062','CAZ043','CAZ044']},'Jewellery':{'inbound':['CAZ050'
    ,'CAZ049','CAZ051','CAZ047'],'outbound':['CAZ048','CAZ049','CAZ051','CAZ047']}}
    
]
df2 = pd.DataFrame(data)

"""
For each quarter, first identify which cameras belong in said quater. Then create a dataframe that only 
contains inbound captures then. Find which inbound captures are in the choosen quarter, then count
the length. Repeat for outbound. Repeat for all quarters.
"""
gun_in = []
gun_out = []
for i in df2['Gun'][0]['inbound']:
    df3 = df.loc[df['Direction of Travel'] == 'Approaching']
    df4 = df3.loc[df3['RSE Id'] == i]
    leng = len(df4)
    gun_in.append(leng)
for i in df2['Gun'][0]['outbound']:
    df3 = df.loc[df['Direction of Travel'] == 'Departing']
    df4 = df3.loc[df3['RSE Id'] == i]
    leng = len(df4)
    gun_out.append(leng)
print(f'The number of vehicles in the Gun Quarter was {sum(gun_in)}, and the number out was {sum(gun_out)}')

east_in = []
east_out = []
for i in df2['Eastside'][0]['inbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    east_in.append(leng)
for i in df2['Eastside'][0]['outbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    east_out.append(leng)
print(f'The number of vehicles in the Eastside was {sum(east_in)}, and the number out was {sum(east_out)}')

dig_in = []
dig_out = []
for i in df2['Digbeth'][0]['inbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    dig_in.append(leng)
for i in df2['Digbeth'][0]['outbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    dig_out.append(leng)
print(f'The number of vehicles in Digbeth was {sum(dig_in)}, and the number out was {sum(dig_out)}')

south_in = []
south_out = []
for i in df2['Southside'][0]['inbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    south_in.append(leng)
for i in df2['Southside'][0]['outbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    south_out.append(leng)
print(f'The number of vehicles in the Southside was {sum(south_in)}, and the number out was {sum(south_out)}')

con_in = []
con_out = []
for i in df2['Convention'][0]['inbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    con_in.append(leng)
for i in df2['Convention'][0]['outbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    con_out.append(leng)
print(f'The number of vehicles in the Convention Quarter was {sum(con_in)}, and the number out was {sum(con_out)}')

jewel_in = []
jewel_out = []
for i in df2['Jewellery'][0]['inbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    jewel_in.append(leng)
for i in df2['Jewellery'][0]['outbound']:
    df3 = df.loc[df['RSE Id'] == i]
    leng = len(df3)
    jewel_out.append(leng)
print(f'The number of vehicles in the Jewellery Quarter was {sum(jewel_in)}, and the number out was {sum(jewel_out)}')
