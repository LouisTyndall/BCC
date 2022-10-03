import requests

import andyconfig
import os
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import json
import csv

net='AWS_Analysis','AWS_ClassCount','AWS_ClassFlow','AWS_Flows','AWS_RoutesAnalysis','AWS_RoutesAverage','AWS_VehicleFlow','AWS_Vehicles'


def getdata(c=False,earliest='04/07/2022',latest='05/07/2022'):
	name=net[1]
	url='https://www.tfwm.onl/'+name+'.json?ApiKey='+os.environ['ALKEY']+'&earliest='+earliest+'&latest='+latest
	print (url)
	'''
	import sys
	n=requests.get(url)
	print (n.content[:1000])
	sys.exit(0)
	'''
	if c:
		with open('testanprsave.json','r') as f:
			data=json.load(f)
	else:
		print ('here')
		n=requests.get(url,timeout=100)
		print (n.content[:1000])
		data=n.json()
		with open('testanprsave.json','w')as f:
			json.dump(data,f)
	print (str(data)[:10000])
	x=[[data[name]['kids'][a]['kids']['camera_name'],data[name]['kids'][a]['kids']['BIN'],data[name]['kids'][a]['kids']['class'],data[name]['kids'][a]['kids']['class_Count']] for a in data[name]['kids']]

	return x
	

def getjtdata(c=True):
	name=net[5]
	url='https://www.tfwm.onl/'+name+'.json?ApiKey='+os.environ['ALKEY']+'&earliest=2021-07-03&latest=2021-02-08'
	print (url)
	'''
	import sys
	n=requests.get(url)
	print (n.content[:1000])
	sys.exit(0)
	'''
	if c:
		with open('testjtsave.json','r') as f:
			data=json.load(f)
	else:
		n=requests.get(url)
		print (n.content[:1000])
		data=n.json()
		with open('testjtsave.json','w')as f:
			json.dump(data,f)
	#x=[[data[name]['kids'][a]['kids']['Segment_ID'],data[name]['kids'][a]['kids']['BIN'],data[name]['kids'][a]['kids']['Current_avg_Segment_Time']] for a in data[name]['kids']]
	x=[[data[name]['kids'][a]['kids']['segment_id'],data[name]['kids'][a]['kids']['BIN'],data[name]['kids'][a]['kids']['segment_avg_time']] for a in data[name]['kids']]

	return x
	
def vehicletypegraph(x,t='GRITTING MACHINE'):
	gdat=[[gr[1],gr[3]] for gr in x if gr[0][0]=='B' and gr[2]==t]
	print (len(gdat))
	gd=defaultdict(int)
	for n in gdat:
		t=datetime.datetime.strptime(n[0],'%Y-%m-%d %H:%M:%S')
		gd[datetime.datetime(t.year,t.month,t.day,t.hour,0,0)]+=int(n[1])

	low=min(gd)
	high=datetime.datetime.now()
	high=datetime.datetime(high.year,high.month,high.day,high.hour,0,0)
	dts=[]
	while low<=high:
		dts.append(low)
		low+=datetime.timedelta(hours=1)

	plt.bar(range(len(dts)),[gd[b] if b in gd else 0 for b in dts])
	plt.xticks(range(len(dts)),[datetime.datetime.strftime(b,'%A %H') for b in dts],rotation='vertical')		

	plt.show()


def simpletotal(x):
	x=[n for n in x if n[0][0]=="B"]
	print (x)
	print (min([rr[1] for rr in x]))
	print (max([rr[1] for rr in x]))
	dd=defaultdict(int)
	for rr in x:
		dd[rr[2]]+=int(rr[3])
	data=[]
	for nn in sorted(dd,key=dd.get,reverse=True):
		data.append([nn,dd[nn]])
	total=sum([y[1] for y in data])
	for n in data:
		print (n[0],int((n[1]/total)*10000)/100,"%")
	print ("total ",total)
	res={}
	for a in list({n[0] for n in x}):
		res[a]=sum([int(y[3]) for y in x if y[0]==a])
	return res

def createdict(x):

		
	res=defaultdict(list)
	for n in x:
		res[n[0]].append(n[1:])
	newdata={}
	for n in res:
		tmp=defaultdict(list)
		for m in res[n]:
			tmp[datetime.datetime.strptime(m[0],'%Y-%m-%d %H:%M:%S')].append({m[1]:int(m[2])})
		newdata[n]=tmp
	return newdata
		

def simplegraph(newdata):
	
	for n in newdata:

		x,y=[],[]
		for a in newdata[n]:
			x.append(a)
			tmp=0

			for c in newdata[n][a]:
				print (c)
				
				tmp+=sum([c[d] for d in c])
			y.append(tmp)
		plt.plot([a for a in x], [b for b in y],'o')
		plt.title(n)
		plt.show()
		plt.close()

