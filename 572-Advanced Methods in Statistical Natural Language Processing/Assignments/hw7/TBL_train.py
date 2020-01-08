import sys
import numpy as np
def readData(filename):
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
    guessLabel = np.full(shape=len(features),fill_value=list(allLabels)[0]) #initialize our first guess to a random class
    return [np.array([labels, guessLabel, features]), allFeatures, allLabels]
def findAndApplyNextTransformation(data, transformation2index, index2transformation):
    #loop through data and model every possible transformation and choose the one that produces the most gain
    gains = np.zeros(len(transformation2index))
    for i in range(len(data[0][0])):
        gold, candidate = data[0][0][i], data[0][1][i]
        for feature in data[0][2][i]:
            for label in data[2]:
                if candidate == gold:
                    gains[transformation2index[(feature, candidate, label)]] -= 1 #bad change so loss
                if label == gold:
                    gains[transformation2index[(feature, candidate, label)]] += 1 #good change so gain
    bestIndex = np.argmax(gains) #index of the highest gain value
    transformation = index2transformation[bestIndex]
    targetFeature, fromClass, toClass = transformation
    for i in range(len(data[0][0])):
        if targetFeature in data[0][2][i] and data[0][1][i] == fromClass: #apply the best transformation to entire dataset
            data[0][1][i] = toClass 
    return data, transformation, gains[bestIndex]
def buildTables(features, classes):
    #build tansformation2index and index2tranformation per suggestion in hw7 slides
    transformation2index, index2transformation = {}, {}
    index = 0
    for feature in features:
        for fromClass in classes:
            for toClass in classes:
                transformation = (feature, fromClass, toClass)
                transformation2index[transformation] = index
                index2transformation[index] = transformation
                index += 1
    return transformation2index, index2transformation
def trainTBL(data, modelFilename, minGain):
    transformation2index, index2transformation = buildTables(data[1],data[2]) #make loopup tables
    gain = minGain + 1
    initClass = ''
    with open(modelFilename,'w') as w:
        while gain >= minGain: #as long as we get gains we keep going
            data, transformation, gain = findAndApplyNextTransformation(data, transformation2index, index2transformation)
            targetFeature, fromClass, toClass = transformation
            if initClass == '':
                initClass = fromClass #we make our first transform the default init class
                w.write('{}\n'.format(initClass))  #init_classname
            w.write('{} {} {} {}\n'.format(targetFeature, fromClass, toClass, int(gain))) #featName from class to class net gain
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: TBL_train.sh <train_data> <model_file> <min_gain>")
        exit(-1)
    else:
        data = readData(sys.argv[1])
        trainTBL(data, sys.argv[2], int(sys.argv[3]))