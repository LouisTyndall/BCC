import datetime
import pandas as pd
from datetime import date,timedelta
import requests
from passwords import key,password
import smtplib
import time


#set up parameters for the api search. Set up variables that check whether or not the database been updated in the last 15,30,45 and 60 minutes, respectively. 
today = date.today()
end= today+datetime.timedelta(days=1)
last_15 = datetime.datetime.now() - timedelta(minutes = 16)
last_30 = datetime.datetime.now() - timedelta(minutes = 31)
last_45 = datetime.datetime.now() - timedelta(minutes = 46)
last_60 = datetime.datetime.now() - timedelta(minutes = 61)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')
last_30 = last_30.strftime('%Y-%m-%d %H:%M:%S')
last_45 = last_45.strftime('%Y-%m-%d %H:%M:%S')
last_60 = last_60.strftime('%Y-%m-%d %H:%M:%S')

#List containing all of the RTEM sensors.
sites=[
    "R0613L1" ,"R0613L2" ,"R0613L3" ,"R0613L4" ,"R1991L1" ,"R1991L2" ,"R1991L3" ,"R1991L4" ,"R1991L5" ,"R1991L6" ,"R1992L1",
    "R1992L2" ,"R1992L3" ,"R1992L4" ,"R1992L5" ,"R1992L6" ,"R1994L1" ,"R1994L2" ,"R1994L3" ,"R1994L4" ,"R1994L5" ,"R1994L6",
    "R1994L7" ,"R2132L1" ,"R2132L2" ,"R2132L3" ,"R2132L4" ,"R4241L1" ,"R4241L2" ,"R4241L3" ,"R4241L4" ,"R4439L1" ,"R4439L2",
    "R4439L3" ,"R4439L4" ,"R4439L5" ,"R4439L6" ,"R4451L1" ,"R4451L2" ,"R4451L3" ,"R4451L4" ,"R4451L5" ,"R4451L6" ,"R1117L1",
    "R1117L2" ,"R1117L3" ,"R1117L4" ,"R1135L1" ,"R1135L2" ,"R1135L3" ,"R1135L4" ,"R1135L5" ,"R1522L1" ,"R1522L2" ,"R1522L3",
    "R1522L4" ,"R1522L5" ,"R1530L1" ,"R1530L2" ,"R1530L3" ,"R1530L4" ,"R2248L1" ,"R2248L2" ,"R2248L3" ,"R2248L4" ,"R2259L1",
    "R2259L2" ,"R2259L3" ,"R1167L1" ,"R1167L2" ,"R4438L1" ,"R4438L2" ,"R4438L3" ,"R4438L4" ,"R2339L1" ,"R2339L2" ,"R2339L3",
    "R2339L4" ,"R2340L1" ,"R2340L2" ,"R2340L3" ,"R2340L4" ,"R2235L1" ,"R2235L2" ,"R2235L3" ,"R2235L4" ,"R2233L1" ,"R2233L2",
    "R2233L3" ,"R2233L4" ,"R2233L5" ,"R0822L1" ,"R0822L2" ,"R0822L3" ,"R0822L4" ,"R0822L5" ,"R0821L1" ,"R0821L2" ,"R0821L3",
    "R3012L1" ,"R3012L2" ,"R3012L3" ,"R3156L1" ,"R3156L2" ,"R3178L1" ,"R3178L2" ,"R3256L1" ,"R3256L2" ,"R3256L3" ,"R4212L1",
    "R4212L2" ,"R4212L3" ,"R4212L4" ,"R4315L1" ,"R4315L2" ,"R0101L1" ,"R0101L2" ,"R0101L3" ,"R0101L4" ,"R0102L1" ,"R0102L2",
    "R0102L3" ,"R0199L1" ,"R0199L2" ,"E0511L1" ,"E0511L2" ,"E0511L3" ,"E0511L4" ,"R0815L1" ,"R0815L2" ,"R0815L3" ,"R0815L4",
    "R0815L5" ,"R0815L6" ,"R8023L1" ,"R8023L2" ,"R8023L3" ,"R8023L4" ,"R4012L1" ,"R4012L2" ,"R4012L3" ,"R4012L4" ,"R4012L5",
    "R4012L6" ,"R0105L1" ,"R0105L2" ,"R0105L3" ,"R0105L4" ,"R7545L1" ,"R7545L2" ,"R7545L3" ,"R7545L4" ,"R7545L5" ,"R7545L6",
    "R1609L1" ,"R1609L2" ,"R19389L1" ,"R19389L2" ,"R19389L3" ,"R19389L4" ,"R1999L1" ,"R1999L2" ,"R1163L1" ,"R1163L2" ,"R2232L1",
    "R2232L2" ,"R2232L3" ,"R2232L4" ,"R1103L1" ,"R1103L2" ,"R4138L1" ,"R1258L1" ,"R1258L2" ,"R2960L1" ,"R2960L2" ,"R2960L3",
    "R2960L4" ,"R2950L1" ,"R2950L2" ,"R2950L3" ,"R2950L4" ,"R2940L1" ,"R2940L2" ,"R2940L3" ,"R2940L4" ,"R2922L1" ,"R2922L2",
    "R2922L3" ,"R2922L4" ,"R2532L1" ,"R2532L2" ,"R2532L3" ,"R2532L4" ,"R0721L1" ,"R0721L2" ,"R0721L3" ,"R0721L4" ,"R0721L5",
    "R0721L6" ,"R0721l7" ,"R0721L8",
]

