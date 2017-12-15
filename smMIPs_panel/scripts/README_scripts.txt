################################
## Contents of scripts Folder ##
################################

This folder contains scripts needed for panel development.

1) assess_CIViC_curation.ipynb = a script that outlines that variants that have been externally validated as clinically relevant, i.e. it is present in at least 10 gene panels; variants that are extensively curated within CIViC (CIViC actionability score > threshold); variants that are extensively curated within CIViC but not externally validated in multiple gene panels; and variants that require curation on sequence ontology identificaiton.

2) probe_selection.ipby = a method that queries the CIViC coordinates and determines that relevant genomic loci required to evalaute the variant. This code evaluates the variants that can be assessed by DNA- and RNA-based methods.

3) exon_tilint_and_SNPs.R = R script that requires conversion.