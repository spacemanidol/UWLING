import sys
import numpy as np
import math
from collections import Counter
def readData(filename):
    labels, features, all_features = [], [], []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            featureCount = {}
            labels.append(l[0])
            for feature in l[1:]:
                word, count = feature.split(':')
                all_features.append(word)
                featureCount[word] = int(count)
            features.append(featureCount)
    all_features = set(all_features)
    return np.array([labels, features]), all_features
def euclidean(a,b):
    dist = 0
    for feature in set(a).union(set(b)):
        valueA, valueB = 0,0
        if feature in a:
            valueA = a[feature]
        if feature in b:
            valueB = b[feature]
        dist += ((valueA - valueB)*(valueA - valueB))
    return math.sqrt(dist)    
def cosine(a,b):
    sumAB,normA,normB = 0,0,0
    for feature in set(a).union(set(b)):
        if feature in a and feature in b:
            sumAB += a[feature]*b[feature]
        if feature in a:
            normA += (a[feature]*a[feature])
        if feature in b:
            normB += (b[feature]*b[feature])
    return sumAB/ (math.sqrt(normA)*math.sqrt(normB)) 
def writeMatrix(candidates, truth):
    lookup = {0:'training', 1:'test'}
    for i in range(2):
        print("Confusion matrix for the {} data:\nrow is the truth, column is the system output\n".format(lookup[i]))
        labels = set(truth[i]).union(set(candidate[i]))
        d = len(labels)
        candidateLength = len(candidate[i])
        m = np.zeros([d,d])
        label2idx, idx2label = {}, {}
        index, count = 0, 0
        for label in labels:
            label2idx[label] = index
            idx2label[index] = label
            index += 1
        for j in range(candidateLength):
            m[label2idx[candidate[i][j]]][label2idx[truth[i][j]]] += 1
            if candidate[i][j] == truth[i][j]:
                count += 1
        out = ''
        for j in range(d):
            out += ' {}'.format(idx2label[i])
        out += '\n'
        for j in range(d):
            out += idx2label[j]
            for k in range(d):
                out += ' {}'.format(str(int(m[j][k])))
            out += '\n'
        print("            {}\n {} accuracy={:.5f}\n".format(out, str(lookup[i].capitalize()), count/candidateLength))
def vote(neighbors, data):
    votes, output = {}, ''
    for neighbor in neighbors:
        label = data[int(neighbor[1])]
        if label not in votes:
            votes[label] = 0
        votes[label] += 1
    total = sum(votes.values())
    for label in sorted(votes.items(), key = lambda x:-x[1]): 
        output += ' {} {}'.format(label[0], votes[label[0]]/total)
    return sorted(votes.items(), key = lambda x:-x[1])[0][0], output
def search(candidateVector, dimensions, data, i, similarityFunc, k, distance):
    for j in range(dimensions):
        neighborVector = data[1][j]
        if similarityFunc == 1:
            distance[j] = [euclidean(candidateVector,neighborVector),j]
        elif similarityFunc == 2:
            distance[j] = [cosine(candidateVector,neighborVector),j]
        else:
            print('incorrect similarity function please use cosine or euclidian(2 or 1)')
            exit(-1)
    if similarityFunc == 1:
        if i != -1:
            distance[i] = float("inf") #if training we set the distance to itself to infinity
        neighbors = distance[distance[:,0].argsort(kind='mergesort')][:k]
    else:
        if i != -1:
            distance[i] = 0 #if training we set the distance to itself zero
        neighbors = distance[distance[:,0].argsort(kind='mergesort')][-k:]
    best, output = vote(neighbors, data[0])
    return best, output
def knn(trainingData, testData, k, similarityFunc, systemOutputFilename):
    candidate, truth = [[],[]], [[],[]]
    dimensions, testDimensions = len(trainingData[1]), len(testData[1])
    distance = np.empty(shape=(dimensions,2))
    with open(systemOutputFilename, 'w') as w:
        w.write('%%%%% training data:\n')
        for i in range(dimensions):
            truth[0].append(trainingData[0][i])
            best, to_write = search(trainingData[1][i], dimensions, trainingData, i, similarityFunc, k, distance) #for each vector we search for knn neighbors and get a result and output string
            w.write('array:{} {} {}\n'.format(i, best, to_write))
            candidate[0].append(best)
        w.write('\n\n%%%%% test data:\n') 
        for i in range(testDimensions):
            truth[1].append(testData[0][i])
            best, to_write = search(testData[1][i], dimensions, trainingData, -1, similarityFunc, k, distance) #for each vector we search for knn neighbors and get a result and output string
            w.write('array:{} {} {}\n'.format(i, best, to_write))
            candidate[1].append(best) 
    return candidate, truth
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:build_kNN.py <training_data> <test_data> <k_val> <similarity_func> <sys_output>")
        exit(-1)
    else:
        trainingData, features = readData(sys.argv[1])
        testData, _ = readData(sys.argv[2])
        candidate, truth = knn(trainingData,testData, int(sys.argv[3]), int(sys.argv[4]),sys.argv[5])
        writeMatrix(candidate, truth)