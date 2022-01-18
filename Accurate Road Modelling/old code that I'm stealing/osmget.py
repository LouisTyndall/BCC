import requests
import json
import math
import pygame

overpass= "https://overpass-api.de" #"http://localhost:12345" #
syntax="/api/interpreter?data="
#52.4947 53.4623 -1.9284 -1.8715
def osmcreate(tl=(52.3802,-2.0338),br=(52.6093,-1.7269)):
	print ('downloading data')
	highwaytypes='motorway','trunk','primary','secondary','tertiary','unclassified','residential','motorway_link','trunk_link','primary_link','secondary_link','tertiary_link','service','living_street'

	url=overpass+syntax+'[out:json][timeout:25];('
	for n in highwaytypes:
		url=url+'way["highway"=\"'+n+'\"]('+str(tl[0])+','+str(tl[1])+','+str(br[0])+','+str(br[1])+');'
	url=url+');out;>;out skel qt;'
	print (url)
	getdata = requests.get(url)
	d=getdata.json()
	print ('finding nodes')
	nodes={n['id']:[n['lat'],n['lon']] for n in d['elements'] if n['type']=='node'}
	p=plot(nodes,1280,720)
	print (len(nodes))
	print ('finding ways')
	waydict={}
	ways=[n for n in d['elements'] if n['type']=='way']
	for n in ways:
		oneway=False
		weight=1
		roadtype='None'
		for ow in n['tags']:
			try:
				if n['tags']['junction']=='roundabout':
					oneway=True
			except:
				pass
			if 'oneway' in ow:
				try:
					if n['tags']['oneway']=='yes':
						oneway=True
				except KeyError:
					print ('error'+ow)
			if 'highway' in ow and roadtype!='noaccess':
				roadtype=n['tags']['highway'] 
			if 'access' in ow:
				try:
					#print ('ok',n['tags']['access'])
					if n['tags']['access'] in ['no','private','restricted','destination']:
						#print ('here')
						weight=100
						roadtype='noaccess'
				except:
					pass
			#weights go here
		prev=None
		for l in n['nodes']:
			current=l
			if current not in waydict:
				waydict[current]=[]
			if prev:
				waydict[prev].append({'destination':current, 'distance':weight*distance(nodes[prev],nodes[current]),'roadtype':roadtype})
				if not oneway:
					waydict[current].append({'destination':prev, 'distance':weight*distance(nodes[prev],nodes[current]),'roadtype':roadtype})
			prev=current
	print (len(waydict))
	print ('not' ,[m for n in waydict for m in waydict[n] if m['roadtype']=='noaccess'])
	
	for n in waydict:
		for m in waydict[n]: 
			#print (m)
			c=(64,64,64)
			#print('neverhere',m['roadtype'])
			if m['roadtype']=='noaccess':
				print('neverhere',m['roadtype'])
				c=(64,0,0)
				print (c)
			p.draw(n,m['destination'],col=c)

	import random
	wc=[n for n in nodes]
	start=random.choice(wc)
	end=random.choice(wc)
	print (start, end)
	print (dij(waydict,start,end,p))




def OsmRouteImport(imported):
	'''
	str imported : content of osm overpass query
	returns route tree of ways ready for Dijkstra algorithm
	and dictionary of all osm nodes on ways
	'''
	root = ET.fromstring(imported)
	waydict={}
	nodes={}
	for m in root.findall('node'):
		nodes[m.attrib['id']]=[float(m.attrib['lat']),float(m.attrib['lon'])]
		#do the translation here
	for n in root.findall('way'):
		oneway=False
		weight=1
		type='None'
		for ow in n.findall('tag'):
			if ow.attrib['k']=='oneway' and ow.attrib['v']=='yes':
				print ('o')
				oneway=True
			if ow.attrib['k']=='highway':
				type=ow.attrib['v']
			#need to add weights in here
		if weight==-1:
			continue
		prev=None
		for l in n.findall('nd'):
			current=l.attrib['ref']
			if current not in waydict:
				waydict[current]={}
			#need to add weights in here
			weight=1
			if prev:
				waydict[prev][current]=[weight*distance(nodes[prev],nodes[current]),type]
				if not oneway:
					waydict[current][prev]=[weight*distance(nodes[current],nodes[prev]),type]
			prev=current
	#convert to format for dikstra function	
	n=[]
	for a in waydict:
		for b in waydict[a]:
			n.append([a,b,waydict[a][b][0],waydict[a][b][1]])
	return n,nodes
	
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

