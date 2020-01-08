./build_kNN.sh train.vectors.txt test.vectors.txt 1 2 sys_1_2 > acc_1_2 &
./build_kNN.sh train.vectors.txt test.vectors.txt 5 2 sys_5_2 > acc_5_2 &
./build_kNN.sh train.vectors.txt test.vectors.txt 10 2 sys_10_2 > acc_10_2 &
./build_kNN.sh train.vectors.txt test.vectors.txt 1 1 sys_1_1 > acc_1_1 &
./build_kNN.sh train.vectors.txt test.vectors.txt 5 1 sys_5_1 > acc_5_1 &
./build_kNN.sh train.vectors.txt test.vectors.txt 10 1 sys_10_1 > acc_10_1 &
mv acc_5_2 acc_file
mv sys_5_2 sys_output
cat train.vectors.txt | ./rank_feat_by_chi_square.sh > feat_list &