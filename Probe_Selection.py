#Pull in Data from JSON
python
import json, requests

gene_dict = {}

gene_list = requests.get('https://civic.genome.wustl.edu/api/genes?count=1000000000').json()['records']

for current_gene in range(0, len(gene_list)):
    gene_dict[gene_list[current_gene]["name"]] = gene_list[current_gene]

print(len(gene_dict))
for k,v in gene_dict.items():
    print(k)


#Create Buckets Variants for Evaluation
Not_Evaluated = []
NanoString_Probes_Needed = []
Capture_Sequence_Probes_Needed = []
Biomarker_Probe_Already_Created = []

#Pull Information from CIVIC
all_genes = []
genes = []
variants = []
chromosomes_1 = []
starts_1 = []
stops_1 = []
chromosomes_2 = []
starts_2 = []
stops_2 = []
probe = []
evidence_rating = []
trust_rating = []

#Filter out variants into Not_Evaluated
	#Criteria: 1. At least 1 B rating evidence items
	#Criteria: 2. At least 1 Trust Rating of 3 Stars
	#Criteria 3. At least 2 Accepted Evidence Items per Variant



#Bucket Variants that Already Have Probe Designs
#Bucket Fusion Proteins and RNA dysregulation into NanoString_Probes_Needed
#Bucket other variants into Capture_Sequence_Probes_Needed

for i in range len(genes):
	gene = gene(i)
	variant = variant(i)	
	chromosome_1 = chromosomes_1(i)	
	start_1 = starts_1(i)	
	stop_1 = stops_1(i)	
	chromosome_2 = chromosomes_2(i)	
	start_2 = starts_2(i)	
	stop_2 = stops_2(i)
	probe = probes(i)
	if probe == “YES”
		Biomarker_Probe_Already_Created.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	elif chromosome_2 > 0:
		NanoString_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	elif variant == “*FUSION*”:
		NanoString_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	elif variant == “AMPLIFICATION”:
		NanoString_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	elif variant == “*EXPRESSION”:
		NanoString_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	elif variant == “LOSS”
		NanoString_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)
	else:
		Capture_Sequence_Probes_Needed.append(gene, variant, chromosome_1, start_1, stop_1, chromosome_2, start_2, stop_2)


#Create Output for Probe Design








