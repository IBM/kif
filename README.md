# Knowledge Integration Framework #

A knowledge integration framework based on [Wikidata](https://www.wikidata.org/).

## Hello world! ##

Prints an arbitrary statement from [Wikidata](https://www.wikidata.org/):
```python
from kif_lib import Store
kb = Store('sparql', 'https://query.wikidata.org/sparql')
print(next(kb.filter()))
```

## Installation ##

```shell
$ pip install kif-lib
```

Or, for the development version:
```shell
$ git clone https://github.com/IBM/kif.git
$ cd kif
$ pip install -e .
```

## Documentation ##

See the [API documentation](https://ibm.github.io/kif/) and [examples](https://github.com/IBM/kif/tree/main/examples).

## Citation ##

[KIF: A Wikidata-Based Framework for Integrating Heterogeneous Knowledge Sources](https://arxiv.org/abs/2403.10304), arXiv, 2024.

## License ##

Released under the [Apache-2.0 license](https://github.com/IBM/kif/blob/main/LICENSE).
