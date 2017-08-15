setwd('/Users/ebarnell/civic-panel/')

#Import Libraries
library(biomaRt)
library(data.table)
library(bedr)

#Read in manually curated tiling
tiling <- read.table('/Users/ebarnell/civic-panel/capture_sequence_tile.txt', head=T, sep='\t')

#Read in captureseq output file from ProbeSelection.py
capture_sequencing <- read.delim('/Users/ebarnell/civic-panel/capture_sequence_probes.tsv', head=T, sep='\t')
capture_sequencing <- subset(capture_sequencing, select=c(gene:stop))

capture_sequencing <- merge(capture_sequencing, tiling, by.x=c('gene', 'soid_name'), by.y = c('gene', 'Mutation'), all.x=TRUE)

capture_sequencing <- subset(capture_sequencing, tile=='yes')

#remove the version number from transcripts
capture_sequencing$transcript <- gsub('\\..*', '', capture_sequencing$transcript)

#Upload the ensembl mart
ensembl_us_west = useMart(biomart="ENSEMBL_MART_ENSEMBL", host="grch37.ensembl.org", dataset="hsapiens_gene_ensembl")

#Use the representative transcripts to get the ENSG IDs
ENSG <- getBM(attributes=c('ensembl_gene_id'), filters ='ensembl_transcript_id', values =c(capture_sequencing$transcript), mart = ensembl_us_west)


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
#Eliminate 5' UTRs
ENST_protein_coding_fewer_UTRs$exon_chrom_end <- apply(ENST_protein_coding_fewer_UTRs, 1, function(x){
  if(!is.na(x['5_utr_end']) & 
     !is.na(x['exon_chrom_end']) &
     x['5_utr_end'] == x['exon_chrom_end']){
       return(as.numeric(x['5_utr_start'])-1)
     } else {
       return(x['exon_chrom_end'])
     }
})
#Eliminate 5' UTRs
ENST_protein_coding_fewer_UTRs$exon_chrom_start <- apply(ENST_protein_coding_fewer_UTRs, 1, function(x){
  if(!is.na(x['5_utr_start']) & 
     !is.na(x['exon_chrom_start']) &
     x['5_utr_start'] == x['exon_chrom_start']){
    return(as.numeric(x['5_utr_end'])+1)
  } else {
    return(x['exon_chrom_start'])
  }
})

#Eliminate 3' UTRs
ENST_protein_coding_fewer_UTRs$exon_chrom_end <- apply(ENST_protein_coding_fewer_UTRs, 1, function(x){
  if(!is.na(x['3_utr_end']) & 
     !is.na(x['exon_chrom_end']) &
     x['3_utr_end'] == x['exon_chrom_end']){
    return(as.numeric(x['3_utr_start'])-1)
  } else {
    return(x['exon_chrom_end'])
  }
})

#Eliminate 3' UTRs
ENST_protein_coding_fewer_UTRs$exon_chrom_start <- apply(ENST_protein_coding_fewer_UTRs, 1, function(x){
  if(!is.na(x['3_utr_start']) & 
     !is.na(x['exon_chrom_start']) &
     x['3_utr_start'] == x['exon_chrom_start']){
    return(as.numeric(x['3_utr_end'])+1)
  } else {
    return(x['exon_chrom_start'])
  }
})

#Create bed file from final exons
ENST_protein_coding_no_UTRs_bed <- ENST_protein_coding_fewer_UTRs[1:3]
ENST_protein_coding_no_UTRs_bed$chromosome_name <- factor(ENST_protein_coding_no_UTRs_bed$chromosome_name,
                                                          levels = c(1:22, 'X', 'Y'))
ENST_protein_coding_no_UTRs_bed$exon_chrom_start <- as.numeric(ENST_protein_coding_no_UTRs_bed$exon_chrom_start)
ENST_protein_coding_no_UTRs_bed$exon_chrom_end <- as.numeric(ENST_protein_coding_no_UTRs_bed$exon_chrom_end)

#Order the bed file based on chromosome then start
ENST_protein_coding_no_UTRs_bed_ordered <- ENST_protein_coding_no_UTRs_bed[with(
  ENST_protein_coding_no_UTRs_bed, order(chromosome_name, exon_chrom_start)), ]

ENST_protein_coding_no_UTRs_bed_ordered$exon_chrom_start <- gsub(' ', '', ENST_protein_coding_no_UTRs_bed_ordered$exon_chrom_start)
ENST_protein_coding_no_UTRs_bed_ordered$exon_chrom_end <- gsub(' ', '', ENST_protein_coding_no_UTRs_bed_ordered$exon_chrom_end)

#Print out final file for merging
write.table(ENST_protein_coding_no_UTRs_bed_ordered, file = "ENST_protein_coding_no_UTRs_bed_ordered.bed",
            quote=F, sep="\t", row.names=F, col.names=F)

