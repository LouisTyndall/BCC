import pandas as pd

#Set up parameters of the search
headers = {
    'Earliest':'2022-11-07 00:00:00',
    'Latest':'2022-11-07 23:59:59',
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

#Create lists of each quarter and their corrosponding cameras
know = ['CAZ001','CAZ002','CAZ003','CAZ004','CAZ005','CAZ006','CAZ007','CAZ008','CAZ009','CAZ059','CAZ060','CAZ061','CAZ062']
east = ['CAZ010','CAZ011','CAZ012','CAZ013','CAZ014','CAZ015', 'CAZ016','CAZ017','CAZ018','CAZ065','CAZ066']
south = ['CAZ019','CAZ020','CAZ021','CAZ022','CAZ023','CAZ024','CAZ025','CAZ026','CAZ027','CAZ064','CAZ068']
con = ['CAZ041','CAZ042','CAZ043','CAZ044','CAZ045','CAZ063']
west = ['CAZ032','CAZ033','CAZ034','CAZ035','CAZ037']
jewel = ['CAZ048','CAZ049','CAZ050','CAZ051','CAZ052','CAZ053','CAZ054','CAZ055','CAZ056','CAZ057','CAZ058','CAZ067']

#Create a new column which corrosponds to which quarter the capture occured.
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

table = []
for df in dfs:
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
    table.append(df)
df = pd.concat(table)
aggregation_functions = {'Know':'sum','East':'sum','West':'sum','South':'sum','Con':'sum','Jewel':'sum','Bound':'sum'}
df = df.groupby(df.index).aggregate(aggregation_functions)
print(df)
