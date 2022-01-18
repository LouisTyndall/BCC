import config
import os
import requests
import xml.etree.cElementTree as ET
import re
import math
import geometry
import shortest
import pickle
import sampleget
import time 
import folium

def dist(x):
	a1=x[0][0]
	a2=x[1][0]
	b1=x[0][1]
	b2=x[1][1]
	return math.sqrt(((a1-a2)**2)+((b1-b2)**2))

def minmax(a):
	minx=min([x[0] for x in a])
	maxx=max([x[0] for x in a])
	miny= min([x[1] for x in a])
	maxy= max([x[1] for x in a])
	return	(minx,miny),(maxx,maxy)

class cache:
	def __init__(self):
		try:
			with open('cache.p','r') as pfile:
				self.c=pickle.load(pfile)
		except:
			self.c={}
		
	def datagrab(self,url):
		par={'ApiKey':os.environ['ALKEY']}
		try:
			n=requests.get(url,params=par,timeout=1)
		except:
			return self.c[url].content
		self.c[url]=n
		with open('cache.p','w') as pfile:
			pickle.dump(self.c,pfile)
		return n.content

def setupshortest(plt,ln,plt1,ln1,t,b,a,origang):
	#plt,ln= shortest.getloc(t,b,a,origang)
	n1=b[ln[0]]
	n2=b[ln[1]]
	d1=shortest.distance(n1,plt)
	d2=shortest.distance(n2,plt)
	ns=[['start',ln[1],d2]]
	o=plt
	t=False
	for tmp in a:
		if tmp[0]==ln[1] and tmp[1] ==ln[0]:
			t=True
	if t:
		ns+=[['start',ln[0],d1]]
	#plt,ln= shortest.getloc(t1,b,a,origang)
	plt=plt1
	ln=ln1
	n1=b[ln[0]]
	n2=b[ln[1]]
	d1=shortest.distance(n1,plt)
	d2=shortest.distance(n2,plt)
	ns+=[[ln[1],'end',d2]]
	t=False
	for tmp in a:
		if tmp[0]==ln[1] and tmp[1] ==ln[0]:
			t=True
	if t:
		ns+=[[ln[0],'end',d1]]
	try:
		temp=list(shortest.Flatten(shortest.Dijkstra(a+ns,'start','end')))
		dist=temp[0]
		temp=temp[2:-1]
	except:
		return 100000,0
	temp=[list(plt)]+[b[nn] for nn in temp]+[list(o)]
	return dist,temp

#print n.content
f=cache()
root=ET.fromstring(f.datagrab('http://bcc.opendata.onl/UTMC Flow.xml'))
locs={}
for flow in root.findall('Flow'):
		try:
			a= flow.find('SCN').text
			b= float(flow.find('Northing').text)
			c= float(flow.find('Easting').text)
			for val in flow.findall('Value'):
				d=int(val.find('Level').text)
		except AttributeError:
			continue
		b,c=geometry.OSGB36toWGS84(c,b)
		#b,c=geometry.deg2num(c,b,zoom=13)
		#print a,((b,c),d)
		locs[a]=((b,c),d)
		

#print n.content
root=ET.fromstring(f.datagrab('http://bcc.opendata.onl/UTMC ANPR.xml'))
ret={}
for flow in root.findall('ANPR'):
		try:
			a= flow.find('Description').text
			b= flow.find('SCN').text
			c= flow.find('Plates').attrib['matched']
			d= flow.find('Time').text
		except AttributeError:
			continue
		tmp=[]
		for t in a.split(' '):
			n=re.findall(r'E\d\d\d\d',t)
			if n:
				tmp.append(n[0][1:])
		if tmp:
			try:
				#print a,[locs[tmp[0]],locs[tmp[1]]],dist([locs[tmp[0]][0],locs[tmp[1]][0]]),d
				ret[b]={'coordinates':[locs[tmp[0]][0],locs[tmp[1]][0]],'Time':d,'Description':a,'matched':c}
			except KeyError:
				print tmp[0],tmp[1]


old=time.time()-os.path.getmtime('sampledata.pickle')
x,y= minmax([ret[x]['coordinates'][0]for x in ret]+[ret[x]['coordinates'][1]for x in ret])
if old>6048000:
	sampleget.osmcreate(x,y)
	
map_osm = folium.Map(location=(52.453678100000005, -1.7901131000000134))
ctr=0
with open('sampledata.pickle') as file:
	osm=pickle.load(file)
	a,b=shortest.OsmRouteImport(osm) #a-links,b-nodes
	minx,maxx,miny,maxy,ratio=shortest.findminmax(b)
	col=['red','green','blue']
for n in ret:
	print float(ctr)/len(ret)
	#print ret[n]['coordinates'][0][0]
	t=geometry.deg2num(ret[n]['coordinates'][0][0],ret[n]['coordinates'][0][1],zoom=13)
	t1=geometry.deg2num(ret[n]['coordinates'][1][0],ret[n]['coordinates'][1][1],zoom=13)
	origang=(shortest.angle(t,t1))
	r2=[]
	for start in shortest.getlocs(t,b,a,origang):
		for end in shortest.getlocs(t1,b,a,origang):
			r2.append(setupshortest(start[0],start[1],end[0],end[1],t,b,a,origang))
			'''if r2[-1][0] > 0 and r2[-1][0]<100000:
				print r2[-1][0],len(r2[-1][1])'''
	print len(r2)
	try:
		temp=[x for x in r2 if x[0]>0]
		for nn in r2:
			print nn[0],len(nn[1])
		temp= [geometry.num2deg(x[0],x[1],13) for x in min(r2)[1]]
		#print temp
	except:
		continue

	folium.PolyLine(temp,popup=ret[n]['Description'],color=col[ctr%3]).add_to(map_osm)
	folium.Marker(ret[n]['coordinates'][0]).add_to(map_osm)
	folium.Marker(ret[n]['coordinates'][1]).add_to(map_osm)
	ctr+=1
	#if ctr==:
	#	break
	'''break'''

map_osm.save('map.html')

import ui,os
import urllib
file_path = 'map.html'
file_path = os.path.abspath(file_path)
w = ui.WebView()
w.load_url(file_path)
w.present()
	
