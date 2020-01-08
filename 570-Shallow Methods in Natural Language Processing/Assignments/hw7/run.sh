rm sy*
./viterbi.sh examples/hmm1 examples/test.word sys1
./viterbi.sh examples/hmm2 examples/test.word sys2
./viterbi.sh examples/hmm3 examples/test.word sys3
./viterbi.sh examples/hmm4 examples/test.word sys4
./viterbi.sh examples/hmm5 examples/test.word sys5
cat sys1 | ./conv_format.sh > sys1_res
cat sys2 | ./conv_format.sh > sys2_res
cat sys3 | ./conv_format.sh > sys3_res
cat sys4 | ./conv_format.sh > sys4_res
cat sys5 | ./conv_format.sh > sys5_res
examples/calc_tagging_accuracy.pl examples/test.word_pos  sys1_res > sys1_res.acc 2>&1
examples/calc_tagging_accuracy.pl examples/test.word_pos  sys2_res > sys2_res.acc 2>&1
examples/calc_tagging_accuracy.pl examples/test.word_pos  sys3_res > sys3_res.acc 2>&1
examples/calc_tagging_accuracy.pl examples/test.word_pos  sys4_res > sys4_res.acc 2>&1
examples/calc_tagging_accuracy.pl examples/test.word_pos  sys5_res > sys5_res.acc 2>&1
cat sys*_res.acc | grep accuracy