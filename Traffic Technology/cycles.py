#!python2
import requests,json
import datetime
import base64
from requests_oauthlib import OAuth2Session
import sys
import time

id='9k1GQrfrK2BuwPWlLC6XyDrbvsUa'
secret='n11vklOFPeyTIJfjqKH8HkgJDZoa'
with open('password.json','w') as f:
	json.dump({'id':id,'secret':secret},f)

with open('password.json','r') as f:
	data=json.load(f)
id=data['id']
secret=data['secret']

import shelve

cachedb='ecosh'

class dates:
	def __init__(self,offset=0):
		n=datetime.date.today()
		n=datetime.datetime.fromordinal(n.toordinal())
		self.today=self.convert(n+datetime.timedelta(days=offset))
		self.yesterday=self.convert(n-datetime.timedelta(days=1+offset))
		self.weekago=self.convert(n-datetime.timedelta(days=7+offset))
		self.monthago=self.convert(n-datetime.timedelta(days=28+offset))
		self.ninetydays=self.convert(n-datetime.timedelta(days=90+offset))
		self.yearstart=self.convert(datetime.datetime(n.year,1,1))

	def convert(self,dt):
		return datetime.datetime.strftime(dt,"%Y-%m-%dT%H:%M:%S")

	def unconvert(self,dt):
		return datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")

class cycles:
	def __init__(self,id,secret):
		self.token=self.get_token(id,secret)

	def get_token(self,id,secret):
		n=base64.standard_b64encode(str(id+":"+secret).encode('ascii'))
		url='https://apieco.eco-counter-tools.com/token'

		h1={'Authorization':'Basic '+str(n,'utf-8'), 'Content-Type':'application/x-www-form-urlencoded'}
		data='grant_type=client_credentials' #&client_id='+id+'&client_secret='+secret
		print (h1)
		#sys.exit(0)
		access_token=requests.post(url, headers=h1,data=data)
		print (access_token.content)
		return access_token.json()['access_token']		

	def get_site_list(self):
		#tok=get_token(id,secret)
		#print 'token got'
		headers={'Accept':'application/json','Authorization':'Bearer '+str(self.token)}
		url='https://apieco.eco-counter-tools.com/api/1.0/site'  
		rep=requests.get(url,headers=headers)
		return rep.json()				

	def get_data(self,id,begin=dates().weekago,end=dates().today,step='day'):
		headers={'Accept':'application/json','Authorization':'Bearer '+str(self.token)}
		url='https://apieco.eco-counter-tools.com/api/1.0/data/site/'+str(id)+'?begin='+str(begin)+'&end='+str(end)+'&step='+str(step)
		print (url)
		rep=requests.get(url,headers=headers)
		#print (rep.content)
		return rep.json()		
		
	def get_processed_data(self,id,begin=dates().weekago,end=dates().today,step='day'):
		#print (id,begin,end,step)
		raw=self.get_data(id,begin,end,step)
		try:
			x=[int(n['counts']) for n in raw]
			y=[datetime.datetime.strptime(n['date'][:-5],"%Y-%m-%dT%H:%M:%S") for n in raw]
			z=sum(x)
		except:
			return {'date':[],'count':[],'total':0}
		return {'date':y,'count':x,'total':z}
		
	def cacheraw(self,loc,begin=dates().weekago,end=dates().today,step='day'):
		days=dates().unconvert(end).date()-dates().unconvert(begin).date()
		cday=dates().unconvert(begin).date()
		data=[[],[],[]]
		today=datetime.date.today()
		missing=[] #datetime.datetime(2020,5,1).date(),datetime.datetime(2020,5,5).date()]
		while cday<=dates().unconvert(end).date():
			index=str(cday)+str(loc)+str(step)
			db= shelve.open(cachedb)
			if index not in db or cday>=today-datetime.timedelta(days=1) or cday in missing:
				db[index]=self.get_processed_data(id=loc,step=step, begin=datetime.datetime(cday.year,cday.month,cday.day).isoformat(), end=(datetime.datetime(cday.year,cday.month,cday.day)+datetime.timedelta(days=1)).isoformat())
			#print (db[index])
			data[0]+=db[index]['date']
			data[1]+=db[index]['count']					
			data[2].append(db[index]['total'])	
			db.close()								
			cday+=datetime.timedelta(days=1)
		#print (dates().unconvert(begin),data[0],dates().unconvert(end))
		#data=[n for n in data if dates().unconvert(begin)<n[0]<dates().unconvert(end)]
		return {'date':data[0],'count':data[1],'total':sum(data[2])}


if __name__=="__main__":
	print (dates().yearstart)
	import sys
	#sys.exit(0)
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdates
	import json
	try:
		import geocoder
	except:
		pass

	plt.figure(figsize=(30,9))
	api=cycles(id,secret)
	sites=api.get_site_list()
	print (sites)
	print (api.get_data(100055036))
	import sys
	sys.exit(0)
	for n in sites:
		tmp=[]
		print ([n])
		for y in n['channels']:
			#print (y)
			#print (y['name'])
			l=api.cacheraw(n['id'],begin=dates().monthago,step='day')
			if l['total']:
				tmp.append([l['date'],l['count']])
				#plt.title(n['name']+', '+y['name'])
		x=[m[1] for m in tmp]
		#print (x)
		x=[sum(yy) for yy in zip(*x)]
		#print (x)
		nm=geocoder.osm([n['latitude'],n['longitude']], method='reverse').street
		time.sleep(.1)
		#plt.plot(tmp[0][0],x,label=nm)
		'''except:
			pass
		'''
		print (n['name'])
		print (n['id'])
		print ([n['longitude'],n['latitude']])
		#sys.exit(0)
		
	
	
	geocoder.osm([n['latitude'],n['longitude']], method='reverse').street

	formatter = mdates.DateFormatter("%d-%m-%Y") #("%H:%M")
	plt.gca().xaxis.set_major_formatter(formatter)
	locator = mdates.DayLocator()
	plt.gca().xaxis.set_major_locator(locator)
	plt.xticks(rotation=90)
	h,l=plt.gca().get_legend_handles_labels()
	plt.gca().legend(h,l)
	plt.grid(b=True, which='major', color='#FAFAFA', linestyle='-')
	plt.title('BCR Cycling Data')
	plt.savefig("cycles.png")
	



'''

for n in rep:
	x=n['serial']

headers={'Accept':'application/json','Authorization':'Bearer '+str(tok)}
url='https://apieco.eco-counter-tools.com/api/1.0/counter/'+x
print requests.get(url,headers=headers).content
'''
			


