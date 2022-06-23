
import cycles
import json
import matplotlib.pyplot as plt
import datetime

now=datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
thisweek=now-datetime.timedelta(days=7)
prevweek=now-datetime.timedelta(days=14)
lastyear=now-datetime.timedelta(days=365)
lastyearweek=now-datetime.timedelta(days=358)

api=cycles.cycles(cycles.id,cycles.secret)
sites=api.get_site_list()
print (sites)
x=api.get_processed_data(100050301,begin=cycles.dates().convert(thisweek))

#plt.bar(range(len(x['count'])),x['count'])
#plt.show()

y=api.get_processed_data(100050301,begin=cycles.dates().convert(prevweek),end=cycles.dates().convert(thisweek))


z=api.get_processed_data(100050301,begin=cycles.dates().convert(lastyear),end=cycles.dates().convert(lastyearweek))


print (x['total'],y['total'],z['total'])

ret='There were '+str(x['total'])+' cycle movements recorded at the sample site on Bristol Road near Edgbaston Road over the past week (Monday - Sunday). This is '+str(int(x['total']/y['total']*100))+'% of the total from the previous week and '+ str(int(x['total']/z['total']*100))+'% of the total from the same week 1 year ago'


notes='This indicator is designed to give an indication of the amount of cycling in the city, by using a bellweather site. Detection is carried out by an inductive loop sensor on the cycle track in the middle of the Bristol Road, near to Edgbaston Road. The sensor does not collect data from cyclist on the road or the footpath.'
print (ret)

