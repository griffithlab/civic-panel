
library(GenVisR)
library(ggplot2)

tmp <- read.delim("~/git/civic-panel/smMIPs_Manuscript/data/smMIPs_waterfall/waterfall_dataframe.tsv", header=TRUE)
tmp <- tmp[,c(2,3,4,5,7)]
colnames(tmp) <- c("sample", "gene", "aaChange", "vaf", "validated")
tmp$variant_class <- "SNV/Indel"

tmp2 <- dplyr::mutate(tmp, validatedBINARY = ifelse(validated>0, "TRUE", "FALSE"))
main.layer <- list(scale_fill_manual(values = c('#1B9CFC', '#D6A2E8')),
                   geom_tile(data = na.omit(tmp2), aes(colour=validatedBINARY), fill=NA, size=1),
                   scale_colour_manual(values=c('#FD7272', '#3B3B98'), na.value = FALSE),
                   labs(colour = 'Validated'),
                   guides(fill = FALSE),
                   theme(legend.text = element_text(size=12), legend.title = element_text(size=14),
                         axis.text.y = element_text(size=12), axis.title.y = element_blank(),
                         axis.title.x = element_text(size=14)))

pdf('~/git/civic-panel/smMIPs_Manuscript/data/smMIPs_waterfall/waterfall.pdf', height=12, width=20)
waterfall(na.omit(tmp2), variant_class_order=c("SNV/Indel"), fileType="Custom", mainGrid = TRUE, mainXlabel = TRUE, mainLabelCol = "vaf",
          mainLayer = main.layer)
dev.off()
