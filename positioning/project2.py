import math
import os
import csv
import pprint
import pickle
from math import sqrt,pow


################################
# FUNCTIONS TO MAKE DATASET
################################

#Points shape:
#{"x":xval,"y":yval,"d":distance}
def weightedAverage(points):
	weightedValueX = 0
	weightedValueY = 0
	totalWeights = 0
	for point in points:
		weight = 1/point["d"]

		weightedValueX += float(point["x"])*weight
		weightedValueY += float(point["y"])*weight
		totalWeights += weight

	mx = weightedValueX/totalWeights 
	my = weightedValueY/totalWeights
	return (mx,my)

def getFileList(path):
	list_of_files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
				if filename.endswith('data_wide.csv'): 
					list_of_files.append(os.sep.join([dirpath, filename]))
	return list_of_files

def makeDataset(directory):
	dirList = getFileList(directory)
	dataset = []
	for path in dirList:
		dataset = addFileToDataset(dataset,path)
	return dataset
	#Dataset structure:   
	#           [
	#               {
	#                   "signals":{edgeNum:edgeVal...},
	#                   "position":{"x":x,"y":y}
	#               }
	#           ]

def addFileToDataset(dataset,fileDir):
	with open(fileDir) as csvFile:
		csvReader = csv.reader(csvFile,delimiter=",")
		first = True
		linecount = 0
		edges = []
		for row in csvReader:
			position = {}
			signals = {}
			if(first):
				first = False
				edges = row[4:]
			else:
				position["x"] = row[2]
				position["y"] = row[3]
				edgeData = row[4:]
				for i in range(len(edges)):
					signals[edges[i]] = edgeData[i]
				dataset.append({"signals":signals,"position":position})
	return dataset


################################
# FUNCTIONS TO GET DISTANCE/NN
################################

#Used to sort by distance
def sortFunc(item):
	return(item["d"])

def distanceWithType(point1,point2,type=1):
	distance = 0
	edgeList = list(set(list(point1.keys())+list(point2.keys())))
	if(type==1):
		for i,key in enumerate(edgeList):
			distance += abs(float(point1.get(key,0))-float(point2.get(key,0)))
	else:
		sum = 0
		for i,key in enumerate(edgeList):
			sum += (abs(float(point1.get(key,0))-float(point2.get(key,0))))**type
		distance = sum**(1/type)
	return distance

def hashFunc(dataPoint):
	return((dataPoint["x"],dataPoint["y"],dataPoint["d"]))

#inData is just signal strength list
def getKnnAll(dataset,inData,elimRepeats=False,distanceType=1):
	nn = []

	datasetDistance=[]
	tester = {}

	for dataPoint in dataset:
		distance = 0
		signalsPoint = dataPoint["signals"]

		distance = distanceWithType(signalsPoint,inData,distanceType)

		dataPointDistance = dataPoint["position"]
		dataPointDistance["d"] = distance
		if(elimRepeats):
			if(not(tester.get(hashFunc(dataPointDistance),False))):
				datasetDistance.append(dataPointDistance)
				tester[hashFunc(dataPointDistance)] = True
		else:
			datasetDistance.append(dataPointDistance)

	#Probably replace this with a priority queue instead of having to sort
	datasetDistance.sort(key=sortFunc)

	nn = datasetDistance
	return nn

def runTest(trainDataset,testDataset,nmin,nstep,nmax,distanceType=1):
	distances = {}
	totalN = len(testDataset)

	for i,testDataPoint in enumerate(testDataset):
		print(f"Calculating sample {i+1}/{totalN}")

		realx,realy = float(testDataPoint["position"]["x"]),float(testDataPoint["position"]["y"])
		nn = getKnnAll(trainDataset,testDataPoint["signals"],distanceType=distanceType)

		for i in range(nmin,nmax+1,nstep):
			infx,infy = weightedAverage(nn[:i])
			infx,infy = float(infx),float(infy)
			distanceMid = distances.get(i,[])
			distanceMid.append(sqrt(pow(abs(infx-realx),2)+pow(abs(infy-realy),2)))
			distances[i]=distanceMid
	return distances

def distancesToAvg(distanceDict):
	res = {}
	for key,value in distanceDict.items():
		res[key] = sum(value)/len(value)
	return res

if __name__ == "__main__":
	directory = "./experiment/experiment1/train"
	trainDataset = makeDataset(directory)
	
	directoryTest = "./experiment/experiment1/test"
	testDataset = makeDataset(directoryTest)
	distances = runTest(trainDataset,testDataset,1,1,300,distanceType=4)
	avgDistances =  distancesToAvg(distances)
	with open('distances.txt','w+') as file:
		file.write(pprint.pformat(avgDistances))
	with open('distances.data','wb') as file:
		pickle.dump(avgDistances,file)

