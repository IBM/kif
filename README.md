# Knowledge Integration Framework #

A framework for integrating heterogeneous knowledge bases using Wikidata as
a lingua franca.

See [KIF Middleware](https://github.ibm.com/brl-kbe/kif-middleware) for the middleware
API.

## Documentation ##

See the [API documentation](https://pages.github.ibm.com/brl-kbe/kif/) and
the notebooks in [examples](./examples).

## Installation ##

```shell
$ git clone git@github.ibm.com:kcsys/kif.git
$ cd kif
$ pip install -e .
```

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
This module is released under the [Apache-2.0 license](LICENSE).