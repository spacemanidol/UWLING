import sys
def readInput():
    labels, features, all_features, labelCount = [], [], [], {}
    l = sys.stdin.readline().strip().split(' ')
    while len(l)> 1:
        label = l[0]
        if label not in labelCount:
            labelCount[label] = 0
        labelCount[label] += 1
        labels.append(label)
        currFeat = set()
        for key in l[1:]:
            feature, _ = key.split(':')
            all_features.append(feature)
            currFeat.add(feature) 
        features.append(currFeat)
        l = sys.stdin.readline().strip().split(' ')
    return [labels, features] ,  set(all_features), labelCount
def rankByChiSquared(data, features, labelCount):
    labels = labelCount.keys()
    dataLength = len(data[0])
    n = sum(labelCount.values())
    results, featureOccourences, featureNonOccourences = [], {}, {}
    for feature in features:
        for label in labels:
            featureOccourences[label] = 0 #Initialize
        for i in range(dataLength):
            if feature in data[1][i]:
                featureOccourences[data[0][i]] += 1 # We could how many times the feature occours in the data for each label
        for label in labels:
            featureNonOccourences[label] = labelCount[label] - featureOccourences[label] #count of the times it doesnt appear for each label
        totalFeatureOccourences = sum(featureOccourences.values())
        totalFeatureNonOccourences = sum(featureNonOccourences.values())
        chi =  sum([((featureOccourences[label]-(labelCount[label]*totalFeatureOccourences/n))**2/(labelCount[label]*totalFeatureOccourences/n) +(featureNonOccourences[label] - (labelCount[label] * totalFeatureNonOccourences/n))**2/(labelCount[label] * totalFeatureNonOccourences/n)) for label in labels]) #Chi squared calc
        results.append([feature, chi, totalFeatureOccourences]) #save the re
    [print('{} {:.5f} {}'.format(*score)) for score in sorted(results, key = lambda x:(-x[1], -x[2], x[0]), reverse=False)] #print features sorted by chi^2 value, count in text, alphabetically
if __name__ == "__main__":
    data, all_features, labelCount= readInput()
    results = rankByChiSquared(data, all_features, labelCount)