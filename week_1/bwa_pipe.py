import subprocess
import os
from collections import defaultdict

source_folder = "/home/andrei/Downloads/challenge2"
reference_genome = os.path.join(source_folder, 'ecoli.fa')

# align fastq files to the reference genome
for file_name in os.listdir(source_folder):
    if file_name[-3:] == '.fq':
        print file_name

        command = "bwa aln %s %s > %s.sai" % (reference_genome,
                                              os.path.join(source_folder, file_name),
                                              os.path.join(source_folder, file_name[:-3]))

        print command
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()
        print out, err


# create pairs of reads for paired-end reads
pairs_list = defaultdict(list)

for file_name in os.listdir(source_folder):
    if file_name[-4:] == '.sai':
        print file_name
        pairs_list[file_name.split('.')[0]].append(os.path.join(source_folder, file_name))

# generate sam files
for title, sai_file_pair in pairs_list.iteritems():
    sai_file_pair = sorted(sai_file_pair)

    payload = (reference_genome, sai_file_pair[0], sai_file_pair[1],
               sai_file_pair[0][:-4] + '.fq', sai_file_pair[1][:-4] + '.fq',
               os.path.join(source_folder, title + '.sam'))

    command = "bwa sampe %s %s %s %s %s > %s" % payload

    print command

    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()
    print out, err