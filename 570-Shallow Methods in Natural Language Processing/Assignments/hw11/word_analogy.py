import sys
import os
import scipy
import numpy as np
from scipy import spatial
def load_vectors(vector_file,flag):
    word_vectors, word2idx, idx2word = [],{},{}
    i = 0
    with open(vector_file,'r') as f:
        for l in f:
            l = l.strip().split(' ')
            word = l[0]
            word2idx[word] = i
            idx2word[i] = word
            values = np.asarray(l[1:], dtype=np.float32)
            if flag != 0:
                values = values/np.linalg.norm(values)
            word_vectors.append(values)
            i += 1
    return word_vectors, word2idx, idx2word
def load_specific_vector(word2idx,word_vectors, word):
    try:
        return word_vectors[word2idx[word]]
    except:
        return word_vectors[0]
def test_file(filename, input_directory, output_directory, word_vectors, word2idx, idx2word, flag2):
    input_file = os.path.join(input_directory, filename)
    output_file = os.path.join(output_directory, filename)
    correct = 0
    with open(os.path.join(input_directory, filename), 'r') as f:
        with open(os.path.join(output_directory, filename), 'w') as w:
            references,candidates, Y_vects = [],[],[]
            for l in f:
                l = l.strip().split()
                if len(l) > 1:
                    word_a, word_b, word_c, word_d = l
                    references.append((word_a, word_b, word_c, word_d))
                    Y_vects.append(load_specific_vector(word2idx,word_vectors,word_b) - load_specific_vector(word2idx,word_vectors,word_a) + load_specific_vector(word2idx,word_vectors,word_c))        
            if flag2 == 0:
                sampling = 'euclidean'
            else:
                sampling =  'cosine'
            for row in spatial.distance.cdist(Y_vects, word_vectors, sampling):
                candidates.append(np.argmin(row))
            for i in range(0,len(references)):
                candidate = idx2word[candidates[i]]
                if candidate == references[i][3]:
                    correct += 1
                w.write("{} {} {} {}\n".format(references[i][0], references[i][1],references[i][2], candidate))
            sys.stdout.write('{}:\nACCURACY TOP1: {}% ({}/{})\n'.format(filename,float(correct/len(candidates))*100, correct, len(candidates)))
            return correct, len(candidates)
def main(vector_file, input_directory, output_directory, flag1, flag2):
    word_vectors, word2idx, idx2word = load_vectors(vector_file, flag1)
    input_files = sorted(os.listdir(input_directory))
    correct, total = 0,0
    for filename in input_files:
        current_correct, current_total = test_file(filename, input_directory, output_directory, word_vectors, word2idx, idx2word, flag2)
        correct += current_correct
        total += current_total
    sys.stdout.write('\nTotal Accuracy: {}% ({}/{})\n'.format(float(correct/total)*100, correct,total))
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:word_analogy.py <vector_file> <input_dir> <flag 1> <flag 2>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))