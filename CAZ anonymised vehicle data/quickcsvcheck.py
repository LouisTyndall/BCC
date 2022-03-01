import csv
import datetime
from collections import defaultdict
filenm='AnonymisedVehicleExtract.csv'


def load_data(f=filenm):
	with open(f,'r') as s:
		sw=csv.DictReader(s)
		ret=list(sw)
	return ret

def read_siemens_time(t):
	format_string = "%Y-%m-%d %H:%M:%S.%f"
	return datetime.datetime.strptime(t+'000',format_string)
	
def by_vehicle(d):
	res=defaultdict(list)
	for n in d:
		if read_siemens_time(n['Capture Date']).date()==datetime.datetime(2022,2,28,0,0,0).date():
			res[n['Hashed VRN']].append([n['RSE Id'],read_siemens_time(n['Capture Date']),n['Direction of Travel']])
	return res
	
if __name__=='__main__':
	d=load_data()
	x=by_vehicle(d)
	tot=0
	st=0
	for n in x:
		record=x[n]
		for y in record:
			if y[0]=='CAZ028' or y[0]=='CAZ029':
				tot+=1
				for l in record:
					if l[0]=='CAZ003' or l[0]=='CAZ004' and 3600>(l[1]-y[1]).total_seconds()>0: #30.21
						st+=1
	print (tot,st,st/tot)
	veh=0
	cr=0
	for n in d:
		veh+=1
		#print (n['Vehicle Recognised'])
		if n['Vehicle Recognised']!='true':
			cr+=1
	print (cr/veh)
			
