import sys
from scipy import spatial
def readVectors(filename):
    idx2vector, word2idx=  {}, {}
    index = 0
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            word = l[0]
            vector = [float(i) for i in l[1:]]
            idx2vector[index] = vector
            word2idx[word] = index
            index += 1
    return idx2vector, word2idx        
def readTargetWords(filename):
    words = []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split('\t')
            words.append((l[0],l[1]))
    return words
def createOutput(idx2vector, word2idx, words, outputFilename):
    with open(outputFilename, 'w') as w:
        for pair in words:
            vector1 = idx2vector[word2idx[pair[0].lower()]]
            vector2 = idx2vector[word2idx[pair[1].lower()]]
            result = spatial.distance.cosine(vector1,vector2)
            w.write('{}\t{}\t{}\n'.format(pair[0],pair[1],result))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: generateCosineDistance.py <vectors_file> <input_file> <output_file>')
        exit(-1)
    else:
        idx2vector, word2idx = readVectors(sys.argv[1])
        words = readTargetWords(sys.argv[2])
        createOutput(idx2vector, word2idx, words, sys.argv[3])