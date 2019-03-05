import sys
import numpy as np
from math import exp
from math import tanh
def readModel(filename):
    weights, supportVectors, svmType, kernelType, gamma, coef, degree, nrClass, totalSV, rho, labels, nrSV, allFeatures = [],[], '','','','','','','','','','',set()
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split(' ')
            if l[0] == 'svm_type':
                svmType = l[1]
            elif l[0] == 'kernel_type':
                kernelType = l[1]
            elif l[0] == 'gamma':
                gamma = float(l[1])
            elif l[0] == 'degree':
                degree = float(l[1])
            elif l[0] == 'nr_class':
                nrClass = int(l[1])
            elif l[0] == 'rho':
                rho = float(l[1])
            elif l[0] == 'coef0':
                coef = float(l[1])
            elif l[0] == 'total_sv':
                totalSV = int(l[1])
            elif l[0] == 'label':
                labels = [int(l[1]), int(l[2])]
            elif l[0] == 'nr_sv':
                nrSV = [int(l[1]),int(l[2])]
            elif l[0] == 'SV':
                pass
            else:
                values = {}
                for item in l[1:]:
                    item = item.split(':')
                    feature = int(item[0])
                    value = int(item[1])
                    values[feature] = value
                    allFeatures.add(feature)
                supportVectors.append(values)
                weights.append(float(l[0]))
    maxFeature = sorted(allFeatures)[-1] + 1
    for i in range(len(supportVectors)):
        for j in range(maxFeature):
            if j not in supportVectors[i]:
                supportVectors[i][j] = 0
        supportVectors[i] = np.array(sorted(supportVectors[i].items(), key = lambda x:(x[0]))).transpose()[1]
    return [weights, supportVectors, svmType, kernelType, gamma, coef,degree,nrClass, totalSV, rho, labels, nrSV, maxFeature]


def readData(filename, maxFeature):
    features,gold = [],[]
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split(' ')
            values = {}
            for item in l[1:]:
                item = item.split(':')
                feature = int(item[0])
                value = int(item[1])
                values[feature] = value
            for i in range(maxFeature):
                if i not in values:
                    values[i] = 0
            values = np.array(sorted(values.items(), key = lambda x:(x[0]))).transpose()[1][:maxFeature]
            gold.append(int(l[0]))
            features.append(values)
    return [gold, features]

def run(model, data):
    correct = 0
    datalen = len(data[1])
    for i in range(dataLen):
        fx = 0
        for j in range(len(model[1])):
            fx += (model[0][j] * calcInnerProduct(model[3], model[4], model[5], model[6], model[1][j], data[1][i]))
        fx -= model[9]
        if fx >= 0:
            sysLabel = 0
        else:
            sysLabel = 1
        if sysLabel == data[0][i]:
            correct += 1
    print(correct/datalen)
def calcInnerProduct(kernel, gamma, coef, degree, v1, v2):
        if kernel == 'linear':
            return np.inner(v1, v2)
        elif kernel == 'polynomial':
            return (gamma * np.inner(v1, v2) + coef) ** degree
        elif kernel == 'rbf':
            return exp(-gamma * ((np.linalg.norm(v1-v2))**2))
        elif kernel == 'sigmoid':
            return tanh(gamma*np.inner(v1, v2) + coef)
def svmClassify(data, model, sysOutputFilename):
    correct = 0
    dataLen = len(data[0])
    with open(sysOutputFilename,'w') as w:
        correct = 0
        datalen = len(data[1])
        for i in range(dataLen):
            fx = 0
            for j in range(len(model[1])):
                fx += (model[0][j] * calcInnerProduct(model[3], model[4], model[5], model[6], model[1][j], data[1][i]))
            fx -= model[9]
            if fx >= 0:
                sysLabel = 0
            else:
                sysLabel = 1
            if sysLabel == data[0][i]:
                correct += 1
            w.write('{} {} {:.5f}\n'.format(data[0][i], sysLabel, fx))
    print('Accuracy:{:.5f}'.format(correct/dataLen))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: svm_classify.sh <test_data> <model_file> <sys_output>")
        exit(-1)
    else:
        model = readModel(sys.argv[2])
        data = readData(sys.argv[1],model[12])
        svmClassify(data, model, sys.argv[3])