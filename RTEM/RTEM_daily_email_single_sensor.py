import datetime
import pandas as pd
from datetime import date,timedelta
import requests
from passwords import key,password
import smtplib
import time

today = date.today()
end= today+timedelta(days=1)
#Can add more sites here
sites= ['R0101L1','R1522L1']
#set up variable to allow a search for the last 15 minutes
last_15 = datetime.datetime.now() - timedelta(minutes = 15)
last_15 = last_15.strftime('%Y-%m-%d %H:%M:%S')

#creates a list of URLs from the sites inputted
urls=[]
for site in sites:
    url=('http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(today)+\
    '&Latest='+str(end)+'&scn='+site+'&ApiKey='+key)
    urls.append(url)

#creates dataframes from the URLs above
results=[]
for url in urls:
    result=requests.get(url).json()
    df = pd.DataFrame(result['RTEM_CSVs']['kids'][n]['kids'] for n in\
    result['RTEM_CSVs']['kids'])
    df['AverageSpeed']=df['AverageSpeed'].astype(int)
    results.append(df)

#function to send email
def send_email(password):
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('louistyndall2@gmail.com',password)
        subject = 'Congestion Alert'
        body = (f'There is congestion at site {loc} with an average spe\
        ed of {speed}kmph, recorded at {date}')
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('louistyndall2@gmail.com','louistyndall2@gmail.co\
        m',msg)
        print('email is sent')
        smtp.quit()

#for loop to find "congested speeds" within the last 15 minutes
#Future work: add check to see how long the congestion has been present
for df in results:
	speed = df.iloc[-1]['AverageSpeed']
	loc = df.iloc[-1]['SCN']['value']
	date=df.iloc[-1]['Date']
	if date > last_15:
		if 0<speed<100:
			send_email(password)

#run every 15 minutes
while(True):
	send_email(password)
	time.sleep(900)
