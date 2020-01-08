import os
import sys
def main():
    for line in sys.stdin:
        sentence, states = line.split(" => ")
        words = sentence.split(' ')
        states = states.split(' ')
        output = ''
        for i in range(0, len(words)):
            temp = words[i] + '/' + states[i+1].split('_')[1]
            output += temp
            output += ' '
        print(output.strip(' '))   
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: conv_format.py")
        exit(-1)
    else:
        main()