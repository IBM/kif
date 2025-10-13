[![Supported Python Versions](https://img.shields.io/pypi/pyversions/kif_lib)](https://pypi.org/project/kif_lib/) [![PyPI version](https://badge.fury.io/py/kif_lib.svg)](https://badge.fury.io/py/kif_lib) [![Downloads](https://pepy.tech/badge/kif_lib/month)](https://pepy.tech/project/kif_lib)

<img src="https://raw.githubusercontent.com/IBM/kif/refs/heads/main/docs/_static/kif-boxed.svg" width="96">

# Knowledge Integration Framework

KIF is a knowledge integration framework from [IBM Research](https://research.ibm.com/).

It is based on [Wikidata](https://www.wikidata.org/) and licensed under the [Apache-2.0 license](./LICENSE).

First time here? Check out the [quickstart guide](https://ibm.github.io/kif/quickstart.html).

## Highlights

* KIF is an interface to query knowledge sources as if they were Wikidata.

* KIF queries are written as simple, high-level filters using entities of the [Wikidata data model](https://www.wikidata.org/wiki/Wikidata:Data_model).

* KIF can be used to query Wikidata itself or other knowledge sources, provided proper mappings are given.

* KIF comes with built-in mappings for [DBpedia](https://www.dbpedia.org/), [FactGrid](https://database.factgrid.de/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), and [UniProt](https://www.uniprot.org/), among others.  New mappings can be added programmatically.

* KIF has full support for [asyncio](https://docs.python.org/3/library/asyncio.html).  KIF async API can be used run queries asynchronously, without blocking waiting on their results.

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
Gets from <a href="https://www.wikidata.org/">Wikidata</a> all statements with property <a href="http://www.wikidata.org/entity/P47">shares border with (P47)</a> and value <a href="http://www.wikidata.org/entity/Q155">Brazil (Q155)</a>.
</summary>
<br/>

<b>KIF CLI</b>

```shell
kif filter -s wikidata --property=wd.shares_border_with --value='wd.Q(155)'
```

> (**Statement** (**Item** [Argentina](http://www.wikidata.org/entity/Q414)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> (**Statement** (**Item** [Peru](http://www.wikidata.org/entity/Q419)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> (**Statement** (**Item** [Paraguay](http://www.wikidata.org/entity/Q733)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))) <br/>
> ⋮

<b>KIF API</b>

```python
from kif_lib import *               # import the KIF namespace
from kif_lib.vocabulary import wd   # import the Wikidata vocabulary module

# Create a SPARQL store loaded with Wikidata mappings and optimized for WDQS.
kb = Store('wikidata', 'https://query.wikidata.org/sparql')

# Filter all statements with the given property and value.
for stmt in kb.filter(property=wd.shares_border_with, value=wd.Q(155)):
    print(stmt)
```
</details>

<details>
<summary>
Counts the number of <a href="http://www.wikidata.org/entity/Q7432">species (Q7432)</a> in <a href="https://www.uniprot.org/">UniProt</a>.
</summary>
<br/>

<b>KIF CLI</b>

```shell
$ kif count -s uniprot --select s --property=wd.taxon_rank --value=wd.species
```

> 2182677

<b>KIF API</b>

```python
# Create a SPARQL store loaded with UniProt mappings.
kb = Store('uniprot', 'https://sparql.uniprot.org/sparql')

# Count the number of distinct subjects of statements with the given property and value.
n = kb.count_s(property=wd.taxon_rank, value=wd.species)
print(n)
```
</details>

<details>
<summary>
Gets from <a href="https://www.wikidata.org/">Wikidata</a> and <a href="https://qlever.cs.uni-freiburg.de/api/pubchem">PubChem</a> the IRI and molecular mass of all chemicals whose formula is H₂O.
</summary>
</br>

<b>KIF CLI</b>

```shell
$ kif filter -s wikidata -s pubchem --select sv --subject='wd.chemical_formula("H₂O")' --property=wd.mass
```

> (**Item** [hydrogen tritium oxide](http://www.wikidata.org/entity/Q106010186)) 20.01878893 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> (**Item** [oxygen-15 atom](http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID10129877)) 17.0187 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> (**Item** [diprotium oxide](http://www.wikidata.org/entity/Q106010185)) 18.010564684 [dalton](http://www.wikidata.org/entity/Q483261) <br/>
> ⋮

<b>KIF API</b>

```python
# Create a mixer store combining:
# • wikidata: A SPARQL store loaded with Wikidata mappings optimized for WDQS.
# • pubchem: A SPARQL store loaded with PubChem RDF mappings.

kb = Store('mixer', [
    Store('wikidata', 'https://query.wikidata.org/sparql'),
    Store('pubchem', 'https://qlever.cs.uni-freiburg.de/api/pubchem')])

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

Guilherme Lima, João M. B. Rodrigues, Marcelo Machado, Elton Soares, Sandro R. Fiorini, Raphael Thiago, Leonardo G. Azevedo, Viviane T. da Silva, Renato Cerqueira.  2024.  ["KIF: A Wikidata-Based Framework for Integrating Heterogeneous Knowledge Sources"](https://arxiv.org/abs/2403.10304), arXiv:2403.10304, 2024.

### Related Papers

Marcelo Machado, João P. P. Campos, Guilherme Lima, Viviane T. da Silva.  2025.  "KIF-QA: Using Off-the-shelf LLMs to Answer Simple Questions over Heterogeneous Knowledge Bases".  In Proc. 5th Wikidata Workshop co-located with the 24th Semantic Web Conference (ISWC 2025), Nara, Japan, November 2-6, 2025. (To be published)

Marcelo Machado, João M. B. Rodrigues, Guilherme Lima, Sandro R. Fiorini, Viviane T. da Silva. 2024. ["LLM Store: Leveraging Large Language Models as Sources of Wikidata-Structured Knowledge"](https://ceur-ws.org/Vol-3853/paper6.pdf). In Joint Proc. 2nd Workshop on Knowledge Base Construction from Pre-Trained Language Models (KBC-LM 2024) and the 3rd Challenge on Language Models for Knowledge Base Construction (LM-KBC 2024) co-located with the 23nd International Semantic Web Conference (ISWC 2024), Baltimore, USA, November 12, 2024.  (Best paper)


## License

Released under the [Apache-2.0 license](./LICENSE).
