.. image:: images/Build.png

==========================
Build Custom Capture Panel
==========================

In this section we will use the CIViC interface to identify variants of interest for custom capture. The interface will then be used to download variants of interest, associated clinical descriptions, and curated coordinates. We will then open an interactive jupyter notebook to format the variant coordinates for probe development. The output from this exercise will be a file that is compatible with commercial probe development companies for custom panel development.


------------------------------
Identify variants for capture
------------------------------

The CIViC database is constantly being updated with new evidence statements and assertions. Therefore, we have provided a real-time query interface that allows users to build a pool of variants required for custom capture. This interface can be accessed by going to the CIViC website, selecting the “SEARCH” button, and navigating to the `Variants” tab: `SEARCH-Variants <https://civicdb.org/search/variants/>`_.

To identify variants for capture, users can add conditions (i.e., search criteria) based on 28 predetermined fields in the drop down menu. If multiple conditions are employed, the user has the option to take the union (i.e., match any of the following conditions) or the intersection (i.e., match all of the following conditions). Additionally, after conditions are employed, the user has the option to further filter the selected variants using column headers in the search grid. The user can filter on Gene Name, Variant Name, Variant Group(s), Variant Types(s), or Description. Once the user is satisfied with the existing variants in the search grid, the user can export the data as a comma-separated values file using the “Get Data” button in the search grid. This will provide users with information required to build probes for all variants selected. Below we have provided a screencast entitled, “Selecting Variants for Capture” to walk users through filtering on the variant evidence score and the pipeline type to select variants for capture.. This screencast covers:

- Accessing the “SEARCH” interface on CIViC
- Filtering variants in CIViC for capture
- Downloading coordinates as a CSV file

TO-DO: Embed YouTube Video:

Although this screencast provides one method to create a variant pool, there are many other examples of criteria that can be useful for identifying variants. Below we have provided a few additional examples of fields that might be helpful for building variant prioritization conditions. Each field has an associated description and links to help documents if applicable.

+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Field                        |   Description                                                                                                             |  Example                                                            |  Associated Help Documents                                                             |
+=============================+===========================================================================================================================+=====================================================================+========================================================================================+
|Assertion                    | Variant is affiliated with clinical assertions that incorporate multiple evidence statements                              | "Variant is associated with an assertion"                           |  Assertion - TO DO                                                                     |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|CIViC Variant Evidence Score | User can indicate minimum threshold for CIViC Variant Evidence Score                                                      | "CIViC Variant Evidence Score is above 20"                          |  Variant Evidence Score - https://civicdb.org/help/variants/variant-evidence-score     |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Description                  | Variant description must contain a keyword                                                                                | "Description contains colorectal cancer"                            |  Variant Summary - https://civicdb.org/help/variants/variants-summary                  |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Disease Implicated (Name)    | Variant must contain at least one evidence item that is implicated in the desired disease                                 | "Disease Implicated is Melanoma"                                    |  Disease Ontology - http://www.disease-ontology.org/                                   |
+-------------+---------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Evidence Items               | User can indicate the required number of evidence items with a certain status                                             | "Evidence Items with status accepted is greater than or equal to 5" |  Evidence Monitoring - https://civicdb.org/help/getting-started/monitoring             |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Gene Name                    | Entrez gene name associated with variant must meet selected criteria                                                      | "Gene Name contains TP53"                                           |  Gene Name - https://civicdb.org/help/genes/genes-overview                             |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Name                         | Variant Name must meet designated criteria                                                                                | "Name does not contain AMPLIFICATION"                               |  Variant Name - https://civicdb.org/help/variants/variants-naming                      |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Pipeline Type                | Variant type is associated with sequence ontology ID(s) that can be evaluated on designated pipeline                      | "Pipeline Type is DNA-based"                                        |  Variant Name - TODO                                                                   |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+
|Variant Type(s)              | Variant type, which is the assigned sequence ontology ID, must meet designated criteria                                   | "Variant Type(s) does not contain Transcript Amplification"         |  Variant Type - https://civicdb.org/help/variants/variants-type                        |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------+----------------------------------------------------------------------------------------+

-------------------------------------------
Build probe list using variant coordinates
-------------------------------------------

`Build Jupiter Notebook <https://mybinder.org/v2/gh/griffithlab/civic-panel/master?filepath=%2Fdocs%2Fbinder_interactive>`_

Jupyter et al., "Binder 2.0 - Reproducible, Interactive, Sharable
Environments for Science at Scale." Proceedings of the 17th Python
in Science Conference. 2018. 10.25080/Majora-4af1f417-011

---------------------------
Build custom capture panel
---------------------------
