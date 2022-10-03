import requests

n=requests.get('http://www.bcctraffic.co.uk/static/stats.json')
data=n.json()
data={n:str(data[n]) for n in data}


def highlow(n):
	n=int(n)
	if n<0:
		return str(-n)+'% lower'
	else:
		return str(n)+'% higher'

res='Traffic on a weekday was at '+ data['weekday']+'% compared to pre-covid (jan-march 2020) and at '+data['weekend']+'% for weekend traffic. Compared to the previous week, traffic was '+highlow(data['weekly'])+' - the AM peak was '+highlow(data['AM'])+' than the previous week and '+highlow(data['PM'])+' in the PM peak. '+data['growth']+'\'s traffic experienced the highest growth from the previous week. Finally, traffic was '+data['lastyear']+'% of the volume of the same week last year.' 

print (res)

notes='Data is taken from the induction loop detectors on the A38(M) beneath Dartmouth Circus and used as a bellweather to indicate the amount of traffic coming into the city centre. The data is quite reliable, although some periods of downtime may affect data.'

