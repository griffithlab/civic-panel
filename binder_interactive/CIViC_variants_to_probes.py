#!/usr/bin/env python3

"""
This is a test python file for the CIViC smMIPs paper

Usage: python3 variants_to_probes.py <CIViC variants file> <output path>

Arguments:
    <CIViC variants file> = TSV (tab separated values) file derived from CIViC that contains list of variants required to build custom capture panel.
    <output path> = path for location of final probe list. Default is Desktop.
    
"""

import sys
import pandas as pd
import requests
from pybedtools import BedTool
from pybiomart import Server

#Pull input file and output directory from command line
if sys.argv[2]:
    out_path = sys.argv[2] + 'OpenCAP_probe_list.tsv'
if not sys.argv[2]:
    out_path = '~/Desktop/OpenCAP_probe_list.tsv'

#Read input file
CIViC_variants = pd.read_csv(sys.argv[1], sep='\t')

#Connect to the Ensembl BioMart Server
server = Server(host='grch37.ensembl.org')
dataset = (server.marts['ENSEMBL_MART_ENSEMBL'].datasets['hsapiens_gene_ensembl'])

#Create list to link ESNG to HUGO gene name
matching_list = dataset.query(attributes=['ensembl_gene_id', 'external_gene_name']).drop_duplicates()

#Create function to create probes for variants of different lengths
def create_probe_list(CIViC_variants): 
    probes_list = []
    for i,row in CIViC_variants.iterrows():
        #Iterate through each variant an pull values
        variant = row['variant']
        gene = row['gene']
        description = row['description']
        chrom = row['chromosome']
        start = row['start']
        stop = row['stop']
        difference = int(stop) - int(start)
        
        #if the variant requires few probes for capture
        if difference <= 1000:
            #create probe for hotspot variant
            probes_list.append([str(1) + '-' + gene + '_' + variant, chrom, start, stop, variant, gene, description])
        
        #If the transcript requires full tiling
        elif difference > 1000:
            #Pull ESNG ID using the HUGO gene name
            ESNG_ID = list(matching_list[matching_list['Gene name'] == gene]['Gene stable ID'])[0]
            
            #query biomart for all protein coding regions
            all_exons = pd.DataFrame(dataset.query(attributes=['chromosome_name','genomic_coding_start','genomic_coding_end'], filters={'link_ensembl_gene_id': [ESNG_ID]})).dropna()
            
            #Sort the values by start position for bedtools format
            all_exons = all_exons.sort_values(by=['Genomic coding start'])
            
            #Force start and stop coordinates to integer (not float)
            all_exons['Genomic coding start'] = all_exons['Genomic coding start'].astype(int)
            all_exons['Genomic coding end'] = all_exons['Genomic coding end'].astype(int)
            
            #Merge all values for all exons in protein coding regions
            final_region = pybedtools.BedTool.from_dataframe(all_exons).merge().to_dataframe()
            
            #Create a probe for each consecutive genomic region across large variant
            for i,row in final_region.iterrows():
                chromosome = row[0]
                start = row[1]
                stop = row[2]
                probes_list.append([str(i + 1) + '-' + gene + '_' + variant, chromosome, start, stop, variant, gene, description])
                
    #Create pandas dataframe of probe list
    probes = pd.DataFrame(probes_list)
    return probes

#Generate probe list
probe_list = create_probe_list(CIViC_variants)
probe_list.columns = ['tag','chromosome','start','stop','variant','gene', 'description']

#Output probe list to output path
probe_list.to_csv(out_path, index=False, sep='\t')