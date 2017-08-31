#Erica Barnell
#6.7.2017
#!/usr/bin/env python3

"""
Information: Probe_Selection.py will pull existing variants from the CIViC Knowledgebase, iterates through all pulled 
variants, and score the variant based on the accepted evidence items. This CIViC Score is calculated by adding the 
Evidence Scores for all accepted Evidence Statements associated with that variant. The Evidence Score is calculated by 
multiplying the Trust Rating by the Evidence Level. The threshold will provide the lower limit required for a variant 
to be considered extensively curated and therefore eligible for probe design. This script will also provide informaiton
on the CIViC Interface relative to other panel genes.


Usage: python3 Probe_Selection.py <Threshold> <panel_genes> <tile_classification>

Example: python3 Probe_Selection.py 20 panel_genes.txt tile_classification.txt

1) <Threshold> = CIViC Score required for Variant
2) <panel_genes> = this input is a .txt file that contains genes within existing gene panels
3) <tile_classificaitons> = this is the manually curated file that dictates if a variant requires tiling

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

There will also be three output files for probe design. Specifically, two bed files will be created to detail the
coordinates for the eligible variants based on the <Threshold> input. Each list will contain four columns.  
These columns will be "name" "chromosome" "start" "stop". The third output file will be a text file that shows if 
there are any new variants that require tile classification curation. The files will be named the following:

1) nanoString_probes: Probes that will need to be evaluated using NanoString Technology
2) capture_sequence_probes: Probes that will need to be evaluated using Capture-Sequencing Technology
3) tile_classification.txt: gene name, variant, tile label, and notes



"""

##TOOLS
#!/usr/bin/env python3
import json
import requests
import sys

##Pull in Data from JSON
variant_list = [] #Create a Variant Dictionary for Eligible Variants

variants_capture = requests.get('https://civic.genome.wustl.edu/api/panels/captureseq/qualifying_variants?minimum_score=' +
                        sys.argv[1]).json()['records'] #Call eligible variants

variants_nanostring = requests.get('https://civic.genome.wustl.edu/api/panels/nanostring/qualifying_variants?minimum_score=' +
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
civic_only = [] #create list for civic only genes
for item in variant_list: #iterate through variant list
    if item not in panel_genes_list: #see if variant not in panel gene list
        if item not in civic_only: #see if it is not in the civic only list
            civic_only.append(item) #if it is not in civic only list add it

#print statements
print('Number of genes in CIViC but not in 10 gene Panels is: ', len(civic_only))
print('Genes in CIViC but not in 10 panels: ', civic_only)
print()

#############################
## Check Sequence Ontology ##
#############################
#Make sure that all variants have SOIDs and that all SOIDs that are currently in CIViC have deignated platforms for analysis

#Pull SOIDs from API Interface (Capture Seq)
SOID_labels = requests.get('https://civic.genome.wustl.edu/api/panels?count=1000000').json()['CaptureSeq']['sequence_ontology_terms'] #pull API
SOID = {} #Create new dictionary to hold SOIDs in API
#Iterate through the API interface
for item in SOID_labels:
    if item['soid'] not in SOID: #Pull the SOIDs
        SOID[item['soid']] = [] #create new list if it is not already in SOID dictioanry
        SOID[item['soid']].append(item['name']) #Add to dictionary

#Pull SOIDs from API Interface (Nanostring)
SOID_labels = requests.get('https://civic.genome.wustl.edu/api/panels?count=1000000').json()['NanoString']['sequence_ontology_terms']
for item in SOID_labels:#iterate through the variants
    if item['soid'] not in SOID: #If the soid is not already in the
        SOID[item['soid']] = [] #create holder
        SOID[item['soid']].append(item['name']) #add to the list

CIViC_SOID = [] #Create new list for all of the SOIDs that are in CIViC
no_SOID_in_CIViC = [] #Create new list for all of the variants that do not have a SOID term attached to it

#Pull all of the variants from the CIViC API
SOID_API = requests.get('https://civic.genome.wustl.edu/api/variants?count=1000000').json()['records']
for item in SOID_API: #iterate through the API
    if item['variant_types'] != []: #If the variant_type is there
        if item['variant_types'][0]['so_id'] not in CIViC_SOID: #and the soid is not in the CIViC SOID list
            CIViC_SOID.append([item['variant_types'][0]['so_id'], item['variant_types'][0]['display_name']]) #add it to the list
    if item['variant_types'] == []: #If the variant type has not been created yet
        if item['entrez_name'] not in no_SOID_in_CIViC: #and the gene name has not already been evaluated
            no_SOID_in_CIViC.append(item['entrez_name']) #Add the gene name to the 'not in civic' list

#print statements
print()
print('Number of genes without Variant Type (SO_id):', len(no_SOID_in_CIViC)) #Print the number of genes that need a variant type :(
print()


#Pull SOIDs from API Interface (Unbinned)
SOID_labels = requests.get('https://civic.genome.wustl.edu/api/panels?count=1000000').json()['unbinned_terms']
if len(SOID_labels) == 0:
    print('There are no SO_ids that need to be added to the API!')
else:
    print('The Following SO_ids need to be added to the API')  # Header
    for item in SOID_labels:#iterate through the variants
        print(item['soid'] + ' - ' + item['name'])

##########################
## Evaluate Capture API ##
##########################
## For variants listed in the CaptureSeq API, create bed-like files for capture design

#make dictionary for evidence types
score = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}

