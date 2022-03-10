import cycles
import json
import matplotlib.pyplot as plt
import datetime

api=cycles.cycles(cycles.id,cycles.secret)
sites=api.get_site_list()
print (sites)
x=api.get_processed_data(100055035,begin=cycles.dates().convert(datetime.datetime(2020,12,1,0,0,0)))

plt.bar(range(len(x['count'])),x['count'])
plt.show()
