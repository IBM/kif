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

A KIF **statement** represents an assertion and consists of two parts: a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  The snak associates a property with a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

This statement stands for the assertion "Brazil shares border with Argentina".  Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates property [shares border with (P47)](http://www.wikidata.org/entity/P47) with value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).

## Data model

KIF data-model objects, such as statements and their components, are built using the data-model object constructors (see the [data model guide](guides/data_model.md)).  For instance, we can construct the statement "Brazil shares border with Argentina" as follows:

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

    KIF data-model objects are immutable: once constructed, they cannot be changed.  Also, data-model object identity is completely determined by the objects' contents: two data-model objects constructed from the same arguments are equal.  Thus, `(stmt == stmt_alt) == True` above.

### Vocabulary

KIF comes with built-in vocabulary modules that ease the construction of entities in certain namespaces.  For instance, instead of writing their full IRIs, we can use the convenience functions [wd.Q][kif_lib.vocabulary.wd.Q] and [wd.P][kif_lib.vocabulary.wd] from the Wikidata vocabulary module [wd][kif_lib.vocabulary.wd] to construct the items [Brazil (Q155)](http://www.wikidata.org/entity/) and [Argentina (Q414)](http://www.wikidata.org/entity/Q414) and the property [shares border with (P47)](http://www.wikidata.org/entity/P47) more succinctly as follows:

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

The [wd][kif_lib.vocabulary.wd] vocabulary module also defines symbolic aliases for popular entities.  For instance, instead of writing `wd.Q(155)` and `wd.Q(414)` for Brazil and Argentina, we can write `wd.Brazil` and `wd.Argentina`.  Similarly, instead of writing `wd.P(47)` for "shares border with", we can write `wd.shares_border_with`.  Most Wikidata properties have symbolic aliases defined in [wd][kif_lib.vocabulary.wd].

!!! note

    Besides [wd][kif_lib.vocabulary.wd], KIF comes with the vocabulary modules [db][kif_lib.vocabulary.db] for [DBpedia](https://www.dbpedia.org/), [fg][kif_lib.vocabulary.fg] for [FactGrid](https://database.factgrid.de/), [pc][kif_lib.vocabulary.pc] for [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [up][kif_lib.vocabulary.up] for [UniProt](https://www.uniprot.org/), among others.

## Store

We now turn to the [Store][kif_lib.Store] API.

As we said earlier, a KIF store is an interface to a knowledge source, typically but not necessarily a knowledge graph.  A store is created using the [Store][kif_lib.Store] constructor which takes as arguments the name of the store plugin to instantiate followed by zero or more arguments to be passed to plugin.  For instance:

```pycon
>>> kb = Store('wikidata')
```

This instantiates and assigns to `kb` a new store using the plugin `wikidata`, which creates a [SPARQL store][kif_lib.store.SPARQL_Store] loaded with the Wikidata SPARQL mappings and targeted at the official Wikidata SPARQL endpoint.  ([SPARQL](https://en.wikipedia.org/wiki/SPARQL) is the query language of [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework), a standard format for knowledge graphs—see the [RDF guide](guides/rdf.md).)

Alternatively, we could have specified the target endpoint explicitly, as the second argument to the [Store()][kif_lib.Store] call:

```pycon
>>> kb = Store('wikidata', 'https://query.wikidata.org/sparql')
```

!!! note

    The available store plugins can be shown using KIF CLI:

    ```shell
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

    In example (3) above, `wd.place_of_birth(wd.Athens)` is another way of construcing the snak `ValueSnak(wd.place_of_birth, wd.Athens)`, while in example (5), `733@wd.kilogram` is another way of constructing the quantity value `Quantity(733, wd.kilogram)`. (See the [data model guide](guides/data_model.md).)

    In example (7), the filter failed to match any statement in Wikidata, as Brazil does not share a border with Chile.  So, the returned iterator is empty and we get a `StopIteration` exception when we try to advance it.

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

> `(1 )` (**Statement** (**Item** [Plato](http://www.wikidata.org/entity/Q859)) (**ValueSnak** (**Property** [notable work](http://www.wikidata.org/entity/P800)) (**Item** [The Republic](http://www.wikidata.org/entity/Q123397))))<br/>
> `(2 )` (**Statement** (**Item** [caffeine](http://www.wikidata.org/entity/Q60235)) (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) 194.08037556 [dalton](http://www.wikidata.org/entity/Q483261)))<br/>
> `(3a)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [official website](http://www.wikidata.org/entity/P856)) https://www.ibm.com/))<br/>
> `(3b)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 16 June 1911))

The [Or][kif_lib.Or] constructor can be used to build value alternatives more conveniently from large collection of values.  For example:

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

Suppose we want to match statements whose subjects are any items that "share border with Argentina".  If we know the subjects beforehand, we can specify them explicitly using the `|` operator:

```pycon
>>> it = kb.filter(subject=wd.Brazil|wd.Uruguay|wd.Chile|...))
```

Sometimes, however, we do not know the subjects beforehand.  In such cases, a more convenient approach is to use as the subject a snak that specifies the desired constraint.  For example:

```pycon
>>> wd.shares_border_with(wd.Argentina)
```

> (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414)))

The filter below matches statements such that the subject is any item that "shares border with Argentina", that is, any item `x` such that there is a statement `wd.shares_border_with(x, wd.Argentina)` in the store `kb`.

```pycon
>>> it = kb.filter(subject=wd.shares_border_with(wd.Argentina))
```

**Snak constraints** such as `wd.shares_border_with(wd.Argentina)` can be given as subject, property, or value arguments to the [`kb.filter()`][kif_lib.Store.filter] method.  Moreover, they can be combined with other constraints using the bitwise "and" (`&`) and "or" (`|`) operators (or the convenience constructors [And][kif_lib.And] and [Or][kif_lib.Or]).  For example:

```pycon
>>> # (1) Subject's "anthem is La Marseillaise" and property is "capital":
>>> next(kb.filter(subject=wd.anthem(wd.La_Marseillaise), property=wd.capital))

>>> # (2) Subject is "water" and property is a "property related to chemistry":
>>> next(kb.filter(
...     subject=wd.water,
...     property=wd.instance_of(wd.Wikidata_property_related_to_chemistry)))

>>> # (3) Property is "place of birth" and value is the "capital of Poland":
>>> next(kb.filter(property=wd.place_of_birth, value=wd.capital_of(wd.Poland)))

>>> # (4) Subject's "language is Portuguese" & "shares border with Argentina";
>>> #     Property is "highest point" | "driving side":
>>> it = kb.filter(
>>>     subject=(wd.official_language(wd.Portuguese)&
...              kb.shares_border_with(wd.Argentina)),
...     property=wd.highest_point|wd.driving_side); print(*it)
```

> `(1 )` (**Statement** (**Item** [France](http://www.wikidata.org/entity/Q142)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Paris](http://www.wikidata.org/entity/Q90))))<br/>
> `(2 )` (**Statement** (**Item** [water](http://www.wikidata.org/entity/Q283)) (**ValueSnak** (**Property** [chemical formula](http://www.wikidata.org/entity/P274)) "H₂O"))<br/>
> `(3 )` (**Statement** (**Item** [Marie Curie](http://www.wikidata.org/entity/Q7186)) (**ValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19)) (**Item** [Warsaw](http://www.wikidata.org/entity/Q270))))
> `(4a)` (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [highest point](http://www.wikidata.org/entity/P610)) (**Item** [Pico da Neblina](http://www.wikidata.org/entity/Q739484))))<br/>
> `(4b)` (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [driving side](http://www.wikidata.org/entity/P1622)) (**Item** [right](http://www.wikidata.org/entity/Q14565199))))

Constraints that require traversing paths of length greater than one can be specified using the property **sequencing operator** `/`.  For example, the filter below matches statements such that:

- the subject "has some notable work in a collection which is part of the Louvre"; and

- the property is "handedness".

```pycon
>>> next(kb.filter(
...     subject=(wd.notable_work/wd.collection/wd.part_of)(wd.Louvre_Museum),
...     property=wd.handedness))
```

> (**Statement** (**Item** [Leonardo da Vinci](http://www.wikidata.org/entity/Q762)) (**ValueSnak** (**Property** [handedness](http://www.wikidata.org/entity/P552)) (**Item** [left-handedness](http://www.wikidata.org/entity/Q789447))))

### Masks and language

The parameters ending in `*_mask` of [`kb.filter()`][kif_lib.Store.filter] specify **masks** that restrict the matched subjects, properties, and values to certain kinds.  The parameter `language` can be used to restrict the **language** of any returned text values. For instance:

```pycon
>>> # (1) Subject is "Louvre Museum" and value is an IRI:
>>> next(kb.filter(subject=wd.Wikidata, value_mask=Filter.IRI))

>>> # (2) Subject is a property and value is a property:
>>> next(kb.filter(subject_mask=Filter.PROPERTY, value_mask=Filter.PROPERTY))

>>> # (3) Subject is "El Capitan" and value is an external id or quantity:
>>> it = kb.filter(
...     subject=wd.El_Capitan,
...     value_mask=Filter.EXTERNAL_ID|Filter.QUANTITY); print(*it)

>>> # (4) Subject is "Mario", property is "catchphrase", value is in Italian:
>>> next(kb.filter(subject=wd.Mario, property=wd.catchphrase, language='it'))
```

> `(1 )` (**Statement** (**Item** [Louvre Museum](http://www.wikidata.org/entity/Q19675)) (**ValueSnak** (**Property** [official website](http://www.wikidata.org/entity/P856)) https://www.louvre.fr/))<br/>
> `(2 )` (**Statement** (**Property** [part of the series](http://www.wikidata.org/entity/P179)) (**ValueSnak** (**Property** [subproperty of](http://www.wikidata.org/entity/P1647)) (**Property** [part of](http://www.wikidata.org/entity/P361))))<br/>
> `(3a)` (**Statement** (**Item** [El Capitan](http://www.wikidata.org/entity/Q1124852)) (**ValueSnak** (**Property** [GeoNames ID](http://www.wikidata.org/entity/P1566)) "5334090"))<br/>
> `(3b)` (**Statement** (**Item** [El Capitan](http://www.wikidata.org/entity/Q1124852)) (**ValueSnak** (**Property** [elevation above sea level](http://www.wikidata.org/entity/P2044)) 2307 [metre](http://www.wikidata.org/entity/Q11573)))<br/>
> `(4 )` (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "Mamma mia!"@it))

!!! note

    As illustrated in example (3) above, masks can be operated through the usual bitwise operations.  See [Filter][kif_lib.Filter] for the available mask values.
