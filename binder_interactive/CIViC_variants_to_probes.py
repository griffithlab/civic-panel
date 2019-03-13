#!/usr/bin/env python3

"""
This is a python file for OpenCAP

Usage: python3 CIViC_variants_to_probes.py <CIViC variants file>

Arguments:
    <CIViC variants file> = TSV (tab separated values) file derived from CIViC that contains list of variants required to build custom capture panel. Each row should contain the following: variant, gene, description, chromosome, start, stop.
    
"""

import sys
import pandas as pd
import pybedtools
from pybedtools import BedTool
from pybiomart import Server

import os
from os import path
import sys
import shutil
import subprocess

bin_dir = path.dirname(sys.executable)
os.environ['PATH'] += os.pathsep + bin_dir
shutil.which('bedtools')
subprocess.run(['bedtools', '--help'])

#Read input file
CIViC_variants = pd.read_csv(sys.argv[1], sep='\t')

#Connect to the Ensembl BioMart Server
server = Server(host='grch37.ensembl.org')
dataset = (server.marts['ENSEMBL_MART_ENSEMBL'].datasets['hsapiens_gene_ensembl'])

#Create list to link ESNG to HUGO gene name
matching_list = dataset.query(attributes=['ensembl_gene_id', 'external_gene_name']).drop_duplicates()

#Create function to create probes for variants of different lengths
def create_probe_list(CIViC_variants): 
    sparse_tile_variant_types = ['LOSS', 'AMPLIFICATION', 'DELETION']
    civic_coordinate_variants = ['DNA BINDING DOMAIN MUTATION', 'PROMOTER DEMETHYLATION', 'CONSERVED DOMAIN MUT']
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
        if difference <= 250:
            #create probe for hotspot variant
            variant_type = 'hotspot coverage'
            probes_list.append([chrom, start, stop, variant, gene, description, str(1) + '-' + gene + '_' + variant, variant_type])
        
        
        
        # If variant type is in a regulatory region or UTR
        elif 'INTRON' in variant or 'UTR' in variant:
            variant_type = 'sparse tiling'
            probes_list.append([chrom, start, stop, variant, gene, description, str(1) + '-' + gene + '_' + variant, variant_type])
        
        
        
        # for variant specific variant types pull CIViC coordiantes
        elif variant in civic_coordinate_variants:
            variant_type = 'sparse tiling'
            probes_list.append([chrom, start, stop, variant, gene, description, str(1) + '-' + gene + '_' + variant, variant_type])
        
        #If the transcript requires full tiling
        else:
            
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

            #Parse down the required coverage for variants in sparse_tile_variants
            if variant in sparse_tile_variant_types:
                #change varinat type to 'full tiling'
                variant_type = 'sparse tiling'
                #Create a probe for each consecutive genomic region across large variant
                for i,row in final_region.iterrows():
                    chromosome = row[0]
                    #find the middle of each exon
                    middle = (row[1] + row[2]) / 2
                    #add 60 bp above and below middle region
                    start = middle - 60
                    stop = middle + 60
                    #append this genomic region to list
                    probes_list.append([chromosome, start, stop, variant, gene, description, str(i + 1) + '-' + gene + '_' + variant, variant_type])

            
            #Else complete full tiling
            else:
                #change varinat type to 'full tiling'
                variant_type = 'full tiling'
                #Create a probe for each consecutive genomic region across large variant
                for i,row in final_region.iterrows():
                    chromosome = row[0]
                    start = row[1]
                    stop = row[2]
                    probes_list.append([chromosome, start, stop, variant, gene, description, str(i + 1) + '-' + gene + '_' + variant, variant_type])
                
    #Create pandas dataframe of probe list
    probes = pd.DataFrame(probes_list)
    return probes

#Generate probe list
probe_list = create_probe_list(CIViC_variants)

#Output probe list to output path
probe_list.to_csv('Categorized_custom_CIViC_variants.txt.bed', index=False, sep='\t', header=False)