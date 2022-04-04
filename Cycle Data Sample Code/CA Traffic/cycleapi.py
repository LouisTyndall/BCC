#!python 3
import requests
import datetime
import json
from collections import defaultdict
import shelve

cachedb='cacache'
#catraffic
token_url="https://Vdanet-beta.ca-traffic.com/Token"
list_url="https://vdanet-beta.ca-traffic.com/api/SiteList/VDAPro-TransportForWestMids/All/NULL/1970-1-1/1970-1-1"
counter_url="https://vdanet-beta.ca-traffic.com/api/FlowData/VDAPro-TransportForWestMids/"
header={'content-type':'application/x-www-form-urlencoded'}

class CycleCounters():
	def __init__(self,payload,url=token_url,header=header):
		n=requests.post(url,data=payload,headers=header) # Alan is a pedant
		self.response=n.json()
		self.auth={'Authorization':'Bearer '+self.response['access_token']}
		self.sitelist=self.counterlist()
		
	def counterlist(self,url=list_url):
		n=requests.get(url,headers=self.auth)
		x=n.json()
		#print (json.dumps(x,indent=2))
		res={}
		for a in x['properties']:
			res[a["SiteReference"]]={'title':a["SiteTitle"],'number':a['SiteNumber'],'location':[a['SiteLatitude'],a['SiteLongitude']],'id':a['SiteID']}
			#print (res)
		return res
		
	def getdata(self,site,startdate,enddate,bins=60,url=counter_url):
		assert (enddate-startdate).days<31,"Query period is greater than a month"
		start=datetime.datetime.strftime(startdate,"%Y-%m-%d")
		end=datetime.datetime.strftime(enddate,"%Y-%m-%d")
		query=str(self.sitelist[site]['id'])+'/'+str(start)+'/'+str(end)+'/'+str(bins)
		#print "url:",url+query
		n=requests.get(url+query,headers=self.auth)
		x=n.json()
		if x['properties']['ReportError']['HasError']:
			return []
		#print (json.dumps(x,indent=2))
		ret={}
		for channels in x['properties']['Channels']:
			chname=(channels['ChannelNo'],channels['ChannelName'])
			vals=[]
			for data in channels['Flows']:
				date=datetime.datetime.strptime(data['DateOfData'],"%Y-%m-%dT%H:%M:%S")
				vals+=sorted([[date+datetime.timedelta(seconds=60*int(val)),data['Values'][val]] for val in data['Values']]) # 60 is because time is quoted in minutes from the beginning of the day
			ret[chname]=vals
		return ret
		
	def ncgetdata(self,site,startdate,enddate,bins=60,url=counter_url):
		assert (enddate-startdate).days<31,"Query period is greater than a month"
		start=datetime.datetime.strftime(startdate,"%Y-%m-%d")
		end=datetime.datetime.strftime(enddate,"%Y-%m-%d")
		query=str(self.sitelist[site]['id'])+'/'+str(start)+'/'+str(end)+'/'+str(bins)
		#print "url:",url+query
		n=requests.get(url+query,headers=self.auth)
		x=n.json()
		if x['properties']['ReportError']['HasError']:
			return []
		#print (json.dumps(x,indent=2))
		ret={}
		for channels in x['properties']['Channels']:
			chname=(channels['ChannelNo'],channels['ChannelName'])
			vals=[]
			for data in channels['Flows']:
				date=datetime.datetime.strptime(data['DateOfData'],"%Y-%m-%dT%H:%M:%S")
				vals+=sorted([[date+datetime.timedelta(seconds=60*int(val)),data['Values'][val]] for val in data['Values']]) # 60 is because time is quoted in minutes from the beginning of the day
			ret[chname]=vals
		res=defaultdict(list)
		for n in ret:
			for y in ret[n]:
				print (y)
				res[y[0]].append(int(y[1]))
		#print (res)
		return [[n,sum(res[n])] for n in res]
		
	def cacheraw(self,loc,start,end,bins=60):
		days=end.date()-start.date()
		cday=start.date()
		data=[]
		today=datetime.date.today()
		missing=[] #datetime.datetime(2020,5,1).date(),datetime.datetime(2020,5,5).date()]
		while cday<=end.date():
			index=str(cday)+str(loc)+str(bins)
			with shelve.open(cachedb) as db:
				if index not in db or cday>=today-datetime.timedelta(days=1) or cday in missing:
					db[index]=self.ncgetdata(site=loc,bins=bins, startdate=datetime.datetime(cday.year,cday.month,cday.day), enddate=datetime.datetime(cday.year,cday.month,cday.day)+datetime.timedelta(days=1))
				data+=db[index]					
			cday+=datetime.timedelta(days=1)
		data=[n for n in data if start<n[0]<end]
		return data # {'date':[n for n in res],'value':sum([res[n] for n in res])}
		
		
if __name__=='__main__':
	with open('config.json',"r") as j:
		payload=json.load(j)

	x=CycleCounters(payload)
	r=x.counterlist()
	import folium
	m = folium.Map(location=[53.0, -1.5])
	for n in r:
		try:
			d=[float(a) for a in r[n]['location']]
		except TypeError:
			print (n,r[n]['title'])
			continue
	
		folium.Marker(d, popup='<i>'+r[n]['title']+'</i>', tooltip=n).add_to(m)

	m.save('map.html')
	
	import ui,os
	import urllib
	file_path = 'map.html'
	file_path = os.path.abspath(file_path)
	w = ui.WebView()
	w.load_url(file_path)
	w.present()




