.. image:: images/Sequence.png



==============================
Methods for sequencing samples
==============================

------------------
Sample procurement
------------------

For the analysis described here, samples must be derived from a germline tissue (normal sample) and a diseased tissue (tumor sample). Procuring samples from these two sample types requires consideration of the malignancy:

- **Liquid Cancers**: A cancer that begins in blood-forming tissue, such as the bone marrow, or in the cells of the immune system (e.g., leukemia, multiple myeloma, and some lymphomas)

- **Solid Cancers**: An abnormal mass that does not contain cysts or liquid areas (e.g., sarcomas, carcinomas, and some lymphomas)


.. image:: sample_procurement.png

It is important to note that blood samples cannot be used as the normal samples for solid cancers if the tumor is metastatic with high circulating tumor cells. In these cases, buccal swabs or skin biopsies are better for tumor normal comparisons.

---------------
Sample storage
---------------

Once samples are procured, they can be fresh-frozen (FF) or formalin-fixed paraffin-embedded (FFPE).

- **Fresh Frozen**: As soon as samples are obtained, fresh frozen preparation requires exposing the sample to liquid nitrogen as quickly as possible. Samples must subsequently be stored  in −80°C freezers until extraction.

- **Formalin-fixed paraffin-embedded**: FFPE samples can be prepared using a variety of available kits (e.g., `QIAamp DNA FFPE Tissue Kit <https://www.horizondiscovery.com/media/resources/Miscellaneous/reference-standards/QIAamp%20DNA%20FFPE%20Tissue%20Kit%20Guidelines%20Digital%20(DISTRIBUTION).pdf>`_, `MagMAX™ FFPE DNA/RNA Ultra Kit <http://tools.thermofisher.com/content/sfs/manuals/MAN0015877_MagMAX_FFPE_DNA_RNA_Ultra_UG.pdf>`_, `Quick-DNA/RNA FFPE Miniprep Kit <https://files.zymoresearch.com/protocols/_d3067_quick-dna_ffpe_miniprep.pdf>`_, etc.). 


------------------------
Nucleic acid generation
------------------------

If samples are stored as FFPE blocks, they require FFPE DNA extraction. This can be accomplished using commercially available kits (e.g., INSERT). In general, these kits require paraffin removal and tissue rehydration, tissue digestion, mild reversal of cross-linkage, and nucleic acid purification. If samples are stored as fresh-frozen tissue blocks, they only require nucleic acid purification.

