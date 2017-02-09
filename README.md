# civic-panel
The CIViC-Panel Project will be used to identify variants within the CIViC Database that will be used in the CIViC Biomarker Capture Panel.  All variants will undergo selection criteria to filter out variants within the database that do not meet selection standards.  Additionally, the CIViC-Panel will create an automated way to design probes for selected variatns so that subsequent additions to the CIViC Database can be quickly incorporated into the CIViC Capture Panel.

#Part 0 - Create Variant CIViC Score 

##Scoring Matrix Rules:
###Evidence Level
1) A = 10 points
2) B = 5 points
3) C = 2.5 points
4) D = 1 point
5) E = 0 points

###Trust Rating:
1) Each Star = 1 point

##Creating CIViC Scores
###Each Evidence Item will receive an Evidence Item Score and each Variant will receive a CIViC Variant Score
1) Evidence Item scores are determined by multiplying the evidence level points by the trust rating points
2) Total CIViC Score for each variant is the summation of all the Evidence Item scores for each variant
3) Eligible Variants must have a CIViC score greater than 30 points.
4) If two Evidence Items with the same variant, disease and drug have conflicting directions, then the Evidence Item score is deducted from the total CIViC Variant Score

Each variant will be called and we will iterate through all of the evidence items.
Evidence items will be given an 'Evidence Item Score'
The Evidence Item Scores will be added together to calculate the CIViC Variant Scores for each variant.


########################################################
## Part 1 - Filter Out Variants Based on CIViC Score ##
########################################################

Each variant will have a CIViC Variant Score.
If the CIViC Variant score is above a certain threshold, the Variant will be eligible for the CIViC Capture Panel
	**NOTE: Can we make the threshold a variable so that we can change the threshold as needed to increase or decrease stringency?**


########################################################
##  Part 2 - Bucket Eligible Variants into Pipelines ##
########################################################


All variants that are eligible for the CIViC Capture Panel will analyzed using two pipelines:
	 1) IDT Capture Sequencing
	 1) NanoString Technologies
The pipeline used for individual variants will be determined by the Sequence Ontology ID.
Each sequence ontology ID can be associated with one or more pipelines for analysis.
If a sequence ontology ID is not associated with any pipeline, it will not be included in the CIViC Capture Panel.

All variants that are bucketed into either the NanoString pipeline or the Capture Sequencing pipeline must have:
	 1) Name of the Gene
	 2) Chromosome of the Variant
 	 3) Start Position
     4) Stop Position

########################################################
##   Part 3 - Determine Capture Sequence Probes      ##
########################################################

Guidelines for Probes:
For capture sequenceing, each probe can cover approximately 100 bases and costs approximately $7.00
Tiling a whole gene costs approximately $70.00
For each Variant, if the (start position) - (stop position) > 200 bases, multiple probes must be created.
If the Variant length is greater than 1,000 bases, the whole gene should be covered.

Creating Output for Probes:
For variants less than 200 bases:
	 1) Output will be gene, chromosome, start, stop

For variants between 100-1,000 bases:
	 1) Number of Probes Needed = ((start position) - (stop position)) / 100
	 2) Output will be gene, chromosome, start, stop for each 100bp increment

For variants greater than 1,000 bases:
    1) Output will be gene


########################################################
## Part 4 - Determine NanoString Technology Probes   ##
########################################################

Guidelines for Probes:
For all variants:
	 1) Output will be gene, chromosome, start, stop



