universe = vanilla
executable = /bin/bash
getenv = true
log = log
error = myerror
arguments = "./build_dt.sh train.vectors.txt test.vectors.txt 1 0 model_file sys_output > acc_file"
transfer_executable=false
queue
