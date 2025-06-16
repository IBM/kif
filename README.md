<img src="https://raw.githubusercontent.com/IBM/kif/refs/heads/main/docs/_static/kif-boxed.svg" width="96">

# Knowledge Integration Framework #

KIF is a knowledge integration framework from [IBM Research](https://research.ibm.com/).

KIF is based on [Wikidata](https://www.wikidata.org/) and it's licensed
under the [Apache-2.0 license](./LICENSE).

First time here? Check out the [quickstart
guide](https://ibm.github.io/kif/quickstart.html).

## Highlights

* KIF is an interface to query knowledge sources as if they were Wikidata.

* KIF queries are written in the KIF pattern language, which is based on
  [Wikidata's data model](https://www.wikidata.org/wiki/Wikidata:Data_model).

* KIF can be used to query Wikidata itself or other knowledge sources,
  provided proper SPARQL mappings are given.

* KIF comes with built-in mappings for [DBpedia](https://www.dbpedia.org/)
  and [PubChem RDF](https://pubchem.ncbi.nlm.nih.gov/docs/rdf).  Other
  mappings can be added programmatically.

## Installation ##

```shell
$ pip install kif-lib
```

## Documentation ##

See [documentation](https://ibm.github.io/kif/) and [examples](./examples).

### Hello world! ###

#### A simple filter ###

Gets from [Wikidata](https://www.wikidata.org/) all statements
with property [shares border with (P47)](http://www.wikidata.org/entity/P47)
and value [Brazil (Q155)](http://www.wikidata.org/entity/Q155):

```python
from kif_lib import *
from kif_lib.vocabulary import wd
kb = Store('wdqs')
for stmt in kb.filter(property=wd.shares_border_with, value=wd.Q(155)):
    print(stmt)
```

Alternatively, using the `kif` command-line utility:

```shell
$ kif filter -s wdqs --property=wd.shares_border_with --value='wd.Q(155)'
```

#### A more complex filter ####

Gets from [Wikidata](https://www.wikidata.org/) and
[PubChem RDF](https://qlever.cs.uni-freiburg.de/api/pubchem) the IRI and
mass value of all chemicals whose formula is H₂O.

```python
kb = Store('mixer', [           # Mixes stmts from:
    Store('wdqs'),              # - Wikidata (WDQS)
    Store('pubchem-sparql')     # - PubChem RDF (QLever's public endpoint)
])
it = kb.filter_sv(                       # Get subject-value of stmts where:
    subject=wd.chemical_formula('H₂O'),  # - subject has chem. formula H₂O
    property=wd.mass)                    # - property is mass (P2067)
for (chem, mass) in it:
    print(chem.iri.content, mass.amount)
```

Alternatively, using the `kif` command-line utility:

```shell
$ kif filter -s wdqs -s pubchem-sparql  'wd.chemical_formula("H₂O")' wd.mass --select sv
```

## Citation ##

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro
R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato
Cerqueira. ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous
Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304,
2024.


## License ##

Released under the [Apache-2.0 license](./LICENSE).
