import pandas as pd
import numpy as np
import requests
import holoviews as hv
from holoviews import opts, dim
from bokeh.sampledata.les_mis import data
pd.options.mode.chained_assignment = None
hv.extension('bokeh')
from holoviews import dim, opts
hv.output(size=200)

#Set up parameters of the search
headers = {
    'Earliest':'2022-11-07 00:00:00',
    'Latest':'2022-11-07 00:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

#get request, then convert the data to a data frame
result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

#Option to limit the search to certain hours of the day
# mask = (df['Capture Date'] > '2022-07-20 13:00:00') & (df['Capture Date'] <= '2022-07-20 14:00:00')
# df = df.loc[mask]

#Remove cameras in the city centre
internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

#Identifying cameras that are facing the 'wrong' way (Facing towards the city centre so approaching would be departing,
#then reversing the direction.
reverse = ['CAZ005','CAZ060','CAZ061','CAZ006','CAZ008','CAZ022','CAZ064','CAZ035','CAZ037','CAZ038','CAZ039','CAZ053',
          'CAZ003','CAZ004','CAZ015','CAZ016','CAZ018','CAZ026','CAZ030','CAZ031','CAZ047']

df_filtered = df[(df["RSE Id"].isin(reverse))]
df_filtered.loc[df_filtered['Direction of Travel'] == 'Approaching','Direction of Travel'] = 'Outbound'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Departing','Direction of Travel'] = 'Approaching'
df_filtered.loc[df_filtered['Direction of Travel'] == 'Outbound','Direction of Travel'] = 'Departing'
df_2 = df[~df['RSE Id'].isin(reverse)]
df = pd.concat([df_filtered,df_2])
df = df[~df['RSE Id'].isin(internal)]

df.loc[df['Direction of Travel'] == 'Approaching', 'Direction of Travel'] = 'Inbound'
df.loc[df['Direction of Travel'] == 'Departing', 'Direction of Travel'] = 'Outbound'

#Create a unique list of cameras and vehicles 
cams = set(df['RSE Id'].tolist())
vrn = set(df['Hashed VRN'].tolist())

#Identify the trips that had an even number of captures (ie X ins and X outs)
#Create data frames for the first pair of in and outs, second pair of in and outs etc.
vrns = []
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
        
df_1 = pd.concat(one)
df_2 = pd.concat(two)
df_3 = pd.concat(single)
df_4 = pd.concat(three)
df_5 = pd.concat(four)
df_6 = pd.concat(five)

#Create a list of matched pair trips
dfs = [df_1,df_2,df_3,df_4,df_5,df_6]

time = []
p =[]
for df in dfs:
    for i in vrn:
        df1 = df.loc[df['Hashed VRN'] == i]
        df1['A'] = df1['Capture Date']
        df1.sort_values(by='A', inplace=True)
        if len(df1) == 2:
            leng = []
            for x in cams:
                if (df1['RSE Id'].iloc[0] == x):
                    leng.append(x)
                    for y in cams:
                        if (df1['RSE Id'].iloc[1] ==y):
                            leng.append(y)
                            if (df1['Direction of Travel'].iloc[0] == 'Inbound') & (df1['Direction of Travel'].iloc[1] == 'Outbound'):
                                if df1.empty == True:
                                    continue
                                else:
                                    if len(df1) > 1:
                                        leng.append((len(df1)/2))
            
            p.append(leng)
        else:
            continue

df=pd.DataFrame(p,columns=['source','target','value'])
df = df[df['value'].notna()]
df['value'].astype(int)
df.sort_values('source',inplace=True, ascending=True)
df.replace('CAZ031','CAZ030')
df.replace('CAZ028','CAZ029')
df.replace('CAZ004','CAZ003')
df.replace('CAZ002','CAZ001')
df.replace('CAZ060','CAZ061')
df.replace('CAZ055','CAZ054')
df = df.groupby(['target','source']).value.sum().reset_index()

print(df)

chord = hv.Chord(df)
chord.opts(
    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), 
               labels='name', node_color=dim('index').str()))
