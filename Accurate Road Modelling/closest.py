import json
import math


def distance(a,b):
	# approximate radius of earth in km
	R = 6373.0
	lat1 = math.radians(a[0])
	lon1 = math.radians(a[1])
	lat2 = math.radians(b[0])
	lon2 = math.radians(b[1])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	return R * c


with open('BCMnetwork/saturncoords.json') as f:
	bcm=json.load(f)
	
with open('OSMnetwork/osmnodes.json') as f:
	osm=json.load(f)
	
	
res=[]
d=0
for m in bcm:
	print (str(d)+'/'+str(len(bcm)))
	name=0
	dist=200000000
	for n in osm:
		cdist=distance(bcm[m],osm[n])
		if cdist<dist:
			name=n
			dist=cdist
	res.append([m,name,dist])
	d+=1
with open('corrected.json','w') as f:
	json.dump(res,f)
