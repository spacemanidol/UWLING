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
            if '' in featureCount:
                featureCount.remove('')
            features.append(featureCount)
    return np.array([labels, features])
def readModel(filename):
    model = {}
    currentClass = ''
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            if len(l) > 2: # Must be a class
                currentClass = l[-1]
                model[currentClass] = {}
            else:
                model[currentClass][l[0]] = float(l[1])
    return model
def classify(data, model, filename):
    candidates = []
    dataLength = len(data[1])
    classes = set(data[0])
    with open(filename,'w') as w:
        for i in range(dataLength):
            probs = {}
            for label in classes:
                exponent = model[label]['<default>']
                for feature in data[1][i]:
                    exponent += model[label][feature]
                probs[label] = math.e ** exponent
            z = sum(probs.values())
            for label in classes:
                probs[label] /= z
            probs = sorted(probs.items(), key = lambda x:(-x[1],x[0]))
            candidates.append(probs[0][0])
            out = 'array:{} {}'.format(i,probs[0][0])
            for p in probs:
                out += ' {} {:.5f}'.format(p[0],p[1])
            w.write("{}\n".format(out))
    writeMatrix(candidates, data[0])
def writeMatrix(candidate, truth):
    print("Confusion matrix for the test data:\nrow is the truth, column is the system output\n")
    labels = set(truth).union(set(candidate))
    d = len(labels)
    candidateLength = len(candidate)
    m = np.zeros([d,d])
    label2idx, idx2label = {}, {}
    index, count = 0, 0
    for label in labels:
        label2idx[label] = index
        idx2label[index] = label
        index += 1
    for j in range(candidateLength):
        m[label2idx[candidate[j]]][label2idx[truth[j]]] += 1
        if candidate[j] == truth[j]:
            count += 1
    out = ''
    for j in range(d):
        out += ' {}'.format(idx2label[j])
    out += '\n'
    for j in range(d):
        out += idx2label[j]
        for k in range(d):
            out += ' {}'.format(str(int(m[j][k])))
        out += '\n'
    print("            {}\n Testing accuracy={:.5f}\n".format(out, count/candidateLength))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: maxent_classify.py <test_data> <model_file> <sys_output>")
        exit(-1)
    else:
        data = readData(sys.argv[1])
        model = readModel(sys.argv[2])
        classify(data, model, sys.argv[3])