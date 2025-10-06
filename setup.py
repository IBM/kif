# ** GENERATED FILE, DO NOT EDIT! **
import re
import setuptools
with open('kif_lib/__version__.py', 'r') as fp:
    text = fp.read()
    VERSION, = re.findall(r"__version__\s*=\s*'(.*)'", text)
with open('README.md', 'r') as fp:
    README = fp.read()
setuptools.setup(
    name='kif-lib',
    version=VERSION,
    description='A knowledge integration framework based on Wikidata',
    long_description=README,
    long_description_content_type='text/markdown',
    author='IBM',
    author_email='Guilherme.Lima@ibm.com',
    url='https://github.com/IBM/kif',
    license='Apache-2.0',
    classifiers=[ 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12', 'Programming Language :: Python :: 3.13', ],
    python_requires='>=3.9',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    package_data={ 'kif_lib': ['py.typed'], 'kif_lib.vocabulary.wd': ['wikidata_properties.tsv'], },
    include_package_data=True,
    package_dir={'kif_lib': 'kif_lib'},
    install_requires=[ 'httpx', 'lark', 'more_itertools', 'networkx', 'rdflib', 'types-networkx', 'typing-extensions', ],
    extras_require={
        'all': [*[ 'myst_nb', 'sphinx-rtd-theme', ],*[ 'click', 'ddgs', 'graphviz', 'jpype1', 'pandas', 'pandas-stubs', 'psutils', 'rich', 'types-click', 'types-psutils', ],*['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox']],
        'docs': [ 'myst_nb', 'sphinx-rtd-theme', ],
        'extra': [ 'click', 'ddgs', 'graphviz', 'jpype1', 'pandas', 'pandas-stubs', 'psutils', 'rich', 'types-click', 'types-psutils', ],
        'tests': ['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox'],
    },
    entry_points={'console_scripts': ['kif = kif_lib.cli:cli'], },
    zip_safe=False,
)
