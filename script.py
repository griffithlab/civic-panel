#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

import sys

final_list = []

file = open(sys.argv[1], 'r')
for line in file:
    line = line.strip('\n')
    line = line.split('.')
    final_list.append(line[0])

end = open('ENST_representative_transcripts', 'w')  # create empy file for nanostring coordinates
for item in final_list:  # iterate through nanostring list
    end.write(item + '\n')
end.close()  # close file
