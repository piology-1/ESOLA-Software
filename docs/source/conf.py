import os
import sys

# pip install sphinx
# pip install sphinx_rtd_theme
# pip install rst2pdf

# Set the path to the root directory of your project
sys.path.insert(0, os.path.abspath('..'))


# sys.path.insert(0, os.getcwd() + "/backend")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ESOLA Code Documentation'
copyright = '2023, Pius Großmann (Piology) and Leon Merk (Lenox)'
author = 'Pius Großmann (Piology) and Leon Merk (Lenox)'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'rst2pdf.pdfbuilder'
]

# Add pdf generation settings
pdf_documents = [('index', u'ESOLA', u'Code Documentation',
                  u'Pius Großmann (Piology) and Leon Merk (Lenox)'), ]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for LaTeX output ------------------------------------------------
# https://www.sphinx-doc.org/en/master/latex.html

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '12pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'\usepackage{amsmath}',
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
