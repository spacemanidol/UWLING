import sys
import numpy as np
def readData(filename, initClass):
    labels, features, allFeatures, = [], [], set()
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            instanceFeatures = set()
            labels.append(l[0])
            for feature in l[1:]:
                if len(feature) > 0:
                    word, count = feature.split(':')
                    allFeatures.add(word)
                    instanceFeatures.add(word)
            features.append(instanceFeatures)
    allLabels = set(labels)
    guessLabel = np.full(shape=len(features),fill_value=initClass) #set all classification to our #initClass
    transitions = np.full(shape=len(features),fill_value='') #empty state to keep track of transitions each data instance has recieved
    return [np.array([labels, guessLabel, features, transitions]), allFeatures, allLabels]
def readModel(filename, maxTransitions):
    model = []
    initClass = ''
    transitions = -1
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            if transitions == maxTransitions: #ignore any more transformations than our depth
                return model, initClass
            if len(l) == 1:
                initClass = l[0]
            else:
                #targetFeature, fromClass, toClass, gain = l
                model.append(l)
            transitions += 1
    return model, initClass
def classifyTBL(data, model, systemOutputFilename):
    #apply all tranformations on data
    for i in range(len(model)):
        targetFeature, fromClass, toClass, gain = model[i]
        for j in range(len(data[0][0])):
            if targetFeature in data[0][2][j] and data[0][1][j] == fromClass: #if data has the feature and fromClass is data's current class then we transform
                data[0][1][j] = toClass
                data[0][3][j] += '{} '.format(model[i][:2]) #ignore the gain value
    #Run inference on data
    candidates, golds = [],[]
    with open(systemOutputFilename, 'w') as w:
        for i in range(len(data[0][0])):
            instanceName = i
            trueLabel = data[0][0][i]
            sysLabel = data[0][1][i]
            transformations = data[0][3][i]
            w.write('{} {} {} {}\n'.format(instanceName, trueLabel, sysLabel, transformations[:-1]))
            golds.append(trueLabel)
            candidates.append(sysLabel)
    writeMatrix(candidates, golds)
def writeMatrix(candidates, golds):
    print("Confusion matrix for the test data:\nrow is the truth, column is the system output\n")
    labels = set(golds).union(set(candidates))
    d = len(labels)
    candidateLength = len(candidates)
    m = np.zeros([d,d])
    label2idx, idx2label = {}, {}
    index, count = 0, 0
    for label in labels:
        label2idx[label] = index
        idx2label[index] = label
        index += 1
    for j in range(candidateLength):
        m[label2idx[candidates[j]]][label2idx[golds[j]]] += 1
        if candidates[j] == golds[j]:
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
    if len(sys.argv) != 5:
        print("Usage: TBL_classify.sh <test_data> <model_file> <sys_outfile> <transformations>")
        exit(-1)
    else:
        model, initClass = readModel(sys.argv[2], int(sys.argv[4]))
        data = readData(sys.argv[1], initClass)
        classifyTBL(data, model, sys.argv[3])