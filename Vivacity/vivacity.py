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
		self.token=n.json()
	
	def refresh_token(self):
		headers={"accept":"application/json","api-version":"2","Content-Type":"application/x-www-form-urlencoded"}
		data={"refresh_token":self.token["refresh_token"]}
		n=requests.post(url+"refresh-token",headers=headers,data=password)
		self.token=n.json()
		
	def counts(self):
		'https://api.vivacitylabs.com/counts?class=car,van,truck&countline=&timeFrom=2020-03-08T16%3A35%3A00.000Z&timeTo=2020-03-08T16%3A45%3A00.000Z'
		data={"class":'cyclist,motorbike,car,pedestrian,taxi,van,minibus,bus,rigid,truck,emergency_car,emergency_van,fire_engine',
			"countline":"",
			"api-version":'2',
			"timeFrom":(datetime.datetime.now()-datetime.timedelta(days=1)).isoformat()[:-3]+'Z',
			"timeTo":(datetime.datetime.now()-datetime.timedelta(days=0)).isoformat()[:-3]+'Z',
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
	import folium
	m = folium.Map(location=[53,-1.5])
	a=vivacity()
	data=a.counts()
	res=a.countline()
	print (len(res))
	with open('really.json','w') as f:
		json.dump(data,f)
	for n in res:
		print (n)
		print (n['location']['centre']['lat']) 
		folium.Marker([n['location']['centre']['lat'],n['location']['centre']['long']], popup=n['id'], tooltip=n['name']).add_to(m)

	m.save('testmap.html')
