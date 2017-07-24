#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

"""
Information: Probe_Selection.py will pull existing variants from the CIViC Knowledgebase, iterate through all pulled 
variants, and score the variant based on the accepted evidence items. This CIViC Score is calculated by adding the 
Evidence Scores for all accepted Evidence Statements associated with that variant. The Evidence Score is calculated by 
multiplying the Trust Rating by the Evidence Level. The threshold will provide the lower limite required for a variant 
to be considered extensively curated and therefore eligible for probe design.


Usage: Probe_Selection.py <Threshold> <panel_genes>

1) <Threshold> = CIViC Score required for Variant
2) <panel_genes> = this input is a .txt file that contains genes within existing gene panels


Output: There are two forms of output, statistics on the capture panel and output files for probe design. The statistics
output will show the following:
1) Total Number of Eligible Variants based on the <Threshold> input
2) Total Number of Eligible Genes based on the <Threshold> input
3) Number of genes in at least 10-panels that have been previosuly described based on the <panel_genes> input
4) Number of missing variants in civic based on the <Threshold> input and the <panel_genes> input
5) List of genes missing in CIViC that are in 10 gene panels
6) Number of genes in CIViC but not on 10 gene panels
7) List of genes in CIViC but are not on 10 gene panels
8) Number of genes that do not have a Vriant Type (SO_id)
9) SO_id Numbers and names that need the be analyzed for either NanoString or CaptureSeq Platforms

There will also be two output files for probe design. Specifically, two bed files will be created to detail the
coordinates for the eligible variants based on the <Threshold> input. Each list will contain four columns.  
These columns will be "name" "chromosome" "start" "stop". The files will be named the following:

1) nanoString_probes: Probes that will need to be evaluated using NanoString Technology
2) capture_sequence_probes: Probes that will need to be evaluated using Capture-Sequencing Technology


"""

##TOOLS
#!/usr/bin/env python3
import json, requests
import sys

##Pull in Data from JSON
variant_list = [] #Create a Variant Dictionary for Eligible Variants
variants_nanostring = requests.get('https://civic.genome.wustl.edu/api/panels/nanostring/qualifying_variants?minimum_score=' +
                        sys.argv[1]).json()['records'] #Call eligible variants

variants_capture = requests.get('https://civic.genome.wustl.edu/api/panels/captureseq/qualifying_variants?minimum_score=' +
                        sys.argv[1]).json()['records'] #Call eligible variants

##Use API to determine the total number of eligible variants and the total number of eligible genes
count = 0 #Start count to determine the total number of eligible variants
for k in range(0, len(variants_nanostring)): #iterate through API and pull all eligible variants
    if variants_nanostring[k]['entrez_name'] not in variant_list: #If the gene is not in the list already
        variant_list.append(variants_nanostring[k]['entrez_name']) #add to the list
    count += 1 #Count all of the eligible variants
for k in range(0, len(variants_capture)): #iterate through API and pull all eligible variants
    if variants_capture[k]['entrez_name'] not in variant_list: #If the gene is not in the list already
        variant_list.append(variants_capture[k]['entrez_name']) #add to the list
    count += 1 #Count all of the eligible variants
print('Total Number of Eligible Variants: ', count) #Print out all variants
print('Total Number of Eligible Genes: ', len(variant_list)) #Print out all Genes
print()

##See how many genes are in panels but not eligible for CIViC
panel_genes = open(sys.argv[2], 'r') #open panel_genes
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
print('List of Genes missing from CIViC ', not_in_CIViC)
print()

#See how many genes are in CIViC but are not on the 10 panel list
civic_only = []
for item in variant_list:
    if item not in panel_genes_list:
        if item not in civic_only:
            civic_only.append(item)

print('Number of genes in CIViC but not in 10 gene Panels is: ', len(civic_only))
print('Genes in CIViC but not in 10 panels: ', civic_only)
print()

#############################
## Check Sequence Ontoloty ##
#############################
#Make sure that all variants have SOIDs and that all SOIDs that are currently in CIViC have deignated platforms for analysis

#Pull SOIDs from API Interface (Capture Seq)
SOID_labels = requests.get('https://civic.genome.wustl.edu/api/panels?count=1000000').json()['CaptureSeq']['sequence_ontology_terms']
SOID = {} #Create new dictionary to hold SOIDs in API
#Iterate through the API interface
for item in SOID_labels:
    if item['soid'] not in SOID: #Pull the SOIDs
        SOID[item['soid']] = [] #create new list if it is not already in SOID dictioanry
        SOID[item['soid']].append(item['name']) #Add to dictionary
    if item['soid'] in SOID: #if it is already there
        continue #move onto the next

