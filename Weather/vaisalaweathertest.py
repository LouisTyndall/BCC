import passwords
import requests

url='https://tfwm.onl/weather.json?meta=true&ApiKey='+passwords.key

n=requests.get(url)

print(n.content[:1000])

y=n.json()


for a in y['Weather_Data']['kids']:
	print (y['Weather_Data']['kids'][a]['kids'])

'''
b'{\r\n"Weather_Data": {"kids":{"Weather": {"kids":{"SCN": "VV_0134","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalDop": "1","reason": "SCHEDULED","heightMetres": "0","Value": "24.1517"}}\r\n,"Weather#1": {"kids":{"SCN": "VV_0135","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalDop": "1","reason": "SCHEDULED","heightMetres": "0","Value": "13.5635"}}\r\n,"Weather#2": {"kids":{"SCN": "VV_0136","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalDop": "1","reason": "SCHEDULED","heightMetres": "0","Value": "13.6366"}}\r\n,"Weather#3": {"kids":{"SCN": "VV_0137","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalDop": "1","reason": "SCHEDULED","heightMetres": "0","Value": "0","Values": "0.0"}}\r\n,"Weather#4": {"kids":{"SCN": "VV_0138","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalDop": "1","reason": "SCHEDULED","heightMetres": "0","Value": "13.4339"}}\r\n,"Weather#5": {"kids":{"SCN": "VV_0139","Date": "2022-01-31 16:00:00","fixQuality": "7","horizontalD'
'''
