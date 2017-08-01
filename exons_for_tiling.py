#Erica Barnell
#6.7.2017
#!/usr/bin/env python3


"""
This python code takes in a list of genes and the coordinates for all transcripts and creates a text file with chr, start
stop, gene_name for all exons.

Usage: exons_for_tiling.py <genes_to_be_tiled>

python3 exons_for_tiling.py genes_to_be_tiled.txt

Input Files:
<genes_to_be_tiled> = list of gene names (ENST) that need to be tiled

Output Files:
<list of exons> = coordinates for all exons in your gene list called  exons_coordinates.txt

"""


##TOOLS
#!/usr/bin/env python3
import json, requests
import sys

#create an empty list of all the genes that need to be tiled
genes_list = []
#iterate through gene list and add gene names to the list
genes = open(sys.argv[1], 'r')
for item in genes:
    item = item.strip('\n')
    item = item.split('.')
    if item[0] not in genes_list:
        genes_list.append(item[0])

#create output file for the exon coordinates for all genes that need to be tiled
final = open('ENST_to_be_tiled', 'w')
for item in genes_list: #iterate through nanostring list
    final.write(str(item) + '\t')
    final.write('\n')
final.close()