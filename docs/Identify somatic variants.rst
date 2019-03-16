.. image:: images/Identify.png

| 
=========================
Identify somatic variants
=========================

The completion of the sequencing pipeline results in raw FASTA files, which are text-based files that represent nucleotide sequencings. In this section, we describe how to align sequencing reads to reference genome, how to call somatic variants using automated software, and how to refine variants using semi-automated processes.

This section was made possible by the wonderful information provided by the `Precision Medicine Bioinformatic Course <https://pmbio.org/>`_ developed in the `Griffith Lab <http://griffithlab.org>`_.

--------------------------------
Outputs from Sequencing Pipeline
--------------------------------

>>>>>>>>>>>>
FASTA Format
>>>>>>>>>>>>

During library preparation and target enrichment, read strands are generated as input for sequencing platforms. These read strands are digitally read by sequencing machines and printed to a `FASTA file <https://en.wikipedia.org/wiki/FASTA_format>`_. If your sequencing machine parameter included paired-end reads, whereby each read was read twice, then you will have two FASTA files per sample. These raw files have a consistent format that can be easily read by aligners. Each line a FASTA file includes a header and a sequence:

--- 
> GAPDH_204s.100.1
AATTAGGAGCGATTTGAGATTGCCCCCGATTTATTGACCCGTTTAGCC

> HAPTB_204s.100.1
AAGGCGTGAGAAAGTGCCCGTGGGTAGTGCGGGAGTGGGATGGTAGCC

--- 

Raw FASTA files will include any indexes, linkers, or unique-molecular identifiers (UMIs) that were employed in library preparation or hybridization capture. These sequences will need to be trimmed from the raw sequencing reads prior to alignment. Often this trimming process will be performed by software provided by the commercial entity associated with the instrument being used.

As FASTA files are processed, read strands in FASTA files are annotated with additional information including alignment location, quality, strand, etc. 


>>>>>>>>>>>>
FASTQ Files
>>>>>>>>>>>>

In addition to FASTA files, sequencing runs often produce `FASTQ files <https://en.wikipedia.org/wiki/FASTQ_format>`_, which provides a high level overview of sequencing quality. FASTQ files also have a consistent format that can be easily read by aligners. Each line a FASTQ file includes a header, a sequence, a separator, and quality scores:

--- 
> GAPDH_204s.100.1
AATTAGGAGCGATTTGAGATTGCCCCCGATTTATTGACCCGTTTAGCC
+
!``*((****+())))>>>>>***+1.(%%%%%^&****#)CCCCC65

> HAPTB_204s.100.1
AAGGCGTGAGAAAGTGCCCGTGGGTAGTGCGGGAGTGGGATGGTAGCC
+
!``*((****+()))>>>>>.%%%%^&**#)C65***+()))>>>>>.%

--- 


Quality scores are based on the `Phred scale <https://en.wikipedia.org/wiki/Phred_quality_score>`_ and are enclosed using `ASCII Annotation <https://en.wikipedia.org/wiki/ASCII>`_ characters (for brevity). Each score is calculated differently depending on the technology/instrument used for sequencing.

>>>>>>>>>>>>>>>>
Pre-Alignment QC
>>>>>>>>>>>>>>>>

FASTQ files can be used to generate FastQC Reports. These reports show basic statistics about sequencing (total reads, total poor quality reads, sequence length, GC content, etc.) and provide graphs that give the user a feel for sequencing quality. An example of this type of report is shown below:

..image:: images/FastQC_Report.png

Generating pre-alignment QC can be accomplished following the commands on the `PreAlignment QC <https://pmbio.org/module-02-inputs/0002/06/01/PreAlignment_QC/>`_ page provided by the Precision Medicine Bioinformatic Course.

---------------------
Alignment Strategies
---------------------

>>>>>>>>>>>>>>>>>>>>
The Reference Genome
>>>>>>>>>>>>>>>>>>>>

The reference genome approximates the complete representation of the human genetic sequence for the 4 billion base pairs in human DNA. Using a representative assembly prevents the need to build an assembly each time a genome is sequenced, however, there are intrinsic flaws to this approach. Specifically, due to single nucleotide polymorphisms (SNPs) intrinsic to an individual, the reference genome does not perfectly match any one individual. Further, repetitive elements (duplications, inverted repeats, tandem repeats), the reference is often incomplete or incorrect. Therefore, new genome assemblies are constantly being built to improve our ability to resolve the true human genome sequence. Most recently, GRCh37 was published in 2009 and GRCh38 was published in 2013. A `summary of genome releases <http://genome.ucsc.edu/FAQ/FAQreleases.html>`_ has been provided by UCSC.

Currently, the CIViC database supports variants from NCBI36 (hg18), GRCh37 (hg19), and GTCh38 (hg20), however most variants are associated with reference build GRCh37 (hg19). Therefore, we recommend that for the pipeline, the alignment strategy should use GRCh37 (hg19).

>>>>>>>>>>>>>>>>>>>>
Alignment Algorithms
>>>>>>>>>>>>>>>>>>>>


Alignment can be performed using various alignment software.


---------------------------------
Automated somatic variant caller
---------------------------------


---------------------------
Somatic variant refinement
---------------------------
