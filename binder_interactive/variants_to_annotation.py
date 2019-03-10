#!/usr/bin/env python3

"""
This is a test python file for the CIViC smMIPs paper

Usage: python3 variants_to_annotation.py <variants file>

Arguments:
    <variants file> = TSV (tab separated values) of putative somatic variants with 5 columns [chromosome, start, stop, reference, variant]
    
"""

import sys
import pandas as pd
import requests

# Pull in variant file
somatic_variants = pd.read_csv(sys.argv[1], sep='\t')

# Pull in CIViC API for all variants
variants_DNA = requests.get('https://civic.genome.wustl.edu/api/panels/DNA-based/qualifying_variants?minimum_score=0').json()['records']


#Functions required for code
def print_name(person): 
    print('Your name is ' + person)
    return


# Execute code
interact(print_name(person))