from datetime import datetime, timedelta
import pandas as pd
import requests
from password import key,password
import time
import smtplib

#set up variable to search the last 15 minutes
last_15 = datetime.now() - timedelta(minutes = 15)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')

#obtain data from API and convert to dataframe
url='http://bcc.opendata.onl/UTMC%20RTEM.json?ApiKey='+key
result=requests.get(url).json()
df = pd.DataFrame(result['RTEMS']['kids'][n]['kids'] for n in result['RTEMS']['kids'])

#creating column from 'SCN' dict to access site
df = df.drop('SCN',axis=1).join(pd.DataFrame(df.SCN.values.tolist()))
df['Speed']=df['Speed'].astype(int)
df.Date = pd.to_datetime(df.Date)
df.set_index('Date',inplace=True)

#filter for the last 15 mins and to access desired speeds
df=df[(df.index > last_15)]
df=df[(df['Speed'] < 9)]
df=df[(df['Speed']>0)]
df['Sensor']=df['value']
df = df[['Sensor','Speed','Direction','Vehicles']]

#function to send email
def send_email(password):
    with smtplib.SMTP_SSL('smtp.gmail.com',456) as smtp:
        smtp.login('EMAIL HERE',password)
        subject = 'Congestion'
        body = ('Congestion',df)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('EMAIL HERE','EMAIL HERE',msg)
        print('email is sent')
        smtp.quit()

send_email(password)
#run every 15 min
while(True):
	send_email(password)
	time.sleep(900)
