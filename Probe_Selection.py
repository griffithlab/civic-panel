#Erica Barnell
#6.7.2017
#!/usr/bin/env python3


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

variant_list = requests.get('https://civic.genome.wustl.edu/api/panels/captureseq/qualifying_variants?minimum_score=30').json()['records']

print(variant_list)






