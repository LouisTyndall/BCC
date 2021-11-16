import requests
from passwords import *
import pandas as pd
import matplotlib.pyplot as plt

date = input('What date do want to search for?')
loc=int(input('Which location do you want to search for?'))
url = f'https://www.tfwm.onl/AWS_Analysis.json?ApiKey={key}&earliest=22/09/2021&latest=23/09/2021'
result = requests.get(url).json()
df = pd.DataFrame(result['AWS_Analysis']['kids'][n]['kids'] for n in result['AWS_Analysis']['kids'])
df['Segment_Speed_MPH']=df['Segment_Speed_MPH'].astype(float)
dfs = dict(tuple(df.groupby('Segment_ID')))
y = df['Segment_ID'].tolist()
y=list(set(y))


values=[]
for i in y:
    value = dfs[i]
    values.append(value)

df1 = {}
keys = range(len(y))
for i in keys:
        df1[i] = values[i]


df1[loc]['BIN'] = pd.to_datetime(df1[loc]['BIN'])
df1[loc]['BIN'] = df1[loc]['BIN'].dt.strftime('%H:%M:%S')
road = df1[loc]['Segment_ID'].iloc[1]

plt.bar(df1[loc]['BIN'],df1[loc]['Segment_Speed_MPH'],label='Average Speed')
plt.xlabel('Time')
plt.xticks(rotation = '25')
plt.ylabel('Average Speed (MPH)')
plt.title(f'Average Speed for {road} across {date}')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(20, 15)
ax = plt.gca()
ax.set_xticks(ax.get_xticks()[::6])
plt.show()
