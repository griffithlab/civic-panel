#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

"""
Information: Probe_Selection.py will pull existing variants from the CIViC Knowledgebase, iterate through all pulled 
variants, and score the variant based on the accepted evidence items. This CIViC Score is calculated by adding the 
Evidence Scores for all accepted Evidence Statements associated with that variant. The Evidence Score is calculated by 
multiplying the Trust Rating by the Evidence Level. The threshold will provide the lower limite required for a variant 
to be considered extensively curated and therefore eligible for probe design.


Usage: Probe_Selection.py <Threshold> <Sequence Ontology Terms> <panel_genes>

1) <Threshold> = CIViC Score required for Variant
2) <Sequence Ontology Terms> = this input requires a .tsv file to determine the appropriate sequence platoform for
 analysis. The 'sequence_ontology_labels.tsv' is a file within the repo that contains SO_IDs that have been manually
evaluated for platform analysis. Each SO_ID is followed by either a "YES" or a "NO" indicating which platform will be 
used for variant evaluation.
3) <panel_genes> = this input is a .txt file that contains genes within existing gene panels


Output: There are two forms of output, statistics on the capture panel and output files for probe design. The statistics
output will show the following:
1) Total Number of Eligible Variants based on the <Threshold> input
2) Total Number of Eligible Genes based on the <Threshold> input
3) Number of genes in at least 10-panels that have been previosuly described based on the <panel_genes> input
4) Number of missing variants in civic based on the <Threshold> input and the <panel_genes> input

There will also be two output files for probe design. Specifically, two bed files will be created to detail the
coordinates for the eligible variants based on the <Threshold> input. Each list will contain four columns.  
These columns will be "name" "chromosome" "start" "stop". The files will be named the following:

1) nanoString_probes: Probes that will need to be evaluated using NanoString Technology
2) capture_sequence_probes: Probes that will need to be evaluated using Capture-Sequencing Technology

WARNING INDICATORS:
- If there are eligible variants whereby the SO_ID is not on the SO_ID input file you will receive an output
list of all SOIDs that need to be manually evalulated for NanoString or Capture Sequencing Analysis

"""

##TOOLS
#!/usr/bin/env python3
import json, requests
import sys

##Pull in Data from JSON
variant_list = [] #Create a Variant Dictionary for Eligible Variants
variants = requests.get('https://civic.genome.wustl.edu/api/panels/captureseq/qualifying_variants?minimum_score=' +
                        sys.argv[1]).json()['records'] #Call eligible variants

##Pull in sequence ontology labels
sequence_ontology_dictionary = {}
file = open(sys.argv[2], 'r')
for line in file:
    row = line.strip('\n')
    row = row.split('\t')
    soid = row[1]
    capture = row[4]
    nanostring = row[5]
    sequence_ontology_dictionary[soid] = [capture, nanostring]

##Use API to determine the total number of eligible variants and the total number of eligible genes
count = 0 #Start count to determine the total number of eligible variants
for k in range(0, len(variants)): #iterate through API and pull all eligible variants
    if variants[k]['entrez_name'] not in variant_list: #If the gene is not in the list already
        variant_list.append(variants[k]['entrez_name']) #add to the list
    count += 1 #Count all of the eligible variants
print('Total Number of Eligible Variants: ', count) #Print out all variants
print('Total Number of Eligible Genes: ', len(variant_list)) #Print out all Genes

##See how many genes are in panels but not eligible for CIViC
panel_genes = open(sys.argv[3], 'r') #open panel_genes
panel_genes_list = [] #create empty file for panel genes
for line in panel_genes: #iterate through panel genes
    line = line.strip('\n') #strip the new line
    line = line.split('\t') #split by tabs
    gene = line[0] #pull gene
    panel_genes_list.append(gene) #append to gene list

not_in_CIViC = [] #create empty list for genes that are not extensively curated
for item in panel_genes_list: #for item in panel list
    if item not in variant_list: #if the item is not in the civic list
        not_in_CIViC.append(item) #append it to the not in civic list
print('Number of genes in at Least 10 Panels is:', len(panel_genes_list)) #print the length of the panel Genes
print('Number of Genes Missing from CIViC is:', len(not_in_CIViC)) #print number of genes not in civic


##Use API to pull information for probe design

unlabeled_SOIDs = [] #Create Bucket for SO_IDs that have not been labeled yet


