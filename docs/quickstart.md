# Quickstart

We start by importing the [Store][kif_lib.Store] constructor from the KIF library:

```pycon
>>> from kif_lib import Store
```

We'll also need the [Wikidata](https://www.wikidata.org/) vocabulary module [wd][kif_lib.vocabulary.wd]:

```pycon
>>> from kif_lib.vocabulary import wd
```

Now, let's create a KIF store pointing to the official [Wikidata query service](https://query.wikidata.org/):

```pycon
>>> kb = Store('wikidata')
```

A KIF **store** is an interface to a knowledge source.  It allows us to query the source as if it were Wikidata and obtain Wikidata-like statements as a result.

The store `kb` we just created is an interface to Wikidata itself.  We can use it, for example, to fetch from Wikidata three statements about [Brazil (Q155)](http://www.wikidata.org/entity/Q155):

```pycon
>>> it = kb.filter(subject=wd.Brazil, limit=3)
>>> for stmt in it:
>>>    print(stmt)
Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P47'), ItemDatatype()), Item(IRI('http://www.wikidata.org/entity/Q414'))))
Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P571'), TimeDatatype()), Time(datetime.datetime(1822, 9, 7, 0, 0, tzinfo=datetime.timezone.utc), 11, 0, Item(IRI('http://www.wikidata.org/entity/Q1985727')))))
Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P37'), ItemDatatype()), Item(IRI('http://www.wikidata.org/entity/Q5146'))))
```

!!! note

    If you run the above code in Jupyter and use `display()` instead of `print()`, then the three statements will be pretty-printed as follows:

    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))<br/>
    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 7 September 1822))<br/>
    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Portuguese](http://www.wikidata.org/entity/Q5146))))

    From now on, we'll use the pretty-printed ([S-expression](https://en.wikipedia.org/wiki/S-expression)) format to display statements.

The **statement** is the basic unit of information in KIF.  It stands for an assertion and consists of two parts: a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  The snak associates a property with a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

This statement stands for the assertion "Brazil shares border with Argentina".  Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates the property [shares border with (P47)](http://www.wikidata.org/entity/P47) with the value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).

## Data model

KIF data-model objects, such as statements and their components, are immutable and are built using the data-model object constructors (see the [data model guide](guides/data_model.md)).  For instance, we can construct the statement "Brazil shares border with Argentina" as follows:

```pycon
>>> from kif_lib import Item, Property, Statement, ValueSnak
>>> Brazil = Item('http://www.wikidata.org/entity/Q155')
>>> shares_border_with = Property('http://www.wikidata.org/entity/P47')
>>> Argentina = Item('http://www.wikidata.org/entity/Q414')
>>> stmt = Statement(Brazil, ValueSnak(shares_border_with, Argentina))
>>> stmt
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

Alternatively, we can apply the property object `shares_border_with` as if it were a Python function to the arguments `Brazil` and `Argentina` to obtain exactly the same statement:

```pycon
>>> stmt_alt = shares_border_with(Brazil, Argentina)
>>> stmt_alt
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

!!! note

    Data-model object identity is completely determined by the objects' contents.  That is, two data-model objects constructed from the same arguments are equal.  Thus, `(stmt == stmt_alt) == True` above.

### Vocabulary

KIF comes with built-in vocabulary modules that ease the construction of entities in a given namespace.  For instance, instead of writing their full IRIs, we can use the convenience functions [wd.Q][kif_lib.vocabulary.wd.Q] and [wd.P][kif_lib.vocabulary.wd] available in the Wikidata vocabulary module [wd][kif_lib.vocabulary.wd] to construct the items [Brazil (Q155)](http://www.wikidata.org/entity/) and [Argentina (Q414)](http://www.wikidata.org/entity/Q414) and the property [shares border with (P47)](http://www.wikidata.org/entity/P47) more succinctly as follows:

```pycon
>>> from kif_lib.vocabulary import wd
>>> Brazil = wd.Q(155)
>>> Brazil
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))

```pycon
>>> Argentina = wd.Q(414)
>>> Argentina
```

> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))

```pycon
>>> shares_border_with = wd.P(47)
>>> shares_border_with
```

> (**Property** [shares border with](http://www.wikidata.org/entity/P47))

As before, we can apply `shares_border_with` to `Brazil` and `Argentina` to obtain the statement "Brazil shares border with Argentina":

```pycon
>>> shares_border_with(Brazil, Argentina)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

The [wd][kif_lib.vocabulary.wd] vocabulary module defines symbolic aliases for some popular entities.  For instance, instead of writing `wd.Q(155)` and `wd.Q(414)` for Brazil and Argentina, we can write `wd.Brazil` and `wd.Argentina`.  Similarly, instead of writing `wd.P(47)` for "shares border with", we can write `wd.shares_border_with`.  Almost all Wikidata properties have symbolic aliases defined in [wd][kif_lib.vocabulary.wd].

!!! note

    Besides [wd][kif_lib.vocabulary.wd], KIF comes with the vocabulary modules [db][kif_lib.vocabulary.db] for [DBpedia](https://www.dbpedia.org/), [fg][kif_lib.vocabulary.fg] for [FactGrid](https://database.factgrid.de/), [pc][kif_lib.vocabulary.pc] for [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [up][kif_lib.vocabulary.up] for [UniProt](https://www.uniprot.org/), among others.

## Store

Let's now turn to the [Store][kif_lib.Store] API.

As we said before, a KIF store is an interface to a knowledge source (typically but not necessarily a knowledge graph).  The [Store][kif_lib.Store] constructor is used to create a store.  It takes as first argument the name of the store plugin to instantiate.  The remaining arguments are passed to the store plugin unmodified.  For instance:

```pycon
>>> kb = Store('wikidata')
```

This instantiates and assigns to `kb` a new store using the plugin `wikidata`, which creates a [SPARQL store][kif_lib.store.SPARQL_Store] loaded with the Wikidata SPARQL mappings and targeted at the official Wikidata SPARQL endpoint.  ([SPARQL](https://en.wikipedia.org/wiki/SPARQL) is the query language of [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework), a standard format for knowledge graphs.)

Alternatively, we could have specified the target endpoint explicitly, as the second argument to the [Store()][kif_lib.Store] call:

```pycon
>>> kb = Store('wikidata', 'https://query.wikidata.org/sparql')
```

!!! note

    The available store plugins can be shown using KIF CLI:

    ```
    $ kif --show-pluings --store
    ```

## Filter

The basic store operation is the *filter*.

The call [`kb.filter(...)`][kif_lib.Store.filter] searches for statements in `kb` matching the constraints `...`.  The result is a (lazy) iterator which when advanced produces the matched statements.  For example:

```pycon
>>> kb = Store('wikidata')
>>> it = kb.filter(subject=wd.Alan_Turing)
>>> next(it)
```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

If no `limit` argument is given to [kb.filter()][kif_lib.Store.filter], the returned iterator will eventually produce all matching statements.  For instance, iterator `it` above will produce every statement about [Alan Turing (Q7251)](http://www.wikidata.org/entity/Q7251) in Wikidata before it is exhausted.

### Basic filters

We can filter statements by specifying any combination of *subject*, *property*, *value* (or *snak*) to match.  None of these are required though.  For example:

```pycon
>>> # (1) Match any statement whatsoever:
>>> next(kb.filter())

>>> # (2) Match statements with subject "water":
>>> next(kb.filter(subject=wd.water))

>>> # (3) Match statements with snak "place of birth is Athens":
>>> next(kb.filter(snak=wd.place_of_birth(wd.Athens))

>>> # (4) Match statements with property "official language":
>>> next(kb.filter(property=wd.official_language))

>>> # (5) Match statements with value "733 kilograms":
>>> next(kb.filter(value=733@wd.kilogram))

>>> # (6) Match statements with subject "Brazil" and
>>> #     snak "shares border with Argentina":
>>> next(kb.filter(subject=wd.Brazil, snak=wd.shares_border_with(wd.Argentina)))

>>> # (7) Match statements with subject "Brazil" and
>>> #     snak "shares border with Chile":
>>> next(kb.filter(subject=wd.Brazil, snak=wd.shares_border_with(wd.Chile)))
StopIteration # *** ERROR: iterator is empty (no such statement)
```

> `(1)` (**Statement** (**Item** [lion](http://www.wikidata.org/entity/Q140)) (**ValueSnak** (**Property** [parent taxon](http://www.wikidata.org/entity/P171)) (**Item** [Panthera](http://www.wikidata.org/entity/Q127960))))<br/>
> `(2)` (**Statement** (**Item** [water](http://www.wikidata.org/entity/Q283)) (**ValueSnak** (**Property** [chemical formula](http://www.wikidata.org/entity/P274)) "H₂O"))<br/>
> `(3)` (**Statement** (**Item** [Socrates](http://www.wikidata.org/entity/Q913)) (**ValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19)) (**Item** [Athens](http://www.wikidata.org/entity/Q1524))))<br/>
> `(4)` (**Statement** (**Item** [Peru](http://www.wikidata.org/entity/Q419)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Spanish](http://www.wikidata.org/entity/Q1321))))<br/>
> `(5)` (**Statement** (**Item** [Voyager 1](http://www.wikidata.org/entity/Q48469)) (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) 733 [kilogram](http://www.wikidata.org/entity/Q11570)))<br/>
> `(6)` (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

!!! note

    In example (3) above, `wd.place_of_birth(wd.Athens)` is another way of constructing `ValueSnak(wd.place_of_birth, wd.Athens)`, that is, the [ValueSnak][kif_lib.ValueSnak] object with property [place of birth (P19)](http://www.wikidata.org/entity/P19) and value [Athens (Q1524)](http://www.wikidata.org/entity/Q1524).  In example (5), `733@wd.kilogram` is another way of constructing `Quantity(733, wd.kilogram)`, that is, the [Quantity][kif_lib.Quantity] object with amount 733 and unit [kilogram (Q11570)](http://www.wikidata.org/entity/Q11570).  See the [data model guide](guides/data_model.md) for details.

Alternative subjects, properties, and values can be specified using bitwise "or" operator (`|`):

```pycon
>>> # (1) Match statements with subject "Socrates" or "Plato":
>>> next(kb.filter(subject=wd.Socrates|wd.Plato))

>>> # (2) Match statements with subject "caffeine" and
>>> #     property "density" or "mass" or "pKa":
>>> next(kb.filter(subject=wd.caffeine, property=wd.density|wd.mass|wd.pKa))

>>> # (3) Match statements with subject "IBM" and
>>> #     value "16 June 1911" or "https://www.ibm.com/":
>>> from kif_lib import IRI, Time
>>> for stmt in.filter(
...     subject=wd.IBM, value=Time('1911-06-16')|IRI('https://www.ibm.com/')):
...     print(stmt)
```

> `(1)` (**Statement** (**Item** [Plato](http://www.wikidata.org/entity/Q859)) (**ValueSnak** (**Property** [notable work](http://www.wikidata.org/entity/P800)) (**Item** [The Republic](http://www.wikidata.org/entity/Q123397))))<br/>
> `(2)` (**Statement** (**Item** [caffeine](http://www.wikidata.org/entity/Q60235)) (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) 194.08037556 [dalton](http://www.wikidata.org/entity/Q483261)))<br/>
> `(3.1)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [official website](http://www.wikidata.org/entity/P856)) https://www.ibm.com/))<br/>
> `(3.2)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 16 June 1911))

The [Or][kif_lib.Or] constructor can be used to build alternatives more conveniently from large lists of values.  For example:

```pycon
>>> south_america_countries = [wd.Brazil, wd.Argentina, wd.Uruguay, ...]
>>> for stmt in kb.filter(
>>>     subject=Or(*south_america_countries), property=wd.capital)):
>>>     print(stmt)
```

> (**Statement** (**Item** [Argentina](http://www.wikidata.org/entity/Q414)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Buenos Aires](http://www.wikidata.org/entity/Q1486))))<br/>
> (**Statement** (**Item** [Uruguay](http://www.wikidata.org/entity/Q77)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Montevideo](http://www.wikidata.org/entity/Q1335))))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Brasília](http://www.wikidata.org/entity/Q2844))))<br/>
> ⋮

### More complex filters

So far, we have used simple values to match the components of statements in filters.  In KIF, we can also specify the desired subject, property, or value indirectly, by giving a constraint that it must satisfy.

!!! example "Example"

    (1) Match any statement such that (i) the subject "shares border with Argentina" and (ii) the property is "official language":

    ```pycon
    >>> next(kb.filter(subject=wd.shares_border_with(wd.Argentina), property=wd.official_language))
    ```

    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Portuguese](http://www.wikidata.org/entity/Q5146))))
