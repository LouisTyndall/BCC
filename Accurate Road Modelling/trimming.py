from matplotlib import pyplot as plt
import json

with open('corrected.json') as f:
	data=json.load(f)
	
	
data.sort(key=lambda x: x[2])
print (len(data))
data=[n for n in data if n[2]<0.1]
with open('ready.json',"w") as f:
	json.dump(data,f)

print (len(data))
plt.plot([n for n in range(len(data))], [a[2] for a in data])
plt.show()
