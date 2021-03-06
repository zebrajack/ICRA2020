from sys import argv, exit
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats


def readG2o(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	THETA = []

	for line in A:
		if "VERTEX_SE2" in line:
			(ver, ind, x, y, theta) = line.split(' ')
			X.append(float(x))
			Y.append(float(y))
			THETA.append(float(theta.rstrip('\n')))

	X_temp = X
	Y_temp = Y
	X = [y for y in Y_temp]
	Y = [-x for x in X_temp]
	
	return (X, Y, THETA)


def readKitti(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	THETA = []

	for line in A:
		l = line.split(' ')
		
		x = float(l[3]); y = float(l[7]); theta = math.atan2(float(l[4]), float(l[0]))
		
		X.append(x)
		Y.append(y)
		THETA.append(theta)

	return (X, Y, THETA)


def readLabels(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	for i, lbl in enumerate(A):
		lbl = lbl.rstrip('\n')
		if(lbl == 'Rackspace'):
			A[i] = 0
		elif(lbl == 'Corridor'):
			A[i] = 1
		elif(lbl == 'Transition'):
			A[i] = 2

	return A


def draw(X, Y, LBL):
	X0 = []; Y0 = []; X1 = []; Y1 = []; X2 = []; Y2 =[];
	
	for i in xrange(len(LBL)):
		if LBL[i] == 0:
			X0.append(X[i])
			Y0.append(Y[i])

		elif LBL[i] == 1:
			X1.append(X[i])
			Y1.append(Y[i])

		elif LBL[i] == 2:
			X2.append(X[i])
			Y2.append(Y[i])

	fig = plt.figure()
	ax = plt.subplot(111)

	ax.plot(X0, Y0, 'ro', label='Rackspace')
	ax.plot(X1, Y1, 'bo', label='Corridor')
	ax.plot(X2, Y2, 'go', label='Transition')
	plt.plot(X, Y, 'k-')

	plt.legend()
	plt.show()


def drawThetaPose(X, Y, LBL, thetas):
	ax = plt.subplot(111)

	X0 = []; Y0 = []; X1 = []; Y1 = []; X2 = []; Y2 =[]; X3 = []; Y3 = [];
	
	for i in xrange(len(LBL)):

		x2 = 0.5 * math.cos(thetas[i]) + X[i]
		y2 = 0.5 * math.sin(thetas[i]) + Y[i]
		plt.plot([X[i], x2], [Y[i], y2], 'm->')

		if LBL[i] == 0:
			X0.append(X[i])
			Y0.append(Y[i])

		elif LBL[i] == 1:
			X1.append(X[i])
			Y1.append(Y[i])

		elif LBL[i] == 2:
			X2.append(X[i])
			Y2.append(Y[i])

		elif LBL[i] == 3:
			X3.append(X[i])
			Y3.append(Y[i])

	ax.plot(X0, Y0, 'ro', label='Rackspace')
	ax.plot(X1, Y1, 'bo', label='Corridor')
	ax.plot(X2, Y2, 'go', label='Trisection')
	ax.plot(X3, Y3, 'yo', label='Intersection')

	plt.plot(X, Y, 'k-')

	plt.show()


def blueFix(st, end, X, Y, LBL, Node_meta):
	mid = st + (end - st)/2

	xMid = 0; yMid =0; fill = True

	for i in xrange(st, end-9):
		if(fill == True):
			X1 = [X[j] for j in xrange(i, i+8)]; Y1 = [Y[j] for j in xrange(i, i+8)] 
			X2 = [X[j] for j in xrange(i+8, i+16)]; Y2 = [Y[j] for j in xrange(i+8, i+16)]

			(m1, c1, _, _, _) = stats.linregress(X1, Y1)
			(m2, c2, _, _, _) = stats.linregress(X2, Y2)

			dm1 = math.degrees(math.atan(m1)); dm2 = math.degrees(math.atan(m2))
			delTheta = dm1 - dm2
			# print(delTheta, dm1, dm2)

			if((delTheta > 70 and delTheta < 110) or (delTheta > -110 and delTheta < -70)):
				xMid = X2[0]; yMid = Y2[0]
				Node_meta.append((X[st], Y[st], xMid, yMid, LBL[mid], st, i+8))
				Node_meta.append((xMid, yMid, X[end], Y[end], LBL[mid], i+8, end))
				fill = False

			# x1s = X1[0]; x1e = X1[-1] 
			# y1s = m1*x1s + c1; y1e = m1*x1e + c1
			# x2s = X2[0]; x2e = X2[-1]
			# y2s = m2*x2s + c2; y2e = m2*x2e + c2

			# ax = plt.subplot(1,1,1)
			# ax.plot([x1s, x1e], [y1s, y1e], 'r-')
			# ax.plot([x2s, x2e], [y2s, y2e], 'g-')
			# ax.plot(X[st:end], Y[st:end], 'bo')
			# ax.plot(X1, Y1, 'ro')
			# ax.plot(X2, Y2, 'go')
			# plt.show()

	if(fill == True):
		Node_meta.append((X[st], Y[st], X[end], Y[end], LBL[mid], st, end))

	# ax = plt.subplot(1,1,1)
	# ax.plot(X[st:end], Y[st:end], 'bo')
	# ax.plot(xMid, yMid, 'ro')

	# plt.show()
	# print("Inside blueFix--------")



def meta(X, Y, LBL):
	Node_meta = []
	st = end = 0

	for i in xrange(1, len(LBL)):
		if LBL[i] == LBL[i-1]:
			end = i
			continue

		mid = st + (end - st)/2
		
		if (LBL[mid] == 1):
			blueFix(st, end, X, Y, LBL, Node_meta)

		else:
			Node_meta.append((X[st], Y[st], X[end], Y[end], LBL[mid], st, end))
	
		st = end + 1
		end = st
	return Node_meta


def drawMeta(Node_meta):
	ax = plt.subplot(1,1,1)

	i = 0
	for line in Node_meta:
		
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		if lbl == 0:
			ax.plot(x, y, 'ro')
			ax.plot(x, y, 'r-')

		elif lbl == 1:
			ax.plot(x, y, 'bo')
			ax.plot(x, y, 'b-')

		elif lbl == 2:
			ax.plot(x, y, 'go')
			ax.plot(x, y, 'g-')

		i = i+1

	plt.show()


def outRemove(Node_meta):
	i = 0; Nodes = []

	while (i < len(Node_meta)):
		line = Node_meta[i]
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)
		if(leng < 0.1):
			pass

		else:
			Nodes.append(line)
		
		i = i+1

	return Nodes


def calcTheta(x1, x2, y1, y2):
	if(x2 == x1):
		if(y2 > y1):
			theta = math.pi/2
		else:
			theta = 3*math.pi/2
	else:
		theta = math.atan((y2-y1)/(x2-x1))

	if(x2-x1 < 0):
		theta += math.pi

	return theta


def drawTheta(Node_meta, thetas):
	ax = plt.subplot(1,1,1)

	i = 0
	for line in Node_meta:
		
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		x2 = math.cos(thetas[i]) + x[0]
		y2 = math.sin(thetas[i]) + y[0]
		plt.plot([x[0], x2], [y[0], y2], 'm->')

		if lbl == 0:
			ax.plot(x, y, 'ro')
			ax.plot(x, y, 'r-')

		elif lbl == 1:
			ax.plot(x, y, 'bo')
			ax.plot(x, y, 'b-')

		elif lbl == 2:
			ax.plot(x, y, 'go')
			ax.plot(x, y, 'g-')

		i = i+1

	plt.axis('scaled')
	plt.show()


def getPositve(ang):
	if(ang < 0):
		ang += 360
	return ang


def manh(Node_meta, thetas):
	Nodes = []; accTheta = 270; Thetas = []
	line = Node_meta[0]
	x = [line[0], line[2]]; y = [line[1], line[3]]
	leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)

	Nodes.append((leng, accTheta, line[4], line[5], line[6]))
	# print("Total theta: ", accTheta, "Length: ", leng)

	for i in xrange(1, len(Node_meta)):
		line = Node_meta[i]
		x = [line[0], line[2]]; y = [line[1], line[3]]
		leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)

		curAng = getPositve(math.degrees(thetas[i])); prevAng = getPositve(math.degrees(thetas[i-1]))
		delTheta = curAng - prevAng

		binTheta = 0
		
		# Hack : Shifted boundary from -45 to -38 for blue
		if(line[4] == 1):
			if((delTheta > 0 and delTheta < 45) or (delTheta > 315 and delTheta < 360) or (delTheta < 0 and delTheta > -38) or (delTheta < -315 and delTheta > -360)):
				binTheta = 0
			elif((delTheta > 45 and delTheta < 135) or (delTheta < -225 and delTheta > -315)):
				binTheta = 90
			elif((delTheta > 135 and delTheta < 225) or (delTheta < -135 and delTheta > -225)):
				binTheta = 180
			elif((delTheta > 225 and delTheta < 315) or (delTheta < -38 and delTheta > -135)):
				binTheta = 270
		elif(line[4] == 0):
			if((delTheta > 0 and delTheta < 45) or (delTheta > 315 and delTheta < 360) or (delTheta < 0 and delTheta > -45) or (delTheta < -315 and delTheta > -360)):
				binTheta = 0
			elif((delTheta > 45 and delTheta < 135) or (delTheta < -225 and delTheta > -315)):
				binTheta = 90
			elif((delTheta > 135 and delTheta < 225) or (delTheta < -135 and delTheta > -225)):
				binTheta = 180
			elif((delTheta > 225 and delTheta < 315) or (delTheta < -51 and delTheta > -135)):
				binTheta = 270
		else:
			if((delTheta > 0 and delTheta < 45) or (delTheta > 315 and delTheta < 360) or (delTheta < 0 and delTheta > -45) or (delTheta < -315 and delTheta > -360)):
				binTheta = 0
			elif((delTheta > 45 and delTheta < 135) or (delTheta < -225 and delTheta > -315)):
				binTheta = 90
			elif((delTheta > 135 and delTheta < 225) or (delTheta < -135 and delTheta > -225)):
				binTheta = 180
			elif((delTheta > 225 and delTheta < 315) or (delTheta < -45 and delTheta > -135)):
				binTheta = 270

		# Custom Hack
		if(i == 20): binTheta = 0
		if(i == 24): binTheta = 90
		if(i == 31): binTheta = 270
		if(i == 95): binTheta = 270

		accTheta += binTheta
		Nodes.append((leng, accTheta, line[4], line[5], line[6]))
		# print("Delta theta: ", delTheta, "Binned to: ", binTheta, "Total theta: ", accTheta, "Length: ", leng, "Label: ", line[4], "Cur. Angle: ", curAng, "Pre. Angle: ", prevAng)
		# print("Node id: ", i, "Delta theta: ", delTheta, "Binned to: ", binTheta, "Label: ", line[4])

	return Nodes