def dij(node,start,end,p):
	p.circle(start)
	p.circle(end)
	#end=-2
	import time
	largevalue=9999
	prev=-1
	visited={n:[largevalue,prev] for n in node}
	visited[start]=[0,-1]
	done={} #tart:[0,-1]}
	current=start

	o=0
	while current!=end:
		#print (current)
		
		for n in node[current]:
			try:
				cdist=visited[n['destination']][0]
			except:
				continue
			ndist=o+n['distance']
			if cdist>ndist:
				visited[n['destination']]=[ndist,current]
				p.draw(current,n['destination'])
		done[current]=visited[current]
		o=done[current][0]
		visited.pop(current)
		try:
			#x=time.time()
			#current= min([[visited[a][0],a] for a in visited])[1]
			#print (current,time.time()-x)
			#x=time.time()
			current=min(visited,key=visited.get)
			#print (current,time.time()-x)
		except ValueError:
			time.sleep(10)
			return 'couldnt find it'
		#print (time.time()-x)
		#import sys
		#sys.exit(0)
	if visited[end][1]==-1:
		return 'not connected'
	done[current]=visited[current]
	length=done[current][1]
	route=[current]
	while current!=start:
		p.draw(current,done[current][1],col=(255,255,255))
		current=done[current][1]
		route.append(current)
	time.sleep(5)
	return length, (route[::-1])
		
def deg2num(lat_deg,lon_deg,zoom=18):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = ((lon_deg +180.0)/360.0 *n)
	ytile = ((1.0 - math.asinh(math.tan(lat_rad)+(1/math.cos(lat_rad)))/math.pi)/2.0 *n)
	#xrem=int((xtile%1)*256)
	#yrem=int((ytile%1)*256)
	#xtile=(xtile*256)
	#ytile=(ytile*256)
	return (xtile,ytile)
	
class plot:
	def __init__(self,nodes,x,y):
		self.nodes={n:deg2num(*nodes[n]) for n in nodes}
		xs=[self.nodes[n][0] for n in self.nodes]
		ys=[self.nodes[n][1] for n in self.nodes]
		xmin=min(xs)
		xmax=max(xs)
		ymin=min(ys)
		ymax=max(ys)
		print (xmax-xmin,x,ymax-ymin,y)
		fx=x/(xmax-xmin)
		fy=y/(ymax-ymin)
		print (fx,fy)
		self.sf=min([fx,fy])
		print ('scaling',self.sf)
		self.xmin=xmin
		self.ymin=ymin
		self.x,self.y=x,y
		print (self.sf,self.xmin,xmax)
		print (self.convert([xmax,ymax]))
		print (self.convert([xmin,ymin]))
		self.c=[]
		#import sys
		#sys.exit(0)
		self.psetup()
		
	def psetup(self):
		pygame.init()
		self.screen=pygame.display.set_mode([self.x,self.y])
	
	def convert(self,n):
		#print (n)
		x=((n[0]-self.xmin)*self.sf)
		y=((n[1]-self.ymin)*self.sf)
		#print(x,y)
		return (int(x),int(y))
	
	def draw(self,a,b,col=(255,0,255)):
		x=self.nodes[a]
		y=self.nodes[b]
		pygame.draw.line(self.screen,col,self.convert(x),self.convert(y),2)
		for a in self.c:
			pygame.draw.circle(self.screen,(128,128,255),self.convert(self.nodes[a]),6)
		pygame.display.flip()
	
	def circle(self,a):
		self.c.append(a)
		
#osmcreate(tl=(34.0202,-118.2890), br=(34.0645,-118.1968))

osmcreate(tl=(52.5053,13.3455), br=(52.5283,13.4129))

'''
for n in range(20):
	osmcreate(tl=(52.4623,-1.9475),br=(52.4947,-1.8490))
=34.0645 34.0202
-118.2890 -118.1968'''
