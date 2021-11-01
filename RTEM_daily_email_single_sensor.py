import datetime
import pandas as pd
from datetime import date
import requests
from passwords import key,password
import smtplib
import time

today = date.today()
end= today+timedelta(days=1)
sites= ['R0101L1','R1522L1']
last_15 = date.today() - timedelta(minutes = 1000)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')

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
print(results)
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
	if date > last_15:
		if 0<speed<100:
			send_email(password)
