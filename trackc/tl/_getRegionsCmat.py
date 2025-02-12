import logging
from typing import List, Sequence, Union

import cooler
import numpy as np
import pandas as pd


class GenomeRegion:
    region = None
    chrom = None
    start = None
    end = None
    fetch_start = None
    fetch_end = None
    length = None
    isReverse = False

    def __init__(self, region: str):
        self.region = region
        tmp = region.split(":")
        self.chrom = tmp[0]
        if len(tmp) == 2:
            self.start = int(tmp[1].split("-")[0])
            self.end = int(tmp[1].split("-")[1])
            if self.start > self.end:
                self.isReverse = True
                self.fetch_start = self.end
                self.fetch_end = self.start
            else:
                self.fetch_start = self.start
                self.fetch_end = self.end
            self.length = abs(self.start - self.end)

    def fetchRegion(self):
        fetch_r = self.chrom
        if self.fetch_start != None:
            fetch_r = fetch_r + ":" + str(self.fetch_start) + "-" + str(self.fetch_end)
        return fetch_r

    def GenomeRegion2df(self):
        """
        region4coolFetch = self.chrom + ":" + str(self.start) + '-' + str(self.end)
        if self.start == None:
            region4coolFetch = self.chrom
        else:
            if self.start > self.end:
                region4coolFetch = self.chrom + ":" + str(self.end) + '-' + str(self.start)
        """
        region4coolFetch = self.fetchRegion()

        df = pd.DataFrame(
            {
                "chrom": [self.chrom],
                "start": [self.start],
                "end": [self.end],
                "isReverse": [self.isReverse],
                "fetch_start": [self.fetch_start],
                "fetch_end": [self.fetch_end],
                "region4coolFetch": [region4coolFetch],
            },
            index=[self.region],
        )

        return df


class RegionsCmat:
    def __init__(
        self, cmat: np.array, row_regions: pd.DataFrame, col_regions: pd.DataFrame
    ):
        self.cmat = cmat
        self.row_regions = row_regions
        self.col_regions = col_regions


# import extractContactRegions as subsetContactRegions


def extractContactRegions(
    clr: Union[cooler.Cooler, str],
    balance: bool = False,
    # divisive_weights = None,
    row_regions: Union[Sequence[str], str, None] = None,
    col_regions: Union[Sequence[str], str, None] = None,
) -> RegionsCmat:
    """
    Extract a set of regions matrix from the cool format Hi-C matrix.

    The extracted matrix will splice intra and inter region interaction according to
    the given order and direction of the regions.

    Parameters
    ----------
    clr: `cooler.Cooler` | `str`
        cool format Hi-C matrix (https://github.com/open2c/cooler) or cool file path

        `cooler.Cooler` e.g. GM12878=cooler.Cooler('./GM12878.chr18.mcool::/resolutions/50000')

        `str` e.g. 'GM12878.chr18.mcool::/resolutions/50000' or 'GM12878.chr18.cool'

    balance: `bool`
        The ``'balance'`` parameters of ``coolMat.matrix(balance=False).fetch('chr6:119940450-123940450')``
    row_regions: `str` | `str list` | None.
        The subset matrix row genome regions.
        e.g. ``"chr6:1000000-2000000"``, e.g. ``["chr6:1000000-2000000", "chr3:5000000-4000000", "chr5"]``
        The start can be larger than the end (e.g. ``"chr6:2000000-1000000"``),
        which means you want to get the reverse region contact matrix
    col_regions: `str` | `str list` | None.
        The subset matrix col genome regions, default is ``None``, which means the sample region as ``row_regions``

    Returns:
    --------
        :class:`~trackc.tl.RegionsCmat`
            row_regions and col_regions contact matrix object

    Example
    -------
    >>> import trackc as tc
    >>> import cooler

    >>> mat1 = tc.tl.extractContactRegions(clr='GM12878.chr18.mcool::/resolutions/50000', row_regions="18:45000000-78077248")
    >>> GM12878 = cooler.Cooler('./GM12878.chr18.mcool::/resolutions/50000')
    >>> mat2 = tc.tl.extractContactRegions(clr=GM12878, row_regions=["18:61140000-63630000", "18:74030000-77560000"], col_regions="18:47340000-50370000")
    >>> print(mat2.cmap.shape)
    >>> print(mat2.row_regions)
    >>> print(mat2.col_regions)
    """
    # divisive_weights: bool, optional
    #    Force balancing weights to be interpreted as divisive (True) or
    #    multiplicative (False). Weights are always assumed to be
    #    multiplicative by default unless named KR, VC or SQRT_VC, in which
    #    case they are assumed to be divisive by default.

    # -------
    if isinstance(row_regions, list):
        row_GenomeRegions = pd.concat(
            [GenomeRegion(i).GenomeRegion2df() for i in row_regions]
        )
    else:
        row_GenomeRegions = GenomeRegion(row_regions).GenomeRegion2df()

    if col_regions == None:
        col_GenomeRegions = row_GenomeRegions.copy()
    else:
        if isinstance(col_regions, list):
            col_GenomeRegions = pd.concat(
                [GenomeRegion(i).GenomeRegion2df() for i in col_regions]
            )
        else:
            col_GenomeRegions = GenomeRegion(col_regions).GenomeRegion2df()

    # ------
    if isinstance(clr, str):
        clr = cooler.Cooler(clr)

    region_mat_dic = {}
    for _, row_row in row_GenomeRegions.iterrows():
        for _, col_row in col_GenomeRegions.iterrows():
            row_col_region_cmat = clr.matrix(balance=balance).fetch(
                row_row["region4coolFetch"], col_row["region4coolFetch"]
            )
            if row_row["isReverse"] == True:
                row_col_region_cmat = np.flip(row_col_region_cmat, 0)
            if col_row["isReverse"] == True:
                row_col_region_cmat = np.flip(row_col_region_cmat, 1)

            region_mat_dic[
                "{0}__{1}".format(
                    row_row["region4coolFetch"], col_row["region4coolFetch"]
                )
            ] = row_col_region_cmat

    vstack_list = [None] * row_GenomeRegions.shape[0]
    hstack_list = [None] * col_GenomeRegions.shape[0]

    for i, row_region in enumerate(row_GenomeRegions["region4coolFetch"].to_list()):
        for ii, col_region in enumerate(
            col_GenomeRegions["region4coolFetch"].to_list()
        ):
            hstack_list[ii] = region_mat_dic["{0}__{1}".format(row_region, col_region)]

        vstack_list[i] = np.hstack(tuple(hstack_list))

    cMat = np.vstack(tuple(vstack_list))

    ####
    row_GenomeRegions["cbins"] = 0
    col_GenomeRegions["cbins"] = 0

    row_index = row_GenomeRegions.index.to_list()
    col_index = col_GenomeRegions.index.to_list()

    # print(row_index)
    # print(col_index)

    for i in row_index:
        for ii in col_index:
            cmat_shape = region_mat_dic[
                "{0}__{1}".format(
                    row_GenomeRegions.loc[i, "region4coolFetch"],
                    col_GenomeRegions.loc[ii, "region4coolFetch"],
                )
            ].shape

            row_GenomeRegions.loc[i, "cbins"] = cmat_shape[0]
            col_GenomeRegions.loc[ii, "cbins"] = cmat_shape[1]

    # print(col_GenomeRegions)
    row_GenomeRegions["chrom"] = row_GenomeRegions["chrom"].astype(str)
    col_GenomeRegions["chrom"] = col_GenomeRegions["chrom"].astype(str)
    # row_GenomeRegions['fetch_start'] = row_GenomeRegions['fetch_start'].astype(int)
    # col_GenomeRegions['fetch_start'] = col_GenomeRegions['fetch_start'].astype(int)

    r_l_regions_cMat = RegionsCmat(
        cmat=cMat, row_regions=row_GenomeRegions, col_regions=col_GenomeRegions
    )

    return r_l_regions_cMat


