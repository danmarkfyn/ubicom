import math
import os
import csv
import pprint
import pickle
from math import sqrt,pow
import matplotlib.pyplot as plt
import project2 as p2


if __name__ == "__main__":
	
	fromData = 8
	toData = 80
	

	resL1,resL2,resL3,resL4={},{},{},{}

	with open("Results/L1Distance/distances.data","rb") as file:
		resL1 = pickle.load(file)
	with open("Results/L2Distance/distances.data","rb") as file:
		resL2 = pickle.load(file)
	with open("Results/L3Distance/distances.data","rb") as file:
		resL3 = pickle.load(file)
	with open("Results/L4Distance/distances.data","rb") as file:
		resL4 = pickle.load(file)
	
	xaxis = range(fromData,toData+1)
	yaxisL1 = list(resL1.values())[fromData-1:min(toData,len(resL1.values()))]
	yaxisL2 = list(resL2.values())[fromData-1:min(toData,len(resL2.values()))]
	yaxisL3 = list(resL3.values())[fromData-1:min(toData,len(resL3.values()))]
	yaxisL4 = list(resL4.values())[fromData-1:min(toData,len(resL4.values()))]

	minValL1 = min(yaxisL1)
	minValL2 = min(yaxisL2)
	minValL3 = min(yaxisL3)
	minValL4 = min(yaxisL4)

	print("Min L1 :" + str(minValL1))
	print("Min L2 :" + str(minValL2))
	print("Min L3 :" + str(minValL3))
	print("Min L4 :" + str(minValL4))

	minmin = min((minValL1,minValL2,minValL3,minValL4))

	fig, ax = plt.subplots()


	#ax.axhline(minValL1,0,1,c='b',ls='dashed',lw=1)
	#ax.axhline(minValL2,0,1,c='g',ls='dashed',lw=1)
	#ax.axhline(minValL3,0,1,c='r',ls='dashed',lw=1)
	#ax.axhline(minValL4,0,1,c='c',ls='dashed',lw=1)
	ax.plot(xaxis,yaxisL1,c='b',label="L1 Distance")
	ax.plot(xaxis,yaxisL2,c='g',label="L2 Distance")
	ax.plot(xaxis,yaxisL3,c='r',label="L3 Distance")
	ax.plot(xaxis,yaxisL4,c='c',label="L4 Distance")
	
	ax.legend(frameon=False)

	plt.xlabel("Value of K")
	plt.ylabel("Average error (m)")
	plt.title("Error of KNN varying the value of K for different metrics")
	plt.show()