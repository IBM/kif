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

See the notebooks in [examples](https://github.com/IBM/kif/tree/main/examples).

## Testing ##

Install the test dependencies:
```shell
$ make install-deps
```

Run all tests:
```shell
$ make check
```

## License ##

Released under the [Apache-2.0 license](https://github.com/IBM/kif/blob/main/LICENSE).
