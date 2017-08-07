#Erica Barnell
#6.7.2017
#!/usr/bin/env python3



import json, requests
import sys


#python3 UTR.py UTRs_all_transcripts.txt

final_list = []


file = open(sys.argv[1], 'r')
file = file.readlines()[1:]
for line in file:
    line = line.strip('\n')
    line = line.split('\t')
    chr = line[4]
    start = int(line[5])
    stop = int(line[6])
    if line[0] and line[1] is None:
        continue

    elif line[0] == line[5] and start > stop:
        start = int(line[1]) - 1
    elif line[0] == line[5] and start < stop:
        start = int(line[1]) + 1

    elif line[0] == line[6] and start > stop:
        stop = int(line[1]) - 1
    elif line[0] == line[6] and start < stop:
        stop = int(line[1]) + 1

    elif line[1] == line[5] and start < stop:
        start = int(line[0]) - 1
    elif line[1] == line[5] and start > stop:
        start = int(line[0]) + 1

    elif line[1] == line[6] and start > stop:
        stop = int(line[0]) - 1

    elif line[1] == line[6] and start < stop:
        stop = int(line[0]) + 1

    elif line[2] == line[5] and start > stop:
        start = int(line[3]) - 1
    elif line[2] == line[5] and start < stop:
        start = int(line[3]) + 1

    elif line[2] == line[6] and start > stop:
        stop = int(line[3]) - 1
    elif line[2] == line[6] and start < stop:
        stop = int(line[3]) + 1

    elif line[3] == line[5] and start > stop:
        start = int(line[2]) - 1
    elif line[3] == line[5] and start < stop:
        start = int(line[2]) + 1

    elif line[3] == line[6] and start > stop:
        stop = int(line[2]) - 1
    elif line[3] == line[6] and start < stop:
        stop = int(line[2]) + 1

    final_list.append([chr, start, stop])

no_UTRs = open('all_exons_merged_no_UTRs.bed', 'w')  # create empy file for nanostring coordinates
for item in final_list:  # iterate through nanostring list
    for k in item:
        no_UTRs.write(str(k) + '\t')
    no_UTRs.write('\n')
no_UTRs.close()  # close file