capture_sequence_probes = [] #create empty list for capture sequence probes
capture_sequence_probes.append(['gene', 'so_id', 'variant_type', 'variant_name', 'representative_transcript', 'top_evidence_level', 'diseases', 'evidence_types', 'number_of_evidence_statements', 'evidence_score', 'chrom', 'start', 'stop'])
for k in range(0, len(variants_capture)): #iterate through API and pull all eligible variants
    gene = variants_capture[k]['entrez_name']  #Call Gene name
    variant = variants_capture[k]['name'] #call variant
    soid = variants_capture[k]['variant_types'][0]['so_id'] #call soid
    variant_type = variants_capture[k]['variant_types'][0]['name'] #call variant type
    transcript = variants_capture[k]['coordinates']['representative_transcript'] #call transcript
    evidence = variants_capture[k]['evidence_items'] #pull evidence items
    evidence_statements = len(variants_capture[k]['evidence_items']) #pull number of evidence statements
    chrom = variants_capture[k]['coordinates']['chromosome'] #call chrom
    start = variants_capture[k]['coordinates']['start'] #call start
    stop = variants_capture[k]['coordinates']['stop'] #call stop
    diseases = [] #set list for all of the diseases for this varinat
    evidence_type = [] #set list for evidence types
    evidence_scores = [] #set list for evidence scores
    top_evidences = [] #set list for top evidence level
    for item in evidence: #iterate through the evidence items
        if item['disease']['name'] not in diseases: #see if disease is already there
            if 'Walden' in item['disease']['name']: #Change waldenstroms issues (the A is not accepted by R code)
                if 'Waldenstroms Macroglobulinemia' not in diseases: #check if it is already there
                    diseases.append('Waldenstroms Macroglobulinemia') #if it is not append to diseases
            else: #if its not a weird name
                diseases.append(item['disease']['name']) #append the disease
        if item['evidence_type'] not in evidence_type: #see if the evidence type is already there
            evidence_type.append(item['evidence_type']) #if it is not append it
        trust_rating = int(item['rating'] or 0) #make the trust rating either what is listed or 0
        evidence_level = int(score[item['evidence_level']]) #make the evidence level the value from the score dictionary
        evidence_scores.append(evidence_level * trust_rating) #calculate the Evidence Score
        if item['evidence_level'] != '[]': #find the evidence levels that are not blank
            top_evidences.append(item['evidence_level'].strip()) #add to the list
    #pull the maximum evidence level
    if 'A' in top_evidences:
        top_evidence = 'A'
    elif 'B' in top_evidences:
        top_evidence = 'B'
    elif 'C' in top_evidences:
        top_evidence = 'C'
    elif 'D' in top_evidences:
        top_evidence = 'D'
    else:
        top_evidence = 'E'
    evidence_score = sum(evidence_scores) #sum the evidence scores to get a CIVic Score
    disease = ', '.join(diseases) #format the diseases
    evidence_types = ', '.join(evidence_type) #format the evidence types

    #Append coordinates to the capture_sequence_probes list
    if variants_capture[k]['coordinates']['chromosome2'] is not None and variants_capture[k]['coordinates']['start2'] is not None and variants_capture[k]['coordinates']['stop2'] is not None: #if there are two chromosomes for the variant
        transcript2 = variants_capture[k]['coordinates']['representative_transcript'] #call transcript
        chrom2 = variants_capture[k]['coordinates']['chromosome2'] #call chrom2
        start2 = variants_capture[k]['coordinates']['start2'] #call start2
        stop2 = variants_capture[k]['coordinates']['stop2'] #call stop2
        capture_sequence_probes.append([gene, soid, variant_type, variant, transcript, top_evidence, disease, evidence_types, evidence_statements, evidence_score, chrom, start, stop, transcript2, chrom2, start2, stop2]) #append new list with bed informaiton
    else: #if there is only 1 chromosome for the variant
        capture_sequence_probes.append([gene, soid, variant_type, variant, transcript, top_evidence, disease, evidence_types, evidence_statements, evidence_score, chrom, start, stop]) #append new list with bed information


