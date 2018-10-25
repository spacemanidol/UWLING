import sys
import os

if __name__ == "__main__":
    fsa_file = sys.argv[1].strip()
    input_file = sys.argv[2].strip()
    with open(input_file, 'r') as f:
        for l in f:
            result = os.popen("echo '{}'|carmel -sliOE -k 1 {}".format(l,fsa_file)).read().strip()
            if result != '0':
                print("{}=>{}".format(l.strip(),result))
            else:
                print("{}=>*none* 0".format(l.strip()))
