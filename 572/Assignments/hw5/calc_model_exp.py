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
def readModel(filename):
    model = {}
    currentClass = ''
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            if len(l) > 2: # Must be a class snce regular lines are <key> <value>
                currentClass = l[-1]
                model[currentClass] = {}
            else:
                model[currentClass][l[0]] = float(l[1])
    return model
def getPYX(labels, features, model):
    probs = {}
    for label in labels:
        exponent = model[label]['<default>']
        for feature in features:
            exponent += model[label][feature]
        probs[label] = math.e ** exponent
    z = sum(probs.values())
    for label in labels:
        probs[label] /= z
    return probs
def writeExp(data, filename, model):
    records = len(data[0])
    labels = set(data[0])
    c = len(labels)
    empExp = {}
    for i in range(records):
        for feature in data[1][i]:
            if model != None:
                probs = getPYX(labels, feature, model)
            else:
                probs = {label:1/c for label in labels} #no model so score is 1/c
            for label in labels:
                py_x = probs[label]
                if label not in empExp:
                    empExp[label] = {}
                if feature not in empExp[label]:
                    empExp[label][feature] = {0:0,1:0}
                empExp[label][feature][0] += 1/records * probs[label] #feature value
                empExp[label][feature][1] += 1 #feature count
    with open(filename,'w') as w:
            for feature, count in sorted(empExp[label].items(), key = lambda x:(-x[1][1],-x[1][0],x[0])):
                w.write('{} {} {:.5f} {}\n'.format(label, feature, count[0], count[1]))
if __name__ == "__main__":
    if len(sys.argv) == 3:
        data = readData(sys.argv[1])
        writeExp(data, sys.argv[2], None)
    elif len(sys.argv) == 4:
        data = readData(sys.argv[1])
        model = readModel(sys.argv[3])
        writeExp(data, sys.argv[2], model)
    else:
        print("Usage: calc_model_exp.sh <training_data> <output_file> <optional model_file>")
        exit(-1)