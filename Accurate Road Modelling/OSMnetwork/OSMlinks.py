import requests
import json
import math

overpass= "https://overpass-api.de" #"http://localhost:12345" #
syntax="/api/interpreter?data="
#52.4947 53.4623 -1.9284 -1.8715
def osmcreate(tl=(52.3802,-2.0338),br=(52.6093,-1.7269)):
	print ('downloading data')
	highwaytypes='motorway','trunk','primary','secondary','tertiary','unclassified','residential','motorway_link','trunk_link','primary_link','secondary_link','tertiary_link','living_street'

	url=overpass+syntax+'[out:json][timeout:25];('
	for n in highwaytypes:
		url=url+'way["highway"=\"'+n+'\"]('+str(tl[0])+','+str(tl[1])+','+str(br[0])+','+str(br[1])+');'
	url=url+');out;>;out skel qt;'
	print (url)
	getdata = requests.get(url)
	print (getdata.text[:10000])
	d=getdata.json()
	print ('finding nodes')
	nodes={n['id']:[n['lat'],n['lon']] for n in d['elements'] if n['type']=='node'}

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
					if n['tags']['access'] in ['no','private','restricted','destination']:
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
	return nodes,waydict

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


if __name__=="__main__":
	a,b=osmcreate()
	with open('osmnodes.json',"w") as f:
		json.dump(a,f)
	with open('osmways.json',"w") as f:
		json.dump(b,f)