#############################
## Evaluate NanoString API ##
#############################
## For variants listed in the NanoString API, create bed-like files for capture design

nanoString_probes = []  # create empty list for nanostring probes
nanoString_probes.append(['gene', 'soid', 'variant_type', 'variant_name', 'representative_transcript', 'top_evidence_level', 'diseases','evidence_types','number_of_evidence_statements', 'chrom', 'start', 'stop', 'transcript2', 'chrom2', 'start2', 'stop2'])
for k in range(0, len(variants_nanostring)):  # iterate through API and pull all eligible variants
    gene = variants_nanostring[k]['entrez_name']  #Call Gene name
    variant = variants_nanostring[k]['name'] #call variant
    soid = variants_nanostring[k]['variant_types'][0]['so_id'] #call soid
    variant_type = variants_nanostring[k]['variant_types'][0]['name'] #call variant type
    transcript = variants_nanostring[k]['coordinates']['representative_transcript'] #call transcript
    top_evidence = variants_nanostring[k]
    diseases = variants_nanostring[k]
    chrom = variants_nanostring[k]['coordinates']['chromosome'] #call chrom
    start = variants_nanostring[k]['coordinates']['start'] #call start
    stop = variants_nanostring[k]['coordinates']['stop'] #call stop
    evidence = variants_nanostring[k]['evidence_items']
    evidence_statements = len(variants_nanostring[k]['evidence_items'])
    diseases = []  # set list for all of the diseases for this varinat
    evidence_type = []  # set list for evidence types
    evidence_scores = []  # set list for evidence scores
    top_evidences = []  # set list for top evidence level
    for item in evidence:  # iterate through the evidence items
        if item['disease']['name'] not in diseases:  # see if disease is already there
            if 'Walden' in item['disease']['name']:  # Change waldenstroms issues (the A is not accepted by R code)
                if 'Waldenstroms Macroglobulinemia' not in diseases:  # check if it is already there
                    diseases.append('Waldenstroms Macroglobulinemia')  # if it is not append to diseases
            else:  # if its not a weird name
                diseases.append(item['disease']['name'])  # append the disease
        if item['evidence_type'] not in evidence_type:  # see if the evidence type is already there
            evidence_type.append(item['evidence_type'])  # if it is not append it
        trust_rating = int(item['rating'] or 0)  # make the trust rating either what is listed or 0
        evidence_level = int(
            score[item['evidence_level']])  # make the evidence level the value from the score dictionary
        evidence_scores.append(evidence_level * trust_rating)  # calculate the Evidence Score
        if item['evidence_level'] != '[]':  # find the evidence levels that are not blank
            top_evidences.append(item['evidence_level'].strip())  # add to the list
    # pull the maximum evidence level
    if 'A' in top_evidences:
        top_evidence = 'A'
    elif 'B' in top_evidences:
        top_evidence = 'B'
    elif 'C' in top_evidences:
        top_evidence = 'C'
    elif 'D' in top_evidences:
        top_evidence = 'D'
    else:
        top_evidence = 'E'
    evidence_score = sum(evidence_scores)  # sum the evidence scores to get a CIVic Score
    disease = ', '.join(diseases)  # format the diseases
    evidence_types = ', '.join(evidence_type)  # format the evidence types

    if variants_nanostring[k]['coordinates']['chromosome2'] is not None and variants_nanostring[k]['coordinates']['start2'] is not None and variants_nanostring[k]['coordinates']['stop2'] is not None:  # if there are two chromosomes for the variant
        chrom2 = variants_nanostring[k]['coordinates']['chromosome2']  # call chrom2
        start2 = variants_nanostring[k]['coordinates']['start2']  # call start2
        stop2 = variants_nanostring[k]['coordinates']['stop2']  # call stop2
        nanoString_probes.append([gene, soid, variant_type, variant, transcript, top_evidence, disease, evidence_types, evidence_statements, chrom, start, stop, chrom2, start2, stop2])  # append new list with bed information
    else:  # if there is only 1 chromosome for the variant
        nanoString_probes.append([gene, soid, variant_type, variant, transcript, top_evidence, disease, evidence_types, evidence_statements, chrom, start, stop])  # append new list with bed information

