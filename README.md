# KIF — Knowledge Integration Framework #

KIF is a knowledge integration framework from IBM Research.

KIF is based on [Wikidata](https://www.wikidata.org/) and it's licensed
under the [Apache-2.0 license](./LICENSE).

First time here? Check out the [quickstart
guide](https://ibm.github.io/kif/quickstart.html).

## Highlights

* KIF can be seen as a Python interface to query Wikidata (RDF).

* KIF queries are written in the KIF pattern language, a high-level query
  language based on [Wikidata's data
  model](https://www.wikidata.org/wiki/Wikidata:Data_model).

* KIF can be used to query knowledge sources other than Wikidata,
  provided proper SPARQL mappings are given.

* KIF comes with built-in mappings for [DBpedia](https://www.dbpedia.org/)
  and [PubChem RDF](https://pubchem.ncbi.nlm.nih.gov/docs/rdf), but other
  mappings can be added programmatically as needed.

### Hello world! ###

Prints an arbitrary statement from [Wikidata](https://www.wikidata.org/):

```python
from kif_lib import *
from kif_lib.compiler.sparql.mapping.wikidata import WikidataMapping
kb = Store('sparql2', 'https://query.wikidata.org/sparql', WikidataMapping())
print(next(kb.filter()))
```

Prints an arbitrary Wikidata-like statement from
[DBpedia](https://www.dbpedia.org/):

```python
from kif_lib import *
from kif_lib.compiler.sparql.mapping.dbpedia import DBpediaMapping
kb = Store('sparql2', 'https://dbpedia.org/sparql', DBpediaMapping())
print(next(kb.filter()))
```

## Installation ##

```shell
$ pip install kif-lib
```

## Documentation ##

See [documentation](https://ibm.github.io/kif/) and [examples](./examples).


## Citation ##

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro
R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato
Cerqueira. ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous
Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304,
2024.


## License ##

Released under the [Apache-2.0 license](./LICENSE).
