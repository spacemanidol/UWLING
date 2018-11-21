import sys
import re
import os
def proc(input_filename, target_label):
    header = 0
    features = {}
    with open(input_filename, 'r') as f:
        for l in f:
            l = l.strip('\n').lower()
            if header == 1:
                l = re.sub("[^a-z]+", ' ', l).strip(' ')
                l = re.sub(" +", ' ', l)
                if l:
                    words = l.split(' ')
                    for word in words:
                        if word not in features:
                            features[word] = 0
                        features[word] += 1
            if len(l) == 0:
                header = 1            
    features = sorted(features.items(), key = lambda x:x[0])
    return features
def train_test_split(filenames, directory, ratio):
    real_files =  []
    print(len(filenames))
    for filename in filenames:
        if os.path.isfile(os.path.join(directory,filename)):
            real_files.append(os.path.join(directory,filename))
    train_size = int(len(real_files) * float(ratio))
    print(len(real_files[:train_size]))
    print(len(real_files[train_size:]))
    return real_files[:train_size], real_files[train_size:]
def main():
    ratio = sys.argv[3]
    for directory in sys.argv[4:]:
        train_filenames, test_filenames = train_test_split(os.listdir(directory), directory, ratio)
        with open(sys.argv[1], 'a') as w:
            for filename in train_filenames:
                features = proc(filename, directory)
                w.write("{}".format(filename))
                for word in features:
                    w.write(" {} {}".format(word[0], word[1]))
                w.write('\n')
        with open(sys.argv[2], 'a') as w:
            for filename in test_filenames:
                features = proc(filename, directory)
                w.write("{}".format(filename))
                for word in features:
                    w.write(" {} {}".format(word[0], word[1]))
                w.write('\n')
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: create_vectors.py <input_filename> <target_label> <output_filename>")
        exit(-1)
    else:
        main()
