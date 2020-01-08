rm train.vectors*
rm test.vectors*
rm me*
./create_vectors.sh train.vectors.txt test.vectors.txt  0.9 /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.guns /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.mideast /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.misc
mallet import-file --input train.vectors.txt --output train.vectors
mallet import-file --input test.vectors.txt --output test.vectors --use-pipe-from train.vectors
vectors2classify --training-file train.vectors --testing-file test.vectors --trainer MaxEnt --output-classifier me-model --report train:accuracy --report test:accuracy >me.stdout 2>me.stderr
cat me.stdout

