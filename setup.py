# ** GENERATED FILE: DO NOT EDIT! **
import itertools
import re
import setuptools
with open('kif_lib/__version__.py') as fp:
    text = fp.read()
    VERSION, = re.findall(r"__version__\s*=\s*'(.*)'", text)
with open('README.md') as fp:
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
    classifiers=[ 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12', 'Programming Language :: Python :: 3.13', 'Programming Language :: Python :: 3.14', ],
    python_requires='>=3.9',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    package_data={ 'kif_lib': ['py.typed'], },
    include_package_data=True,
    package_dir={'kif_lib': 'kif_lib'},
    install_requires=[ 'httpx', 'lark', 'more_itertools', 'networkx', 'rdflib', 'types-networkx', 'typing-extensions', ],
    extras_require={'all': [*['mkdocs'], *['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox'], *itertools.chain(*{ 'cli': [ 'click', 'rich', ], 'extra': [ 'ddgs', 'graphviz', 'jpype1', 'pandas', 'pandas-stubs', 'psutil', 'types-click', 'types-psutil', ], }.values())], 'dev': ['build', 'twine', *[*['mkdocs'], *['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox'], *itertools.chain(*{ 'cli': [ 'click', 'rich', ], 'extra': [ 'ddgs', 'graphviz', 'jpype1', 'pandas', 'pandas-stubs', 'psutil', 'types-click', 'types-psutil', ], }.values())]], 'docs': ['mkdocs'], 'tests': ['flake8', 'isort', 'mypy', 'pylint', 'pyright', 'pytest', 'pytest-asyncio', 'pytest-cov', 'pytest-mypy', 'pyupgrade', 'setuptools', 'tox'], **{ 'cli': [ 'click', 'rich', ], 'extra': [ 'ddgs', 'graphviz', 'jpype1', 'pandas', 'pandas-stubs', 'psutil', 'types-click', 'types-psutil', ], }},
    entry_points={ 'console_scripts': ['kif = kif_lib.cli:cli'], },
    zip_safe=False,
)
