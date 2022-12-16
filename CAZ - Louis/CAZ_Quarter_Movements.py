import pandas as pd

df = pd.read_csv ('july2_2022.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

reverse = ['CAZ005','CAZ060','CAZ061','CAZ006','CAZ008','CAZ022','CAZ064','CAZ035','CAZ037','CAZ038','CAZ039','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ047']


internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])
df = df[~df['RSE Id'].isin(internal)]

know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006','CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037','CAZ038']
jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']

bound = ['CAZ028','CAZ029','CAZ030','CAZ031','CAZ039','CAZ040','CAZ046','CAZ047']

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

vrn = set(df['Hashed VRN'].tolist())
df_vrn=[]
for i in vrn:
    df1 = df.loc[df['Hashed VRN'] == i]
    if len(df1) == 2:
        if df1['Direction of Travel'].iloc[0] == 'Inbound':
            df1.sort_values(by='Capture Date', inplace=True)
            df_vrn.append(df1)
df = pd.concat(df_vrn)

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

dics = []
for i in cams:
    df1 = df.loc[df['RSE Id'] == i]
    df1 = df1.loc[df1['Direction of Travel'] == 'Inbound']
    lis = df1['Hashed VRN'].tolist()
    df2 = df.loc[df['Direction of Travel'] == 'Outbound']
    df2 = df2.loc[df2['Hashed VRN'].isin(lis)]
    cam = df2['Location'].tolist()

    dic = {i:cam.count(i) for i in cam}
    dic = pd.DataFrame(dic, index=[str(i)])
    dics.append(dic)

df = pd.concat(dics)

know1 = []
for i in know:
    df1 = df.loc[df.index == i]
    know1.append(df1)
know1 = pd.concat(know1)
know1.loc['Know1'] = know1[['Know','East','West','South','Con','Jewel','Bound']].sum()

east1 = []
for i in east:
    df1 = df.loc[df.index == i]
    east1.append(df1)
east1 = pd.concat(east1)
east1.loc['East1'] = east1[['Know','East','West','South','Con','Jewel','Bound']].sum()

west1 = []
for i in west:
    df1 = df.loc[df.index == i]
    west1.append(df1)
west1 = pd.concat(west1)
west1.loc['West1'] = west1[['Know','East','West','South','Con','Jewel','Bound']].sum()

south1 = []
for i in south:
    df1 = df.loc[df.index == i]
    south1.append(df1)
south1 = pd.concat(south1)
south1.loc['South1'] = south1[['Know','East','West','South','Con','Jewel','Bound']].sum()

con1 = []
for i in con:
    df1 = df.loc[df.index == i]
    con1.append(df1)
con1 = pd.concat(con1)
con1.loc['Con1'] = con1[['Know','East','West','South','Con','Jewel','Bound']].sum()

jewel1 = []
for i in jewel:
    df1 = df.loc[df.index == i]
    jewel1.append(df1)
jewel1 = pd.concat(jewel1)
jewel1.loc['Jewel1'] = jewel1[['Know','East','West','South','Con','Jewel','Bound']].sum()

bound1 = []
for i in bound:
    df1 = df.loc[df.index == i]
    bound1.append(df1)
bound1 = pd.concat(bound1)
bound1.loc['Bound1'] = bound1[['Know','East','West','South','Con','Jewel','Bound']].sum()


df = pd.concat([know1,east1,west1,south1,con1,jewel1,bound1])
locs = ['Know1','East1','West1','South1','Con1','Jewel1','Bound1']

df = df.loc[df.index.isin(locs)]
print(df)
