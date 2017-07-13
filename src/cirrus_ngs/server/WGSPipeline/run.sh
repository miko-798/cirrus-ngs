#!/bin/bash

yaml_file=$1
log_dir=$2

exec 1>>$log_dir/run.log
exec 2>>$log_dir/run.log

python /shared/workspace/WGSPipeline/WGSPipeline.py $yaml_file
