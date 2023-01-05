import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import requests

headers = {
    'Earliest':'2022-09-10 00:00:00',
    'Latest':'2022-09-10 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

reverse = ['CAZ003','CAZ004','CAZ005','CAZ006','CAZ008','CAZ015','CAZ016','CAZ018','CAZ022','CAZ026','CAZ030','CAZ031',
          'CAZ035','CAZ037','CAZ038','CAZ039','CAZ041','CAZ047','CAZ053','CAZ060','CAZ061','CAZ064']

internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

cams = set(df['RSE Id'].tolist())

one= []
two = []
three = []
four =[]
five = []
six = []
seven = []
eight = []
nine = []
ten = []
vrn = set(df['Hashed VRN'].tolist())

for i in vrn:
    df1 = df.loc[df['Hashed VRN'] == i]
    if len(df1) == 1:
            one.append(df1)
    elif len(df1) == 2:
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        two.append(df1)
    elif len(df1) ==3:
        three.append(df1)
    elif len(df1) == 4:
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        four.append(df1)
    elif len(df1) == 5:
        five.append(df1)
    elif len(df1) == 6:
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        six.append(df1)
    elif len(df1) == 7:
        seven.append(df1)
    elif len(df1) == 8:
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        eight.append(df1)
    elif len(df1) == 9:
        nine.append(df1)
    elif len(df1) == 10:
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        ten.append(df1)
    else:
        continue
df_1 = pd.concat(one)
d = df_1.loc[df_1['Direction of Travel'] == 'Inbound']
print('One capture, Inbound',len(d))
d = df_1.loc[df_1['Direction of Travel'] == 'Outbound']
for i in cams:
    p = df_1.loc[df_1['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_1.loc[df_1['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
print('One capture, Outbound',len(d))
print('Captures of length 1:',len(df_1))

df_2 = pd.concat(two)
for i in cams:
    p = df_2.loc[df_2['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_2.loc[df_2['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_2.loc[df_2['Direction of Travel'] == 'Inbound']
print('Two capture, Inbound',len(d))
d = df_2.loc[df_2['Direction of Travel'] == 'Outbound']
print('Two capture, Outbound',len(d))
print('Captures of length 2:',len(df_2)/2)

df_3 = pd.concat(three)
for i in cams:
    p = df_3.loc[df_3['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_3.loc[df_3['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_3.loc[df_3['Direction of Travel'] == 'Inbound']
print('Three capture, Inbound',len(d))
d = df_3.loc[df_3['Direction of Travel'] == 'Outbound']
print('Three capture, Outbound',len(d))
print('Captures of length 3:',len(df_3)/3)

df_4 = pd.concat(four)
for i in cams:
    p = df_4.loc[df_4['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_4.loc[df_4['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_4.loc[df_4['Direction of Travel'] == 'Inbound']
print('Four capture, Inbound',len(d))
d = df_4.loc[df_4['Direction of Travel'] == 'Outbound']
print('Four capture, Outbound',len(d))
print('Captures of length 4:',len(df_4)/4)

df_5 = pd.concat(five)
for i in cams:
    p = df_5.loc[df_5['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_5.loc[df_5['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_5.loc[df_5['Direction of Travel'] == 'Inbound']
print('Five capture, Inbound',len(d))
d = df_5.loc[df_5['Direction of Travel'] == 'Outbound']
print('Five capture, Outbound',len(d))
print('Captures of length 5:',len(df_5)/5)

df_6 = pd.concat(six)
for i in cams:
    p = df_6.loc[df_6['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_6.loc[df_6['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_6.loc[df_6['Direction of Travel'] == 'Inbound']
print('Six capture, Inbound',len(d))
d = df_6.loc[df_6['Direction of Travel'] == 'Outbound']
print('Six capture, Outbound',len(d))
print('Captures of length 6:',len(df_6)/6)

df_7 = pd.concat(seven)
for i in cams:
    p = df_7.loc[df_7['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_7.loc[df_7['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_7.loc[df_7['Direction of Travel'] == 'Inbound']
print('Seven capture, Inbound',len(d))
d = df_7.loc[df_7['Direction of Travel'] == 'Outbound']
print('Seven capture, Outbound',len(d))
print('Captures of length 7:',len(df_7)/7)

df_8 = pd.concat(eight)
for i in cams:
    p = df_8.loc[df_8['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_8.loc[df_8['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_8.loc[df_8['Direction of Travel'] == 'Inbound']
print('Eight capture, Inbound',len(d))
d = df_8.loc[df_8['Direction of Travel'] == 'Outbound']
print('Eight capture, Outbound',len(d))
print('Captures of length 8:',len(df_8)/8)

df_9 = pd.concat(nine)
for i in cams:
    p = df_9.loc[df_9['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_9.loc[df_9['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_9.loc[df_9['Direction of Travel'] == 'Inbound']
print('Nine capture, Inbound',len(d))
d = df_9.loc[df_9['Direction of Travel'] == 'Outbound']
print('Nine capture, Outbound',len(d))
print('Captures of length 9:',len(df_9)/9)

df_10 = pd.concat(ten)
for i in cams:
    p = df_10.loc[df_10['Direction of Travel'] == 'Inbound']
    print(f'In {i}',len(p.loc[p['RSE Id'] == i]))

    p = df_10.loc[df_10['Direction of Travel'] == 'Outbound']
    print(f'Out {i}',len(p.loc[p['RSE Id'] == i]))
d = df_10.loc[df_10['Direction of Travel'] == 'Inbound']
print('Ten capture, Inbound',len(d))
d = df_10.loc[df_10['Direction of Travel'] == 'Outbound']
print('Ten capture, Outbound',len(d))
print('Captures of length 10:',len(df_10)/10)

print('Total captures:',len(vrn))
