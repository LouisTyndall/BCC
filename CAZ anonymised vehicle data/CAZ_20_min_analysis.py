import pandas as pd
from datetime import timedelta
pd.options.mode.chained_assignment = None
import numpy as np

df = pd.read_csv ('sept19_2022.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

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

internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]
remove = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ028','CAZ029','CAZ030','CAZ031']
#df = df[~df['RSE Id'].isin(remove)]

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

cams = set(df['RSE Id'].tolist())
vrn = set(df['Hashed VRN'].tolist())

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
    if len(df1) == 4:
        df1.sort_values(by='Capture Date', inplace=True)
        df_one = df1.head(2)
        one.append(df_one)
        df_two = df1.tail(2)
        two.append(df_two)
    if len(df1) == 6:
        df1.sort_values(by='Capture Date', inplace=True)
        df__1 = df1.iloc[0:2]
        df__2 = df1.iloc[2:4]
        df__3 = df1.iloc[4:6]
        one.append(df__1)
        two.append(df__2)
        three.append(df__3)
    if len(df1) == 8:
        df1.sort_values(by='Capture Date', inplace=True)
        df__1 = df1.iloc[0:2]
        df__2 = df1.iloc[2:4]
        df__3 = df1.iloc[4:6]
        df__4 = df1.iloc[6:8]
        one.append(df__1)
        two.append(df__2)
        three.append(df__3)
        four.append(df__4)
    if len(df1) == 10:
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
time = []
times = []
for df in dfs:
    for i in vrn:
        df1 = df.loc[df['Hashed VRN'] == i]
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        if len(df1) == 2:
            #if (df1['Location'].iloc[0] == 'Know') & (df1['Location'].iloc[1] == 'Bound'):
            #if (df1['RSE Id'].iloc[0] == 'CAZ054') & (df1['RSE Id'].iloc[1] == 'CAZ053'):
            if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                times.append(df1)
                df1['Capture Date'] =pd.to_datetime(df1['Capture Date'])
                diff = (df1['Capture Date'].iloc[1]) - (df1['Capture Date'].iloc[0])
                time.append(diff)

df2 = pd.DataFrame({'col':time})
if len(df2) >= 1:
    df2['col'] = df2['col'] / np.timedelta64(1, 's')

df3 = pd.concat(times)
first = len(df2)
print('Number of journeys:',first)
#df3 = df2.loc[df2['col'] > 21600]
#df4 = df3.loc[df3['col'] < 28800]
df4 = df2.loc[df2['col'] < 1200]
second = len(df4)
print('Percent of journeys under 20 mins:',second/first*100)
