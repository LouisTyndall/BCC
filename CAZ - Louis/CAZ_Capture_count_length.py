import pandas as pd
import numpy as np
import requests

headers = {
    'Earliest':'2022-11-14 00:00:00',
    'Latest':'2022-11-14 23:59:59',
    'ApiKey':'7N0BRC3CT4KIB4BY5342743137151'
}
url='http://opendata.onl/caz.json?'

result = requests.get(url, headers = headers).json()
df = pd.DataFrame(result['CAZ']['kids']['Data'])
df = pd.json_normalize(df['kids'])

df = df.rename({'kids.Site.attrs.LL': 'co-ords', 'kids.Site.value': 'Site', 'kids.Vehicle': 'Hashed VRN',
                'kids.Camera': 'RSE Id', 'kids.Captured':'Capture Date', 'kids.Received': 'Received Date',
               'kids.Approach':'Direction of Travel','kids.Lane':'Lane'}, axis=1)

internal = ['CAZ063','CAZ064','CAZ065','CAZ066','CAZ067','CAZ068']
df = df[~df['RSE Id'].isin(internal)]

vrn = set(df['Hashed VRN'].tolist())
print(len(vrn))


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


for i in vrn:
    df1 = df.loc[df['Hashed VRN'] == i]
    if len(df1) == 1:
        one.append(df1)
    else:
        if len(df1) == 2:
            two.append(df1)
        else:
            if len(df1) ==3:
                three.append(df1)
            else:
                if len(df1) == 4:
                    four.append(df1)
                else:
                    if len(df1) == 5:
                        five.append(df1)
                    else:
                        if len(df1) == 6:
                            six.append(df1)
                        else: 
                            if len(df1) == 7:
                                seven.append(df1)
                            else:
                                if len(df1) == 8:
                                    eight.append(df1)
                                else:
                                    if len(df1) == 9:
                                        nine.append(df1)
                                    else:
                                        if len(df1) == 10:
                                            ten.append(df1)
                                        else:
                                            continue
df_1 = pd.concat(one)
print('One Capture:'len(df_1))

df_2 = pd.concat(two)
print('Two Captures:'len(df_2)/2)

df_3 = pd.concat(three)
print('Three Captures:'len(df_3)/3)

df_4 = pd.concat(four)
print('Four Captures:'len(df_4)/4)

df_5 = pd.concat(five)
print('Five Captures:'len(df_5)/5)

df_6 = pd.concat(six)
print('Six Captures:'len(df_6)/6)

df_7 = pd.concat(seven)
print('Seven Captures:'len(df_7)/7)

df_8 = pd.concat(eight)
print('Eight Captures:'len(df_8)/8)

df_9 = pd.concat(nine)
print('Nine Captures:'len(df_9)/9)

df_10 = pd.concat(ten)
print('Ten Captures:'len(df_10)/10)
