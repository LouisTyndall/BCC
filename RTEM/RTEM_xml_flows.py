import datetime
import requests
import passwords
from collections import defaultdict
import json
alkey=passwords.key


def getrtdata(begin=datetime.datetime.now().strftime('%d/%m/%Y'),end=(datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%d/%m/%Y'),scn='R0822D1L0',key=alkey):
	ret=defaultdict(dict)
	base='bcc.bccutc.com'
	url='http://bcc.opendata.onl/UTMC RTEM.json?scn='+scn+'&TS=true&Earliest='+begin+'&Latest='+end+'&ApiKey='+key
	#print (url)

	n=requests.get(url)
	y=n.json()
	
	for n in y["RTEMs"]['kids']:
		#ret[y["RTEMs"]['kids'][n]['kids']['SCN']['value']][datetime.datetime.strptime(y["RTEMs"]['kids'][n]['kids']['Date'],"%Y-%m-%d %H:%M:%S")]=[float(y["RTEMs"]['kids'][n]['kids']['Speed']),float(y["RTEMs"]['kids'][n]['kids']['Vehicles'])]
		ret[datetime.datetime.strptime(y["RTEMs"]['kids'][n]['kids']['Date'],"%Y-%m-%d %H:%M:%S")]=[float(y["RTEMs"]['kids'][n]['kids']['Speed']),float(y["RTEMs"]['kids'][n]['kids']['Vehicles'])]
	return ret
	
for b in range(6):
	tmpa,tmpb=[],[]
	for a in range(1):
		olddata=getrtdata(begin=str(13-b)+"/09/2019",end=str(14-b)+"/09/2019",scn='R0199D1L'+str(a))
		newdata=getrtdata(begin=str(14-b)+"/09/2022",end=str(15-b)+"/09/2022",scn='R0199D1L'+str(a))
		tmpa.append(sum([olddata[n][1]for n in olddata]))
		tmpb.append(sum([newdata[n][1]for n in newdata]))
	print (sum(tmpa), sum(tmpb))
	#for n in olddata:
#	print (olddata[n])
#	break
