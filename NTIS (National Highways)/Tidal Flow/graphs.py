import passwords
import requests
import datetime
import json
import os
from collections import defaultdict
alkey=passwords.key


class dates:
	def __init__(self):
		n=datetime.date.today()
		n=datetime.datetime.fromordinal(n.toordinal())
		self.today=self.convert(n)
		self.yesterday=self.convert(n-datetime.timedelta(days=1))
		self.tomorrow=self.convert(n+datetime.timedelta(days=1))
		self.weekago=self.convert(n-datetime.timedelta(days=7))
		self.monthago=self.convert(n-datetime.timedelta(days=28))
		self.ninetydays=self.convert(n-datetime.timedelta(days=90))
		self.oneeightydays=self.convert(n-datetime.timedelta(days=180))

	def convert(self,dt):
		return datetime.datetime.strftime(dt,"%Y-%m-%dT%H:%M:%S")
		
	def encode(self,dt):
		return datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")
	
	def rencode(self,dt):
		return datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")




def getdata(begin=dates().today,end=dates().tomorrow,key=alkey):
	url='http://bcc.opendata.onl/rtem_csv.json?Earliest='+begin+'&Latest='+end+'&ApiKey='+key
	print (url)
	try:
		with open('tmp.json','r') as f:
			y=json.load(f)
	except:
		n=requests.get(url)
		y=n.json()
		with open('tmp.json','w') as f:
			json.dump(y,f)

	ret=defaultdict(dict)
	for n in y["RTEM_CSVs"]['kids']:
		ret[y["RTEM_CSVs"]['kids'][n]['kids']['SCN']['value']][dates().rencode(y["RTEM_CSVs"]['kids'][n]['kids']['Date'])]=[int(y["RTEM_CSVs"]['kids'][n]['kids']['AverageSpeed']),int(y["RTEM_CSVs"]['kids'][n]['kids']['Total'])]
	return ret


import matplotlib.pyplot as plt
n=getdata('26/4/2022','27/4/2022')
j=['R0101L3','R0101L4']
res={}
for x in n[j[0]]:
	if x in n[j[1]]:
		res[x]=[int((n[j[0]][x][0]+n[j[1]][x][0])/2),n[j[0]][x][1]+n[j[1]][x][1]]
	else:
		res[x]=n[j[0]][x]
print (res)
low=min(res)
dates=[low+datetime.timedelta(minutes=5*x) for x in range(288)]
flows=[res[x][1] if x in res and res[x][0]>20  else 0 for x in dates]
bflows=[res[x][1]  if x in res and res[x][0]<=20 else 0 for x in dates]

aa=plt.bar([a for a in range(len(dates))], flows,width=1)
plt.bar([a for a in range(len(dates))], bflows,color='red',width=1)

j=['R0101L1','R0101L2']
res={}
for x in n[j[0]]:
	if x in n[j[1]]:
		res[x]=[int((n[j[0]][x][0]+n[j[1]][x][0])/2),n[j[0]][x][1]+n[j[1]][x][1]]
	else:
		res[x]=n[j[0]][x]

low=min(res)
dates=[low+datetime.timedelta(minutes=5*x) for x in range(288)]
flows=[-res[x][1] if x in res else 0 for x in dates]
bflows=[-res[x][1]  if x in res and res[x][0]<=20 else 0 for x in dates]
bb=plt.bar([a for a in range(len(dates))], flows,width=1)
cc=plt.bar([a for a in range(len(dates))], bflows,color='red',width=1)

plt.title('A38M at Dartmouth Circus\nInflow vs Outflow\n'+datetime.datetime.strftime(low,"%Y-%m-%d"))



plt.gca().set_xticks([a for a in range(0,len(dates),12)])
plt.gca().set_xticklabels([datetime.datetime.strftime(b,'%H') for b in dates[::12]])
plt.grid(True)
plt.ylim(-300,300)
plt.gca().legend([aa,bb,cc],['Inbound','Outbound','Congested'])
plt.xlabel('Time of Day')
plt.ylabel('veh/5 min')
plt.show()



	
