import os
import sys

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
copyright = get_copyright()
extensions = [
    'myst_parser',
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
]

templates_path = ['_templates']
source_suffix = ['.rst']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
add_module_names = False

# html_theme = 'sphinx_rtd_theme'
html_theme = 'pydata_sphinx_theme'

graphviz_output_format = 'svg'
inheritance_graph_attrs = dict(
    rankdir='TB',
    ratio='compress',
)
inheritance_node_attrs = dict(
    fillcolor='lightgray',
    fontsize=10,
    ordering='out',
    # shape='ellipse',
    style='filled',
)
inheritance_edge_attrs = dict(
    dir='back',
)
