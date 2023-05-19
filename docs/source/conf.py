# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import datetime
from pathlib import Path
#sys.path.insert(0, os.path.abspath('.'))

HERE = Path(__file__).parent
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath("_ext"))
#sys.path.insert(0, str(HERE.parent.parent))    
sys.path.insert(0, str(HERE / "extensions"))
package_dir = os.path.abspath(os.path.join(HERE, '..', '..', 'src'))

sys.path.insert(0, package_dir) # this way, we don't have to install squidpy

#sys.path.insert(0, os.path.abspath('../src'))
from sphinx.application import Sphinx
from sphinx_gallery.gen_gallery import DEFAULT_GALLERY_CONF
#from sphinx_gallery.directives import MiniGallery
#from docs.source.utils import ( 
#    _fetch_notebooks,
#)

# -- Project information -----------------------------------------------------

project = 'trackc'
copyright = 'seqyuan'
author = 'Zan Yuan'

# The short X.Y version
version = '0.1.1'
# The full version, including alpha/beta/rc tags
release = '0.1.1'


copyright = f"{datetime.now():%Y}, {author}"  # noqa: A001

github_org = "seqyuan"
github_repo = "trackc"
github_ref = "main"
github_nb_repo = "trackc_notebooks"
#_fetch_notebooks(repo_url=f"https://github.com/{github_org}/{github_nb_repo}")


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx_gallery.load_style",
    "sphinx_gallery.gen_gallery",
    "nbsphinx",
    "sphinxcontrib.bibtex",
    'sphinx_last_updated_by_git',  # get "last updated" from Git
    "typed_returns",
    #'sphinxcontrib.rsvgconverter',  # for SVG->PDF conversion in LaTeX output
    "IPython.sphinxext.ipython_console_highlighting",
    'sphinx_codeautolink',  # automatic links from code to documentation
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
#source_suffix = [".rst", ".ipynb"]
# Don't add .txt suffix to source files:
html_sourcelink_suffix = ''

# The master toctree document.
master_doc = 'index'
pygments_style = "sphinx"

nbsphinx_custom_formats = {
    '.pct.py': ['jupytext.reads', {'fmt': 'py:percent'}],
    '.md': ['jupytext.reads', {'fmt': 'Rmd'}],
}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.

exclude_patterns = ['Thumbs.db', 
                    '.DS_Store',
                    "auto_*/**.ipynb",
                    "auto_*/**.md5",
                    "auto_*/**.py",
                    "auto_*/**/index.rst",
                    "**.ipynb_checkpoints",
                    ]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

autosummary_generate = True
autodoc_member_order = "groupwise"
autodoc_typehints = "signature"
autodoc_docstring_signature = True
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True
napoleon_use_param = True
todo_include_todos = False



def reset_matplotlib(_gallery_conf, _fname):
    import matplotlib as mpl

    mpl.use("agg")

    import matplotlib.pyplot as plt

    plt.rcdefaults()
    mpl.rcParams["savefig.bbox"] = "tight"
    mpl.rcParams["savefig.transparent"] = True
    mpl.rcParams["figure.figsize"] = (12, 8)
    mpl.rcParams["figure.dpi"] = 96
    mpl.rcParams["figure.autolayout"] = True
                 
_root = Path(__file__).parent.parent.parent
sphinx_gallery_conf = {
    "image_scrapers": "matplotlib",
    "reset_modules": (
        "seaborn",
        reset_matplotlib,
    ),
    "filename_pattern": f"{os.path.sep}(compute_|plot_|tutorial_)",
    "examples_dirs": [_root / "examples"],
    "gallery_dirs": ["auto_examples", "tutorials"],
    "abort_on_example_error": True,
    "show_memory": True,
    "reference_url": {
        "sphinx_gallery": None,
    },
    "line_numbers": False,
    "compress_images": (
        "images",
        "thumbnails",
        "-o3",
    ),
    "remove_config_comments": True,
    "inspect_global_variables": False,
    "backreferences_dir": "gen_modules/backreferences",
    "doc_module": "squidpy",
    "download_all_examples": False,
    "show_signature": False,
    "pypandoc": {
        "extra_args": [
            "--mathjax",
        ],
        "filters": [str(_root / ".scripts" / "filters" / "strip_interpreted_text.py")],
    },
    "default_thumb_file": "docs/source/_static/img/squidpy_vertical.png",
    "plot_gallery": "'True'",  # https://github.com/sphinx-gallery/sphinx-gallery/issues/913
}

nbsphinx_thumbnails = {
    'notebooks/zoomin_heatmap': 'notebooks/zoomin_heatmap.png',
}


# bibliography
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"
bibtex_default_style = "alpha"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
#html_theme = 'sphinx_book_theme'
html_theme = 'sphinx_rtd_theme'
html_show_sphinx = False

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_logo = 'images/trackc_logo.png'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    "navigation_depth": 4
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'trackcdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'trackc.tex', 'trackc Documentation',
     'Zan Yuan', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'trackc', 'trackc Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'trackc', 'trackc Documentation',
     author, 'seqyuan', 'Genome rearrangement omics view',
     'hello'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------
# add sourcecode to path
#import sys, os
#sys.path.insert(0, os.path.abspath('../src'))
#sys.path.insert(1, '/staging/leuven/stg_00002/lcb/sdewin/Programs/anaconda3/envs/SCENIC+/lib/python3.7/site-packages')

if 'html_theme' not in globals():
    try:
        import insipid_sphinx_theme
    except ImportError:
        pass
    else:
        html_theme = 'insipid'
        html_copy_source = False
        html_permalinks_icon = '#'

#if globals().get('html_theme') == 'insipid':
    # This controls optional content in index.rst:
#    tags.add('insipid')

def setup(app: Sphinx) -> None:
    DEFAULT_GALLERY_CONF["src_dir"] = str(HERE)
    #DEFAULT_GALLERY_CONF["backreferences_dir"] = "gen_modules/backreferences"
    DEFAULT_GALLERY_CONF["download_all_examples"] = False
    DEFAULT_GALLERY_CONF["show_signature"] = False
    DEFAULT_GALLERY_CONF["log_level"] = {"backreference_missing": "info"}
    DEFAULT_GALLERY_CONF["gallery_dirs"] = ["auto_examples", "auto_tutorials"]
    DEFAULT_GALLERY_CONF["default_thumb_file"] = "docs/source/_static/img/squidpy_vertical.png"

    #app.add_config_value("sphinx_gallery_conf", DEFAULT_GALLERY_CONF, "html")
    #app.add_directive("minigallery", MiniGallery)
    app.add_css_file("css/custom.css")
    app.add_css_file("css/sphinx_gallery.css")
    app.add_css_file("css/nbsphinx.css")
    app.add_css_file("css/dataframe.css")  # had to add this manually

#setup(Sphinx)

