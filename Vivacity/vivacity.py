import requests
import json
import datetime

with open("password.json","r") as f:
	password=json.load(f)

url='https://api.vivacitylabs.com/'

class vivacity:
	def __init__(self):
		headers={"accept":"application/json","api-version":"2","Content-Type":"application/x-www-form-urlencoded"}
		n=requests.post(url+"get-token",headers=headers,data=password)
		print ("hello")
		self.token=n.json()
	
	def refresh_token(self):
		headers={"accept":"application/json","api-version":"2","Content-Type":"application/x-www-form-urlencoded"}
		data={"refresh_token":self.token["refresh_token"]}
		n=requests.post(url+"refresh-token",headers=headers,data=password)
		self.token=n.json()
		
	def counts(self):
		tfrom=(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=1)-datetime.timedelta(days=0)).isoformat()[:-3]+'Z'
		tto=(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=1)+datetime.timedelta(days=1)).isoformat()[:-3]+'Z'
		print (tfrom,tto)
		'https://api.vivacitylabs.com/counts?class=car,van,truck&countline=&timeFrom=2020-09-04T16%3A35%3A00.000Z&timeTo=2020-09-04T16%3A45%3A00.000Z'
		c='cyclist,motorbike,car,pedestrian,taxi,van,minibus,bus,rigid,truck,emergency_car,emergency_van,fire_engine'
		c='cyclist','escooter'
		data={"class":c,
			"countline":"",
			"api-version":'2',
			"timeFrom":tfrom,
			"timeTo":tto,
			"includeZeroCounts":"true"}
		headers={"accept":"application/json","api-version":"2","Authorization":"Bearer "+self.token['access_token']}
		n=requests.get(url+"counts",headers=headers,params=data)
		print (n.url)
		print (n.content)
		return n.json()
	
	def countline(self):
		headers={"accept":"application/json","api-version":"2","Authorization":"Bearer "+self.token['access_token']}
		n=requests.get(url+"countline",headers=headers)
		return n.json()
	
	def sensor(self):
		headers={"accept":"application/json","api-version":"2","Authorization":"Bearer "+self.token['access_token']}
		n=requests.get(url+"sensor",headers=headers)
		return n.json()


if __name__=='__main__':
	print ("hello")
	import folium
	m = folium.Map(location=[53,-1.5])
	a=vivacity()
	data=a.counts()
	#print (data)
	res=a.countline()
	print (len(res))
	with open('really.json','w') as f:
		json.dump(data,f)
	tot=0
	for n in res:
		print (n)
		r=[data[n['id']][m]['counts'][0]['countIn'] for m in data[n['id']]]
		s=[data[n['id']][m]['counts'][0]['countOut'] for m in data[n['id']]]
		t=[data[n['id']][m]['counts'][1]['countIn'] for m in data[n['id']]]
		u=[data[n['id']][m]['counts'][1]['countOut'] for m in data[n['id']]]
		#print (r)
		cyclists=sum(r)+sum(s)
		peds=sum(t)+sum(u)
		#print (n['location']['centre']['lat']) 
		if True: #"cycl" in n['name']:
			folium.Marker([n['location']['centre']['lat'],n['location']['centre']['long']], popup=n['name']+'\n'+n['id'], tooltip='cyclists '+str(cyclists)+'\npedestrians '+str(peds)).add_to(m)
			print (n['id'],n['name'])
			sb=[[int(g/12),sum([r[g+i] for i in range(12)])] for g in range(0,288,12)]
			print ('southbound',sum(r))
			for nn in sb:
				print (nn)
			nb=[[int(g/12),sum([s[g+i] for i in range(12)])] for g in range(0,288,12)]
			print ('northbound',sum(s))
			import matplotlib.pyplot as plt
			plt.title(n['name'])
			plt.plot([a[0] for a in sb],[a[1] for a in sb])
			plt.plot([a[0] for a in nb],[a[1] for a in nb])
			#plt.show()
		tot+=cyclists
	print (tot)
	m.save('testmap.html')