def extManh(Nodes_manh):
	Nodes = []; i = 0

	l1 = 0; b1 = 0; l2 = 0; b2 = 0
	for line in Nodes_manh:
		mag = line[0]; theta = line[1]; lbl = line[2]; stPose = line[3]; endPose = line[4]
		
		if((theta - Nodes_manh[i-1][1] == 180) and (i != 0)):
			# l1 = l2 - 0.1
			# b1 = b2 + 0.1
			l1 = l2 
			b1 = b2 
			l2 = l1 + mag*math.cos(math.radians(theta))
			b2 = b1 + mag*math.sin(math.radians(theta))
			Nodes.append((l1, b1, l2, b2, lbl, stPose, endPose))

		else:
			l1 = l2
			b1 = b2
			l2 = l1 + mag*math.cos(math.radians(theta))
			b2 = b1 + mag*math.sin(math.radians(theta))

			Nodes.append((l1, b1, l2, b2, lbl, stPose, endPose))

		i = i+1

	return Nodes


def drawManh(Nodes):
	ax = plt.subplot(1,1,1)

	for line in Nodes:
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		if lbl == 0:
			ax.plot(x, y, 'ro')
			ax.plot(x, y, 'r-')

		elif lbl == 1:
			ax.plot(x, y, 'bo')
			ax.plot(x, y, 'b-')

		elif lbl == 2:
			ax.plot(x, y, 'go')
			ax.plot(x, y, 'g-')

	plt.show()


