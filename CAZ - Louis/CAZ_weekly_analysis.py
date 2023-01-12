from datetime import datetime, timedelta
import requests
import pandas as pd

#Ask user to input date, then set up variables for each day of the week. (MUST INPUT MONDAY DATE FOR A WEEK OF DATA)
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

#Create empty lists to add data too, inbound and outbound
ins = []
outs = []

#get request for each day of the week defined above
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
    
    #Removes cameras that are in the city centre
    internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
    df = df[~df['RSE Id'].isin(internal)]
    
    #List of cameras that are facing the 'wrong' way. The camera direction is then flipped to ensure Approaching means inbound
    #and Departing means outbound
    reverse = ['CAZ003','CAZ004','CAZ005','CAZ006','CAZ008','CAZ015','CAZ016','CAZ018','CAZ022','CAZ026','CAZ030','CAZ031',
          'CAZ035','CAZ037','CAZ038','CAZ039','CAZ041','CAZ047','CAZ053','CAZ060','CAZ061','CAZ064'

    df_filtered = df[(df["RSE Id"].isin(reverse))]
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
    df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
    df_2 = df[~df['RSE Id'].isin(reverse)]
    df = pd.concat([df_filtered,df_2])

    df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
    df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

    #variables to get the total number of vehicles entering and leaving the city
    x = len(df.loc[df['Direction of Travel'] == 'Inbound'])
    y = len(df.loc[df['Direction of Travel'] == 'Outbound'])

    ins.append(x)
    outs.append(y)

#Creates a table to display the data, with days of the week down the side and 
#inbound and outbound along the top.
df_todays = dict(zip(days, ins))
df_today = pd.DataFrame(df_todays.items())
df_today = df_today.set_axis(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
df_today['Outbound'] = outs
df_today.rename(columns={df_today.columns[1]: "Inbound" }, inplace = True)
df_today.rename(columns={df_today.columns[0]: "Date" }, inplace = True)

#Setting up the variables for the same week last year as the user inputted
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

#get request for each day of the week defined above
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
               
    #Removes cameras that are in the city centre          
    internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
    df = df[~df['RSE Id'].isin(internal)]

    #List of cameras that are facing the 'wrong' way. The camera direction is then flipped to ensure Approaching means inbound
    #and Departing means outbound          
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
    
    #variables to get the total number of vehicles entering and leaving the city
    x = len(df.loc[df['Direction of Travel'] == 'Inbound'])
    y = len(df.loc[df['Direction of Travel'] == 'Outbound'])

    ins.append(x)
    outs.append(y)

#Creates a table to display the data, with days of the week down the side and 
#inbound and outbound along the top.               
df_lastyears = dict(zip(days, lastyears))
df_lastyear = pd.DataFrame(df_lastyears.items())
df_lastyear = df_lastyear.set_axis(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
df_lastyear['OutboundL'] = outs
df_lastyear.rename(columns={df_lastyear.columns[1]: "InboundL" }, inplace = True)
df_lastyear.rename(columns={df_lastyear.columns[0]: "DateL" }, inplace = True)

#Concatenating the data from last week and last year.               
df_t = pd.concat([df_today, df_lastyear], axis=1)
df = df_t

#Creating a new column that shows the percentage difference between last year and last week
df['Inbound Percentage Difference'] = ((df['Inbound'] - df['InboundL'])/df['InboundL'])*100
df['Outbound Percentage Difference'] = ((df['Outbound'] - df['OutboundL'])/df['OutboundL'])*100
print(df_t)
dfweekday = df.head(5)
dfweekend = df.tail(2)

wd_in = str(round(dfweekday['Inbound Percentage Difference'].mean(),2))
wd_out = str(round(dfweekday['Outbound Percentage Difference'].mean(),2))
wk_in = str(round(dfweekend['Inbound Percentage Difference'].mean(), 2))
wk_out = str(round(dfweekend['Outbound Percentage Difference'].mean(),2))

#Printing the statement that tells the user the % difference between last week and last year
#for inbound and outbound, and weekend and weekday.
print(f'Average weekday change is {wd_in}% for inbound and {wd_out}% for outbound')
print(f'Average weekend change is {wk_in}% for inbound and {wk_out}% for outbound')
