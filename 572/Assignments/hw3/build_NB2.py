import sys
import numpy as np
import math
from collections import Counter

def readData(filename):
    labels, features= [],[]
    with open(filename, 'r') as f:
        for l in f:
            featuresCount = {}
            l = l.strip().split(' ')
            labels.append(l[0])
            for feature in l[1:]:
                word, count = feature.split(':')
                featuresCount[word] = int(count)
            features.append(featuresCount)
    all_features = set()
    for feature in features:
        all_features = all_features.union(feature.keys())
    return np.array([labels, features]), all_features

def writeMatrix(result, truth):
    lookup = {0:'training', 1:'test'}
    for i in range(2):
        print("Confusion matrix for the {} data:\nrow is the truth, column is the system output\n".format(lookup[i]))
        labels = set(truth[i]).union(set(result[i]))
        d = len(labels)
        resultLength = len(result[i])
        m = np.zeros([d,d])
        label2idx, idx2label = {}, {}
        index, count = 0, 0
        for label in labels:
            label2idx[label] = index
            idx2label[index] = label
            index += 1
        for j in range(resultLength):
            m[label2idx[result[i][j]]][label2idx[truth[i][j]]] += 1
            if result[i][j] == truth[i][j]:
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
        print("            {}\n {} accuracy={}\n".format(out, lookup[i], count/resultLength))

def countDocsInClassForAllTerms(trainingData):
    classes = set(trainingData[0])
    N = len(trainingData[1])
    Nct= {}
    Vc = {}
    for i in range(N):
        document = trainingData[1][i]
        c = trainingData[0][i]
        if c not in Vc:
            Vc[c] = 0
        for t in document:
            if c not in Nct:
                Nct[c] = {}
            if t not in Nct[c]:
                Nct[c][t] = 0
            Vc[c] += trainingData[1][i][t]
            Nct[c][t] += trainingData[1][i][t]
    return Nct, Vc

def outputModel(filename, priors, condprobs):
    with open(filename, 'w') as w:
        w.write('%%%%% prior prob P(c) %%%%%\n')
        for key in priors:
            w.write('{} {} {}\n'.format(key,priors[key],math.log10(priors[key])))
        w.write('%%%%% conditional prob P(f|c) %%%%%\n')
        for c in condprobs:
            w.write('%%%%% conditional prob P(f|c) c={} %%%%%\n'.format(c))
            for word in sorted(condprobs[c]):
                w.write('{} {} {:.5f} {:.5f}\n'.format(word, c, condprobs[c][word], math.log10(condprobs[c][word])))

def trainMultinomialiNB(trainingData, vocab, classPriorDelta, condProbDelta):
    classes = set(trainingData[0])
    N = len(trainingData[1])
    V = len(vocab)
    Nct, Vc = countDocsInClassForAllTerms(trainingData)
    priors, condprobs, Nc = {}, {}, {}
    for c in classes:
        condprobs[c] = {}
        Nc[c] = (trainingData[0] == c).sum()
        priors[c] = (classPriorDelta + Nc[c])/(len(classes)*classPriorDelta + N)
        for t in vocab:
            numerator = condProbDelta
            if t in Nct[c]:
                numerator += Nct[c][t]
            condprobs[c][t] = numerator/(V*condProbDelta+ Vc[c])
    return priors, condprobs

def applyMultinomialiNB(classes, vocab, priors,condprobs,d):
    scores,results = {}, {}
    for c in classes:
        scores[c] = math.log10(priors[c])
        for t in vocab:
            if t in d:
                scores[c] += (math.log10(condprobs[c][t])*d[t] - sum([math.log10(n) for n in range(1,d[t]+1)]))
    prediction = max(scores, key=scores.get)
    total = sum([pow(10,i) for i in np.array(list(scores.values()))-scores[prediction]])
    for c in classes:
        results[c] = pow(10,scores[c]-scores[prediction])/total
    return prediction, results

def eval(trainingData,testData, filename, vocab, priors, condprobs):
    classes = set(trainingData[0])
    results = [[],[]]
    data = [trainingData,testData]
    strings = ['%%%%% training data:','\n\n%%%%% test data:']
    with open(filename,'w') as w:
        for j in range(2):
            for i in range(len(data[j][0])):
                prediction, probs = applyMultinomialiNB(classes, vocab, priors,condprobs,data[j][1][i])
                out = 'array:{} {}'.format(i, data[j][0][i])
                for key in sorted(probs, reverse=False):
                    out += ' {} {}'.format(key, probs[key])
                w.write('{}\n'.format(out))
                results[j].append(prediction)
    return results
    
def main():
    trainingData, vocab = readData(sys.argv[1])
    testData, _ = readData(sys.argv[2])
    priors, condprobs =  trainMultinomialiNB(trainingData, vocab, float(sys.argv[3]), float(sys.argv[4]))
    outputModel(sys.argv[5], priors, condprobs)
    predictions = eval(trainingData,testData, sys.argv[6], vocab, priors, condprobs)
    writeMatrix(predictions, [trainingData[0],testData[0]])

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage:build_NB2.py <trainingData> <test_data> <class_ripr_delta> <conditional_probability_delta> <model_file> <sys.output>")
        exit(-1)
    else:
        main()