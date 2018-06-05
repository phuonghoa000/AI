import sys
import math
import pdb
import csv
import re
import numpy as np
from pylab import *
import copy

def readfile(fname):                            
    data = []
    file = open(fname, 'r')

    att_names = file.readline().strip().split(',')
    while True:
        line = file.readline()
        if line == '':
            break
        data.append(convert_dat(line.strip().split(',')))
    return att_names, data


def writefile(att_names, data, fname):         # Ghi ket qua ra file
    file = open(fname, 'w')
    for i in range(0, len(att_names)):          
        file.write(att_names[i])
        file.write(',')
    file.write('Cluster\n')

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            file.write(str(data[i][j]))
            file.write(',')
        file.write('\n')

def convert_dat(data):                      
    for i in range(0, len(data)):
        if data[i] == ' ' or str == '?':
            continue
        try:
            data[i] = int(data[i])
        except ValueError:
            try:
                data[i] = float(data[i])
            except ValueError:
                continue
    return data

class cluster:
    
    pList = []
    name = ""
    def __init__(self,name):
        self.name = name
        self.pList = []
    
    def addPoint(self,point):
        self.pList.append(point)
        
    def getPoints(self):
        return self.pList
    
    def erase(self):
        self.pList = []
    
    def has(self,point):
        
        if point in self.pList:
            return True
        
        return False
    
    # gan gia tri cua thuoc tinh Cluster    
    def setPoints(self, dataset):
        m = copy.deepcopy(dataset)
        for item in self.pList:
            for i in range(0,len(dataset)):
                a = map(str,item)
                b = map(str,dataset[i])
                if (a == b):
                    m[i].append(int(self.name))
        return m
            

class dbscanner:
    
    dataSet = []
    outputDataSet = []
    count = 0
    visited = []
    member = []
    Clusters = []
    
    #khoi chay thuat toan DBScan
    def dbscan(self,D,eps,MinPts):  
        self.dataSet = D[:]
        self.outputDataSet = D[:]
        C = -1
        Noise = cluster('Noise')
        maxitem = 0
        for point in D:
            if point not in self.visited:
                self.visited.append(point)
                NeighbourPoints = self.regionQuery(point,eps)
                
                if len(NeighbourPoints) < MinPts:
                    Noise.addPoint(point)
                else:
                    name = str(self.count)
                    C = cluster(name)
                    self.count+=1;
                    self.expandCluster(point,NeighbourPoints,C,eps,MinPts)
        # gan gia tri Noise cho cac bo bi nhieu
        for item in self.outputDataSet:
            if (len(item)>maxitem):
                maxitem = len(item)
        for item in self.outputDataSet:
            if (len(item)<maxitem):
                item.append('Noise')
        return self.outputDataSet             
                    
                    
            
    # ghe tham cac diem
    def expandCluster(self,point,NeighbourPoints,C,eps,MinPts):
        C.addPoint(point)
        for p in NeighbourPoints:
            if p not in self.visited:
                self.visited.append(p)
                np = self.regionQuery(p,eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)
                    
            for c in self.Clusters:
                if not c.has(p):
                    if not C.has(p):
                        C.addPoint(p)
                        
            if len(self.Clusters) == 0:
                if not C.has(p):
                    C.addPoint(p)
                        
        self.Clusters.append(C)
        
        self.outputDataSet = C.setPoints(self.outputDataSet)
        
                    
                
    # Xet epsilon                 
    def regionQuery(self,P,eps):
        result = []
        for d in self.dataSet:
            if (((d[0]-P[0])**2 + (d[1] - P[1])**2)**0.5)<=eps:
                result.append(d)
        return result


def main():
    in_name = sys.argv[1]
    out_name = sys.argv[2]
    epsilon = float(sys.argv[3])
    minPoints = int(sys.argv[4])
    finalDataSet = []
    NumericData = []
    names, data = readfile(in_name)
    
    for item in range(0,len(data)):
        NumericData.append([])
        for i in range(1,len(data[0])):
            NumericData[item].append(data[item][i])
            
    dbc= dbscanner()
    finalDataSet = dbc.dbscan(NumericData, epsilon, minPoints)
    
    for item in range(0,len(finalDataSet)):
        finalDataSet[item].insert(0,data[item][0])
        
    writefile(names, finalDataSet, out_name)


main()
