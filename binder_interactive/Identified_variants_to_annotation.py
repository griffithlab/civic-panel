#!/usr/bin/env python3

"""
This is a python file for the OpenCAP

Usage: python3 identified_variants_to_annotation.py <somatic variants file>

Arguments:
    <somatic variants file> = TSV (tab separated values) of putative somatic variants with 5 columns [chromosome, start, stop, reference, variant].
    
"""

import sys
import pandas as pd
import requests
from docx import Document
from docx.shared import Inches

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