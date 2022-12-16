import pandas as pd
import numpy as np
from datetime import timedelta
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

x = ['july18_2022.csv','july19_2022.csv','july20_2022.csv','july21_2022.csv','july22_2022.csv','july23_2022.csv','july24_2022.csv']
dfs = []

for i in x:
    df = pd.read_csv (f'{i}', dtype={'Site_Id': str,'Lane':int,'RSE Id': str, 'Direction of Travel': str,
                                         'Hashed VRN': int, 'Nationality': str, 'ANPR Confidence': int,
                                         'ANPR Id':str, 'Payment Cleared': str, 'Locally Exempt':str,
                                         'Exemption Type': str, 'System Direction': str, 'Display Direction': str})

    reverse = ['CAZ005','CAZ060','CAZ061','CAZ062','CAZ006','CAZ008','CAZ022','CAZ064','CAZ037','CAZ038','CAZ039','CAZ053',
              'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ057','CAZ047']

    internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']

    df_filtered = df[(df["RSE Id"].isin(reverse))]
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
    df_2 = df[~df['RSE Id'].isin(reverse)]
    df = pd.concat([df_filtered,df_2])
    df = df[~df['RSE Id'].isin(internal)]
    
    remove = ['CAZ046','CAZ047']
    df = df[df['RSE Id'].isin(remove)]
    
    con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
    know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006',
            'CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
    east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
    south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
    west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
    jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']
    #df = df[df['RSE Id'].isin(jewel)]

    df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
    df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

    #df = df.loc[df['Direction of Travel'] == 'Inbound']
    vrn = set(df['Hashed VRN'].tolist())
    df_vrn = []
    for i in vrn:
        df1 = df.loc[df['Hashed VRN'] == i]
        if len(df1) == 2:
            df1.sort_values(by='Capture Date', inplace=True)
            df_vrn.append(df1)
    df = pd.concat(df_vrn)

    df['Capture Date'] =pd.to_datetime(df['Capture Date'])
    df.set_index('Capture Date', inplace=True)

    df = df.resample('15 Min').sum()
    df = df[['Lane']]
    dfs.append(df)

df = pd.concat(dfs)
df.sort_values(by='Capture Date', ascending=True, inplace=True)

start = datetime.datetime.strptime('2022-8-01', '%Y-%m-%d')
days = 7
end = start+datetime.timedelta(days=days)
rng = pd.date_range(start, end, freq='5 min')
time = df['Lane'].tolist()
diff = np.array_split(time, days)
date = pd.date_range(start,end-timedelta(days=1),freq='d').strftime('%Y-%m-%d').tolist()
df = pd.DataFrame(data=diff, columns=rng[:96].strftime('%H-%M-%S'), index=[date])
df['Date'] = date
df['Date'] =pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.resample('1D').mean()
df.replace(0, np.nan, inplace=True)

print(df)
df.to_excel('46to47.xlsx')

fig, ax = plt.subplots(figsize=(20,15)) 
x_axis_labels = ["00:00:00", "00:15:00", "00:30:00", "00:45:00", "01:00:00", "01:15:00", "01:30:00", "01:45:00",
                 "02:00:00", "02:15:00", "02:30:00", "02:45:00", "03:00:00", "03:15:00", "03:30:00", "03:45:00", 
                 "04:00:00", "04:15:00", "04:30:00", "04:45:00", "05:00:00", "05:15:00", "05:30:00", "05:45:00", 
                 "06:00:00", "06:15:00", "06:30:00", "06:45:00", "07:00:00", "07:15:00", "07:30:00", "07:45:00", 
                 "08:00:00", "08:15:00", "08:30:00", "08:45:00", "09:00:00", "09:15:00", "09:30:00", "09:45:00", 
                 "10:00:00", "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", "11:30:00", "11:45:00", 
                 "12:00:00", "12:15:00", "12:30:00", "12:45:00", "13:00:00", "13:15:00", "13:30:00", "13:45:00", 
                 "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00", "15:15:00", "15:30:00", "15:45:00", 
                 "16:00:00", "16:15:00", "16:30:00", "16:45:00", "17:00:00", "17:15:00", "17:30:00", "17:45:00", 
                 "18:00:00", "18:15:00", "18:30:00", "18:45:00", "19:00:00", "19:15:00", "19:30:00", "19:45:00", 
                 "20:00:00", "20:15:00", "20:30:00", "20:45:00", "21:00:00", "21:15:00", "21:30:00", "21:45:00", 
                 "22:00:00", "22:15:00", "22:30:00", "22:45:00", "23:00:00", "23:15:00", "23:30:00", "23:45:00"]


ax = sns.heatmap(df, cbar_kws={'label': 'Count', 'orientation': 'horizontal'},
                   mask=df.isnull(),cmap="YlGnBu", xticklabels=x_axis_labels, ax = ax)

plt.title('CAZ Traffic Count', fontsize = 20)
plt.xlabel('Time', fontsize = 15)
plt.ylabel('Date', fontsize = 15)

plt.show()
