import subprocess
import os

source_folder = "/home/andrei/Downloads/challenge2"
reference_genome = os.path.join(source_folder, 'ecoli.fa')

# convert sam files to bam files
for file_name in os.listdir(source_folder):
    if file_name[-4:] == '.sam':
        print file_name

        command = "samtools view -b -S -o %s.bam %s" % (os.path.join(source_folder, file_name[:-4]),
                                                        os.path.join(source_folder, file_name))

        print command
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()
        print out, err

# sort and index alignements
for file_name in os.listdir(source_folder):
    if file_name[-4:] == '.bam':
        print file_name

        command = "samtools sort -o %s.sorted.bam %s " % (
                                            os.path.join(source_folder, file_name[:-4]),
                                            os.path.join(source_folder, file_name))

        print command
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()

        print out, err

        command2 = "samtools index %s.sorted.bam %s.sorted.bai" % (
                   os.path.join(source_folder, file_name[:-4]),
                   os.path.join(source_folder, file_name[:-4]))

        print command2
        p = subprocess.Popen(command2,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()

        print out, err

# perform the pileup
for file_name in os.listdir(source_folder):
    if file_name[-11:] == '.sorted.bam':
        print file_name

        prefix = os.path.join(source_folder, file_name[:-11])
        command = "samtools mpileup -v -u -f %s %s.sorted.bam > %s.vcf" % (reference_genome,
                                                                 prefix, prefix)

        print command
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()

        print out, err