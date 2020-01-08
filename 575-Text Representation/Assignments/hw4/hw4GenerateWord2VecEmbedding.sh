make
if [ ! -e enwik8 ]; then
  if hash wget 2>/dev/null; then
    wget http://mattmahoney.net/dc/enwik8.zip
  else
    curl -O http://mattmahoney.net/dc/enwik8.zip
  fi
  unzip enwik8.zip
  rm enwik8.zip
fi
#perl wikifil.pl enwiki8 > text
#time ./word2vec -train text -output NormalCBOW.bin -cbow 1 -size 200 -window 8 -negative 0 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
#time ./word2vec -train text -output NormalSG.bin -cbow 0 -size 200 -window 8 -negative 0 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
#HS for CBOW and SG
time ./word2vec -train text -output HSCBOW.bin -cbow 1 -size 200 -window 8 -negative 0 -hs 1 -sample 1e-4 -threads 20 -binary 1 -iter 15
time ./word2vec -train text -output HSSG.bin -cbow 0 -size 200 -window 8 -negative 0 -hs 1 -sample 1e-4 -threads 20 -binary 1 -iter 15
#Negative sampling for CBOW and SG
time ./word2vec -train text -output NSCBOW.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
time ./word2vec -train text -output NSSG.bin -cbow 0 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
#./distance NormalCBOW.bin