# import extractCisRegion as subsetCisRegion


def extractCisContact(
    clr: Union[cooler.Cooler, str],
    region: str,
    extend: int = 0,
    balance: bool = False,
    # divisive_weights = None,
) -> np.array:
    """
    Extract cis contact matrix from the cool or mcool format Hi-C matrix.

    Parameters
    ----------
    clr: `cooler.Cooler` | `str`
        cool format Hi-C matrix (https://github.com/open2c/cooler) or cool file path

        `cooler.Cooler` e.g. GM12878=cooler.Cooler('./GM12878.chr18.mcool::/resolutions/50000')

        `str` e.g. 'GM12878.chr18.mcool::/resolutions/50000' or 'GM12878.chr18.cool'
    region: `str`
        The subset matrix row genome regions
        eg. ``"chr6:1000000-2000000"`` or ``chr6``

    extend: `int`
        contact map extend to start and end position
    balance: `bool`
        The ``'balance'`` parameters of ``coolMat.matrix(balance=False).fetch('chr6:119940450-123940450')``

    Returns:
    --------
    contact matrix: np.array
        matrix start with top-left

    Example
    -------
    >>> import trackc as tc
    >>> import cooler
    >>> mat1 = tc.tl.extractCisContact(clr='GM12878.chr18.mcool::/resolutions/50000', region="18:45000000-78077248")
    >>> GM12878 = cooler.Cooler('./GM12878.chr18.mcool::/resolutions/50000')
    >>> mat2 = tc.tl.extractCisContact(clr=GM12878, region="18:45000000-78077248")
    >>> print(mat2.shape)
    """

    if isinstance(clr, str):
        clr = cooler.Cooler(clr)

    resolution = clr.binsize
    genome_region = GenomeRegion(region)

    if genome_region.chrom not in clr.chromsizes:
        print(genome_region.chrom, " is not a chrom in the cool matrix")
        if genome_region.chrom.startswith("chr"):
            genome_region.chrom = genome_region.chrom.lstrip("chr")
        else:
            genome_region.chrom = "chr" + genome_region.chrom
        print(f"{genome_region.chrom} instead")

    maxChromL = clr.chromsizes[genome_region.chrom]

    # ------
    if genome_region.fetch_start != None:
        genome_region.fetch_start = genome_region.fetch_start - extend * resolution
        if genome_region.fetch_start < 0:
            # genome_region.fetch_start = 0
            logging.error("Error: Extend start is less than 0, set extend=0 is ok\n")
            # sys.exit(1)

        genome_region.fetch_end = genome_region.fetch_end + extend * resolution
        if genome_region.fetch_end > maxChromL:
            # genome_region.fetch_end = maxChromL
            logging.error(
                "Error: extend is larger than chrom length, set extend=0 is ok\n"
            )
            # sys.exit(1)

    df = clr.matrix(balance=balance).fetch(genome_region.fetchRegion())
    return df