#Pull SOIDs from API Interface (Nanostring)
SOID_labels = requests.get('https://civic.genome.wustl.edu/api/panels?count=1000000').json()['NanoString']['sequence_ontology_terms']
for item in SOID_labels:#iterate through the variants
    if item['soid'] not in SOID: #If the soid is not already in the
        SOID[item['soid']] = [] #create holder
        SOID[item['soid']].append(item['name']) #add to the list
    if item['soid'] in SOID: #If it is already there
        continue #move onto the next

CIViC_SOID = [] #Create new list for all of the SOIDs that are in CIViC
no_SOID_in_CIViC = [] #Create new list for all of the variants that do not have a SOID term attached to it

#Pull all of the variants from the CIViC API
SOID_API = requests.get('https://civic.genome.wustl.edu/api/variants?count=1000000').json()['records']
for item in SOID_API: #iterate through the API
    if item['variant_types'] != []: #If the variant_type is there
        if item['variant_types'][0]['so_id'] not in CIViC_SOID: #and the soid is not in the CIViC SOID list
            CIViC_SOID.append(item['variant_types'][0]['so_id']) #add it to the list
    if item['variant_types'] == []: #If the variant type has not been created yet
        if item['entrez_name'] not in no_SOID_in_CIViC: #and the gene name has not already been evaluated
            no_SOID_in_CIViC.append(item['entrez_name']) #Add the gene name to the 'not in civic' list

print()
print('Number of genes without Variant Type (SO_id):', len(no_SOID_in_CIViC)) #Print the number of genes that need a variant type :(
print()

print('The Following SO_ids need to be added to the API') #Header
for k,v in SOID.items(): #Iterate through the soids from civic and nanotring
    if k not in CIViC_SOID: #if there is an SOID that is in CIVic but it is not in the SOID API
        print(k, v) #print out the soid number and name (NEED TO ADD THESE TO CIVIC)


##########################
## Evaluate Capture API ##
##########################
## For variants listed in the CaptureSeq API, create bed-like files for capture design

capture_sequence_probes = [] #create empty list for capture sequence probes

#Create a dictionary with the .bed information for the two analysis platforms
bed_information = {}
for k in range(0, len(variants_capture)): #iterate through API and pull all eligible variants
    gene = variants_capture[k]['entrez_name']  #Call Gene name
    soid = variants_capture[k]['variant_types'][0]['so_id'] #call soid
    chrom = variants_capture[k]['coordinates']['chromosome'] #call chrom
    start = variants_capture[k]['coordinates']['start'] #call start
    stop = variants_capture[k]['coordinates']['stop'] #call stop
    if variants_capture[k]['coordinates']['chromosome2'] is not None and variants_capture[k]['coordinates']['start2'] is not None and variants_capture[k]['coordinates']['stop2'] is not None: #if there are two chromosomes for the variant
        chrom2 = variants_capture[k]['coordinates']['chromosome2'] #call chrom2
        start2 = variants_capture[k]['coordinates']['start2'] #call start2
        stop2 = variants_capture[k]['coordinates']['stop2'] #call stop2
        capture_sequence_probes.append([gene, chrom, start, stop, chrom2, start2, stop2]) #append new list with bed informaiton
    else: #if there is only 1 chromosome for the variant
        capture_sequence_probes.append([gene, chrom, start, stop]) #append new list with bed information


#############################
## Evaluate NanoString API ##
#############################
## For variants listed in the NanoString API, create bed-like files for capture design

nanoString_probes = []  # create empty list for nanostring probes

for k in range(0, len(variants_nanostring)):  # iterate through API and pull all eligible variants
    gene = variants_nanostring[k]['entrez_name']  # Call Gene name
    soid = variants_nanostring[k]['variant_types'][0]['so_id']  # call soid
    chrom = variants_nanostring[k]['coordinates']['chromosome']  # call chrom
    start = variants_nanostring[k]['coordinates']['start']  # call start
    stop = variants_nanostring[k]['coordinates']['stop']  # call stop
    if variants_nanostring[k]['coordinates']['chromosome2'] is not None and variants_nanostring[k]['coordinates']['start2'] is not None and variants_nanostring[k]['coordinates']['stop2'] is not None:  # if there are two chromosomes for the variant
        chrom2 = variants_nanostring[k]['coordinates']['chromosome2']  # call chrom2
        start2 = variants_nanostring[k]['coordinates']['start2']  # call start2
        stop2 = variants_nanostring[k]['coordinates']['stop2']  # call stop2
        nanoString_probes.append([gene, chrom, start, stop, chrom2, start2, stop2])  # append new list with bed information
    else:  # if there is only 1 chromosome for the variant
        nanoString_probes.append([gene, chrom, start, stop])  # append new list with bed information

###########################
## Generate Output files ##
###########################

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



