import zipfile
import io
import shapefile
import json
import geometry as g

def getshapedata(f="BCM_Snowhill_Network"):
	zipshape = zipfile.ZipFile(open(f+'.zip', 'rb'))
	sf = shapefile.Reader(
		shp=zipshape.open(f+".shp"),
		shx=zipshape.open(f+".shx"),
		dbf=zipshape.open(f+".dbf"))

	print (len(sf))
	print (sf.shapeType)
	record = sf.records()
	return [[n[0],n[1]] for n in record],{n[0]:g.OSGB36toWGS84(float(n[3]),float(n[4])) for n in record}

if __name__=="__main__":
	x,y=getshapedata()
	with open('saturnlinks.json','w') as f:
		json.dump(x,f)
	with open('saturncoords.json','w') as f:
		json.dump(y,f)