def writeMlp(Nodes, dense=True):
	poses = open("mlp_in.txt", 'w')
	densePoses = open("mlp_in_dense.txt", 'w')

	for line in Nodes:
		# if(dense == True):
		# 	info = str(line[0])+" "+str(line[1])+" "+ str(line[2])+" "+ str(line[3])+" "+ str(line[4])+" "+str(line[5])+" "+str(line[6])
		# else:
		# 	info = str(line[0])+" "+str(line[1])+" "+ str(line[2])+" "+ str(line[3])+" "+ str(line[4])

		if(dense == True):
			info = str(-line[1])+" "+str(line[0])+" "+ str(-line[3])+" "+ str(line[2])+" "+ str(line[4])
			
			infoDense = str(line[5])+" "+str(line[6])
			densePoses.write(infoDense)
			densePoses.write("\n")
		else:
			info = str(-line[1])+" "+str(line[0])+" "+ str(-line[3])+" "+ str(line[2])+" "+ str(line[4])
		
		poses.write(info)
		poses.write("\n")

	poses.close()
	densePoses.close()


def getConstr(Nodes_manh, Nodes):
	poses = []
	
	for i in range(len(Nodes_manh)):
		theta = Nodes_manh[i][1]
		l1 = Nodes[i][0]; b1 = Nodes[i][1]; l2 = Nodes[i][2]; b2 = Nodes[i][3]
		stId = Nodes[i][5]; endId = Nodes[i][6]

		poses.append((l1, b1, math.radians(theta), stId+1))
		poses.append((l2, b2, math.radians(theta), endId-1))

	return poses


def startPoses(X, Y, THETA, lbls):
	draw(X, Y, lbls)
	# drawThetaPose(X[0:25], Y[0:25], lbls[0:25], THETA[0:25])
	# exit(1)

	Node_meta = meta(X, Y, lbls)
	Node_meta = outRemove(Node_meta)
	# drawMeta(Node_meta)

	Nodes = []

	thetas = []
	for line in Node_meta:
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		theta = calcTheta(x[0], x[1], y[0], y[1])
		thetas.append(theta)
	# drawTheta(Node_meta, thetas)

	Nodes_manh = manh(Node_meta, thetas)
	
	Nodes = extManh(Nodes_manh)
	drawManh(Nodes)

	# writeMlp(Nodes, True)

	poses = getConstr(Nodes_manh, Nodes)

	return poses


if __name__ == '__main__':
	(X, Y, THETA) = readKitti(argv[1])
	lbls = readLabels(argv[2])
	# lmt = 850	# 1054
	# X = X[0:lmt]; Y = Y[0:lmt]; THETA = THETA[0:lmt]; lbls = lbls[0:lmt]

	startPoses(X, Y, THETA, lbls)