#####################################
## Evaluate and Update Tiling File ##
#####################################

tiling_output = [] #create empty list for output file
tiling_file = [] #create dictionary for keys as the gene, variant and values as tile notes
tile_panel = open(sys.argv[3], 'r') #open tiled genes input file
for line in tile_panel: #iterate through the tile pane
    line = line.strip('\n')  # strip the new line
    line = line.split('\t')  # split by tabs
    gene = line[0]  # pull gene
    variant = line[1] #pull variant
    tile = line[2] #pull tile value
    note = line[3] #pull note
    tiling_file.append([gene, variant])
    tiling_output.append([gene, variant, tile, note])

for item in capture_sequence_probes: #iterate through the capture_sequencing_list
    if [item[0], item[3]] not in tiling_file: #see if the gene, variant matches with the keys in tiling dictionary
        tiling_output.append([item[0], item[3]]) #if it is not there, append the gene and variant to the tiling list for curation

###########################
## Generate Output files ##
###########################

capture = open('capture_sequence_probes.tsv', 'w') #create empy file for capture sequence coordinates
for item in capture_sequence_probes: #iterate through capture list
    for k in item:
        if k is item[-1]:
            capture.write(str(k))
        else:
            capture.write(str(k) + '\t')
    capture.write('\n')
capture.close() #close file


nanostring = open('nanoString_probes.tsv', 'w')  #create empy file for nanostring coordinates
for item in nanoString_probes: #iterate through nanostring list
    for k in item:
        if k is item[-1]:
            nanostring.write(str(k))
        else:
            nanostring.write(str(k) + '\t')
    nanostring.write('\n')
nanostring.close() #close file


tiling = open('tile_classification.txt', 'w')
for item in tiling_output:
    for k in item:
        if k is item[-1]:
            tiling.write(str(k))
        else:
            tiling.write(str(k) + '\t')
    tiling.write('\n')
tiling.close()


