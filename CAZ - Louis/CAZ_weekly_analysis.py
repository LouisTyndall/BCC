from datetime import datetime, timedelta
import requests
import pandas as pd

day = input('ENTER START DATE:')
dt = datetime.strptime(day, '%Y-%m-%d')
mon = dt.date()
tues = (dt + timedelta(days=1)).date()
weds = (dt + timedelta(days=2)).date()
thurs = (dt + timedelta(days=3)).date()
fri = (dt + timedelta(days=4)).date()
sat = (dt + timedelta(days=5)).date()
sun = (dt + timedelta(days=6)).date()

days = [mon, tues, weds, thurs, fri, sat, sun]

ins = []
outs = []
total = []

for day in days:
    headers = {
        'Earliest':f'{day} 00:00:00',
        'Latest':f'{day} 23:59:59',
        'ApiKey':'HDMWDFKB8IB64BFQ3351251166261'
        #'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
    }
    url='http://opendata.onl/caz.json?'

    result = requests.get(url, headers = headers).json()
    df = pd.DataFrame(result['CAZ']['kids']['Data'])
    df = pd.json_normalize(df['kids'])

    df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                    'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
                   'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

    #reverse = ['CAZ003','CAZ004','CAZ005','CAZ006','CAZ008','CAZ015','CAZ016','CAZ018','CAZ022','CAZ026','CAZ030','CAZ031',
    #          'CAZ035','CAZ037','CAZ038','CAZ039','CAZ041','CAZ047','CAZ053','CAZ060','CAZ061','CAZ064']
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

    x = len(df.loc[df['Direction of Travel'] == 'Inbound'])
    y = len(df.loc[df['Direction of Travel'] == 'Outbound'])

    ins.append(x)
    outs.append(y)

df_ins = dict(zip(days, ins))
df_in = pd.DataFrame(df_ins.items())
df_in = df_in.set_axis(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
df_in['Outbound'] = outs
df_in.rename(columns={df_in.columns[1]: "Inbound" }, inplace = True)
df_in.rename(columns={df_in.columns[0]: "Date" }, inplace = True)

df_today = df_in

mon = (mon - timedelta(days = 364))
tues = (tues - timedelta(days = 364))
weds = (weds - timedelta(days = 364))
thurs = (thurs - timedelta(days = 364))
fri = (fri - timedelta(days = 364))
sat = (sat - timedelta(days = 364))
sun = (sun - timedelta(days = 364))

days = [mon, tues, weds, thurs, fri, sat, sun]

ins = []
outs = []

for day in days:
    headers = {
        'Earliest':f'{day} 00:00:00',
        'Latest':f'{day} 23:59:59',
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

    x = len(df.loc[df['Direction of Travel'] == 'Inbound'])
    y = len(df.loc[df['Direction of Travel'] == 'Outbound'])

    ins.append(x)
    outs.append(y)

df_ins = dict(zip(days, ins))
df_in = pd.DataFrame(df_ins.items())
df_in = df_in.set_axis(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
df_in['OutboundL'] = outs
df_in.rename(columns={df_in.columns[1]: "InboundL" }, inplace = True)
df_in.rename(columns={df_in.columns[0]: "DateL" }, inplace = True)

df_lastyear = df_in

df_t = pd.concat([df_today, df_lastyear], axis=1)
df = df_t

df['Inbound Percentage Difference'] = ((df['Inbound'] - df['InboundL'])/df['InboundL'])*100
df['Outbound Percentage Difference'] = ((df['Outbound'] - df['OutboundL'])/df['OutboundL'])*100
print(df_t)
dfweekday = df.head(5)
dfweekend = df.tail(2)

wd_in = str(round(dfweekday['Inbound Percentage Difference'].mean(),2))
wd_out = str(round(dfweekday['Outbound Percentage Difference'].mean(),2))
wk_in = str(round(dfweekend['Inbound Percentage Difference'].mean(), 2))
wk_out = str(round(dfweekend['Outbound Percentage Difference'].mean(),2))

print(f'Average weekday change is {wd_in}% for inbound and {wd_out}% for outbound')
print(f'Average weekend change is {wk_in}% for inbound and {wk_out}% for outbound')
