setwd('/Users/ebarnell/civic-panel/')

#Import Libraries
library(biomaRt)
library(bedr)


#Read in list of ENSTs with version numbers of all genes that need to be tiled
representative_transcripts <- read.table('/Users/ebarnell/civic-panel/ENST_representative_transcripts_version.txt', head=T, sep='\t')
#remove the version number
representative_transcripts$transcript_ID <- gsub('\\..*', '', representative_transcripts$transcript_ID)


#Upload the ensembl mart
ensembl_us_west = useMart(biomart="ENSEMBL_MART_ENSEMBL", host="uswest.ensembl.org", dataset="hsapiens_gene_ensembl")

#Use the representative transcripts to get the ENSG IDs
ENSG <- getBM(attributes=c('ensembl_gene_id'), filters ='ensembl_transcript_id', values =c(representative_transcripts$transcript_ID), mart = ensembl_us_west)


#Use the ENSG IDs to get all ENST IDs assocaited with ENSG

ENST_all <- getBM(attributes=c('ensembl_transcript_id','chromosome_name','exon_chrom_start','exon_chrom_end', 'transcript_biotype'
                               ), filters ='ensembl_gene_id', values =c(ENSG$ensembl_gene_id), mart = ensembl_us_west)

#Filter by protein coding ENSTs
ENST_protein_coding <- subset(ENST_all, ENST_all$transcript_biotype == 'protein_coding')

#Obtain the UTRs for all protein coding ENSTs
ENST_protein_coding_UTRs <- getBM(attributes=c('chromosome_name','exon_chrom_start','exon_chrom_end','5_utr_start', '5_utr_end', '3_utr_start', 
                                               '3_utr_end'), filters ='ensembl_transcript_id', values =c(ENST_protein_coding$ensembl_transcript_id),
                                  mart = ensembl_us_west)

#Eliminate exons that is all UTR
ENST_protein_coding_fewer_UTRs <- ENST_protein_coding_UTRs[-which((ENST_protein_coding_UTRs$exon_chrom_start == ENST_protein_coding_UTRs$`5_utr_start` & 
                                                                     ENST_protein_coding_UTRs$exon_chrom_end == ENST_protein_coding_UTRs$`5_utr_end`) | 
                                                                    (ENST_protein_coding_UTRs$exon_chrom_start == ENST_protein_coding_UTRs$`3_utr_start` & 
                                                                       ENST_protein_coding_UTRs$exon_chrom_end == ENST_protein_coding_UTRs$`3_utr_end`) |
                                                                  (ENST_protein_coding_UTRs$exon_chrom_end == ENST_protein_coding_UTRs$`5_utr_start` &
                                                                      ENST_protein_coding_UTRs$exon_chrom_start == ENST_protein_coding_UTRs$`5_utr_end`) |
                                                                    (ENST_protein_coding_UTRs$exon_chrom_end == ENST_protein_coding_UTRs$`3_utr_start` &
                                                                       ENST_protein_coding_UTRs$exon_chrom_start == ENST_protein_coding_UTRs$`3_utr_end`)
                                                                  ), 
                                                           ]

ENST_protein_coding_no_UTRs <- ENST_protein_coding_fewer_UTRs[-which()
  
]

