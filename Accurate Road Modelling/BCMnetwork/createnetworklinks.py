import zipfile
import io
import shapefile
import json
import geometry as g

def getshapedata(f="BCM_Snowhill_Network_No_Connectors"):
	zipshape = zipfile.ZipFile(open(f+'.zip', 'rb'))
	sf = shapefile.Reader(
		shp=zipshape.open(f+".shp"),
		shx=zipshape.open(f+".shx"),
		dbf=zipshape.open(f+".dbf"))

	#print (len(sf))
	#print (sf.shapeType)
	record = sf.records()
	return [[n[0],n[1]] for n in record],{n[0]:g.OSGB36toWGS84(float(n[3]),float(n[4])) for n in record}

if __name__=="__main__":
	
	
	from collections import defaultdict
	dd=defaultdict(int)
	x,y=getshapedata()
	for n in x:
		dd[n[0]]+=1
		#dd[n[1]]+=1
	c=0
	for n in sorted(dd):
		if dd[n]==1:
			c+=1
	print (c)

	with open('saturnlinks.json','w') as f:
		json.dump(x,f)
	with open('saturncoords.json','w') as f:
		json.dump(y,f)

