import requests
from passwords import key
import datetime
import csv

site='R1521L4'
with open('vicaragedelays'+site+'.csv','w') as f:
	sw=csv.writer(f)
	sw.writerow(['date','AM Peak','PM Peak','7am-7pm','24 hr','flow'])
for c in range(365,0,-1):	

	start=(datetime.datetime.now()-datetime.timedelta(days=c+1)).date()
	end=(datetime.datetime.now()-datetime.timedelta(days=c)).date()

	url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(start)+'&Latest='+str(end)+'&scn='+site+'&ApiKey='+key 

	n=requests.get(url)

	data=n.json()
	try:
		simplify=[[data['RTEM_CSVs']['kids'][record]['kids']['Date'],int(data['RTEM_CSVs']['kids'][record]['kids']['Total']),int(data['RTEM_CSVs']['kids'][record]['kids']['AverageSpeed'])] for record in data['RTEM_CSVs']['kids']]
	except:
		continue

	am=sum([5 if 0<n[2]<10 else 0 for n in simplify[90:113]])
	pm=sum([5 if 0<n[2]<10 else 0 for n in simplify[192:215]])
	ss=sum([5 if 0<n[2]<10 else 0 for n in simplify[84:227]])
	allday=sum([5 if 0<n[2]<10 else 0 for n in simplify])
	flow=sum([n[1] for n in simplify])
	with open('vicaragedelays'+site+'.csv','a') as f:
		sw=csv.writer(f)
		sw.writerow([start,am,pm,ss,allday,flow])
	print (start,am,pm,ss,allday,flow)


'''
am = 90,113 (7:30-9:30)
pm = 192,215 (16:00-18:00
7-7= 84,227

b'{\r\n"RTEM_CSVs": {"attrs":{"Database":"false","EndDate":"2022-05-24 00:00:00","NullDataPoints":"true","RepeatedPoints":"true","StartDate":"2022-05-23 00:00:00"}\r\n,"kids":{"Data": {"kids":{"SCN": {"attrs":{"Site":"14"}\r\n, "value":"R1521L2"}\r\n,"Date": "2022-05-23 00:00:00","Lane": "2","Total": "4","MotorBike": "1","Car": "3","Trailer": "0","LGV": "0","HGV": "0","Bus": "0","AverageSpeed": "29","Speed_85": "40","AverageHeadway": "658","Headway_85": "1264"}}\r\n
'''
