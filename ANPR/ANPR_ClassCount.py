import requests
from passwords import *
import pandas as pd

#Potential to add input() to allow search date
url = f'https://www.tfwm.onl/AWS_ClassCount.json?ApiKey={key}&earliest=01/11/2021&latest=02/11/2021'
result = requests.get(url).json()

#Format data to dataframe
df = pd.DataFrame(result['AWS_ClassCount']['kids'][n]['kids'] for n in result['AWS_ClassCount']['kids'])
df['class_Count'] = df['class_Count'].astype(int)

#Select location. Can add input() to allow user to select location
df_new = df.loc[df['camera_name'] == 'SW A4032 Churchbridge SB (Oldbury)']

#Creates a list of each type of vehicle
t = df['class'].tolist()
vehicle_type=list(set(t))

#For loop to count, and print, the number of each vehicle type
for i in vehicle_type:
    df_new = df_new.loc[df_new['class'] == i]
    num_vehicles = df_new['class_Count'].sum()
    if num > 0:
        print(f'There are {num_vehicles} for {i}')
