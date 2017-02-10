# civic-panel
The CIViC-Panel Project will be used to identify variants within the CIViC Database that will be used in the CIViC Biomarker Capture Panel.  All variants will undergo selection criteria to filter out variants within the database that do not meet selection standards.  Additionally, the CIViC-Panel will create an automated way to design probes for selected variatns so that subsequent additions to the CIViC Database can be quickly incorporated into the CIViC Capture Panel.


#Part 0 - Create Variant CIViC Score 

##Scoring Matrix Rules:
###Evidence Level

- A = 10 points
- B = 5 points
- C = 2.5 points
- D = 1 point
- E = 0 points


###Trust Rating:
- Each Star = 1 point

##Creating CIViC Scores
###Evidence Item Scores
Evidence Item scores will be calculated for each Evidence Item.  This score is calculated by multiplying the Evidence Level points by the Trust Rating points.  If an evidence item has a direction that is negative, and it has a matching positive evidence item, it will be deducted from the total CIViC score. If an evidence item has a direction that is negative but it does not have a matching positive evidence item, it will not be counted towards to total CIViC score.  This score will be used to calcualte the CIViC Variant Score.

[Matching Evidence Item = Same Variant, Disease, Drug but conflicting Directions]

- Total CIViC Score for each variant is the summation of all the Evidence Item Scores for each Variant.
- Eligible Variants must have a CIViC score greater than a certain threshold.  Currently that threshold is 30 points.
- If an Evidence Item is diagnostic, predisposing, or prognostic, and has a negative Direction, then the Evidence Item Score is 0 regardless of the Trust Rating and Evidence Level.
- If the Evidence Item is Predictive  and has a negative Direction, the Evidence Item Score will follow the normal pattern.
- If two Evidence Items with the same variant and disease have conflicting directions, then the Evidence Item score is deducted from the total CIViC Variant Score.

###CIViC Variant Scores
CIViC Variant Scores will be calculated for each Variant.  The score is calculated by adding all of the positive Evidence Item Scores and subtracting any negative Evidence Item Scores that have Matching Evidence Items.  This score will be used to determine if variants are eligible for the CIViC Capture Panel.


#Part 1 - Eligiability Based on CIViC Score

##Eligiable Variants
All Variants with a CIViC Variant score that meets a certain threshold will be eligible for the CIViC Capture Panel.  Currently, the threshold is set at 30 points, however, this is a variable that can be changed to increase or decrease stringency.
	
	
#Part 2 - Pipelines for Eligible Variants

##Pipelines
All variants that are eligible for the CIViC Capture Panel will analyzed using two pipelines:
- IDT Capture Sequencing
- NanoString Technologies
The pipeline used for individual variants will be determined by the Sequence Ontology ID.  Each sequence ontology ID will be associated with one or more pipelines for analysis.  If a sequence ontology ID is not associated with any pipeline, it will not be included in the CIViC Capture Panel.

##Output
All variants that are bucketed into either the NanoString pipeline or the Capture Sequencing pipeline must have:
- Name of the Gene
- Variant Chromosome
- Start Position
- Stop Position
- If the variant is a fusion gene, we will also need the Chromosome2, Start2, and Stop2
     
     
#Part 3 - Determine Capture Sequence Probes

##Guidelines for Probes
For capture sequenceing, each probe can cover approximately 100 bases and costs approximately $7.00 whereas tiling a whole gene costs approximately $70.00.  Therefore, if the variant length is greater than 1,000 bases, the whole gene should be covered.  Additionally, for variants that are longer than 200 bases, multiple probes must be created.

##Creating Output for Probes:
###For variants less than 200 bases:
- Output will be gene, chromosome, start, stop

###For variants between 100-1,000 bases:
- Number of Probes Needed = ((start position) - (stop position)) / 100
- Output will be gene, chromosome, start, stop for each 100bp increment

###For variants greater than 1,000 bases:
- Output will be gene


#Part 4 - Determine NanoString Technology Probes

##Guidelines for Probes:
###For all variants:
- Output will be gene, chromosome, start, stop



