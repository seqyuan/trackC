=====
gene
=====

The trackc's gene input formats is `BED12 <https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format/>`_.

the bed12 file description can be found from the link below: `https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format <https://bedtools.readthedocs.io/en/latest/content/general-usage.html#genome-file-format/>`_.

How to generate gene track bed12
=================================

gtf2bed.pl
----------
You can use gtf2bed to convert gene annotation files in gtf format to bed12 format.
`gtf2bed` 4`12444is a perl script, can be get from the link below: `https://github.com/ExpressionAnalysis/ea-utils/blob/master/clipper/gtf2bed <https://raw.githubusercontent.com/ExpressionAnalysis/ea-utils/master/clipper/gtf2bed>`_.

.. code-block:: shell

    perl gtf2bed GRCh38.84.gtf >GRCh38.84.gtf.bed12

.. csv-table:: bed12
   :file: GRCh38.84.gtf.bed12
   :header-rows: 1

Please note that, the bed12 from gtf2bed.pl is `based on transcript id`, each row is a transcript, the `column-4` is `transcript id` not gene name


