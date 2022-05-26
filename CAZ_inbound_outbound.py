import pandas as pd

df = pd.read_csv ('data1.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

reverse = ['CAZ005','CAZ059','CAZ060','CAZ062','CAZ006','CAZ008','CAZ022','CAZ063','CAZ036','CAZ037','CAZ040','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ038','CAZ046','CAZ030''CAZ031','CAZ039']
internal = ['CAZ066','CAZ062','CAZ067','CAZ065']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])

gun = ['CAZ004','CAZ005','CAZ055','CAZ056','CAZ057','CAZ058','CAZ060','CAZ061']
east = ['CAZ001','CAZ002','CAZ006','CAZ007','CAZ008','CAZ009','CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ064','CAZ065']
dig = ['CAZ017','CAZ018','CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ063']
south = ['CAZ029','CAZ031','CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
con = ['CAZ040','CAZ041','CAZ042','CAZ043','CAZ044','CAZ062']
jewel = ['CAZ047','CAZ048','CAZ049','CAZ050','CAZ051']

bound = ['CAZ001','CAZ003','CAZ015', 'CAZ016','CAZ026','CAZ027','CAZ028','CAZ030','CAZ038','CAZ039','CAZ045','CAZ046'
    ,'CAZ052','CAZ053','CAZ054','CAZ059','CAZ066','CAZ067','CAZ068',]

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

for cam in internal:
    df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Internal'
    df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Internal'

for cam in gun:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Gun'

for cam in east:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'East'

for cam in dig:
    df.loc[df['RSE Id'] == cam, 'Location'] = 'Dig'

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
    lis = df1['Hashed VRN'].tolist()
    df2 = df.loc[df['Hashed VRN'].isin(lis)]
    cam = df2['Location'].tolist()

    dic = {i:cam.count(i) for i in cam}
    dic = pd.DataFrame(dic, index=[str(i)])
    dics.append(dic)

df = pd.concat(dics)

gun1 = []
for i in gun:
    df1 = df.loc[df.index == i]
    gun1.append(df1)
gun1 = pd.concat(gun1)
gun1.loc['Gun1'] = gun1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

east1 = []
for i in east:
    df1 = df.loc[df.index == i]
    east1.append(df1)
east1 = pd.concat(east1)
east1.loc['East1'] = east1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

dig1 = []
for i in dig:
    df1 = df.loc[df.index == i]
    dig1.append(df1)
dig1 = pd.concat(dig1)
dig1.loc['Dig1'] = dig1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

south1 = []
for i in south:
    df1 = df.loc[df.index == i]
    south1.append(df1)
south1 = pd.concat(south1)
south1.loc['South1'] = south1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

con1 = []
for i in con:
    df1 = df.loc[df.index == i]
    con1.append(df1)
con1 = pd.concat(con1)
con1.loc['Con1'] = con1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

jewel1 = []
for i in jewel:
    df1 = df.loc[df.index == i]
    jewel1.append(df1)
jewel1 = pd.concat(jewel1)
jewel1.loc['Jewel1'] = jewel1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()

bound1 = []
for i in bound:
    df1 = df.loc[df.index == i]
    bound1.append(df1)
bound1 = pd.concat(bound1)
bound1.loc['Bound1'] = bound1[['Gun','East','Dig','South','Con','Jewel','Bound']].sum()


df = pd.concat([gun1,east1,dig1,south1,con1,jewel1,bound1])
locs = ['Gun1','East1','Dig1','South1','Con1','Jewel1','Bound1']

df = df.loc[df.index.isin(locs)]
print(df)
