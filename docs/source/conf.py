# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CAN Monitor Dashboard'
copyright = '2024, Vitor Matias'
author = 'Vitor Matias'
release = 'a1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
# sys.path.insert(0, os.path.abspath("../../"))


extensions = ['myst_parser',
              'sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'autoapi.extension']


templates_path = ['_templates']
exclude_patterns = []

autoapi_dirs = ['../../Map','../../Plot']

autodoc_typehints = 'both'

autodoc_default_flags = [
    'private-members',
    'show-inheritance',
    'members',
]

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
