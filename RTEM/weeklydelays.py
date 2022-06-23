import requests
from passwords import key,password
import datetime
import json
import csv
from collections import defaultdict
day=datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)-datetime.timedelta(days=7)
end=day+datetime.timedelta(days=7)

def meta():
	url="https://bcc.opendata.onl/meta/rtem.json?ApiKey="+key
	data=requests.get(url).json()
	print (data)
	locdict={data['RTEM']['kids'][n]['kids']['SystemCodeNumber']:[float(data['RTEM']['kids'][n]['kids']['Latitude']),float(data['RTEM']['kids'][n]['kids']['Longitude'])] for n in data['RTEM']['kids']}
	loclist=[[data['RTEM']['kids'][n]['kids']['SystemCodeNumber'],data['RTEM']['kids'][n]['kids']['Description'],float(data['RTEM']['kids'][n]['kids']['Latitude']),float(data['RTEM']['kids'][n]['kids']['Longitude'])] for n in data['RTEM']['kids']]
	with open('metadata.csv','w') as f:
		sw=csv.writer(f)
		sw.writerows(loclist)




def getdata(day,end):
	url=('http://bcc.opendata.onl/rtem_csv.json?Earliest='+str(day)+'&Latest='+str(end)+'&ApiKey='+key)
	try:
		with open('weeklyspeeds.json','r') as f:
			data=json.load(f)
	except:
		n=requests.get(url)
		data=n.json()
		with open('weeklyspeeds.json','w') as f:
			json.dump(data,f)


	j=defaultdict(list)
	for n in data['RTEM_CSVs']['kids']:
		j[data['RTEM_CSVs']['kids'][n]['kids']['SCN']['value']].append([datetime.datetime.strptime(data['RTEM_CSVs']['kids'][n]['kids']['Date'],'%Y-%m-%d %H:%M:%S'),int(data['RTEM_CSVs']['kids'][n]['kids']['Total']),int(data['RTEM_CSVs']['kids'][n]['kids']['AverageSpeed'])])
	return j

def congestion(flow,speed):
	if flow>0 and 0<speed<8:
		return 1
	else:
		return 0

def edges(data):
	c=0
	start=[]
	end=[]
	for n in data:
		if n[1]==1 and c==0:
			start.append(n[0])
			c=1
		if n[1]==0 and c==1:
			end.append(n[0])
			c=0
	res=[]
	for n in range(len(start)):
		try:
			res.append([end[n]-start[n],start[n],end[n]])
		except:
			res.append([data[-1][0]-start[n],start[n],data[-1][0]])
			
	return res
	
def smooth(data):
	res=[]
	try:
		res.append(data[0])
	except:
		print (data)
	for n in range(len(data)-3):
		#print ([i[1] for i in data[n-1:n+2]])
		if [i[1] for i in data[n-1:n+2]]==[1,0,1]:
			print ('beep')
			res.append([data[n][0],1])
		else:
			res.append(data[n])
	res.append(data[-1])
	return res
		

if __name__=='__main__':
	meta()
	data=getdata(day,end)
	res=[]
	for n in data:
		if len(n)==0:
			continue
		counter=sorted(data[n])
		temp=[[n[0],congestion(n[1],n[2])] for n in counter]
		temp=smooth(temp)
		temp=edges(temp)


		for m in temp:
			res.append(m+[n])
		
	for n in sorted(res)[::-1]:
		print (n)
