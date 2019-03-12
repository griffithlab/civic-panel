.. image:: images/Header.png

|
=====
About
=====

Welcome to the Open-sourced CIViC Annotation Pipeline (OpenCAP). This resource is a step-by-step tutorial that allows users to build a custom clinical capture panel that is linked to clinical variant annotations. This capture panel development is accomplished using the publicly available `CIViC database <www.civicdb.org>`_. Through the tutorial, we first describe the CIViC database and introduce users to relevant information within CIViC that will be used to build the capture panel. We then go through methods to build a CIViC capture panel using existing variants within the CIViC database. Specifically, variants of interest are identified using heuristic filters and variant coordinates are queried using CIViC’s public API. Coordinates identified are then used to build custom capture probes that target variants of interest. After custom capture panel development, we describe how to prospectively employ capture sequencing reagents on tumor samples. This includes library preparation, high throughput sequencing and somatic variant calling. Once variants are identified using automated somatic variants calling and somatic variant refinement, we then show users how to link these variants back to the CIViC database to annotate the tumor sample for clinical relevance. Successful execution of this tutorial will provide users with a unique capture panel customized to the individual's need with linkage to clinical relevance summaries for all variants within the panel.

OpenCAP is intended for research use only and clinical applications of subsequent panels designed using the SOP would require further panel validation.