#Create a dictionary with the .bed information for the two analysis platforms
bed_information = {}
for k in range(0, len(variants)): #iterate through API and pull all eligible variants
    gene = variants[k]['entrez_name']  #Call Gene name
    soid = variants[k]['variant_types'][0]['so_id'] #call soid
    chrom = variants[k]['coordinates']['chromosome'] #call chrom
    start = variants[k]['coordinates']['start'] #call start
    stop = variants[k]['coordinates']['stop'] #call stop
    if soid not in sequence_ontology_dictionary.keys(): #if the soid is not in the soid dictionary
        unlabeled_SOIDs.append(soid) #put it in the unlabeled soid list for the soid warning
        capture = 'no' #set capture to no
        nanostring = 'no' #set nanostring to no
    if soid in sequence_ontology_dictionary.keys(): #if the soid is in the seqontology dictionary
        capture = sequence_ontology_dictionary[soid][0] #set the capture status to the first value in the dict
        nanostring = sequence_ontology_dictionary[soid][1] #set the nanostring status to the second value in the dictionary
    if variants[k]['coordinates']['chromosome2'] is not None and variants[k]['coordinates']['start2'] is not None and variants[k]['coordinates']['stop2'] is not None: #if there are two chromosomes for the variant
        chrom2 = variants[k]['coordinates']['chromosome2'] #call chrom2
        start2 = variants[k]['coordinates']['start2'] #call start2
        stop2 = variants[k]['coordinates']['stop2'] #call stop2
        if soid in bed_information: #is SOID is already in the bed dictionary
            bed_information[soid].append([capture, nanostring, gene, chrom, start, stop, chrom2, start2, stop2]) #append new list with bed information
        if soid not in bed_information: #if the SOID is not in the bed dictionary
            bed_information[soid] = [] #create a new blank list
            bed_information[soid].append([capture, nanostring, gene, chrom, start, stop, chrom2, start2, stop2]) #append new list with bed informaiton
    else: #if there is only 1 chromosome for the variant
        if soid in bed_information: #if the SOID is not in the bed dictionary
            bed_information[soid].append([capture, nanostring, gene, chrom, start, stop]) #append new list with bed information
        if soid not in bed_information: #if the SOID is not in the bed dictionary
            bed_information[soid] = [] #create a new blank list
            bed_information[soid].append([capture, nanostring, gene, chrom, start, stop]) #append new list with bed information

nanoString_probes = [] #create empty list for nanostring probes
capture_sequence_probes = [] #create empty list for capture sequence probes

for k,v in bed_information.items(): #iterate through the bed information dictonary
    for item in v: #for each list in the dictionary's values
        if item[0] == 'Yes': #if the capture label is yes
            if len(item) == 6: #if there is only one chrom, start, stop
                capture_sequence_probes.append([item[2], item[3], item[4], item[5]]) #append informaiton to the capture list
            if len(item) == 9: #if there are two chroms, starts, stops
                capture_sequence_probes.append([item[2], item[3], item[4], item[5], item[6], item[7], item[8]]) #append informaiton to the capture list
        if item[1] == 'Yes': #if the nanostring label is yes
            if len(item) == 6: #if there is only one chrom, start, stop
                nanoString_probes.append([item[2], item[3], item[4], item[5]]) #append information to the nanostring list
            if len(item) == 9: #if there are two chroms, starts, stops
                nanoString_probes.append([item[2], item[3], item[4], item[5], item[6], item[7], item[8]]) #append information to the nanostring list

##Output files
nanostring = open('nanoString_probes.tsv', 'w')  #create empy file for nanostring coordinates
nanostring.write('gene' + '\t' + 'chromosome' + '\t' + 'start' + '\t' + 'stop' + '\t' + 'chrosome2' + '\t' + 'start2' + '\t' + 'stop2' + '\n') #write header
for item in nanoString_probes: #iterate through nanostring list
    if len(item) == 4: #if they have one set of coordinates
        nanostring.write(str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\n') #add to the file
    if len(item) == 7: #if they have two sets of coordinates
        nanostring.write(str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\t' + str(item[4]) + '\t' + str(item[5]) + '\t' + str(item[6]) + '\n') #add to file
nanostring.close() #close file


capture = open('capture_sequence_probes.tsv', 'w') #create empy file for capture sequence coordinates
capture.write('gene' + '\t' + 'chromosome' + '\t' + 'start' + '\t' + 'stop' + '\t' + 'chrosome2' + '\t' + 'start2' + '\t' + 'stop2' + '\n') #write header
for item in capture_sequence_probes: #iterate through capture list
    if len(item) == 4: #if they have one set of coordinates
        capture.write(str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\n') #add to the file
    if len(item) == 7: #if they have two sets of coordinates
        capture.write(str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\t' + str(item[4]) + '\t' + str(item[5]) + '\t' + str(item[6]) + '\n') #add to the file
capture.close() #close file

#CREATE WARNING FOR UNLABELED SOIDs
if len(unlabeled_SOIDs) != 0: #if the length of the unlabeled_SOID list is not empty
    print('WARNING: the following SO_IDs have not been entered into ' + sys.argv[2]) #state that we are missing annotation for at least 1 SOID
    for i in unlabeled_SOIDs: #iterate through the list
        print(i) #print out the sequence ontology IDs that we need to manually add to the .tsv file


