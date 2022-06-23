import requests
from passwords import key
import datetime
import csv



url='http://bcc.opendata.onl/rtem.json?ApiKey='+key 

n=requests.get(url)
print (n.content)
data=n.json()
simplify=[[data['RTEMS']['kids'][record]['kids']['SCN']['value'],data['RTEMS']['kids'][record]['kids']['Description'],data['RTEMS']['kids'][record]['kids']['Northing'],data['RTEMS']['kids'][record]['kids']['Easting'],datetime.datetime.strptime(data['RTEMS']['kids'][record]['kids']['Date'],'%Y-%m-%d %H:%M:%S')] for record in data['RTEMS']['kids']]

broken={}
for n in simplify:
	if datetime.timedelta(days=365)>datetime.datetime.now()-n[4]>datetime.timedelta(minutes=600):
		broken[n[0][:5]]=[n[1],n[2],n[3],str(n[4])]
		
for n in broken:
	print (n,broken[n][0],broken[n][1],broken[n][2],broken[n][3])
with open('broken.csv','w') as f:
	sw=csv.writer(f)
	sw.writerow(['Ref','Description','Northing','Easting','Date last working'])
	for n in broken:
		sw.writerow([n,broken[n][0],broken[n][1],broken[n][2],broken[n][3]])

'''
b'{\r\n"RTEMS": {"kids":{"RTEM": {"kids":{"SCN": {"attrs":{"Site":"1","Station":"1"}\r\n, "value":"R0001D1L0"}\r\n,"Description": "A45 Coventry Road / Holder Road","Northing": "284939.00","Easting": "412172.00","Date": "2022-05-14 11:43:27","Direction": "1","Lane": "0","Speed": "32","Headway": "89","Occupancy": "5","Vehicles": "21","Motorbikes": "0","Cars": "20","Trailers": "0","Rigids": "1","HGVs": "0","Buses": "0"}}\r\n,"RTEM#1": {"kids":{"SCN": {"attrs":{"Site":"1","Station":"1"}\r\n, "value":"R0001D1L1"}\r\n,"Description": "A45 Coventry Road / Holder Road","Northing": "284942.00","Easting": "412172.00","Date": "2022-05-14 11:43:27","Direction": "1","Lane": "1","Speed": "40","Headway": "94","Occupancy": "4","Vehicles": "20","Motorbikes": "0","Cars": "20","Trailers": "0","Rigids": "0","HGVs": "0","Buses": "0"}}\r\n,"RTEM#2": {"kids":{"SCN": {"attrs":{"Site":"1","Station":"1"}\r\n, "value":"R0001D1L2"}\r\n,"Description": "A45 Coventry Road / Holder Road","Northing": "284946.00","Easting": "412172.00","Date": "2022-05-14 11:43:27","Direction": "1","Lane": "2","Speed": "41","Headway": "192","Occupancy": "1","Vehicles": "10","Motorbikes": "0","Cars": "10","Trailers": "0","Rigids": "0","HGVs": "0","Buses": "0"}}\r\n,"RTEM#3": {"kids":{"SCN": {"attrs":{"Site":"1","Station":"1"}\r\n, "value":"R0001D1L3"}\r\n,"Description": "A45 Coventry Road / Holder Road","Northing": "284949.00","Easting": "412172.00","Date": "2022-05-14 11:43:27","Direction": "1","Lane": "3","Speed": "0","Headway": "0","Occupancy": "0","Vehicles": "0","Motorbikes": "0","Cars": "0","Trailers": "0","Rigids": "0","HGVs": "0","Buses": "0"}}\r\n,"RTEM#4": {"kids":{"SCN": {"attrs":{"Site"
'''
