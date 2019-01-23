universe = vanilla
executable = /bin/bash
getenv = true
output = acc_file
log = log
arguments = "./build_dt.sh train.vectors.txt test.vectors.txt 10 .1 model_file sys_output"
transfer_executable=false
queue