def typejoin(x):
	car=['NHSV', 'NOT LICENSED',  'DISABLED PASSENGER VEHICLE',  'ELECTRIC',  'PETROL CAR', 'POLICE', 'HACKNEY', 'ALTERNATIVE FUEL CAR',  'MOWING MACHINE', 'DIESEL CAR', 'DISABLED', 'PERSONAL EXPORT PRIVATE', 'STEAM', 'EXEMPT (SEC 7(1) VE ACT)',  'EXEMPT (NIL LICENCE)', 'DIRECT EXPORT PRIVATE', 'EXEMPT (NO LICENCE)', 'SPECIAL VEHICLE',  'HISTORIC VEHICLE', 'SPECIAL TYPES VEHICLES', 'ROAD CONSTRUCTION', 'RECOVERY VEHICLE', 'SMALL ISLANDS', 'N/A', 'LIMITED USE']
	motorbike=['BICYCLE','TRICYCLE','ELECTRIC MOTORCYCLE']
	LGV=['AMBULANCE','LIGHT GOODS VEHICLE LGV','LIGHT GOODS FARMERS', 'PRIVATE LIGHT GOODS (PLG)','WORKS TRUCK','GOODS ELECTRIC','EURO 4 LGV',]
	HGV=['TRAILER HGV' 'PRIVATE HGV', 'GRITTING MACHINE','LIFEBOAT HAULAGE', 'ROAD ROLLER','SNOW PLOUGH', 'HGV CT',  'HGV', 'GENERAL HAULAGE','FIRE SERVICE', 'AGRICULTURAL MACHINE','DIGGING MACHINE',  'FIRE ENGINE']
	Bus=['BUS']
	ret=[]
	for n in x:
		if n[2] in car:
			ret.append([n[0],n[1],'Car',n[3]])
		if n[2] in motorbike:
			ret.append([n[0],n[1],'Mbike',n[3]])
		if n[2] in LGV:
			ret.append([n[0],n[1],'LGV',n[3]])
		if n[2] in HGV:
			ret.append([n[0],n[1],'HGV',n[3]])
		if n[2] in Bus:
			ret.append([n[0],n[1],'Bus',n[3]])
	return ret
	
	
def barcreate(x,c=['Car','Mbike','LGV','HGV','Bus']):
		r=[]
		f=True
		x=sorted(x)
		for cat in range(5): #  (self.file['daily'][1:])): #plots a graph for each category		r.append(gapfill(n.split(counters=count,groupby=str(interval),mode=cat,dates=(lt,nw)),int(interval)))
			print(cat)
			for n in x:
				print (n)
				print (x[n])
				break
			print('after')
			dat=[x[n][c[cat]] for n in x]
			print (dat)
			if f==True:
				l=[plt.bar(range(len(dat)),dat,1)]
				old=dat
				f=False
			else:
				l.append(plt.bar(range(len(dat)),dat,bottom=old,width=1))
				print (len(old), len(dat))
				old=[old[n]+dat[n] for n in range(len(dat))]
	
def justlocs():
	n=getdata(c=True)
	return {x[0] for x in n}
	

		
def geocode():
	from geopy import Nominatim
	import time
	locator = Nominatim(user_agent='myGeocoder')
	data={}
	for n in justlocs():
		
		raw=n[3:].split('(')
		if len(raw)==1:
			road=raw[0]
			town=""
			direction=""
		else:
			print (raw)
			town=raw[1][:-1]
			if raw[0][-2]=="B":
				road=raw[0][:-4]
				direction=raw[0][-3:-1]
			else:
				road=raw[0][:-1]
				direction=""
		print (town)
		print (road)
		print (direction)
		time.sleep(1)
		
		location = locator.geocode(road+', '+town+', UK')
		try:
			print (location.latitude,location.longitude)
			data[n]=[town,road,direction,(location.latitude,location.longitude)]
		except:
			data[n]=[town,road,direction,None]
	with open('anprgeo.json','w')as f:
		json.dump(data,f)
	
if __name__=='__main__':
	with open('location_lookup_table.json','r') as f:
		lut=json.load(f)
	
	from collections import defaultdict
	res=defaultdict(list)
	for dd in range(14):
		earliest=str((datetime.datetime.now()-datetime.timedelta(days=14-dd)).date())
		latest=str((datetime.datetime.now()-datetime.timedelta(days=13-dd)).date())
		d=getdata(c=False,earliest=earliest,latest=latest)
		#data=[[lut[n[0]]]+n[1:] for n in d if n[0] in lut]
		data=d
		r=simpletotal(data)
		for y in r:
			res[y].append(r[y])
	
	
	with open('last2weeks.csv','w') as f:
		sw=csv.writer(f)
		for n in res:
			sw.writerow([n]+res[n])
	
	
	
	
	
	
	import sys
	sys.exit(0)
	n=getdata(c=True)
	
	import time
	time.sleep(100)
	x=getjtdata(c=False)
	y=defaultdict(list)
	for n in [a for a in x if a[0][:2]=='PB']:
		y[n[0]].append([datetime.datetime.strptime(n[1],'%Y-%m-%d %H:%M:%S'),float(n[2])/60])  # if n[0][:2]=='PB'}
	for n in y:
		print (y)
		plt.figure(figsize=(20,10))
		plt.plot([a[0] for a in y[n]],[b[1] for b in y[n]],'o')
		plt.xticks(rotation=90)
		plt.title(n)
		
		
		ax = plt.gca()
		import matplotlib.dates as mdates

		formatter = mdates.DateFormatter("%a, %I%p")
		ax.xaxis.set_major_formatter(formatter)

		locator = mdates.HourLocator()

		ax.xaxis.set_major_locator(locator)
		#ax.set_xlim([datetime.datetime(2020,10,1),datetime.datetime(2020,10,8)])
		ax.set_ylim([0,max([b[1] for b in y[n]])+1])
		ax.set_xlim([datetime.datetime(2021,2,6),datetime.datetime(2021,2,8)])
		ax.set_ylabel('Time in minutes')
		ax.grid(True,linestyle='--')

		plt.show()
		plt.close()
	'''
	x=[gr for gr in x if gr[0][0]=='B']
	x=typejoin(x)
	x=createdict(x)
	print (len(x))
	with open('roughanprlocations.txt','w') as f:
		for n in x:
			f.write(n+'\n')
	#print (json.dumps(x),indent=2)
	#for n in x:
#		print (n,x[n][0])
		#barcreate(x[n])
		#break
	'''
