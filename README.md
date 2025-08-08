[![Supported Python Versions](https://img.shields.io/pypi/pyversions/kif_lib)](https://pypi.org/project/kif_lib/) [![PyPI version](https://badge.fury.io/py/kif_lib.svg)](https://badge.fury.io/py/kif_lib) [![Downloads](https://pepy.tech/badge/kif_lib/month)](https://pepy.tech/project/kif_lib)

<img src="https://raw.githubusercontent.com/IBM/kif/refs/heads/main/docs/_static/kif-boxed.svg" width="96">

# Knowledge Integration Framework

KIF is a knowledge integration framework from [IBM
Research](https://research.ibm.com/).

It is based on [Wikidata](https://www.wikidata.org/) and licensed under the
[Apache-2.0 license](./LICENSE).

First time here? Check out the [quickstart
guide](https://ibm.github.io/kif/quickstart.html).

## Highlights

* KIF is an interface to query knowledge sources as if they were Wikidata.

* KIF queries are written as simple, high-level filters using entities of
  the [Wikidata data
  model](https://www.wikidata.org/wiki/Wikidata:Data_model).

* KIF can be used to query Wikidata itself or other knowledge sources,
  provided proper mappings are given.

* KIF comes with built-in mappings for [DBpedia](https://www.dbpedia.org/)
  and [PubChem RDF](https://pubchem.ncbi.nlm.nih.gov/docs/rdf).  Other
  mappings can be added programmatically.

* KIF has full support for
  [asyncio](https://docs.python.org/3/library/asyncio.html).  KIF async API
  can be used run queries asynchronously, without blocking waiting on their
  results.

## Installation

Latest release:

```shell
$ pip install kif-lib
```

Development version:

```shell
$ pip install kif-lib@git+https://github.com/IBM/kif.git
```

## Documentation

See [documentation](https://ibm.github.io/kif/).

## Examples

Click on the headings for details.

<details>
<summary>
Gets from <a href="https://www.wikidata.org/">Wikidata</a> all statements with property <a href="http://www.wikidata.org/entity/P47">shares border with (P47)</a> and value
<a href="http://www.wikidata.org/entity/Q155">Brazil (Q155)</a>.
</summary>

Using the `kif` command-line utility:

```shell
kif filter -s wdqs --property=wd.shares_border_with --value='wd.Q(155)'
```

> (**Statement** (**Item** [Argentina](http://www.wikidata.org/entity/Q414)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> (**Statement** (**Item** [Peru](http://www.wikidata.org/entity/Q419)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> (**Statement** (**Item** [Paraguay](http://www.wikidata.org/entity/Q733)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> ⋮

Using the KIF API:

```python
from kif_lib import *               # import the KIF namespace
from kif_lib.vocabulary import wd   # import the Wikidata vocabulary module

# Create a SPARQL store loaded with Wikidata mappings and optimized for WDQS.
kb = Store('wdqs', 'https://query.wikidata.org/sparql')

# Filter all statements with the given property and value.
for stmt in kb.filter(property=wd.shares_border_with, value=wd.Q(155)):
    print(stmt)
```
</details>

<details>
<summary>
Gets from <a href="https://www.wikidata.org/">Wikidata</a> and <a href="https://qlever.cs.uni-freiburg.de/api/pubchem">PubChem</a> the IRI and molecular
mass of all chemicals whose formula is H₂O.
</summary>

Using the `kif` command-line utility:

```shell
$ kif filter -s wdqs -s pubchem-sparql --select sv --subject='wd.chemical_formula("H₂O")' --property=wd.mass
```

> (**Item** [hydrogen tritium oxide](http://www.wikidata.org/entity/Q106010186)) 20.01878893 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> (**Item** [oxygen-15 atom](http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID10129877)) 17.0187 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> (**Item** [diprotium oxide](http://www.wikidata.org/entity/Q106010185)) 18.010564684 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> ⋮

Using the KIF API:

```python
# Create a mixer store combining:
# • wdqs: A SPARQL store loaded with Wikidata mappings optimized for WDQS.
# • pubchem-sparql: A SPARQL store loaded with PubChem RDF mappings.

kb = Store('mixer', [
    Store('wdqs', 'https://query.wikidata.org/sparql'),
    Store('pubchem-sparql', 'https://qlever.cs.uni-freiburg.de/api/pubchem')])

# Filter the subject and value (sv) of all statements where:
# • subject has chemical formula (P274) H₂O.
# • property is mass (P2067).

it = kb.filter_sv(subject=wd.chemical_formula('H₂O'), property=wd.mass)
for chem, mass in it:
    print(chem, mass)
```
</details>

See [examples](./examples) for more examples.

## Citation

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro
R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato
Cerqueira. ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous
Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304,
2024.

## License

Released under the [Apache-2.0 license](./LICENSE).
