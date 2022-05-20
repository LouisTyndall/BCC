import json
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

with open('really.json') as a:
	data=json.load(a)


cleaned={}
for countline in data:
	print(countline)
	t,d=[],[]
	for time in data[countline]:
		dt=datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
		print (dt.hour)
		dd=0
		for x in data[countline][time]['counts']:
			#print (x['class'],x['countIn'],x['countOut'])
			dd+=(x['countIn']+x['countOut'])
		t.append(time)
		d.append(dd)
	#print (t,d)
	plt.plot(t,d)
	plt.show()
	break
