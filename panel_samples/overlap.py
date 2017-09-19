#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

"""


Usage: python3 Probe_Selection.py <Threshold> <panel_genes> <tile_classification>

Example 38: python3 overlap.py coordinates_merge_38.txt Pembrolizumab_MASTER_MAF.tsv

Example 37: python3 overlap.py coordinates_merge_37.txt samples_from_ben.tsv 



1) <civic_gene_panel> = 
2) <sample_panel> = as many samples as you wish to test

"""

import sys

def append_file_to_list(file):
    list = []
    f = open(file, 'r')
    for line in f:
        line = line.strip('\n')
        line = line.split('\t')
        list.append(line)
    return list

civic_coordinates = append_file_to_list(sys.argv[1])

sample1 = append_file_to_list(sys.argv[2])

mutation_overlap = {}
count = 0
header = sample1[0]
sample = header.index('sample')
gene = header.index('gene_name')
VAF = header.index('VAF')
variant = header.index('amino_acid')

for item in sample1:
    for exon in civic_coordinates:
        if str(item[0]) == str(exon[0]) and int(item[1]) >= int(exon[1]) and int(item[2]) <= int(exon[2]): #and item[40] == 'tumor':
            count += 1
            if item[sample] not in mutation_overlap:
                mutation_overlap[item[sample]] = [0]
                mutation_overlap[item[sample]][0] += 1
                mutation_overlap[item[sample]].append(item[gene])
                mutation_overlap[item[sample]].append(item[variant])
                mutation_overlap[item[sample]].append(item[VAF])

            else:
                mutation_overlap[item[sample]][0] += 1
                mutation_overlap[item[sample]].append(item[gene])
                mutation_overlap[item[sample]].append(item[variant])
                mutation_overlap[item[sample]].append(item[VAF])

for k,v in mutation_overlap.items():
    print(k, v)

print('Total number of overlaps:', count)
print('Total number of exons in CIViC', len(civic_coordinates))
print('Total number of mutations in all samples', len(sample1))