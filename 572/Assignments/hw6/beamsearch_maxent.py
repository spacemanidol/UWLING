import sys
import math
import numpy as np
def readData(filename):
    vectors = []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            features = {}
            featureLength =  len(l)
            for x in range(2, len(l),2):
                features[l[x]] = l[x+1] 
            vectors.append((l[0], l[1], features))
    return vectors
def readModel(filename):
    model, features, labels, allFeatures = {}, set(), set(), set()
    currentClass = ''
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            if len(l) > 2: # Must be a class snce regular lines are <key> <value>
                currentClass = l[-1]
                labels.add(l[-1])
                model[currentClass] = {}
            else:
                features.add(l[0])
                allFeatures.add(l[0])
                model[currentClass][l[0]] = float(l[1])
    return [model, features, labels, ], len(allFeatures)
def readBoundaries(filename):
    boundries = []
    with open(filename, 'r') as f:
        for l in f:
            boundries.append(int(l.strip()))
    return boundries
def getPYX(features, model):
    probs = {}
    for label in model[2]:
        exponent = model[0][label]['<default>']
        for feature in features:
            if feature in model[0][label]: #Keep us from trying to use something in the test data our training data doesnt have
                exponent += model[0][label][feature]
        probs[label] = math.e ** exponent
    z = sum(probs.values())
    for label in model[2]:
        probs[label] /= z
    return probs
def prune(beamSize, topK, sequences):
    maxProb = max(sequences.values())[0]
    topKNodes = {}
    for tag in sequences: #First we make a list of all potnetial paths that meet our criterea
        if (math.log(sequences[tag][0]) + beamSize) >= math.log(maxProb):
            topKNodes[tag] =  sequences[tag]
    new={}
    for path in sorted(topKNodes.items(), key = lambda x: x[1][0], reverse=True)[:topK]:#we soer by probability and keep only the highest prob choices 
        new[path[0]] = path[1]
    return new
def generateResults(sentence, sequences):
    #given our final sequences and the words in the sentence produce the model predicted tags by following the tree backward
    sentenceLength = len(sequences) 
    candidate = max(sequences[sentenceLength-1])
    path = [candidate]
    output = []
    for i in range(sentenceLength):
        probs = sequences[sentenceLength-i-1][candidate][0]
        gold = sentence[sentenceLength-i-1][1]
        instance = sentence[sentenceLength-i-1][0]
        output.append("{} {} {} {}\n".format(instance, gold, candidate, probs))
        candidate = sequences[sentenceLength-i-1][candidate][1]
        path.append(candidate)
    toWrite = ''
    for i in reversed(output[1:]): #Remove final
        toWrite += i
    return list(reversed(path))[1:], toWrite # we remove the BOS tag in path with [1:]
def writeMatrix(candidate, truth, featureNum):
    labels = set(truth).union(set(candidate))
    d = len(labels)
    print("class_num={} feat_num={}\n".format(d, featureNum))
    print("Confusion matrix for the test data:\nrow is the truth, column is the system output\n")
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
    print("            {}\n Test accuracy={:.5f}\n".format(out, count/candidateLength))
def beamSearch(data, model, systemOutputFilename, beamSize, topN, topK, numFeatures):
    sequences, candidates, truths, sentence = {}, [], [], []
    boundaryIndex, index = 0, 0
    with open(systemOutputFilename, 'w') as w:
        w.write("\n\n%%%%% test data:\n")
        for word, gold, features in data:
            truths.append(gold)
            if index == model[3][boundaryIndex]: #Start of a new sentence
                if sentence != []: 
                    path, output = generateResults(sentence, sequences) #generate output and add all out candiate answers to candidates
                    candidates += path
                    w.write(output)
                sentence = []
                index = 0
                boundaryIndex += 1
                sequences = {}
                sequences[index] = {}
                features["prevT=BOS"] = 1
                features["prevTwoTags=BOS+BOS"] = 1
                topNTags = sorted(getPYX(features,model).items(), key = lambda x:-x[1])[:topN]
                for tag in topNTags:
                    sequences[index][tag[0]] =  (tag[1], 'BOS', 1) #tuple of prob, previous tag and previous prob
            else:
                sequences[index] = {}
                for sequence in sequences[index-1]:
                    if len(sequences) == 1:
                        prevTT = 'BOS'
                    else:    
                        prevTT = sequences[index-1][sequence][1]
                    features["prevT={}".format(sequence)] = 1
                    features["prevTwoTags={}+{}".format(sequence, prevTT)] = 1
                topNTags = sorted(getPYX(features,model).items(), key = lambda x:-x[1])[:topN] # Only take the topN based on probability
                for tag in topNTags:
                    sequences[index][tag[0]] =  (tag[1], sequence, 1) #tuple of prob, previous tag and previous prob
                sequences[index] = prune(beamSize, topK, sequences[index]) #prune to topK 
            sentence.append((word, gold))
            index += 1
        path, output = generateResults(sentence, sequences) #generate output and add all out candiate answers to candidates
        candidates += path
        w.write(output)
    writeMatrix(candidates, truths, numFeatures)
if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: beamsearch_maxent.py <test_data> <boundary_file> <model_file> <sys_output> <beam_size> <topN> <topK>")
        exit(-1)
    else:
        boundries = readBoundaries(sys.argv[2])
        data = readData(sys.argv[1])
        model, numFeatures = readModel(sys.argv[3])
        model.append([0] + readBoundaries(sys.argv[2]))
        beamSearch(data, model, sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), numFeatures)