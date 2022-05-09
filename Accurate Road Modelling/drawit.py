
import json
import folium
import math
import pickle 
def deg2num(lat_deg, lon_deg, zoom):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = float((lon_deg + 180.0) / 360.0 * n)
	ytile = float((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
	return (xtile, ytile)
 
def num2deg(xtile, ytile, zoom):
	n = 2.0 ** zoom
	lon_deg = xtile / n * 360.0 - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
	lat_deg = math.degrees(lat_rad)
	return (lat_deg, lon_deg)

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

def findlineintersection(a,b):
	x1,x2=float(a[0][0]),float(a[1][0])
	y1,y2=float(a[0][1]),float(a[1][1])	
	A1 = y2-y1
	B1 = x1-x2
	C1 = A1*x1+B1*y1
	#print (A1,B1,C1)
	x1,x2=float(b[0][0]),float(b[1][0])
	y1,y2=float(b[0][1]),float(b[1][1])	
	A2 = y2-y1
	B2 = x1-x2
	C2 = A2*x1+B2*y1
	#print (A2,B2,C2)
	delta = A1 * B2 - A2 * B1
	print (delta)
	if delta==0:
		return a[1][0],a[1][1]

	x = (B2 * C1 - B1 * C2) / delta
	y = (A1 * C2 - A2 * C1) / delta
	return x,y

def offset(line,metres=.05,zoom=19):
	if len(line)<3:
		return line
	coords=[[deg2num(*line[n],zoom),deg2num(*line[n+1],zoom),(initial_bearing(tuple(line[n]),tuple(line[n+1]))+90)%360] for n in range(len(line)-1)]
	#print (coords)
	res=[]
	for n in coords:
		x=(math.sin(math.radians(n[2]))*metres)+n[0][0]
		y=-(math.cos(math.radians(n[2]))*metres)+n[0][1]
		x1=(math.sin(math.radians(n[2]))*metres)+n[1][0]
		y1=-(math.cos(math.radians(n[2]))*metres)+n[1][1]
		res.append((num2deg(x,y,zoom),num2deg(x1,y1,zoom)))
	ret=[res[0][0]]+[findlineintersection(res[n],res[n+1]) for n in range(len(res)-1)]+[res[-1][1]]
	#print (ret)
	return ret

with open('OSMnetwork/osmnodes.json') as f:
	nodes=json.load(f)

with open('path.json') as f:
	paths=json.load(f)
with open('BCM count data/AADT.json','rb') as f:
	counts=pickle.load(f)

import shapefile
w = shapefile.Writer('SaturnRoads',shapeType=3)
w.field('A_Node', 'N')
w.field('B_Node', 'N')
w.field('AADT', 'N')

m = folium.Map(location=[52, -1.5])


cols=['red','green','yellow','brown']
c=0
for path in paths:
	line=[nodes[node] for node in path[3:]]

	line=offset(line)
	try:
		aadt=counts[int(path[0]),int(path[1])]
	except:
		print (path,line)

	try:
		folium.PolyLine(line,weight=int(math.sqrt(aadt)/10),color=cols[int(math.sqrt(aadt)/30)%4],tooltip=path[0]+','+path[1]+"   "+str(int(path[2]*1000))+'AADT = '+str(aadt)).add_to(m)
	except:
		print (path,line)
	line=[[n[1],n[0]] for n in line]
	w.line([line])
	w.record(int(path[0]),int(path[1]),aadt)
	c+=1
	if c==4:
		c=0
w.close()
prj = open("SaturnRoads.prj", "w") 
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
with open('BCMnetwork/saturncoords.json') as f:
	coords=json.load(f)
	
for n in coords:
	folium.Marker(coords[n],tooltip=n).add_to(m)
m.save('google.html')
