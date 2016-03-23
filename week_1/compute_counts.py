import numpy as np
import os
from csv import reader
from pickle import dump
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

source_folder = "/home/andrei/Downloads/challenge2"
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

# print genes_stack.shape


def pull_depth_from_vcf(file_name):
    stack = []

    with open(os.path.join(source_folder, file_name)) as current_file:
        line_iterator = reader(current_file, delimiter='\t')
        for line in line_iterator:
            if line[0][0] != "#":
                # print line
                if 'DP' in line[7].split(';')[0]:
                    stack.append([int(line[1]), int(line[7].split(';')[0].split('=')[1])])
                    # print line[1], line[7].split(';')[0].split('=')[1]

    stack = np.array(stack)
    sort_arr = np.argsort(stack[:, 0])
    stack = stack[sort_arr]
    # print stack.shape
    return stack


def pull_average_depth_for_genes(stack):
    stack_of_depths = []

    for item in genes_stack.tolist():
        stack_content = stack[np.logical_and(stack[:, 0] > int(item[0]), stack[:, 0] < int(item[1])),
                             :][:, 1]
        # plt.plot(stack_content)
        # plt.show()
        if int(item[2]) > 60:
            stack_of_depths.append([item[3], np.nanmean(stack_content[70:-70])])
        else:
            # plt.plot(stack_content)
            # plt.show()
            print 'unable to analyze:', item[3], item[2],\
                item[0], item[1], np.nanmean(stack_content)
            # print stack_content

    return stack_of_depths


def master_loop():
    gene_names = []
    master_store = []
    time_stamps = []
    dump_dict = {}
    for file_name in os.listdir(source_folder):
        if file_name[-4:] == '.vcf':
            print file_name
            master_mix = np.array(pull_average_depth_for_genes(pull_depth_from_vcf(file_name)))
            time_stamps.append(file_name[:-4])
            gene_names = master_mix[:, 0]
            master_store.append(master_mix[:, 1])
            dump_dict[file_name[:-4]] = [master_mix]

    print dump_dict
    dump(dump_dict, open('my_pipe.dmp', 'w'))
    arg_sorter = np.argsort(np.array([int(val[1:]) for val in time_stamps]))
    time_stamps = np.array(time_stamps)[arg_sorter]
    print time_stamps
    master_store = np.array(master_store)
    master_store = master_store[arg_sorter, :].astype(np.float32)
    master_store[np.isnan(master_store)] = 0
    print master_store
    dataframe = pd.DataFrame(data=master_store.T, index=gene_names, columns=time_stamps)
    sns.heatmap(dataframe)
    sns.plt.show()
    sns.clustermap(dataframe)
    sns.plt.show()
    sns.clustermap(dataframe, col_cluster=False)
    sns.plt.show()



if __name__ == "__main__":
    master_loop()
    # print pull_average_depth_for_genes(pull_depth_from_vcf('t1.vcf'))