
import json
import folium

with open('OSMnetwork/osmnodes.json') as f:
	nodes=json.load(f)

with open('path.json') as f:
	paths=json.load(f)
	
m = folium.Map(location=[52, -1.5])


cols=['red','green','blue','grey']
c=0
for path in paths:
	
	folium.PolyLine([nodes[node] for node in path[3:]],color=cols[c],tooltip=path[0]+','+path[1]+"   "+str(int(path[2]*1000))).add_to(m)
	c+=1
	if c==4:
		c=0
m.save('test.html')
