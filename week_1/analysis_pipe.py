from csv import reader
import numpy as np
import seaborn as sns
import pandas as pd

with open('expression.txt', 'r') as source:
    read_generator = reader(source, delimiter='\t')
    header = read_generator.next()
    table = []
    for line in read_generator:
        table.append(line)
    np_array = np.array(table)

    gene_titles = np_array[:, 0].tolist()
    data = np_array[:, 1:].astype(np.float32)

    # print header
    # print gene_titles
    # print data

    dataframe = pd.DataFrame(data=data, index=gene_titles, columns=header[1:])
    sns.heatmap(dataframe)
    sns.plt.show()
    sns.clustermap(dataframe)
    sns.plt.show()
    sns.clustermap(dataframe, col_cluster=False)
    sns.plt.show()