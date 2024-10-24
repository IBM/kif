# KIF — Knowledge Integration Framework #

KIF is a knowledge integration framework from IBM Research.  It is licensed
under the [Apache-2.0 license](./LICENSE).

First time here? Check out the [quickstart
guide](https://ibm.github.io/kif/quickstart.html).

## What? How?

KIF is a knowledge integration framework based on
[Wikidata](https://www.wikidata.org/).

* Using KIF, one can easily combine heterogeneous knowledge sources into a
  *virtual knowledge base*.  This behaves like an extended Wikidata and can
  be queried uniformly using a simple but expressive *pattern language*.

* KIF leverages [Wikidata's data
  model](https://www.wikidata.org/wiki/Wikidata:Data_model) plus
  user-defined mappings to construct a unified view of the underlying
  knowledge sources while keeping track of the context and provenance of
  their statements.

* KIF pattern language is based on Wikidata's data model and is embedded in
  Python—its constructs can be created and operated programmatically from
  within Python.

### Hello world! ###

Prints an arbitrary statement from [Wikidata](https://www.wikidata.org/):

```python
from kif_lib import *      # import KIF namespacee
kb = Store('wikidata')     # create a store pointing to Wikidata
print(next(kb.filter()))   # obtain and print one arbitrary statement
```

## Installation ##

```shell
$ pip install kif-lib
```

## Documentation ##

See [documentation](https://ibm.github.io/kif/) and [examples](./examples).


## Citation ##

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro
R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato
Cerqueira. ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous
Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304,
2024.


## License ##

Released under the [Apache-2.0 license](./LICENSE).
