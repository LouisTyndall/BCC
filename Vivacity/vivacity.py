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

if __name__=='__main__':
	a=vivacity()
	data=a.counts()
	for n in data:
		print (n)

