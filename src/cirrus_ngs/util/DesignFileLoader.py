__author__ = 'Guorong Xu<g1xu@ucsd.edu>'

import re

## load design file
def load_design_file(design_file):
    sample_list = []
    group_list = []
    normal_samples = {}
    tumor_samples = {}
    
    with open(design_file, 'r+') as f:
        for line in f:
            if not line.startswith("##"):
                fields = line.split("\t")
                if not len(fields) >= 2:
                    raise IndexError("""Design file lines must follow format
<sample_name><OPTIONAL sample_name_reverse_reads><TAB><group_name>.
No tabs were found in line:\n\t\"{}\" """.format(line.strip()))

                if fields[0].find(",") > -1:
                    sample_pair = fields[0].split(",")
                    paired_samples_1 = sample_pair[0]
                    paired_samples_2 = sample_pair[1]
                    sample_list.append([paired_samples_1, paired_samples_2])
                else:
                    sample_list.append([fields[0]])
                group_list.append(fields[1].rstrip())

                if len(fields) == 3:
                    fields[2] = fields[2].rstrip()
                    if fields[2] == "Normal":
                        normal_samples[group_list[-1]] = sample_list[-1][0].split(".")[0]
                    elif fields[2] == "Tumor":
                        tumor_samples[group_list[-1]] = sample_list[-1][0].split(".")[0]
                    else:
                        raise ValueError("Design file third column must be either \"Normal\" or \"Tumor\". Current value is {}".format(fields[2]))

    pair_list = {normal_samples[x]: tumor_samples[x] for x in normal_samples.keys()}

    print(sample_list)
    print(group_list)
    print(pair_list)
    
    return sample_list, group_list, pair_list


## load chipseq design file
def load_chipseq_design_file(design_file):
    sample_hash = {}
    sample_list = []
    group_list = []
    
    with open(design_file, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("##"):
                continue
            else:
                fields = re.split(r'\t+', line)
                if len(fields) == 1:
                    if fields[0].rstrip() not in sample_hash:
                        sample_hash.update({fields[0].rstrip(): fields[0].rstrip()})
                        sample_list.append(fields[0].rstrip())
                if len(fields) > 1:
                    if fields[0] not in sample_hash:
                        sample_hash.update({fields[0]: fields[0]})
                        sample_list.append(fields[0])
                    if fields[1].rstrip() not in sample_hash:
                        sample_hash.update({fields[1].rstrip(): fields[1].rstrip()})
                        sample_list.append(fields[1].rstrip())
                    group_list.append([fields[0], fields[1].rstrip()])

    return sample_list, group_list
