import math
import os
import csv
import pprint
import pickle
from math import sqrt,pow
import matplotlib.pyplot as plt
import project2 as p2


if __name__ == "__main__":
	
	res={}
	with open("resultsMultiknn.data","rb") as file:
		res = pickle.load(file)
	xaxis = []
	yaxis = []
	for i,(key,val) in enumerate(res.items()):
		if(i>100):
			break
		xaxis.append(key)
		yaxis.append(val)
	plt.plot(xaxis,yaxis)
	plt.xlabel("value of K")
	plt.ylabel("Average error (m)")
	plt.title("Error of KNN varying the value of K")
	plt.show()