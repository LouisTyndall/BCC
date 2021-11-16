import datetime
import pandas as pd
from datetime import date
import requests
from passwords import key,password
import smtplib
import time

today = date.today()
end= today+datetime.timedelta(days=1)
sites= ['R0101L1','R0101L2','R0101L3','R0101L4']

urls=[]
for site in sites:
    url=('http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(today)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key)
    urls.append(url)

results=[]
for url in urls:
    result=requests.get(url).json()
    df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in result['RTEM_CSVs']['kids'])
    df['AverageSpeed']=df['AverageSpeed'].astype(int)
    results.append(df)

def send_email(password):
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('louistyndall2@gmail.com',password)
        subject = 'Congestion Alert'
        body = ('There is congestion at',loc,'with an average speed of',speed,'kmph, recorded at',date)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('louistyndall2@gmail.com','louistyndall2@gmail.com',msg)
        print('email is sent')
        smtp.quit()

for df in results:
    speed = df.iloc[-1]['AverageSpeed']
    loc = df.iloc[-1]['SCN']['value']
    date=df.iloc[-1]['Date']
    if 0< speed < 12:
        
        speed2 = df.iloc[-2]['AverageSpeed']
        loc2 = df.iloc[-2]['SCN']['value']
        date2 = df.iloc[-2]['Date']
        if 0< speed2 <15:
            
            speed3 = df.iloc[-3]['AverageSpeed']
            loc3 = df.iloc[-3]['SCN']['value']
            date3 = df.iloc[-3]['Date']
            if 0< speed3 <15:
                print(f'There has been congestion for over 30 minutes, with speeds of {speed3}KPH at {loc3}')
            
            else:
                print(f'There has been congestion for 30 minutes, with speeds of {speed2}KPH at {loc2}')
        
        else: 
            print(f'There has been congestion for 15 minutes, with speeds of {speed}KPH at {loc}')
    
    else: 
        print(f'There is no congestion at {loc}')
        #send_email(password)
