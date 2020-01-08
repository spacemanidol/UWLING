import sys
import os

if __name__ == "__main__":
    fsa_file = sys.argv[1]
    input_file = sys.argv[2]
    with open(input_file, 'r') as f:
        for l in f:
            result = os.popen("echo '{}'|carmel -sli {}".format(l,fsa_file)).read().strip()
            if result != '':
                print("{}=>yes".format(l.strip()))
            else:
                print("{}=>no".format(l.strip()))
