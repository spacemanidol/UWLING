files = ['evalfiles/MEN3k.txt','evalfiles/SimLex999.txt','evalfiles/wordsim353.txt']
words = set()
for file in files:
    with open(file,'r') as f:
        for l in f:
            l = l.strip().split()
            words.add(l[0])
            words.add(l[1])

with open('fakecorpus','w') as w:
    for word in words:
        for word2 in words:
            w.write("{} {}\n".format(word,word2))
