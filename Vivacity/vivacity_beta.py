import requests
import json
import time


with open("password.json","r") as f:
	password=json.load(f)

url='https://beta.api.vivacitylabs.com/'

class vivacity:
	def __init__(self):
		url='https://api.vivacitylabs.com/'
		headers={"accept":"application/json","api-version":"2","Content-Type":"application/x-www-form-urlencoded"}
		n=requests.post(url+"get-token",headers=headers,data=password)
		self.token=n.json()
	
	def refresh_token(self):
		url='https://api.vivacitylabs.com/'
		headers={"accept":"application/json","api-version":"2","Content-Type":"application/x-www-form-urlencoded"}
		data={"refresh_token":self.token["refresh_token"]}
		n=requests.post(url+"refresh-token",headers=headers,data=password)
		self.token=n.json()
		
	def metadata(self):
		headers={"accept":"application/json","api-version":"3","Authorization":"Bearer "+self.token['access_token']}
		n=requests.get(url+"countline/metadata",headers=headers)
		return n.json()
	
	def countline(self,cl):
		headers={"accept":"application/json","api-version":"3","Authorization":"Bearer "+self.token['access_token']}
		payload = {'countline_ids': str(cl), 'classes': 'traffic13','from':str(((int(time.time()/300))*300)-7200),'to':str((int(time.time()/300)*300)),'time_bucket':'5m','speed_bucket_number':'20','max_speed':'44','fill_nulls':'true'}
		n=requests.get(url+"countline/speed",params=payload,headers=headers)
		return n.json()



#zonalspeeds

'''
countlines with speed data
40950
41013
41014
41048
41049
41050
41060
41061
41062
41074
'''



if __name__=='__main__':
	print ({'from':str(((int(time.time()/300))*300)-3600),'to':str((int(time.time()/300)*300))})
	a=vivacity()
	c=a.metadata()
	r=a.countline('40950')
	print (r)
