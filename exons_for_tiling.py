#Erica Barnell
#6.7.2017
#!/usr/bin/env python3


"""
This python code takes in a list of genes and the coordinates for all transcripts and creates a text file with chr, start
stop, gene_name for all exons.

Usage: exons_for_tiling.py <genes_to_be_tiled> <bed file with transcripts>

<genes_to_be_tiled> = list of gene names (HUGO) that need to be tiled
<bed file with transcripts> = UCSC_exons_modif_canonical.bed for canonical transcripts or other for full tile

"""


##TOOLS
#!/usr/bin/env python3
import json, requests
import sys

#Create an empty list for all of the imported transcript coordinates
coordinates = []

#iterate through the coordinates and pull chr, start, stop, name
transcripts = open(sys.argv[2], 'r')
for line in transcripts:
    line = line.strip('\n')
    line = line.split('\t')
    coordinates.append([line[0], line[1], line[2], line[3]])

#create an empty list of all the genes that need to be tiled
genes_list = []
#iterate through gene list and add gene names to the list
genes = open(sys.argv[1], 'r')
for item in genes:
    item = item.strip('\n')
    genes_list.append(item)

#create an empty list for the final coordinates for the genes that need to be tiled
exons = []
#link both spreadsheets by name and append coordinates to the exons
for item in genes_list:
    for k in coordinates:
        if item == k[3]:
            exons.append(k)

#create output file for the exon coordinates for all genes that need to be tiled
final = open('exons_coordinates.txt', 'w')
for item in exons: #iterate through nanostring list
    for k in item:
        final.write(str(k) + '\t')
    final.write('\n')
final.close()