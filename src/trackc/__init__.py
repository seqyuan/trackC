# the actual API
from trackc import tl, pl, pa
from trackc.gs import (
    make_spec,
    tenon,
    savefig
)

__all__ = [
    "tl",
	"pl",
    "pa",
    "make_spec",
    "tenon"
]

import sys
sys.modules.update({f'{__name__}.{m}': globals()[m] for m in ['tl', 'pl', 'pa']})
from ._utils import annotate_doc_types
annotate_doc_types(sys.modules[__name__], 'trackc')
del sys, annotate_doc_types
