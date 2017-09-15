setwd('/Users/ebarnell/civic-panel/panel_samples')

library(MASS)

#Read in pembro samples
pembro_samples <- read.table('/Users/ebarnell/civic-panel/panel_samples/Pembrolizumab_MASTER_MAF.tsv', head=T, sep='\t')
pembro_samples <- subset(pembro_samples, pembro_samples$Day0_DNA_VAF > 0)

#Read in CIViC Coordinates
civic_coordinates <- read.table('/Users/ebarnell/civic-panel/panel_samples/coordinates_merged.bed', head=F, sep='\t')

civic_coordinates$V1 <- paste('chr', civic_coordinates$V1,':',civic_coordinates$V2,'-',civic_coordinates$V3, sep = "")
civic_coordinates <- civic_coordinates[1]

write.table(civic_coordinates, file = "coordinates_merged_lift.bed",
            quote=F, sep=c('\t'), row.names=F, col.names=F)
