import json
from collections import defaultdict
import heapq



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
		
		
if __name__=="__main__":
	with open('ready.json',"r")as f:
		links=json.load(f)
	with open('OSMnetwork/osmways.json',"r") as f:
		ways=json.load(f)
	with open('BCMnetwork/saturnlinks.json',"r") as f:
		saturn=json.load(f)
	for n in ways:
		for m in ways[n]:
			print (n,m['destination'])
		break
	edges=[[str(n),str(m['destination']),m['distance']] for n in ways for m in ways[n]]
	#for n in edges:
	#	print (n)

	tr={n[0]:n[1] for n in links}
	res=[]
	e=len(saturn)
	d=1
	for n in saturn:
		print (d,e)
		d+=1
		print(n)
		try:
			res.append(n+list(Flatten(Dijkstra(edges,str(tr[n[0]]),str(tr[n[1]])))))
		except:
			continue
		if d==200:    #just run the first 200 iterations for test purposes
			break
	print (res)
	with open('path.json',"w") as f:
		json.dump(res,f)
	print('DONE')
