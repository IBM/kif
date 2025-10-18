![KIF](https://raw.githubusercontent.com/IBM/kif/refs/heads/main/docs/_static/kif-b.svg#only-light)
![KIF](https://raw.githubusercontent.com/IBM/kif/refs/heads/main/docs/_static/kif-w.svg#only-dark)

---

# Knowledge Integration Framework

KIF is a Python framework for knowledge integration from [IBM Research](https://research.ibm.com/).

It is based on [Wikidata](https://www.wikidata.org/) and licensed under the
[Apache-2.0
license](https://raw.githubusercontent.com/IBM/kif/refs/heads/main/LICENSE).

First time here? Check out the [quickstart guide](quickstart.md).

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/kif_lib)](https://pypi.org/project/kif_lib/) [![PyPI version](https://badge.fury.io/py/kif_lib.svg)](https://badge.fury.io/py/kif_lib) [![Downloads](https://pepy.tech/badge/kif_lib/month)](https://pepy.tech/project/kif_lib)

---

Install KIF using pip:

```shell
$ pip install kif-lib
```

Use KIF to query [Wikidata](https://www.wikidata.org/):

```pycon
>>> from kif_lib import Store
>>> from kif_lib.vocabulary import wd
>>> kb = Store('wikidata')
>>> next(kb.filter(subject=wd.Alan_Turing, property=wd.doctoral_advisor))
Statement(Item(IRI('http://www.wikidata.org/entity/Q7251')), ValueSnak(...))
```

Or, via KIF CLI (the command-line interface):

```shell
$ pip install kif-lib[cli]    # KIF CLI is an optional dependency
$ kif filter --subject=wd.Alan_Turing --property=wd.doctoral_advisor
```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

KIF can also be used to query other knowledge sources.  Here is a similar query over [DBpedia](https://www.dbpedia.org/) (note the `-s dbpedia` switch):

```shell
$ kif filter -s dbpedia --subject=db.Alan_Turing --property=wd.doctoral_advisor
```

> (**Statement** (**Item** [dbr:Alan_Turing](http://dbpedia.org/resource/Alan_Turing)) (**ValueSnak** (**Property** [dbo:doctoralAdvisor](http://dbpedia.org/ontology/doctoralAdvisor)) (**Item** [dbr:Alonzo_Church](http://dbpedia.org/resource/Alonzo_Church))))

The result is a stream of Wikidata-like statements containing DBpedia entities.

## Features

* KIF allows one to query knowledge sources as if they were Wikidata.

* KIF queries are written as simple, high-level filters using entities of the [Wikidata data model](https://www.wikidata.org/wiki/Wikidata:Data_model), such as items, properties, quantities, snaks, statements, etc.

* KIF can be used to query Wikidata itself or other knowledge sources, provided proper mappings are given.

* KIF comes with built-in mappings for [DBpedia](https://www.dbpedia.org/), [FactGrid](https://database.factgrid.de/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), and [UniProt](https://www.uniprot.org/), among others; new mappings can be added programmatically.

* KIF has full support for [asyncio](https://docs.python.org/3/library/asyncio.html).  KIF async API can be used run queries asynchronously, without blocking waiting on their results.

## Installation

To install the KIF library, use:

```shell
$ pip install kif-lib
```

To include KIF CLI, use:

```shell
$ pip install kif-lib[cli]
```

To include all extras, use:

```shell
$ pip install kif-lib[extra]
```

## Documentation

KIF documentation is available at [https://ibm.github.io/kif/](https://ibm.github.io/kif/).

For a primer on KIF, see the [quickstart guide](quickstart.md).

## Dependencies

Required:

* `httpx` - HTTP support.
* `lark` - Parsing.
* `more_itertools` - Extra itertools.
* `networkx` - Graph algorithms.
* `rdflib` - RDF support.
* `typing-extensions` - Typing backports.

KIF CLI (optional):

* `click` - Option parsing. *(Optional, with `kif-lib[cli]`)*
* `rich` - Rich terminal support.  *(Optional, with `kif-lib[cli]`)*

Extra (optional):

* `graphviz` - Graph drawing. *(Optional, with `kif-lib[extra]`)*
* `jpype1` - Java support. *(Optional, with `kif-lib[extra]`)*
* `pandas` - CSV/DataFrame support. *(Optional, with `kif-lib[extra]`)*
* `psutil` - Process information. *(Optional, with `kif-lib[extra]`)*

## Citation

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato Cerqueira.  2024.  ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304, 2024.
