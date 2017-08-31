#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

import sys

bed = open(sys.argv[1], 'r')
bed_list = []
count = 0
for line in bed:
    line = line.strip('\n')
    line = line.split('\t')
    chr = line[0]
    start = line[1]
    stop = line[2]
    diff = abs(int(start) - int(stop))
    bed_list.append([chr,start,stop])
    if diff < 360:
        count += 1
    #if diff > 360:
        #count += (round(int((diff - 360)/120)) + 2)
print(count)