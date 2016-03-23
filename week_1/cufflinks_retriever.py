import numpy as np
import os
from csv import reader
import subprocess
from pickle import dump
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

source_folder = "/home/andrei/Downloads/challenge2"
reference_genome = os.path.join(source_folder, 'ecoli.fa')
ref_genes = os.path.join(source_folder, 'refgenes.ptt')

genes_stack = []
with open(ref_genes) as current_file:
    line_iterator = reader(current_file, delimiter='\t')
    for line in line_iterator:
        start, stop = line[0].split('..')
        start, stop = sorted([int(start), int(stop)])
        genes_stack.append([start, stop, int(line[2]), line[4]])
        # print line[0].split('..'), int(line[2]), int(line[4])

genes_stack = np.array(genes_stack)
genes_sort_arr = np.argsort(genes_stack[:, 0].astype(np.int64))
genes_stack = genes_stack[genes_sort_arr]


def run_cufflinks():
    data_dict = {}
    for file_name in os.listdir(source_folder):
        if file_name[-11:] == '.sorted.bam':
            command = "cufflinks -b %s %s" % (reference_genome,
                                              os.path.join(source_folder, file_name))

            print command
            p = subprocess.Popen(command,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            out, err = p.communicate()
            print out, err
            data_dict[file_name[:-11]]=match_genes()
    return data_dict


def match_genes():
    match_set = []
    with open(os.path.join(source_folder, 'genes.fpkm_tracking')) as source:
        line_iterator = reader(source, delimiter='\t')
        line_iterator.next()
        for line in line_iterator:
            start, stop = line[6].split(':')[1].split('-')
            start, stop = sorted([int(start), int(stop)])
            fpkm = float(line[9])
            match_set.append([start, stop, fpkm])

    final_set = []
    for start, stop, fpkm in match_set:
        mask = np.logical_and(genes_stack[:, 0].astype(np.int32) <= start,
                              genes_stack[:, 1].astype(np.int32) >= stop)
        if genes_stack[mask].shape[0] != 1:
            # print genes_stack[mask], genes_stack[mask].shape
            # print start, stop
            # print genes_stack[:, 0]
            # print genes_stack[:, 1]
            pass

        else:
            final_set.append([genes_stack[mask][0][-1], fpkm])

    return np.array(final_set)

if __name__ == "__main__":
    final_data_dict = run_cufflinks()
    print final_data_dict
    dump(final_data_dict, open('cufflinks.dmp', 'w'))
