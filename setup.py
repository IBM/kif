# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re
import setuptools

with open('Makefile.conf') as fp:
    text = fp.read()
    NAME, = re.findall(r'NAME\s*=\s*(.*)', text)
    PACKAGE, = re.findall(r'PACKAGE\s*=\s*(.*)', text)
    DESCRIPTION, = re.findall(r'DESCRIPTION\s*=\s*(.*)', text)
    AUTHOR, = re.findall(r'AUTHOR\s*=\s*(.*)', text)
    EMAIL, = re.findall(r'EMAIL\s*=\s*(.*)', text)
    URL, = re.findall(r'URL\s*=\s*(.*)', text)
    LICENSE, = re.findall(r'LICENSE\s*=\s*(.*)', text)

with open(f'{PACKAGE}/__init__.py') as fp:
    text = fp.read()
    VERSION, = re.findall(r"__version__\s*=\s*'(.*)'", text)

with open('README.md', "r") as fp:
    README = fp.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    python_requires='>=3.9',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    package_data={
        PACKAGE: ['py.typed'],
        f'{PACKAGE}.vocabulary': ['wikidata-properties.json'],
    },
    package_dir={'kif_lib': 'kif_lib'},
    include_package_data=True,
    install_requires=[
        'lark',
        'more_itertools',
        'rdflib',
        'requests',
        'types-requests',
        'typing-extensions',
    ],
    extras_require={
        'docs': [
            'myst_parser',
            'pydata_sphinx_theme',
        ],
        'tests': [
            'flake8',
            'isort',
            'mypy',
            'pytest',
            'pytest-cov',
            'pytest-mypy',
            'tox',
        ],
    },
    zip_safe=False,
)
