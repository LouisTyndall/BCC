import requests
import json


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
		headers={"accept":"application/json","api-version":"2","Authorization":"Bearer "+self.token['access_token']}
		n=requests.get(url+"counts",headers=headers)
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
	for n in res:
		print (n)
		for y in n:
			print (y)

			print (res[n][y]['location']['centre']['lat']) #,n[y]['location']['centre']['long'])
			folium.Marker([y['location']['centre']['lat'],y['location']['centre']['lon']], popup=y['id'], tooltip=y['name']).add_to(m)

	m.save('testmap.html')
