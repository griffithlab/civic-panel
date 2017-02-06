"""Probe_Selection.py will pull existing variants from the CIViC Knowledgebase, iterate through all pulled variants, and divide variants into lists.  
The output will be four lists of variants:
1) Not_Evaluated: Probes that will not be evaluated in the Biomarker Capture Panel
2) NanoString_Probes_Needed: Probes that will need to be evaluated using NanoString Technology
3) Capture_Sequence_Probes_Needed: Probes that will need to be evaluated using Capture-Sequencing Technology
4) Biomarker_Probe_Already_Created: Probe that have already been designed and validated

Each list will contain four columns.  These columns will be "name" "chromosome" "start" "stop". 

Usage: Probe_Selection.py

"""

##Pull in Data from JSON
#!/usr/bin/env python3
import json, requests

variant_dict = {}

variant_list = requests.get('https://civic.genome.wustl.edu/api/variants?count=1000000000').json()['records']

Not_Evaluated = []
NanoString_Probes_Needed = []
Capture_Sequence_Probes_Needed = []
Non_Bucketed = []
ids = []
#Biomarker_Probe_Already_Created = [] (NOT EVALUATED YET)

##Iterate through list and Pull out Not_Evaluated
	#Criteria for Not_Evaluated = 1) No accepted evidence items
	#Criteria for NanoString_Probes_Needed = 1) Fusion Variant 2) mRNA transcript 
	#Criteria for Capture_Sequence_Probes_Needed = 1)SNP
	#Criteria for Biomarker_Probe_Already_Created = N/A
for current_variant in range(0, len(variant_list)):
	if (variant_list[current_variant]['evidence_items']['accepted_count'] == 0) or ("SERUM LEVELS" in variant_list[current_variant]['name']) or (variant_list[current_variant]['coordinates']['chromosome'] is None):
		Not_Evaluated.append([variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop']])
		ids.append(variant_list[current_variant]['id'])
	elif variant_list[current_variant]['coordinates']['chromosome2'] is not None:
		NanoString_Probes_Needed.append([variant_list[current_variant]['id'], variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop'], variant_list[current_variant]['coordinates']['chromosome2'], variant_list[current_variant]['coordinates']['start2'], variant_list[current_variant]['coordinates']['stop2']])
		ids.append(variant_list[current_variant]['id'])	
	elif ("EXPRESSION" in variant_list[current_variant]['name']) or ('FRAME SHIFT' in variant_list[current_variant]['name']) or ("METHYLATION" in variant_list[current_variant]['name']) or (variant_list[current_variant]['name'] is "LOSS") or ("DELETION" in variant_list[current_variant]['name']):
		NanoString_Probes_Needed.append([variant_list[current_variant]['id'], variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop'], variant_list[current_variant]['coordinates']['representative_transcript']])
		ids.append(variant_list[current_variant]['id'])
	elif int(variant_list[current_variant]['coordinates']['start']) - int(variant_list[current_variant]['coordinates']['stop']) <= 1:
		Capture_Sequence_Probes_Needed.append([variant_list[current_variant]['id'], variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop']])
		ids.append(variant_list[current_variant]['id'])
	else:
		Non_Bucketed.append([variant_list[current_variant]['id'], variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop']])
		ids.append(variant_list[current_variant]['id'])


##ERROR Codes

#Total ids pulled
if len(ids) < len(variant_list):
	print("Error: Some Variants Were Not Bucketed!")
if len(ids) > len(variant_list):
	print("Error: Some Variants Were Bucketed Multiple Times")


##Create Output for Probe Design
# Create a variable that opens a writeable file:
Not_Evaluated = open('Probes_Not_Evaluated.tsv', "w")
# Write probe information to the file:
Not_Evaluated.write('[variant_list[current_variant]['entrez_name'], variant_list[current_variant]['coordinates']['chromosome'], variant_list[current_variant]['coordinates']['start'], variant_list[current_variant]['coordinates']['stop']]')
# Close files:
Not_Evaluated.close()







