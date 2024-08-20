# Knowledge Integration Framework #

A knowledge integration framework based on [Wikidata](https://www.wikidata.org/).

It written in Python and is released as [open-source](./LICENSE).

First time here? Check out the [quickstart
guide](https://ibm.github.io/kif/quickstart.html).

For more information, see the [documentation](https://ibm.github.io/kif/)
and [examples](./examples).


## Installation ##

```shell
$ pip install kif-lib
```

## Hello world! ##

Prints an arbitrary statement from [Wikidata](https://www.wikidata.org/):

```python
from kif_lib import *      # import KIF namespacee
kb = Store('wikidata')     # create a store pointing to Wikidata
print(next(kb.filter()))   # obtain and print one arbitrary statement
```

## Citation ##

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro
R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato
Cerqueira. ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous
Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304,
2024.


## License ##

Released under the [Apache-2.0 license](./LICENSE).