Nucleic acid purification requires cell lysis, binding of nucleic acid, washing off non nucleic acid material, drying of nucleic acid, and elution into a buffer. There are many commercially available kits that can perform nucleic acid purification (e.g., ). These steps can also be automated using commercially available equipment (e.g., `QIAsymphony® SP <https://agtc.med.wayne.edu/pdfs/qiasymphony_sp_brochure.pdfn>`_, `NUCLISENS® easyMAG® <https://www.mediray.co.nz/media/15757/om_biomerieux_nucleic-acids-isolation_nuclei-sens-user-manual-easymag.pdf>`_, etc.). Below we describe each step in detail:

	1) **Lyse**: Tissue samples are typically stored as whole cells. The lysis step is used to disrupt the cellular membrane to expose the nucleic acid. Lysis buffers typically comprises a chaotropic agent, which breaks the hydrogen bonds network between water molecules and optionally a surfactant to lower surface tension between membrane components and nucleic acid-containing solution. Some chaotropic agents can include: guanidium thiocyanate or magnesium chloride. Some surfactants can include: Triton-X-100, or sodium dodecyl sulfate.
 
	2) **Bind**: After nucleic acid has been suspended in solution, it can be reversibly bound to a positively charged material for purification. These materials can include magnetic particles, columns, filters, silica beads, or organic solvent-based methods. 

	3) **Wash**: Once the nucleic acid is bound to a positively charged material, remaining substances in the lysate are washed from solution. A washing solution does not disrupt the covalent bond between the nucleic acid and the positively charged material used for purification. Washing buffers can include: INSERT.

	4) **Dry**: To ensure proper elution, bound nucleic acid typically needs to be completely devoid of all liquid. To avoid degradation, alcohols can be used to expedite the drying step.

	5) **Elute**: Elution buffers are solvents that displace the nucleic acid from the positively charged material used for purification. Elution buffers can include: 10 mM Tris at pH 8-9, Warmed MilliQ (60 oC), or 1X TE.

	6) **Cleanup**: Elutions can be optionally treated with either RNAse (`RNase ONE™ Ribonuclease <https://www.promega.com/-/media/files/resources/msds/m4000/m4261.pdf?la=en-us>`_, `RNase A <https://files.zymoresearch.com/sds/e1008-1_e1008-8_e1008-24_e1008-30_rnase_a.pdf>`_, etc.) or DNAse (e.g., `DNase I` <https://www.neb.com/protocols/0001/01/01/a-typical-dnase-i-reaction-protocol-m0303>, `Baseline-ZERO™ DNase <http://www.epibio.com/docs/default-source/protocols/baseline-zero-dnase.pdf?sfvrsn=8>`_, etc.) to eliminate nucleic acid that is not being used in downstream analysis.

	7) **Quality check**: After the nucleic acid generation step, it is recommended to assess the quantity and quality of the final elution. This can be accomplished using spectrophotometry and/or electropherograms.

		- **Spectrophotometry** measures a substance's ability to absorb a specific wavelength, which in turn is a proxy for concentration and purity. First, the sample is exposed an ultraviolet light at a wavelength of 260 nanometres (nm) and the DNA and RNA in the sample will absorb a relative amount of the light that is proportional to the concentration. Next a photo-detector measures the light that passes through the sample (i.e., not absorbed), which allows you to calculate the quantification of DNA/RNA in the sample. `Nucleic acid quantification <https://en.wikipedia.org/wiki/Nucleic_acid_quantitation>`_ using spectrophotometry relies on the `Beer–Lambert law <https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law>`_. 

		- **Electropherograms** measure the nucleic acid concentration and size using a fluorescent spectrum. The `Agilent 2100 Bioanalyzer <https://ipmb.sinica.edu.tw/microarray/index.files/Agilent%202100%20Bioanalyzer%20user%20guide.pdf>`_ evaluates the sample using spectrum of fluorescents. The `Qubit 4 Fluorometer <https://www.thermofisher.com/document-connect/document-connect.html?url=https%3A%2F%2Fassets.thermofisher.com%2FTFS-Assets%2FLSG%2Fmanuals%2FMAN0017209_Qubit_4_Fluorometer_UG.pdf&title=VXNlciBHdWlkZTogUXViaXQgNCBGbHVvcm9tZXRlcg==>`_ utilizes fluorescent dyes that are specific to the target of interest.

-----------------------------
Target enrichment strategies
-----------------------------

Target enrichment strategies are used to generate a specific collection of DNA fragments for sequencing. In advance of next-generation sequencing (NGS) development of these libraries typically require genomic fragmentation, ligation to custom linkers called adapters, and polymerase chain reaction (PCR) amplification.

	1) **Genome fragmentation** requires breaking the DNA into smaller pieces using physical or chemical means. 
		- Physical fragmentation methods including sonication, nebulization or enzymatic reactions. 
		- Chemical fragmentation relies on hydroxyl radicals to break DNA into fragments, which can accommodate more material, but can induce false positives through novel mutations or transversion artifacts.

	2) **Adding adaptors** are chemically synthesized double stranded DNA molecules that tag individual reads. These adaptors allow users to tag molecules for sequencing as well as employ unique molecular identifier (UMI) strategies.

	3) **PCR amplification** is a method to make many copies of a specific DNA segment. PCR requires first denaturing dsDNA to create ssDNA using heat, binding of targeted primers to ssDNA fragments, and elongation of ssDNA to create a copied dsDNA.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PCR-based library preparation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~
