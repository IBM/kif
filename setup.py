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
    packages=[PACKAGE],
    package_data={PACKAGE: ['py.typed']},
    include_package_data=True,
    install_requires=[
        'lark',
        'more_itertools',
        'rdflib',
        'requests',
        'types-requests',
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
    keywords=NAME,
    zip_safe=True,
)
