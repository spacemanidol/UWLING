import sys
import re
import os
def proc(input_filename):
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
def train_test_split(directory, ratio):
    filenames = os.listdir(directory)
    real_files =  []
    for filename in filenames:
        if os.path.isfile(os.path.join(directory,filename)):
            real_files.append(filename)
    train_size = int(len(real_files) * float(ratio))
    return real_files[:train_size], real_files[train_size:]
def write_result(input_filename, target_label, output_filename, features):
    out_f = open(output_filename, 'a')
    out_f.write(input_filename + ' ' + target_label)
    for item in features:
        out_f.write(' ' + item[0] + ' ' + str(item[1]))
    out_f.write("\n")
    out_f.close()
def main():
    dirs = []
    for i in range(4, len(sys.argv)):
        dirs.append(sys.argv[i])
    ratio = sys.argv[3]
    for directory in dirs:
        train_filenames, test_filenames = train_test_split(directory, ratio)
        with open(sys.argv[1], 'a') as w:
            for filename in train_filenames:
                file_path = os.path.join(directory, filename) 
                features = proc(file_path)
                w.write("{} {}".format(filename, os.path.basename(directory)))
                for item in features:
                    w.write(" {} {}".format(item[0], item[1]))
                w.write('\n')
        with open(sys.argv[2], 'a') as w:
            for filename in test_filenames:
                file_path = os.path.join(directory, filename) 
                features = proc(file_path)
                w.write("{} {}".format(filename, os.path.basename(directory)))
                for item in features:
                    w.write(" {} {}".format(item[0], item[1]))
                w.write('\n')
if __name__ == "__main__":
    main()
