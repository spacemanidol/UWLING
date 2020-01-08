import sys
import re
def main(input_filename, target_label, output_filename):
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
    with open(output_filename,'w') as w:
        w.write("{} {}".format(input_filename, target_label))
        for word in features:
            w.write(" {} {}".format(word[0], word[1]))
        w.write("\n")
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: proc_file.py <input_filename> <target_label> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
