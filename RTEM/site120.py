import requests
from passwords import key
import datetime
import csv
import time
from collections import defaultdict

def lastminute():
	url='http://bcc.bccutc.com/rtem.json?ApiKey='+key 
	n=requests.get(url)
	data=n.json()
	simplify=[[data['RTEMS']['kids'][record]['kids']['SCN']['value'],data['RTEMS']['kids'][record]['kids']['Description'],data['RTEMS']['kids'][record]['kids']['Northing'],data['RTEMS']['kids'][record]['kids']['Easting'],datetime.datetime.strptime(data['RTEMS']['kids'][record]['kids']['Date'],'%Y-%m-%d %H:%M:%S'),data['RTEMS']['kids'][record]['kids']['Vehicles'],data['RTEMS']['kids'][record]['kids']['Speed']] for record in data['RTEMS']['kids']]

	inbound=[]
	outbound=[]
	for n in simplify:
		if n[0][:5]=='R0120':
			if int(n[0].split('L')[-1])<=5:
				inbound.append(n)
			else:
				outbound.append(n)

	return sum([int(n[-2]) for n in inbound]),sum([int(n[-2]) for n in outbound])

def today(site='120'):
	start=datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)-datetime.timedelta(days=0)
	end=start+datetime.timedelta(days=1)
	url='http://bcc.bccutc.com/rtem.json?TS=true&Earliest='+str(start)+'&Latest='+str(end)+'&ApiKey='+key 
	n=requests.get(url)
	print (n.content[:1000])
	data=n.json()
	#print (data['RTEMS']['kids'])
	simplify=[[data['RTEMs']['kids'][record]['kids']['SCN']['value'],datetime.datetime.strptime(data['RTEMs']['kids'][record]['kids']['Date'],'%Y-%m-%d %H:%M:%S'),float(data['RTEMs']['kids'][record]['kids']['Vehicles']),float(data['RTEMs']['kids'][record]['kids']['Speed'])] for record in data['RTEMs']['kids'] if data['RTEMs']['kids'][record]['kids']['SCN']['attrs']['Site']==site]
	bynum=[[n[0],int(((n[1]-simplify[0][1]).total_seconds())/60),n[2],n[3]] for n in simplify]
	bynumdict=defaultdict(list)
	for n in bynum:
		bynumdict[n[0]].append(n[1:])
	inbound=defaultdict(int)
	outbound=defaultdict(int)
	for n in bynumdict:
		for y in bynumdict[n]:
			if int(n.split('L')[-1])>=6:
				inbound[y[0]]+=y[1]
			else:
				outbound[y[0]]+=y[1]
	sinbound=defaultdict(int)
	soutbound=defaultdict(int)
	for n in bynumdict:
		for y in bynumdict[n]:
			if int(n.split('L')[-1])>=6:
				sinbound[y[0]]+=y[2]
			else:
				soutbound[y[0]]+=y[2]
				
	sinbound={n:0 if inbound[n]==0 else sinbound[n]/inbound[n] for n in sinbound}
	soutbound={n:0 if outbound[n]==0 else soutbound[n]/outbound[n] for n in outbound}
	print (inbound)
	
	
	import matplotlib.pyplot as plt
	
	
	aa=plt.bar([a for a in inbound], [inbound[n] for n in inbound],width=1)
	bb=plt.bar([a for a in outbound], [-outbound[n] for n in outbound],width=1)

	plt.title('A38M at Dartmouth Circus\nInflow vs Outflow\n'+datetime.datetime.strftime(start,"%Y-%m-%d"))



	plt.gca().set_xticks([a for a in range(0,len(inbound),60)])
	plt.gca().set_xticklabels([int(a/60) for a in range(0,len(inbound),60)])
	plt.grid(True)
	plt.ylim(-70,70)
	#plt.gca().legend([aa,bb,cc],['Inbound','Outbound','Congested'])
	plt.xlabel('Time of Day')
	plt.ylabel('veh/min')
	plt.show()



'''
b'{\r\n"RTEMs": {"attrs":{"Database":"false","EndDate":"2022-08-10 00:27:00","NullDataPoints":"true","RepeatedPoints":"true","StartDate":"2022-08-09 00:27:00"}\r\n,"kids":{"Data": {"kids":{"SCN": {"attrs":{"Site":"120","Station":"120"}\r\n, "value":"R0120D1L10"}\r\n,"Date": "2022-08-09 00:27:57","Direction": "1","Lane": "10","Speed": "0.0","Headway": "0","Occupancy": "0","Vehicles": "0","Motorbikes": "0","Cars": "0","Trailers": "0","Rigids": "0","HGVs": "0","Buses": "0"}}\r\n,"Data#1": {"kids":{"SCN": {"attrs":{"Site":"120","Station":"120"}\r\n, "value":"R0120D1L9"}\r\n,"Date": "2022-08-09 00:27:57","Direction": "1","Lane": "9","Speed": "0.0","Headway": "0","Occupancy": "0","Vehicles": "0","Motorbikes": "0","Cars": "0","Trailers": "0","Rigids": "0","HGVs": "0","Buses": "0"}}\r\n,"Data#2": {"kids":{"SCN": {"attrs":{"Site":"120","Station":"120"}\r\n, "value":"R0120D1L8"}\r\n,"Date": "2022-08-09 00:27:57","Direction": "1","Lane": "8","Speed": "0.0","Headway": "0","Occupancy": "0","Vehicles": "0","Motorbikes": '

'''


today()

