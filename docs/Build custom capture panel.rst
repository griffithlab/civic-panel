==========================
Build custom capture panel
==========================

# Identify variants for capture

The CIViC database is constantly being updated with new evidence statements and assertions. Therefore, we have provided a real-time query interface that allows users to build a pool of variants required for custom capture. This interface can be accessed by going to the CIViC website, selecting the "SEARCH" button, and navigating to the `Variants" tab: [https://civicdb.org/search/variants/]`_. The interface should look like the screenshot shown below:

.. image:: Identify\ Variants.png

To identify variants for capture, users can add conditions based on 28 predetermined fields in the drop down menu. If multiple conditions are employed, the user has the option to take the union (i.e., Match all of the following conditions) or the intersection (i.e., Match any of the following conditions). Additionally, after conditions are employed, the user has the option to further filter the selected variants using column headers in the search grid. The user can filter on Gene Name, Variant Name, Variant Group(s), Varian Types(s), or Description. Once the user is satisfied with the existing variants in the search grid, the user can export the data as a comma-separated values file using the "Get Data" button in the search grid. This will provide users with information required to build probes for all variants selected. Below we have provided a screencast entitled, "Selecting Variants for Capture" to walk users through editing item (i.e., evidence items, variants, or genes, etc.)  in CIViC. This screencast covers:

- Accessing the "SEARCH" interface on CIViC
- Filtering variants in CIViC for capture
- Downloading coordinates as a CSV file

TO DO: INSERT SCREEN CAST

Although this screencast provides one method to create a variant pool, there are many other examples of conditions that can be useful for identifying variants. Below we have provided a few additional examples of fields that might be helpful for building conditions. Each field has an associated description and links to help documents if applicable.

+---------+-------------+----------+--------------------------+
|Field      Description    Example   Associated Help Documents|
+=======================================================================
|Assertion | Variant is affiliated are written descriptions of the variant implications that incorporate multiple evidence statements across the whole database | "Variant is associated with an assertion" | _Assertion_ - TO DO |
+-------------+--------------------+------------------------+-------------------------+
|CIViC Variant Evidence Score | User can indicate minimum threshold for CIViC Variant Evidence Score | "CIViC Variant Evidence Score is above 20"  |  _Variant Evidence Score_ - https://civicdb.org/help/variants/variant-evidence-score |
+-------------+--------------------+------------------------+-------------------------+
|Description | Variant description must contain a keyword | "Description contains colorectal cancer" |  _Variant Summary_ - https://civicdb.org/help/variants/variants-summary |
+-------------+--------------------+------------------------+-------------------------+
|Disease Implicated (Name) | Variant must contain at least one evidence item that is implicated in the desired disease | "Disease Implicated is Melanoma" |  _Disease Ontology_ - http://www.disease-ontology.org/ |
+-------------+--------------------+------------------------+-------------------------+
|Evidence Items | User can indicate the required number of evidence items with a certain status  | "Evidence Items with status accepted is greater than or equal to 5" |  _Evidence Monitoring_ - https://civicdb.org/help/getting-started/monitoring |
+-------------+--------------------+------------------------+-------------------------+
|Gene | Entrez gene name associated with variant must meet selected criteria | "Variant does contain TP53" |  _Gene Name_ - https://civicdb.org/help/genes/genes-overview |
+-------------+--------------------+------------------------+-------------------------+
|Name | Variant Name must meet designated criteria | "Name does not contain AMPLIFICATION" |  _Variant Name_ - https://civicdb.org/help/variants/variants-naming |
+-------------+--------------------+------------------------+-------------------------+
|Pipeline Type | Variant type is associated with sequence ontology ID(s) that can be evaluated on designated pipeline | "Pipeline Type is DNA-based" |  _Variant Name_ - TODO |
+-------------+--------------------+------------------------+-------------------------+
|Variant Type(s) | Variant type, which is the assigned sequence ontology ID, must meet designated criteria  | "Variant Type(s) does not contain Transcript Amplification" |  _Variant Type_ - https://civicdb.org/help/variants/variants-type |
+-------------+--------------------+------------------------+-------------------------+

# Build probe list using variant coordinates

# Build custom capture panel
