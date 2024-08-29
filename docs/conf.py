# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import os
import sys

# Make Sphinx operate directly on the sources.
sys.path.insert(0, os.path.abspath('..'))


def get_copyright():
    import datetime
    copyright = os.getenv('COPYRIGHT', 'unknown')
    if copyright.endswith('.'):
        copyright = copyright[:-1]
    end_year = datetime.date.today().year
    start_year = int(os.getenv('COPYRIGHT_START_YEAR', end_year))
    if start_year < end_year:
        return f'{start_year}-{end_year}, {copyright}'
    else:
        return f'{end_year}, {copyright}'


project = os.getenv('NAME', 'unknown')
version = os.getenv('VERSION', 'unknown')
copyright = get_copyright()
extensions = [
    'myst_nb',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
source_suffix = ['.rst']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

add_module_names = False

autodoc_content = 'both'
autodoc_class_signature = 'mixed'  # separated
autodoc_member_order = 'bysource'  # alphabetical, groupwise
autodoc_default_options = {
    # 'exclude-members': (
    #     'datatype_class,'
    #     'object_class,'
    #     'template_class,'
    #     'variable_class,'
    # ),
    'show-inheritance': True,
    'special-members': '__init__',
}

html_theme = 'sphinx_rtd_theme'
# html_theme = 'pydata_sphinx_theme'
# html_theme = 'sphinx_immaterial'

graphviz_output_format = 'svg'
inheritance_graph_attrs = {
    'rankdir': 'TB',
    'ratio': 'compress',
}
inheritance_node_attrs = {
    'fillcolor': 'lightgray',
    'fontsize': 10,
    'ordering': 'out',
    # 'shape': 'ellipse',
    'style': 'filled',
}
inheritance_edge_attrs = {
    'dir': 'back',
}