#Set up list containing urls populated from the list above.
urls=[]
for site in sites:
    url=('http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(today)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key)
    urls.append(url)

#This for loop contains a get request for the URLs above, which is turned into a dataframe. The dataframes are checked for
#number of columns. If there is only one column it means the database is empty and so is put into the list, results_empty.
#If there are multiple columns, this dataframe is reformated and added to list results.
results=[]
results_empty=[]
for url in urls:
    result=requests.get(url).json()
    df = pd.DataFrame(result['RTEM_CSVs'])
    x = (len(df.columns))
    if x > 1:
        df2 = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
        df2['AverageSpeed'] = df2['AverageSpeed'].astype(int)
        results.append(df2)
    results_empty.append(df)

#This creates a function that sends an email. Not currently in use yet.
def send_email(password):
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('louistyndall2@gmail.com',password)
        subject = 'Congestion Alert'
        body = f'There is congestion at {loc} with an average speed of {speed} kmph, recorded at {date}'
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('louistyndall2@gmail.com','louistyndall2@gmail.com',msg)
        print('email is sent')
        smtp.quit()

#If-else loop that creates three variables, speed, location and date. First the date is checked to ensure
#the results are from the last 15 minutes (30,45 and 60 later), if this is false then a message will be printed
#such as 'there are no current data points. If true, the speed is checked. If the speed is in the congestion zone,
#0<x<12, then it checks if the speed was also in that range 30 minutes ago. If false, a message is printed that there
#is no congestion. This continues until either there is no congestion x minutes ago, or a message is printed that
#there has been congestion for over an hour. The end goal is to use the email function to send this data in an 
#email. loc is used to identify which RTEM sensor is being used.
for df in results:
    speed = df.iloc[-1]['AverageSpeed']
    loc = df.iloc[-1]['SCN']['value']
    date=df.iloc[-1]['Date']
    if date > last_15:
        if 0< speed < 40:
        
            speed2 = df.iloc[-2]['AverageSpeed']
            loc2 = df.iloc[-2]['SCN']['value']
            date2 = df.iloc[-2]['Date']
            if date2 > last_30: 
                if 0< speed2 <40:
            
                    speed3 = df.iloc[-3]['AverageSpeed']
                    loc3 = df.iloc[-3]['SCN']['value']
                    date3 = df.iloc[-3]['Date']
                    if date3 > last_45:
                        if 0< speed3 <40:
                            
                            speed4 = df.iloc[-3]['AverageSpeed']
                            loc4 = df.iloc[-3]['SCN']['value']
                            date4= df.iloc[-3]['Date']
                            if date4 > last_60:
                                if 0< speed3 <40:
                                    print(f'There has been been congestion for over 60 minutes, with speeds of {speed4}KPH at {loc4}')
                                else:
                                    print(f'There has been congestion for 45 minutes, with speeds of {speed3}KPH at {loc3}')
                            else:
                                print(f'There has been congestion for 45 minutes, with speeds of {speed3}KPH at {loc3}')
                        else:
                            print(f'There has been congestion for 30 minutes, with speeds of {speed2}KPH at {loc2}')
                    else:
                        print(f'There has been congestion for 30 minutes, with speeds of {speed2}KPH at {loc2}')
                else:
                    print(f'There has been congestion for 15 minutes, with speeds of {speed}KPH at {loc}')
            else:
                print(f'There has been congestion for 15 minutes, with speeds of {speed}KPH at {loc}')
        else: 
            print(f'There is no congestion at {loc}')
    else:
        print(f'There are no recent data points for {loc}'