Molecular inversion probes
~~~~~~~~~~~~~~~~~~~~~~~~~~




~~~~~~~~~~~~~~~~~~~~~~
Hybridization capture
~~~~~~~~~~~~~~~~~~~~~~

Sequencing reads generated via library preparation are ultimately evaluated by exciting individual fluorescent probes and digitally reading fluorescent output on the sequencing platform. Therefore, the commercially available library preparation kit chosen for library development should be consistent with the ultimate sequencing platform used for reading sequences.



~~~~~~~~~~~~~~~~~~~~~~
Other considerations
~~~~~~~~~~~~~~~~~~~~~~

Of note, for RNA sequencing, total RNA must be subjected to reverse transcriptase treatment (e.g., `ProtoScript® II Reverse Transcriptase <https://www.neb.com/protocols/2016/04/26/first-strand-cdna-synthesis-standard-protocol-neb-m0368>`_, `SuperScript™ III Reverse Transcriptase <https://www.thermofisher.com/document-connect/document-connect.html?url=https%3A%2F%2Fassets.thermofisher.com%2FTFS-Assets%2FLSG%2Fmanuals%2FsuperscriptIII_man.pdf&title=U3VwZXJTY3JpcHQgSUlJIFJldmVyc2UgVHJhbnNjcmlwdGFzZQ==>`_) to generate cDNA prior to subjecting to library preparation. 


--------------------------
High throughput sequencing
--------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~
Next-generation sequencing
~~~~~~~~~~~~~~~~~~~~~~~~~~

Sequencing is the next step in genomic analysis pipeline. The most commonly used sequencing technique is next-generation sequencing (NGS), which evaluates millions of sequences in parallel to dramatically reduce time and cost of the analysis. There are two main platforms that harness the power of next-generation sequencing to efficiently sequence tumor samples:

	- **Illumina sequencing** anneals individual reads to a bead or plate using DNA adaptors and the molecule is amplified through polymerase chain reaction. Amplified reads are sequenced by individually adding single blocked-nucleotides to the complementary DNA sequence and exposing the nucleotide to light to produce a characteristic fluorescence. These blocked-nucleotides can be un-blocked to allow for an additional base to bind and the process repeated until the whole complementary sequence is elucidated. This platform has a high accuracy rate and can evaluate 50-300 base-pairs with massive parallel sequencing to decrease time and cost of the analysis. Each run takes approximately 2-3 days to complete in under $1,000 per sample.

	- **ThermoFisher ION Torrent** evaluates hydrogen atoms emitted during polymerization of base pairs, which can be measured as a variation in the solution’s pH. This method has a low error rate for substitutions and point mutations and it is relatively inexpensive with a fast turn-around for data production (2-7 hours per run), however, the platform has higher error rates for insertions and deletions, it cannot read long chains of mononucleotides, and it cannot currently match the power and throughput of the Illumina sequencing platform.



~~~~~~~~~~~~~~~~~~~~~~~~~~~
Third generation sequencing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Third Generation Sequencing Platforms: PacBio and NanoPore and third generation sequencing technologies that can sequence longer reads at a reduced cost to address the existing problems associated with NGS.

	- **PacBio** utilizes hairpin adaptors to create a loop of DNA that can be fed through an immobilized polymerase to add complementary base pairs. As each nucleotide is held in the detection volume by the polymerase, a light pulse identifies the base. This platform requires high quality intact DNA with highly controlled fragmentation and can read strands up to 1Mb in length.

	- **Oxford NanoPore Sequencing** utilizes biological transmembrane proteins that translocalize DNA. Measurement of changes in electoral conductivity as the DNA passes through the pore elucidates sequence reads. This platform can evaluate variable length reads and is incredibly inexpensive relative to other technologies. Specifically, the MinION device is completely portable, commercially available and can evaluate 20-100MB per run. The tradeoff is its low fidelity rate of only 85%.
