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



###Create bed file from final exons

exons <- ENST_protein_coding_fewer_UTRs[c(3:5,1)]
names(exons) <- c('chrom', 'start', 'stop', 'gene')
exons <- merge(exons, capture_sequencing[1:2], by.x=('gene'), by.y=('gene'), all.x=T, all.y=F)
exons <- exons[c(2:4,1,5)]

exons$chrom <- factor(exons$chrom,levels = c(1:22, 'X', 'Y'))
exons$start <- as.numeric(exons$start)
exons$stop <- as.numeric(exons$stop)


#Order the bed file based on chromosome then start
exons <- exons[with(exons, order(chrom, start)), ]

exons$start <- exons$start
exons$start <- gsub(' ', '', exons$start)
exons$stop <- gsub(' ', '', exons$stop)

#Print out final file for merging
write.table(exons, file = "exon_coordinates.txt", quote=F, sep="\t", row.names=F, col.names=F)




###################################
## Analyze Single Probe Variants ##
###################################

#pull variants that require only one probe for analysis
single_probe <- subset(capture_sequencing, tile=='no')
single_probe <- single_probe[c(11:13,1,2)]

single_probe$chrom <- factor(single_probe$chrom,levels = c(1:22, 'X', 'Y'))
single_probe$start <- as.numeric(single_probe$start)
single_probe$stop <- as.numeric(single_probe$stop)

single_probe <- single_probe[with(single_probe, order(chrom, start)), ]

single_probe$start <- single_probe$start

single_probe$start <- gsub(' ', '', single_probe$start)
single_probe$stop <- gsub(' ', '', single_probe$stop)

#Print out final file for merging
write.table(single_probe, file = "single_probe_coordinates.txt",
            quote=F, sep="\t", row.names=F, col.names=F)



###################################
##     Analyze Ten Variants      ##
###################################

#pull variants that need to be tiled
exon_tiling <- subset(capture_sequencing, tile=='ten')

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

###Create file for ten probes

ten_exons <- ENST_protein_coding_fewer_UTRs[c(3:5,1)]
names(ten_exons) <- c('chrom', 'start', 'stop', 'gene')
ten_exons <- merge(ten_exons, capture_sequencing[1:2], by.x=('gene'), by.y=('gene'), all.x=T, all.y=F)
ten_exons <- ten_exons[c(2:4,1,5)]


ten_exons$chrom <- factor(ten_exons$chrom,levels = c(1:22, 'X', 'Y'))
ten_exons$start <- as.numeric(ten_exons$start)
ten_exons$stop <- as.numeric(ten_exons$stop)


#Order the bed file based on chromosome then start
ten_exons <- ten_exons[with(ten_exons, order(chrom, start)), ]

ten_exons$start <- ten_exons$start
ten_exons$start <- gsub(' ', '', ten_exons$start)
ten_exons$stop <- gsub(' ', '', ten_exons$stop)

#Print out final file for merging
write.table(ten_exons, file = "ten_coordinates.txt", quote=F, sep="\t", row.names=F, col.names=F)




###################################
##  create files for samples     ##
###################################

##CIVIC 37 COORDINATES
civic_coordinates_37 <- rbind(ten_exons, single_probe, exons)
civic_coordinates_37 <- civic_coordinates_37[1:3]
civic_coordinates_37$chrom <- factor(civic_coordinates_37$chrom,levels = c(1:22, 'X', 'Y'))
civic_coordinates_37$start <- as.numeric(civic_coordinates_37$start)
civic_coordinates_37$stop <- as.numeric(civic_coordinates_37$stop)

civic_coordinates_37 <- civic_coordinates_37[with(civic_coordinates_37, order(chrom, start)), ]

civic_coordinates_37$start <- civic_coordinates_37$start
civic_coordinates_37$start <- gsub(' ', '', civic_coordinates_37$start)
civic_coordinates_37$stop <- gsub(' ', '', civic_coordinates_37$stop)

write.table(civic_coordinates_37, file = "civic_coordinates_37.txt", quote=F, sep="\t", row.names=F, col.names=F)

#CIVIC 37 COORDINATES FOR LIFTOVER
civic_coordinates_37 <- read.table('coordinates_merged_37.txt', 'r', header=F, sep='\t')
names(civic_coordinates_37) <- c('chrom', 'start', 'stop')
civic_coordinates_37$chrom <- paste0("chr", civic_coordinates_37$chrom, ':', civic_coordinates_37$start, '-', civic_coordinates_37$stop)
write.table(civic_coordinates_37[1], file = "civic_coordinates_37_for_lift.txt", quote=F, sep="\t", row.names=F, col.names=F)


