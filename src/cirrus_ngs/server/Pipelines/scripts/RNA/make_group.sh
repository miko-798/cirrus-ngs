#!/bin/bash

project_name=$1
file_suffix=$2  #extension of input file, does not include .gz if present in input
root_dir=$3
fastq_end1=$4
fastq_end2=$5
input_address=$6    #this is an s3 address e.g. s3://path/to/input/directory
output_address=$7   #this is an s3 address e.g. s3://path/to/output/directory
log_dir=$8
is_zipped=$9    #either "True" or "False", indicates whether input is gzipped

#logging
mkdir -p $log_dir
log_file=$log_dir/'make_group.log'
exec 1>>$log_file
exec 2>>$log_file

#prepare output directories
workspace=$root_dir/$project_name
mkdir -p $workspace

# Make a new group file
touch $workspace/group.txt
# Call the group file maker
python /shared/workspace/Pipelines/util/GroupFileMaker.py $workspace/group.txt \
/shared/workspace/Pipelines/yaml_examples/$project_name.yaml $output_address

# View the group file
head $workspace/group.txt

# Upload the group file
aws s3 cp $workspace $output_address/ --exclude "*" --include "*group.txt*" --recursive
