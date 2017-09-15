setwd('/Users/ebarnell/civic-panel/')

#Import Libraries
library(biomaRt)
library(data.table)


#Read in manually curated tiling
tiling <- read.table('/Users/ebarnell/civic-panel/tile_classification.txt', head=T, sep='\t')

#Read in captureseq output file from ProbeSelection.py
capture_sequencing <- read.delim('/Users/ebarnell/civic-panel/capture_sequence_probes.tsv', head=T, sep='\t')

#Merge tiling file and capture sequencing file
capture_sequencing <- merge(capture_sequencing, tiling, by.x=c('gene', 'variant_name'), by.y = c('gene', 'variant_name'), all.x=TRUE)



##################################
## Analyze Exon Tiling Variants ##
##################################

#pull variants that need to be tiled
exon_tiling <- subset(capture_sequencing, tile=='yes')

#remove the version number from transcripts
exon_tiling$representative_transcript <- gsub('\\..*', '', exon_tiling$representative_transcript)

#Upload the ensembl mart
ensembl_us_west = useMart(biomart="ENSEMBL_MART_ENSEMBL", host="grch37.ensembl.org", dataset="hsapiens_gene_ensembl")

#Use the representative transcripts to get the ENSG IDs
ENSG <- getBM(attributes=c('ensembl_gene_id'), filters ='ensembl_transcript_id', values =c(exon_tiling$representative_transcript), mart = ensembl_us_west)


#Use the ENSG IDs to get all ENST IDs assocaited with ENSG
ENST_all <- getBM(attributes=c('ensembl_transcript_id','chromosome_name','exon_chrom_start','exon_chrom_end', 'transcript_biotype'
                               ), filters ='ensembl_gene_id', values =c(ENSG$ensembl_gene_id), mart = ensembl_us_west)

#Filter by protein coding ENSTs
ENST_protein_coding <- subset(ENST_all, ENST_all$transcript_biotype == 'protein_coding')

#Obtain the UTRs for all protein coding ENSTs
ENST_protein_coding_UTRs <- getBM(attributes=c('external_gene_name', 'ensembl_transcript_id', 'chromosome_name','exon_chrom_start','exon_chrom_end','5_utr_start', '5_utr_end', '3_utr_start', 
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
ENST_protein_coding_no_UTRs_bed <- ENST_protein_coding_fewer_UTRs[1:5]
ENST_protein_coding_no_UTRs_bed$chromosome_name <- factor(ENST_protein_coding_no_UTRs_bed$chromosome_name,
                                                          levels = c(1:22, 'X', 'Y'))
ENST_protein_coding_no_UTRs_bed$exon_chrom_start <- as.numeric(ENST_protein_coding_no_UTRs_bed$exon_chrom_start)
ENST_protein_coding_no_UTRs_bed$exon_chrom_end <- as.numeric(ENST_protein_coding_no_UTRs_bed$exon_chrom_end)


###################################
## Analyze Single Probe Variants ##
###################################

#pull variants that require only one probe for analysis
single_probe <- subset(capture_sequencing, tile=='no')
single_probe <- single_probe[c(11:13,1,2,14)]


#########################################
## Merge Exon Tiling and Single Probes ##
#########################################

single_probe <- single_probe[c(1:3)] 
ENST_protein_coding_no_UTRs_bed <- ENST_protein_coding_no_UTRs_bed[c(3:5)]

names(ENST_protein_coding_no_UTRs_bed) <- c('chrom', 'start', 'stop')
coordinates <- rbind(single_probe, ENST_protein_coding_no_UTRs_bed)

#Order the bed file based on chromosome then start
coordinates <- coordinates[with(
  coordinates, order(chrom, start)), ]

coordinates$start <- coordinates$start - 1

coordinates$start <- gsub(' ', '', coordinates$start)
coordinates$stop <- gsub(' ', '', coordinates$stop)


#################
## Write Files ##
#################

#Print out final file for merging
write.table(coordinates, file = "coordinates.bed",
            quote=F, sep="\t", row.names=F, col.names=F)



