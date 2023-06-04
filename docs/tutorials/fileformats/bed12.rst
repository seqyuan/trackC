=====
bed12
=====

The `trackc.pl.gene_track` method input formats is `BED12 <https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format/>`_.

Bed12 file description can be found from the link below: `https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format <https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format/>`_.


gtf2bed4trackc
==============
If you have installed `trackc`, you can conver GTF to bed12 using `gtf2bed4trackc` command.
the `column-4` of outfile is `gene name`

.. code-block:: shell

    gtf2bed4trackc -g GRCh38.84.gtf -o GRCh38.84.bed12

.. csv-table:: bed12-gene-name
   :file: GRCh38.84.bed12
   :header-rows: 0
   :delim: tab


gtf2bed.pl
==========
You can use `gtf2bed` convert gtf format to bed12 format.

`gtf2bed` is a perl script, can be get from the link below: `https://github.com/ExpressionAnalysis/ea-utils/blob/master/clipper/gtf2bed <https://raw.githubusercontent.com/ExpressionAnalysis/ea-utils/master/clipper/gtf2bed>`_.

.. code-block:: shell

    perl gtf2bed GRCh38.84.gtf >GRCh38.84.gtf.bed12

Below table is the output of `gtf2bed`:

.. csv-table:: bed12-transcript-id
   :file: GRCh38.84.gtf.bed12
   :header-rows: 0
   :delim: tab

please note that, the bed12 from gtf2bed.pl is based on transcript id, each row is a transcript, the `column-4` is `transcript id` not gene name


read bed12
===========

read bed12 file to pd.DataFrame for `trackc.pl.gene_track` input data

.. code-block:: python

    gene_bed12 = pd.read_table("GRCh38.84.bed12", sep="\t", header=None)
    # The naming of chromosomes may be different for different multi-group data. 
    # If you want to keep the naming of chromosomes consistent, please refer to one of the following code
    #gene_bed12[0] = gene_bed12[0].str.lstrip('chr')
    #gene_bed12[0] = 'chr' + gene_bed12[0].astype(str)
