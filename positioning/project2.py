import math
import os
import csv
import pprint
import pickle
from math import sqrt,pow

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

#Used to sort by distance
def sortFunc(item):
	return(item["d"])

#n is number of neighbors
#inData is just signal strength list
def getKnn(dataset,n,inData,elimRepeats):
	nn = []

	datasetDistance=[]

	for dataPoint in dataset:
		distance = 0
		signalsPoint = dataPoint["signals"]
		for i,key in enumerate(inData.keys()):
			distance += abs(float(signalsPoint.get(key,0))-float(inData.get(key,0)))
			dataPointDistance = dataPoint["position"]
			dataPointDistance["d"] = distance
			datasetDistance.append(dataPointDistance)

	for dataPoint in datasetDistance:
		insert = True
		if(elimRepeats):
			insert = dataPoint not in nn
		if(insert):
			nn.append(dataPoint)
			nn.sort(key=sortFunc)
		if len(nn)>n:
			nn = nn[0:n]
	return nn


def hashFunc(dataPoint):
	return((dataPoint["x"],dataPoint["y"],dataPoint["d"]))

#n is number of neighbors
#inData is just signal strength list
def getKnn2(dataset,n,inData,elimRepeats):
	nn = []

	datasetDistance=[]
	tester = {}

	for dataPoint in dataset:
		distance = 0
		signalsPoint = dataPoint["signals"]
		for i,key in enumerate(inData.keys()):
			distance += abs(float(signalsPoint.get(key,0))-float(inData.get(key,0)))
		dataPointDistance = dataPoint["position"]
		dataPointDistance["d"] = distance
		if(elimRepeats):
			if(not(tester.get(hashFunc(dataPointDistance),False))):
				datasetDistance.append(dataPointDistance)
				tester[hashFunc(dataPointDistance)] = True
		else:
			datasetDistance.append(dataPointDistance)


	datasetDistance.sort(key=sortFunc)

	nn = datasetDistance[0:n]

	return nn

def getKnnAll(dataset,inData,elimRepeats=False):
	nn = []

	datasetDistance=[]
	tester = {}

	for dataPoint in dataset:
		distance = 0
		signalsPoint = dataPoint["signals"]
		for i,key in enumerate(inData.keys()):
			distance += abs(float(signalsPoint.get(key,0))-float(inData.get(key,0)))
		dataPointDistance = dataPoint["position"]
		dataPointDistance["d"] = distance
		if(elimRepeats):
			if(not(tester.get(hashFunc(dataPointDistance),False))):
				datasetDistance.append(dataPointDistance)
				tester[hashFunc(dataPointDistance)] = True
		else:
			datasetDistance.append(dataPointDistance)


	datasetDistance.sort(key=sortFunc)

	nn = datasetDistance
	return nn

def runTest(trainDataset,testDataset,nmin,nstep,nmax,inFile=None,outFile=None):
	distances = {}
	totalN = len(testDataset)

	for i,testDataPoint in enumerate(testDataset):
		print(f"Calculating sample {i+1}/{totalN}")

		realx,realy = float(testDataPoint["position"]["x"]),float(testDataPoint["position"]["y"])
		
		if(inFile == None):
			nn = getKnnAll(trainDataset,testDataPoint["signals"])
		else:
			with open(inFile,'rb') as fileObj:
				nn = pickle.load(inFile)

		if(outFile != None):
			with open(outFile, 'wb') as fileObj:
				pickle.dump(nn,fileObj)

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
	distances = runTest(trainDataset,testDataset,1,1,300,outFile="nearestNeighbors.data")
	avgDistances =  distancesToAvg(distances)
	with open('resultsMultiknn.txt','w+') as file:
		file.write(pprint.pformat(avgDistances))
	with open('resultsMultiknn.data','wb') as file:
		pickle.dump(avgDistances,file)

