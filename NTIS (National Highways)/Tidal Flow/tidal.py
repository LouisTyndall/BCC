#!python3
import requests
import andyconfig
from passwords import key,password
import os
import folium
import datetime
import csv
import json
import lzma
import time
from collections import defaultdict


#camera feed to check https://public.highwaystrafficcameras.co.uk/cctvpublicaccess/html/03814.html

class NTIS():
	def __init__(self):
		url='https://bccutc.com/NTIS%20VMS.json'
		par={'ApiKey':key}
		n=requests.get(url,params=par)
		n.encoding="ISO-8859-1"
		#print (n.text[:1000])
		d=json.loads(n.text,strict=False)
		j=d['NTIS_VMS']['kids']
		self.data=[j[a]['kids'] for a in j]
		self.unit={n['Identity']:n['UnitID'] for n in self.data}
	
	def historic(self,early=datetime.datetime.now().date()-datetime.timedelta(days=5),day=1):
		late=(early+datetime.timedelta(days=day)).date()
		early,late=str(early.date()),str(late)
		url='https://bccutc.com/NTIS%20VMS.json'
		par={'ApiKey':key,'Earliest':early,'Latest':late}
		
		z=lzmastuff()
		f=z.get(early+late)
		if f==False:
			n=requests.get(url,params=par)
			n.encoding="ISO-8859-1"
			f=n.content
			time.sleep(.5)
			print (early)
			#if datetime.datetime.now()-dates().encodenote(begin)>datetime.timedelta(days=2):
			z.add(early+late,f)
		#print (f[:10000])
		d=json.loads(f,strict=False)
		j=d['NTIS_VMS']['kids']
		
		return [j[a]['kids'] for a in j]



class lzmastuff:
	def __init__(self,zipname='lzma'):
		self.zipname=zipname
		if not os.path.exists(zipname):
			os.mkdir(zipname)

	def get(self,name):
		if name+'.xz' in os.listdir(self.zipname):
			with lzma.open(self.zipname+'/'+name+'.xz','r') as data:
				print ('using')
				return data.read()
		else:
			return False
		
	def add(self,name,data):
		with lzma.open(self.zipname+'/'+name+'.xz', "w") as f:
			f.write(data)
	
		
class NTISsites():
	def __init__(self,linearid):
		url='http://bcc.opendata.onl/NTIS_Sites.json'
		par={'ApiKey':os.environ['ALKEY'],'LinearID':str(linearid)}
		n=requests.get(url,params=par)
		#print (n.url)
		#d=n.json()
		#print (n.content[:1000])
		
	def sitelinear(self,linearid):
		NTIS_sites.xml
		n=requests.get(url,params=par)
		d=n.json()
		j=d['NTIS_TrafficSpeed']['kids']
		self.data=[j[a]['kids'] for a in j]

def hetime(n):
	return datetime.datetime.strptime(n,"%Y-%m-%d %H:%M:%S")


def tidaltimes(day=datetime.datetime.now()-datetime.timedelta(days=35)):
	x=NTIS()
	day=datetime.datetime(day.year,day.month,day.day,0,0,0)
	print (day)
	d=x.historic(early=day)
	ret=defaultdict(list)
	for n in d:
		try:
			ret[x.unit[n['Identity']]].append([n['Dates'],n['Pictogram']])
		except:
			pass
			#print ('oops')

	test=ret['A38M/3827A4']
	ib=[]
	ob=[]
	for n in test:
		if n[1]=='laneClosed':
			ib.append(['closed',n[0]])
		if n[1]=='laneOpen':
			ib.append(['open',n[0]])
	test=ret['A38M/3827B4']
	for n in test:
		if n[1]=='laneOpen':
			ob.append(['open',n[0]])
		if n[1]=='laneClosed':
			ob.append(['closed',n[0]])
	return ib,ob

def tidal_status():
	x=NTIS()
	vms={v: k for k, v in x.unit.items()}
	info=x.data
	site='A38M/3827A4'
	#northbound
	for n in info:
		#print (n)
		if n['Identity']==vms[site]:
			nb=[n['Dates'],n['Pictogram'],vms[site]]
			print (n)
	#southbound
	site='A38M/3827B4'
	for n in info:
		if n['Identity']==vms[site]:
			sb=[n['Dates'],n['Pictogram'],vms[site]]
			#print (n)
	print (nb,sb)
	status='not operating'
	if nb[1]=='laneOpen':
		status='northbound'
	if nb[1]=='advisorySpeed':
		status='northbound (with advisory speed)'
	if sb[1]=='laneOpen':
		status='Southbound'
	if sb[1]=='advisorySpeed':
		status='southbound (with advisory speed)'
	return status





if __name__=="__main__":
	for n in range(5):
		print (tidaltimes(day=datetime.datetime.now()-datetime.timedelta(days=n)))
	print (tidal_status())
