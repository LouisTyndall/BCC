import json
import math
from collections import defaultdict
import heapq

ang=40
dist=.1
highwaytypes='motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary','secondary_link','tertiary','tertiary_link','unclassified','residential','service','living_street'

def Dijkstra(edges,f,t):
	#returns shortest path
	g=defaultdict(list)
	for l,r,c in edges:
		g[l].append((c,r))	
	q,seen = [(0,f,())],set()
	while q:
		(cost,v1,path)=heapq.heappop(q)
		if v1 not in seen:
			seen.add(v1)
			path = (v1,path)
			if v1==t:return (cost,path)
			for c, v2 in g.get(v1,()):
				if v2 not in seen:
					heapq.heappush(q,(cost+c, v2, path))
	return (-1,-1)

def Flatten(L):
	while len(L)>0:
		yield L[0]
		L=L[1]
		

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

def initial_bearing(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def anglediff(a,b):
	r=(b-a)%360
	if r>=180:
		r-=360
	return r



with open('BCMnetwork/saturncoords.json') as f:
	bcm=json.load(f)
with open('BCMnetwork/saturnlinks.json') as f:
	bcmways=json.load(f)
	
with open('OSMnetwork/osmnodes.json') as f:
	osm=json.load(f)
with open('OSMnetwork/osmways.json') as f:
	osmways=json.load(f)
	

#turn the osm data into the right shape for the dijksta algorithm 	
edges=[[str(n),str(m['destination']),m['distance']] for n in osmways for m in osmways[n]]

#find bearings for each link
bearings=[[n,(tuple(bcm[n[0]]),tuple(bcm[n[1]])),initial_bearing(tuple(bcm[n[0]]),tuple(bcm[n[1]]))] for n in bcmways if n[0] in bcm and n[1] in bcm]

osmbearings=[]
for n in osmways:
	for m in osmways[n]:
		a=tuple(osm[n])
		b=tuple(osm[str(m['destination'])])

		osmbearings.append([[n,str(m['destination'])],(a,b),initial_bearing(a,b),m['roadtype']])

#match start and end node of bcm to osm nodes that are within 100metres (.1km) and within 45 degrees otherwise discard
d=0
e=len(bearings)
res=[]
errors=[]
for n in bearings:
	print ()
	candidates=[[distance(n[1][0],m[1][0])]+m for m in osmbearings if distance(n[1][0],m[1][0])<dist]
	ocandidates=candidates
	if len(candidates)==0:
		print ('start node, no candidates within 50m')
	hcandidates=[]
	for i in candidates:
		try:
			off=((highwaytypes.index(i[4]))*.02)
		except:
			off=10
		hcandidates.append([i[0]+off]+i[1:])
	try:
		start=sorted([i for i in candidates if -ang<anglediff(n[2],i[3])<ang])[0]    # -22.5<(n[2]-i[3])%360<22.5]
	except:
		print ('start node, no candidates within 45 degrees',n[1][0],n[2])
		for zz in hcandidates:
			print (zz,anglediff(n[2],zz[3]))
		continue
	candidates=[[distance(n[1][1],m[1][1])]+m for m in osmbearings if distance(n[1][1],m[1][1])<dist]
	if len(candidates)==0:
		print ('end node, no candidates within 50m')
	hcandidates=[]
	for i in candidates:
		try:
			off=((highwaytypes.index(i[4]))*.02)
		except:
			off=10
		hcandidates.append([i[0]+off]+i[1:])
	try:
		end=sorted([i for i in candidates if -ang<anglediff(n[2],i[3])<ang])[0]
		#for zz in sorted(hcandidates):
		#	if 0<anglediff(n[2],zz[3])<45:
		#		print (zz,anglediff(n[2],zz[3]))
	except:
		print ('end node, no candidates within 45 degrees',n[1][1],n[2])
		continue
	#print (start)
	#print (end)


	try:
		dij=list(Flatten(Dijkstra(edges,str(start[1][0]),str(end[1][1]))))
	except:
		continue
	if dij[0]>(distance(*n[1])*2):
		print ('too long')
		errors.append([ocandidates,candidates,n])
		continue
	res.append(n[0]+dij)

	d+=1
	print (d,e)
	#if d>200:
	#	break
with open('path.json',"w") as f:
	json.dump(res,f)
with open('errors.json','w')as f:
	json.dump(errors,f)
print('DONE')

'''
res=[]
d=0
for m in bcm:
	print (str(d)+'/'+str(len(bcm)))
	print (m)
	name=0
	dist=200000000
	for n in osm:
		cdist=distance(bcm[m],osm[n])
		if cdist<dist:
			name=n
			dist=cdist
	res.append([m,name,dist])
	d+=1
'''
pass
'''
with open('corrected.json','w') as f:
	json.dump(res,f)
'''
