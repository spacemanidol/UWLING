import sys
import numpy as np
import math
def readData(filename):
    labels, features = [], []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            featureCount = set()
            labels.append(l[0])
            for feature in l[1:]:
                featureCount.add(feature.split(':')[0])
            featureCount.remove('')
            features.append(featureCount)
    return np.array([labels, features])
def countExp(data, labels):
    empExp = {}
    dataLength = len(data[1])
    for i in range(dataLength):
        label = data[0][i]
        for feature in data[1][i]:
            if label not in empExp:
                empExp[label] = {}
            if feature not in empExp[label]:
                empExp[label][feature] = 0
            empExp[label][feature] += 1
    return empExp
def writeExp(empExp, filename, labels, records):
    with open(filename,'w') as w:
        for label in labels:
            for feature, count in sorted(empExp[label].items(), key = lambda x:(-x[1],x[0])):
                w.write('{} {} {:.5f} {}\n'.format(label, feature, count/records, count))
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: calc_emp_exp.py <training_data> <output_file>")
        exit(-1)
    else:
        data = readData(sys.argv[1])
        labels = sorted(set(data[0]))
        empExp = countExp(data, labels)
        writeExp(empExp, sys.argv[2], labels, len(data[0]))