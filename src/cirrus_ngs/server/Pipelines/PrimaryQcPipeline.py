__author__ = 'Mengyi Liu<mel097@ucsd.edu>'

import sys
import subprocess
import PBSTracker
import YamlFileReader

root = "/scratch"
workspace = "/shared/workspace/Pipelines/"
scripts = "/shared/workspace/Pipelines/scripts/"
log = "/shared/workspace/logs/MultiQC"

# specify files to perform multiqc on; each file in one quote, separated by comma
multiqc_file_list = "AD2-WK4_GTAGAG_S16_L001_R1_001_fastqc.zip"   ## output of fastqc


def run_analysis(yaml_file):
    documents = YamlFileReader.parse_yaml_file(yaml_file)

    project_name = documents.get("project")
    analysis_steps = documents.get("analysis")
    s3_input_address = documents.get("upload")
    sample_list = documents.get("sample")

    # makes logs directory
    global log
    log += '/' + project_name

    # run fastqc
    if "fastqc" in analysis_steps:
        for sample in sample_list:
            sample_info = get_sample_info(sample)
            print("SAMPLE INFO: ")
            print(sample_info)
            print("project name: " + project_name)
            run_fastqc(project_name, sample_info.get("file_suffix"), root, sample_info.get("fastq_end1"),
                       sample_info.get("fastq_end2"), s3_input_address,
                       sample_info.get("s3_output_address"), log, sample_info.get("is_zipped"))

    # run multiqc
    if "multiqc" in analysis_steps:
        for sample in sample_list:
            sample_info = get_sample_info(sample)
            print("SAMPLE INFO: ")
            print(sample_info)
            print("project name: " + project_name)
            run_multiqc(project_name, root, s3_input_address,
                       sample_info.get("s3_output_address"), log, multiqc_file_list)


# process samples
def get_sample_info(sample):
    files = sample.get("filename")
    # set file suffix
    file_suffix = ".fastq"
    if files.find(".fq") > -1:
        file_suffix = ".fq"
    # check if the file is zipped
    is_zipped = "False"
    if files.find(".gz") > -1:
        is_zipped = "True"

    # get forward and reverse end names without suffix
    # fastq_end1 is the forward reads, fastq_end2 is the reverse reads
    file_list = [x.strip() for x in files.split(',')]
    if len(file_list) < 2:
        fastq_end1 = file_list[0][:file_list[0].find(file_suffix)]
        fastq_end2 = "NULL"
    else:
        fastq_end1 = file_list[0][:file_list[0].find(file_suffix)]
        fastq_end2 = file_list[1][:file_list[1].find(file_suffix)]

    # get output address
    s3_output_address = sample.get("download")

    sample_info = {'file_suffix': file_suffix, 'fastq_end1': fastq_end1, 'fastq_end2': fastq_end2,
                   's3_output_address': s3_output_address, 'is_zipped': is_zipped}

    return sample_info


# run fastqc
# TODO: parallel process fastq?
def run_fastqc(project_name, file_suffix, root_dir, fastq_end1, fastq_end2, s3_input_address, s3_output_address,
               log_dir, is_zipped):

    print("running fastqc...")
    print(project_name, isinstance(log_dir, str))
    print(file_suffix, isinstance(file_suffix, str))
    print(root_dir, isinstance(root_dir, str))
    print(fastq_end1, isinstance(fastq_end1, str))
    print(fastq_end2, isinstance(fastq_end2, str))
    print(s3_input_address, isinstance(s3_input_address, str))
    print(s3_output_address, isinstance(s3_output_address, str))
    print(log_dir, isinstance(log_dir, str))
    print(is_zipped, isinstance(is_zipped, str))

    subprocess.call(['qsub', "-o", "/dev/null", "-e", "/dev/null", scripts + 'fastqc.sh',
                    project_name, file_suffix, root_dir, fastq_end1, fastq_end2, s3_input_address, s3_output_address,
                    log_dir, is_zipped])

    PBSTracker.trackPBSQueue(1, "fastqc")


# run multiqc
# TODO: check how well *args works out
def run_multiqc(project_name, root_dir, s3_input_address, s3_output_address, log_dir, *multiqc_files):
    print("running multiqc")
    print(project_name, isinstance(log_dir, str))
    print(root_dir, isinstance(root_dir, str))
    print(s3_input_address, isinstance(s3_input_address, str))
    print(s3_output_address, isinstance(s3_output_address, str))
    print(log_dir, isinstance(log_dir, str))
    print(*multiqc_file_list)

    subprocess.call(['qsub', "-o", "/dev/null", "-e", "/dev/null", scripts + "multiqc.sh",
                    project_name, root_dir, s3_input_address, s3_output_address, log_dir, *multiqc_files])

    PBSTracker.trackPBSQueue(1, "multiqc")


if __name__ == "__main__":
    run_analysis(sys.argv[1])