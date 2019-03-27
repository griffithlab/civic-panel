.. image:: images/About_OpenCAP.png

====================
OpenCAP introduction
====================

The Open-sourced CIViC Annotation Pipeline (OpenCAP) is a tutorial that provides users with a method to develop a customized capture panel for which the variants contained within the panel are linked to clinical relevance summaries in the CIViC knowledgebase. This tutorial contains four chapters:

- **Build Custom Capture Panel**: In this section we will use the CIViC interface to identify variants of interest for custom capture. The interface will then be used to download variants of interest, associated clinical descriptions, and curated coordinates. We will then use an interactive interface (jupyter notebook) to format the variant coordinates for probe development. The output from this exercise will be a file that is compatible with commercial probe development companies for custom panel development.


- **Sequence Samples**: This section describes the massively parallel sequencing pipeline. We first detail methods for sample procurement and nucleic acid extraction. Subsequently we provide an overview of library preparation, target enrichment, and next-generation sequencing (NGS) on the Illumina platform. We also touch on new platforms for NGS, including PacBio and Oxford NanoPore. This high-level overview gives brief insight into how we employ custom capture reagents on tumor samples to enrich for sequence regions of interest.


- **Identify Somatic Variants**: The completion of the sequencing pipeline results in raw sequence files (e.g., FASTQ), which are text-based files that represent nucleotide sequences for individual reads. In this section, we briefly describe how to align sequencing reads to a reference genome, how to call somatic variants using automated software, and how to refine called variants using semi-automated processes.


- **Annotate Variants**: After defining a putative list of somatic variants associated with the patient's tumor, this section describes how to link variants back to the CIViC database to annotate the sample for clinical relevance. We again use an interactive jupyter notebook to import somatic variant calls and output an editable report for the user. 
