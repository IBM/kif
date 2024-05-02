# *** GENERATED FILE, DO NOT EDIT! ***
import re
import setuptools
with open('kif_lib/__init__.py') as fp:
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
    python_requires='>=3.9',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    package_data={ 'kif_lib': ['py.typed'], 'kif_lib.vocabulary': ['wikidata_properties.json'], },
    include_package_data=True,
    package_dir={'kif_lib': 'kif_lib'},
    install_requires=[ 'lark', 'more_itertools', 'rdflib', 'requests', 'types-requests', 'typing-extensions', ],
    extras_require={
        'docs': [ 'myst_parser', 'pydata_sphinx_theme', ],
        'tests': ['flake8', 'isort', 'mypy', 'pytest', 'pytest-cov', 'pytest-mypy', 'tox'],
    },
    zip_safe=False,
)
