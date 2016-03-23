import numpy as np
import os
from csv import reader, writer

source_folder = "/home/andrei/Downloads/challenge2"
reference_ppt = os.path.join(source_folder, 'refgenes.ptt')
destination_gff = os.path.join(source_folder, 'refgenes.gff')


with open(reference_ppt) as ptt, open(destination_gff, 'w') as gff:
    line_iterator = reader(ptt, delimiter='\t')
    gff_writer = writer(gff, delimiter='\t')
    for line in line_iterator:
        start, stop = line[0].split('..')
        strand = line[1]
        hid = line[4]
        gff_writer.writerow(['X', '.', 'Gene', start, stop, '.', strand, '.', "hid=%s"%hid])
