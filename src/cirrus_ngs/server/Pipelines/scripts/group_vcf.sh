#!/bin/bash

project_name=$1
file_suffix=$2  #extension of input file, does not include .gz if present in input
root_dir=$3
group_name=$4       ##NEW## name of group being combined
fastq_end2=$5       ##NEW## always null now
input_address=$6    #this is an s3 address e.g. s3://path/to/input/directory
output_address=$7   #this is an s3 address e.g. s3://path/to/output/directory
log_dir=$8
is_zipped=$9    #either "True" or "False", indicates whether input is gzipped
files_in_group=${10}    #all files in current group
num_threads=${11}

#logging
mkdir -p $log_dir
log_file=$log_dir/'combine_vcf.log'
exec 1>>$log_file
exec 2>>$log_file

. /shared/workspace/software/software.conf

#prepare output directories
workspace=$root_dir/$project_name/$group_name
mkdir -p $workspace

#reference files
genome_fai=$software_dir/sequences/Hsapiens/ucsc.hg19.fasta.fai
genome_fasta=$software_dir/sequences/Hsapiens/ucsc.hg19.fasta
dbsnp=$software_dir/variation/dbsnp_138.hg19.vcf


##DOWNLOAD##
downloads_needed="False"
for file in $files_in_group
do
    if [ ! -f $workspace/$file$file_suffix ]
    then
        downloads_needed="True"
    fi
done

if [ "$downloads_needed" == "True" ]
then
    #this is the suffix of the input from s3
    download_suffix=$file_suffix

    #changes extension if S3 input is zipped
    if [ "$is_zipped" == "True" ]
    then
        download_suffix=$file_suffix".gz"
    fi

    #download all separated vcf and bam files
    for file in $files_in_group
    do
        aws s3 cp $input_address/$project_name/$file/$file$file_suffix $workspace/
        aws s3 cp $input_address/$project_name/$file/$file$file_suffix.tbi $workspace/
    done
fi
##END_DOWNLOAD##

variant_list=""

for file in $files_in_group
do
    variant_list=$variant_list"--variant $workspace/$file$file_suffix "
done


##COMBINEVCF##
$java -Xmx2g -Djava.io.tmpdir=$workspace/temp \
    -jar $gatk \
    -T CombineGVCFs \
    -R $genome_fasta \
    $variant_list \
    -o $workspace/$group_name.merged.vcf

$java -Xms454m -Xmx3181m -Djava.io.tmpdir=$workspace/temp \
    -jar $gatk \
    -T GenotypeGVCFs \
    -R $genome_fasta \
    -nt $num_threads \
    --variant $workspace/$group_name.merged.vcf \
    -o $workspace/$group_name.g.vcf.gz \
    --dbsnp $dbsnp

#END_COMBINEVCF##

##UPLOAD##
aws s3 cp $workspace/ $output_address --exclude "*" --include "$group_name.g.vcf*" --recursive
##END_UPLOAD
