from datetime import datetime, timedelta
import pandas as pd
import requests
from passwords import key,password
import time
import smtplib

last_15 = datetime.now() - timedelta(minutes = 15)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')

url='http://bcc.opendata.onl/UTMC%20RTEM.json?ApiKey='+key
result=requests.get(url).json()
df = pd.DataFrame(result['RTEMS']['kids'][n]['kids'] for n in result['RTEMS']['kids'])
df = df.drop('SCN',axis=1).join(pd.DataFrame(df.SCN.values.tolist()))
df['Speed']=df['Speed'].astype(int)
df.Date = pd.to_datetime(df.Date)
df.set_index('Date',inplace=True)
df=df[(df.index > last_15)]
df=df[(df['Speed'] < 15)]
df=df[(df['Speed']>0)]
df['Sensor']=df['value']
df = df[['Sensor','Speed','Direction','Vehicles']]

def send_email(password):
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('louistyndall2@gmail.com',password)
        subject = 'Congestion'
        body = ('Congestion',df)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('louistyndall2@gmail.com','louistyndall2@gmail.com',msg)
        print('email is sent')
        smtp.quit()

send_email(password)
#run every 15 min
while(True):
	send_email(password)
	time.sleep(900)
