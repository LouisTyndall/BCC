import json
from collections import defaultdict
import heapq
import math

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

with open('errors.json') as f:
	data=json.load(f)

with open('OSMnetwork/osmnodes.json') as f:
	osm=json.load(f)
with open('OSMnetwork/osmways.json') as f:
	osmways=json.load(f)
	

#turn the osm data into the right shape for the dijksta algorithm 	
edges=[[str(n),str(m['destination']),m['distance']] for n in osmways for m in osmways[n]]

ret=[]
print (len(data))
for n in data:
	dist=distance(n[2][1][0],n[2][1][1])
	origins={}
	for a in n[0]:
		origins[a[1][0]]=[a[0],a[2][0]]

	dests={}
	for a in n[1]:
		dests[a[1][0]]=[a[0],a[2][0]]
	print (len(origins),len(dests))
		
	cand=[]	
	c=0
	for a in origins:	
		c+=1
		for b in dests:
			if a == b:
				continue
			cand.append([dist*distance(origins[a][1],dests[b][1]),a,b])
	cand=sorted(cand)[:10]
	res=[]
	for y in cand:
		#print (y[0],dist)
		try:
			dij=list(Flatten(Dijkstra(edges,y[1],y[2])))
		except:
			continue
		if dij[0]>(dist*1.8):
			continue
		if (dist*.7)>dij[0]:
			continue 
		res.append(dij)
	if res:
		ret.append(n[2][0]+sorted(res)[0])
	#break
	
with open('epath.json',"w") as f:
	json.dump(ret,f)


