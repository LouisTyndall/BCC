import pandas as pd

df = pd.read_csv ('data1.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

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
