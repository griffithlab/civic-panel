.. image:: images/About_OpenCAP.png

|
====================
OpenCAP introduction
====================

The Open-sourced CIViC Annotation Pipeline (OpenCAP) is a tutorial that provides users with a method to develop a customized capture panel for which the variants contained within the panel are linked to clinical relevance summaries in the CIViC knowledgebase. This tutorial contains four chapters:

- **Build Custom Capture Panel**: In this section we will use the CIViC interface to identify variants of interest for custom capture. The interface will then be used to download variants of interest, associated clinical descriptions, and curated coordinates. We will then open an interactive jupyter notebook to format the variant coordinates for probe development. The output from this exercise will be a file that is compatible with commercial probe development companies for custom panel development.


- **Sequence Samples**: This section describes the massively parallel sequencing pipeline. We first detail methods for samples procurement and nucleic acid extraction. Subsequently we provide an overview of library preparation, target enrichment, and next-generation sequencing (NGS). We also touch on new methods for NGS, which includes describing PacBio and NanoPore Sequencing. This high-level overview gives brief insight into how we employ custom capture reagents on tumor samples to enriched capture for variants of interest.


- **Identify Somatic Variants**: The completion of the sequencing pipeline results in raw FASTA files, which are text-based files that represent nucleotide sequencings. In this section, we describe how to align sequencing reads to reference genome, how to call somatic variants using automated software, and how to refine variants using semi-automated processes.


- **Annotate Variants**: After defining a putative list of somatic variants associated with the patient's tumor, this section describes how to ink variants back to the CIViC database to annotate the sample for clinical relevance. We again use an interactive jupyter notebook to pull in somatic variants calls and output a report that can be easily consumed by the user. 
