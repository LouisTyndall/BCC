import pandas as pd
pd.options.mode.chained_assignment = None

df = pd.read_csv ('sept19_2022.csv', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                     'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                     'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                     'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

reverse = ['CAZ005','CAZ060','CAZ061','CAZ062','CAZ006','CAZ008','CAZ022','CAZ064','CAZ037','CAZ038','CAZ039','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ057','CAZ047']

internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

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
    else:
        if len(df1) == 2:
            df1['A'] = df1['Capture Date']
            df1.sort_values(by='A', inplace=True)
            if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                two.append(df1)
            else:
                continue
        else:
            if len(df1) ==3:
                    three.append(df1)
            else:
                if len(df1) == 4:
                    df1['A'] = df1['Capture Date']
                    df1.sort_values(by='A', inplace=True)
                    if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                        four.append(df1)
                    else:
                        continue
                else:
                    if len(df1) == 5:
                            five.append(df1)
                    else:
                        if len(df1) == 6:
                            df1['A'] = df1['Capture Date']
                            df1.sort_values(by='A', inplace=True)
                            if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                                six.append(df1)
                            else:
                                continue
                        else: 
                            if len(df1) == 7:
                                    seven.append(df1)
                            else:
                                if len(df1) == 8:
                                    df1['A'] = df1['Capture Date']
                                    df1.sort_values(by='A', inplace=True)
                                    if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                                        eight.append(df1)
                                    else:
                                        continue
                                else:
                                    if len(df1) == 9:
                                            nine.append(df1)
                                    else:
                                        if len(df1) == 10:
                                            df1['A'] = df1['Capture Date']
                                            df1.sort_values(by='A', inplace=True)
                                            if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                                                ten.append(df1)
                                            else:
                                                continue
                                        else:
                                            continue
df_1 = pd.concat(one)
print('Captures of length 1:',len(df_1))

df_2 = pd.concat(two)
print('Captures of length 2:',len(df_2))

df_3 = pd.concat(three)
print('Captures of length 3:',len(df_3)/3)

df_4 = pd.concat(four)
print('Captures of length 4:',(len(df_4)/4)*2)

df_5 = pd.concat(five)
print('Captures of length 5:',len(df_5)/5)

df_6 = pd.concat(six)
print('Captures of length 6:',(len(df_6)/6)*3)

df_7 = pd.concat(seven)
print('Captures of length 7:',len(df_7)/7)

df_8 = pd.concat(eight)
print('Captures of length 8:',(len(df_8)/8)*4)

df_9 = pd.concat(nine)
print('Captures of length 9:',len(df_9)/9)

df_10 = pd.concat(ten)
print('Captures of length 10:',(len(df_10)/10)*5)

print('Total captures:',len(vrn))
