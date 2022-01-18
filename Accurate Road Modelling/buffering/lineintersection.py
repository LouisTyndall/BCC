



def findlineintersection(a,b):
	x1,x2=float(a[0][0]),float(a[1][0])
	y1,y2=float(a[0][1]),float(a[1][1])	
	A1 = y2-y1
	B1 = x1-x2
	C1 = A1*x1+B1*y1
	print (A1,B1,C1)
	x1,x2=float(b[0][0]),float(b[1][0])
	y1,y2=float(b[0][1]),float(b[1][1])	
	A2 = y2-y1
	B2 = x1-x2
	C2 = A2*x1+B2*y1
	print (A2,B2,C2)
	delta = A1 * B2 - A2 * B1

	if delta==0: 
		return 'parallel'

	x = (B2 * C1 - B1 * C2) / delta
	y = (A1 * C2 - A2 * C1) / delta
	return x,y

if __name__=='__main__':
	from matplotlib import pyplot as plt
	a,b=((0,0),(3,5),((2,5),(-1,1))
	n=findlineintersection(a,b)
	plt.plot([x[0] for x in a],[y[1] for y in a] )
	plt.plot([x[0] for x in b],[y[1] for y in b] )
	plt.plot(n[0],n[1],"ro")
	plt.show()
