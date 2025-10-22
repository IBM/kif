# Tutorial

Create a Python virtual environment, activate it, and use [pip](https://pypi.org/project/pip/) to install the latest release of [kif-lib](https://pypi.org/project/kif-lib/) (with KIF CLI included):

```shell
$ python -m env tutorial
$ source tutorial/bin/activate
(tutorial) $ pip install kif-lib[cli]
```

The rest of the tutorial assumes this environment.

We start by importing the [Store][kif_lib.Store] constructor from the KIF library:

```py
from kif_lib import Store
```

We'll also need the [Wikidata](https://www.wikidata.org/) vocabulary module [wd][kif_lib.vocabulary.wd]:

```py
from kif_lib.vocabulary import wd
```

Now, let's create a KIF store pointing to the official [Wikidata query service](https://query.wikidata.org/):

```py
kb = Store('wikidata')
```

A KIF **store** is an interface to a knowledge source.  It allows us to query the source as if it were Wikidata and obtain Wikidata-like statements as a result.

The store `kb` we just created is an interface to Wikidata itself.  We can use it, for example, to fetch from Wikidata three statements about [Brazil (Q155)](http://www.wikidata.org/entity/Q155):

=== "Python"

    ```py
    it = kb.filter(subject=wd.Brazil, limit=3)
    for stmt in it:
       print(stmt)
    # -- output --
    # Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P47'), ItemDatatype()), Item(IRI('http://www.wikidata.org/entity/Q414'))))
    # Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P571'), TimeDatatype()), Time(datetime.datetime(1822, 9, 7, 0, 0, tzinfo=datetime.timezone.utc), 11, 0, Item(IRI('http://www.wikidata.org/entity/Q1985727')))))
    # Statement(Item(IRI('http://www.wikidata.org/entity/Q155')), ValueSnak(Property(IRI('http://www.wikidata.org/entity/P37'), ItemDatatype()), Item(IRI('http://www.wikidata.org/entity/Q5146'))))
    ```

=== "CLI"

    ```sh
    $ kif filter --store=wikidata --subject=wd.Brazil --limit=3
    ```

!!! note

    Most Python examples shown in this tutorial can be reproduced on the command-line using [KIF CLI](guides/cli.md).  Click on the "CLI" tab above to see the equivalent KIF CLI shell invocation.

If you run the previous Python code in Jupyter and use `display()` instead of `print()`, then the three statements will be pretty-printed in [S-expression](https://en.wikipedia.org/wiki/S-expression) format as follows:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 7 September 1822))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Portuguese](http://www.wikidata.org/entity/Q5146))))

From now on, we'll use this pretty-printed format to display statements and their components.

A KIF **statement** represents an assertion and consists of two parts: a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  The snak associates a property with a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

This statement stands for the assertion "Brazil shares border with Argentina".  Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates property [shares border with (P47)](http://www.wikidata.org/entity/P47) with value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).

## Data model

KIF data-model objects, such as statements and their components, are built using the data-model object constructors (see the [data model guide](guides/data_model.md)).  For instance, we can construct the statement "Brazil shares border with Argentina" as follows:

```py
from kif_lib import Item, Property, Statement, ValueSnak
Brazil = Item('http://www.wikidata.org/entity/Q155')
shares_border_with = Property('http://www.wikidata.org/entity/P47')
Argentina = Item('http://www.wikidata.org/entity/Q414')
stmt = Statement(Brazil, ValueSnak(shares_border_with, Argentina))
print(stmt)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

Alternatively, we can apply the property object `shares_border_with` as if it were a Python function to the arguments `Brazil` and `Argentina` to obtain exactly the same statement:

```py
stmt_alt = shares_border_with(Brazil, Argentina)
print(stmt_alt)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

!!! note

    KIF data-model objects are immutable: once constructed, they cannot be changed.  Also, data-model object identity is completely determined by the objects' contents: two data-model objects constructed from the same arguments are equal.  Thus, `(stmt == stmt_alt) == True` above.

### Vocabulary

KIF comes with built-in vocabulary modules that ease the construction of entities in certain namespaces.  For instance, instead of writing their full IRIs, we can use the convenience functions [`wd.Q`][kif_lib.vocabulary.wd.Q] and [`wd.P`][kif_lib.vocabulary.wd] from the Wikidata vocabulary module [wd][kif_lib.vocabulary.wd] to construct the items [Brazil (Q155)](http://www.wikidata.org/entity/) and [Argentina (Q414)](http://www.wikidata.org/entity/Q414) and the property [shares border with (P47)](http://www.wikidata.org/entity/P47) as follows:

```py
from kif_lib.vocabulary import wd
Brazil = wd.Q(155)
print(Brazil)
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))

```py
Argentina = wd.Q(414)
print(Argentina)
```

> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))

```py
shares_border_with = wd.P(47)
print(shares_border_with)
```

> (**Property** [shares border with](http://www.wikidata.org/entity/P47))

As before, we can apply `shares_border_with` to `Brazil` and `Argentina` to obtain the statement "Brazil shares border with Argentina":

```py
stmt = shares_border_with(Brazil, Argentina)
print(stmt)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

The [wd][kif_lib.vocabulary.wd] vocabulary module defines symbolic aliases for popular entities.  For instance, instead of writing `wd.Q(155)` and `wd.Q(414)` for Brazil and Argentina, we can write `wd.Brazil` and `wd.Argentina`.  Similarly, instead of writing `wd.P(47)` for "shares border with", we can write `wd.shares_border_with`.  Most Wikidata properties have symbolic aliases defined in [wd][kif_lib.vocabulary.wd].

!!! note

    Besides [wd][kif_lib.vocabulary.wd], KIF comes with the vocabulary modules [db][kif_lib.vocabulary.db] for [DBpedia](https://www.dbpedia.org/), [fg][kif_lib.vocabulary.fg] for [FactGrid](https://database.factgrid.de/), [pc][kif_lib.vocabulary.pc] for [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [up][kif_lib.vocabulary.up] for [UniProt](https://www.uniprot.org/), among others.

## Store

Let's now turn to the [Store][kif_lib.Store] API.

As we said earlier, a KIF store is an interface to a knowledge source, typically but not necessarily a knowledge graph.  A store is created using the [Store][kif_lib.Store] constructor which takes as arguments the name of the store plugin to instantiate followed by zero or more arguments to be passed to plugin.  For instance:

```py
kb = Store('wikidata')
```

This instantiates and assigns to `kb` a new store using the plugin `wikidata`, which creates a [SPARQL store][kif_lib.store.SPARQL_Store] loaded with the Wikidata SPARQL mappings and targeted at the official Wikidata SPARQL endpoint.  ([SPARQL](https://en.wikipedia.org/wiki/SPARQL) is the query language of [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework), a standard format for knowledge graphs; see the [RDF guide](guides/rdf.md).)

Alternatively, we could have specified the target SPARQL endpoint explicitly, as the second argument to the [`Store()`][kif_lib.Store] call:

```py
kb = Store('wikidata', 'https://query.wikidata.org/sparql')
```

!!! note

    The available store plugins can be shown using KIF CLI:

    ```sh
    $ kif --show-pluings --store
    ```

## Filter

The basic store operation is the *filter*.

The call [`kb.filter(...)`][kif_lib.Store.filter] searches for statements in `kb` matching the constraints `...`.  The result is a (lazy) iterator which when advanced produces the matched statements.  For example:

=== "Python"

    ```py
    kb = Store('wikidata')
    it = kb.filter(subject=wd.Alan_Turing)
    print(next(it))
    ```

=== "CLI"

    ```sh
    $ kif filter --store=wikidata --subject=wd.Alan_Turing
    ```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

If no `limit` argument is given to [kb.filter()][kif_lib.Store.filter], the returned iterator will eventually produce all matching statements.  For instance, iterator `it` above will produce every statement about [Alan Turing (Q7251)](http://www.wikidata.org/entity/Q7251) in Wikidata before it is exhausted.

### Basic filters

We can filter statements by specifying any combination of *subject*, *property*, *value* (or *snak*) to match.  None of these are required though.  For example:

=== "Python"

    ```py
    # (1) Match any statement whatsoever:
    it = kb.filter()
    print(next(it))

    # (2) Match statements with subject "water":
    it = kb.filter(subject=wd.water)
    print(next(it))

    # (3) Match statements with snak "place of birth is Athens":
    it = kb.filter(snak=wd.place_of_birth(wd.Athens))
    print(next(it))

    # (4) Match statements with property "official language":
    it = kb.filter(property=wd.official_language)
    print(next(it))

    # (5) Match statements with value "733 kilograms":
    it = kb.filter(value=733@wd.kilogram)
    print(next(it))

    # (6) Match statements with subject "Brazil" and
    #     snak "shares border with Argentina":
    it = kb.filter(subject=wd.Brazil, snak=wd.shares_border_with(wd.Argentina))
    print(next(it))

    # (7) Match statements with subject "Brazil" and
    #     snak "shares border with Chile":
    it = kb.filter(subject=wd.Brazil, snak=wd.shares_border_with(wd.Chile))
    print(next(it)) # *** ERROR: iterator is empty (no such statement) ***
    ```

=== "CLI"

    ```sh
    # (1) Match any statement whatsoever:
    $ kif filter --limit=1

    # (2) Match statements with subject "water":
    $ kif filter --subject=wd.water --limit=1

    # (3) Match statements with snak "place of birth is Athens":
    $ kif filter --snak="wd.place_of_birth(wd.Athens)" --limit=1

    # (4) Match statements with property "official language":
    $ kif filter --property=wd.official_language --limit=1

    # (5) Match statements with value "733 kilograms":
    $ kif filter --value=733@wd.kilogram --limit=1

    # (6) Match statements with subject "Brazil" and
    #     snak "shares border with Argentina":
    $ kif filter --subject=wd.Brazil\
        --snak="wd.shares_border_with(wd.Argentina)" --limit=1

    # (7) Match statements with subject "Brazil" and
    #     snak "shares border with Chile":
    $ kif filter --subject=wd.Brazil\
         --snak="wd.shares_border_with(wd.Chile)" --limit=1
    # *** no output ***
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

Alternative subjects, properties, and values can be specified using Python's bitwise "or" operator (`|`):

=== "Python"

    ```py
    # (1) Match statements with subject "Socrates" or "Plato":
    it = kb.filter(subject=wd.Socrates|wd.Plato)
    print(next(it))

    # (2) Match statements with subject "caffeine" and
    #     property "density" or "mass" or "pKa":
    it = kb.filter(subject=wd.caffeine, property=wd.density|wd.mass|wd.pKa)
    print(next(it))

    # (3) Match statements with subject "IBM" and
    #     value "16 June 1911" or "https://www.ibm.com/":
    from kif_lib import IRI, Time
    it = kb.filter(
        subject=wd.IBM, value=Time('1911-06-16')|IRI('https://www.ibm.com/'))
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # (1) Match statements with subject "Socrates" or "Plato":
    $ kif filter --subject="wd.Socrates|wd.Plato" --limit=1

    # (2) Match statements with subject "caffeine" and
    #     property "density" or "mass" or "pKa":
    $ kif filter --subject=wd.caffeine\
        --property="wd.density|wd.mass|wd.pKa" --limit=1

    # (3) Match statements with subject "IBM" and
    #     value "16 June 1911" or "https://www.ibm.com/":
    $ kif filter --subject=wd.IBM\
        --value="Time('1911-06-16')|IRI('https://www.ibm.com/')" --limit=2
    ```

> `(1 )` (**Statement** (**Item** [Plato](http://www.wikidata.org/entity/Q859)) (**ValueSnak** (**Property** [notable work](http://www.wikidata.org/entity/P800)) (**Item** [The Republic](http://www.wikidata.org/entity/Q123397))))<br/>
> `(2 )` (**Statement** (**Item** [caffeine](http://www.wikidata.org/entity/Q60235)) (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) 194.08037556 [dalton](http://www.wikidata.org/entity/Q483261)))<br/>
> `(3a)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [official website](http://www.wikidata.org/entity/P856)) https://www.ibm.com/))<br/>
> `(3b)` (**Statement** (**Item** [IBM](http://www.wikidata.org/entity/Q37156)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 16 June 1911))

The [Or][kif_lib.Or] constructor can be used to build value alternatives more conveniently from large collection of values.  For example:

```py
south_america_countries = [wd.Brazil, wd.Argentina, wd.Uruguay, ...]
it = kb.filter(subject=Or(*south_america_countries), property=wd.capital)
for stmt in it:
    print(stmt)
```

> (**Statement** (**Item** [Argentina](http://www.wikidata.org/entity/Q414)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Buenos Aires](http://www.wikidata.org/entity/Q1486))))<br/>
> (**Statement** (**Item** [Uruguay](http://www.wikidata.org/entity/Q77)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Montevideo](http://www.wikidata.org/entity/Q1335))))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Brasília](http://www.wikidata.org/entity/Q2844))))<br/>
> ⋮

### More complex filters

Suppose we want to match statements whose subjects are any items that "share border with Argentina".  If we know the subjects beforehand, we can specify them explicitly using the `|` operator:

```py
it = kb.filter(subject=wd.Brazil|wd.Uruguay|wd.Chile|...))
```

Sometimes, however, we do not know the subjects beforehand.  In such cases, a more convenient approach is to use a snak that captures the desired constraint.  For example:

```py
snak = wd.shares_border_with(wd.Argentina)
print(snak)
```

> (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414)))

The filter below matches statements such that the subject is any item that "shares border with Argentina", that is, any item `x` such that there is a statement `wd.shares_border_with(x, wd.Argentina)` in the store `kb`.

```py
it = kb.filter(subject=wd.shares_border_with(wd.Argentina))
```

**Snak constraints** such as `wd.shares_border_with(wd.Argentina)` can be given as subject, property, or value arguments to [`kb.filter()`][kif_lib.Store.filter].  Moreover, they can be combined with other constraints using the bitwise "and" (`&`) and "or" (`|`) operators (or the convenience constructors [And][kif_lib.And] and [Or][kif_lib.Or]).  For example:

=== "Python"

    ```py
    # (1) Subject's "anthem is La Marseillaise" and property is "capital":
    print(next(kb.filter(
        subject=wd.anthem(wd.La_Marseillaise), property=wd.capital)))

    # (2) Subject is "water" and property is any "property related to chemistry":
    print(next(kb.filter(
        subject=wd.water,
        property=wd.instance_of(wd.Wikidata_property_related_to_chemistry))))

    # (3) Property is "place of birth" and value is the "capital of Poland":
    print(next(kb.filter(
        property=wd.place_of_birth, value=wd.capital_of(wd.Poland))))

    # (4) Subject's "language is Portuguese" & "shares border with Argentina";
    #     Property is "highest point" | "driving side":
    it = kb.filter(
        subject=(wd.official_language(wd.Portuguese)&
                 wd.shares_border_with(wd.Argentina)),
        property=wd.highest_point|wd.driving_side)
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # (1) Subject's "anthem is La Marseillaise" and property is "capital":
    $ kif filter --subject="wd.anthem(wd.La_Marseillaise)"\
        --property=wd.capital --limit=1

    # (2) Subject is "water" and property is a "property related to chemistry":
    $ kif filter --subject=wd.water\
        --property="wd.instance_of(wd.Wikidata_property_related_to_chemistry)"\
        --limit=1

    # (3) Property is "place of birth" and value is the "capital of Poland":
    $ kif filter --property=wd.place_of_birth --value="wd.capital_of(wd.Poland)"

    # (4) Subject's "language is Portuguese" & "shares border with Argentina";
    #     Property is "highest point" | "driving side":
    $ kif filter --subject="wd.official_language(wd.Portuguese)&\
                            wd.shares_border_with(wd.Argentina)"\
        --property="wd.highest_point|wd.driving_side"
    ```

> `(1 )` (**Statement** (**Item** [France](http://www.wikidata.org/entity/Q142)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Paris](http://www.wikidata.org/entity/Q90))))<br/>
> `(2 )` (**Statement** (**Item** [water](http://www.wikidata.org/entity/Q283)) (**ValueSnak** (**Property** [chemical formula](http://www.wikidata.org/entity/P274)) "H₂O"))<br/>
> `(3 )` (**Statement** (**Item** [Marie Curie](http://www.wikidata.org/entity/Q7186)) (**ValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19)) (**Item** [Warsaw](http://www.wikidata.org/entity/Q270))))
> `(4a)` (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [highest point](http://www.wikidata.org/entity/P610)) (**Item** [Pico da Neblina](http://www.wikidata.org/entity/Q739484))))<br/>
> `(4b)` (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [driving side](http://www.wikidata.org/entity/P1622)) (**Item** [right](http://www.wikidata.org/entity/Q14565199))))

Constraints that require traversing paths of length greater than one can be specified using the **sequencing operator** `/`.  For example, the filter below matches statements such that:

- the subject "has some notable work in a collection which is part of the Louvre"; and

- the property is "handedness".

=== "Python"

    ```py
    next(kb.filter(
        subject=(wd.notable_work/wd.collection/wd.part_of)(wd.Louvre_Museum),
        property=wd.handedness))
    ```

=== "CLI"

    ```sh
    $ kif filter --subject="(wd.notable_work/wd.collection/wd.part_of)(wd.Louvre_Museum)"\
        --property=wd.handedness
    ```

> (**Statement** (**Item** [Leonardo da Vinci](http://www.wikidata.org/entity/Q762)) (**ValueSnak** (**Property** [handedness](http://www.wikidata.org/entity/P552)) (**Item** [left-handedness](http://www.wikidata.org/entity/Q789447))))

### Masks and language

The parameters *subject_mask*, *property_mask*, and *value_mask* of [`kb.filter()`][kif_lib.Store.filter] can be used to restrict the kinds of entities, properties, and values to be matched. For example:

=== "Python"

    ```py
    from kif_lib import Filter

    # (1) Subject is "Louvre Museum" and value is an IRI:
    it = kb.filter(subject=wd.Wikidata, value_mask=Filter.IRI)
    print(next(it))

    # (2) Subject is a property and value is a property:
    it = kb.filter(subject_mask=Filter.PROPERTY, value_mask=Filter.PROPERTY)
    print(next(it))

    # (3) Subject is "El Capitan" and value is an external id or quantity:
    it = kb.filter(
        subject=wd.El_Capitan, value_mask=Filter.EXTERNAL_ID|Filter.QUANTITY)
    print(next(it))
    ```

=== "CLI"

    ```sh
    # (1) Subject is "Louvre Museum" and value is an IRI:
    $ kif filter --subject=wd.Wikidata, value-mask=Filter.IRI

    # (2) Subject is a property and value is a property:
    $ kif filter --subject-mask=Filter.PROPERTY --value-mask=Filter.PROPERTY

    # (3) Subject is "El Capitan" and value is an external id or quantity:
    $ kif filter --subject=wd.El_Capitan\
        --value-mask="Filter.EXTERNAL_ID|Filter.QUANTITY"
    ```

> `(1 )` (**Statement** (**Item** [Louvre Museum](http://www.wikidata.org/entity/Q19675)) (**ValueSnak** (**Property** [official website](http://www.wikidata.org/entity/P856)) https://www.louvre.fr/))<br/>
> `(2 )` (**Statement** (**Property** [part of the series](http://www.wikidata.org/entity/P179)) (**ValueSnak** (**Property** [subproperty of](http://www.wikidata.org/entity/P1647)) (**Property** [part of](http://www.wikidata.org/entity/P361))))<br/>
> `(3a)` (**Statement** (**Item** [El Capitan](http://www.wikidata.org/entity/Q1124852)) (**ValueSnak** (**Property** [GeoNames ID](http://www.wikidata.org/entity/P1566)) "5334090"))<br/>
> `(3b)` (**Statement** (**Item** [El Capitan](http://www.wikidata.org/entity/Q1124852)) (**ValueSnak** (**Property** [elevation above sea level](http://www.wikidata.org/entity/P2044)) 2307 [metre](http://www.wikidata.org/entity/Q11573)))<br/>

!!! note

    As illustrated in example (3) above, masks can be operated through the usual bitwise operations.  See [Filter][kif_lib.Filter] for the available mask values.

Another mask parameter of [`kb.filter()`][kif_lib.Store.filter] is *snak_mask* which determines the kinds of snaks to be matched.  So far, we have dealt only with value snaks ([ValueSnak][kif_lib.ValueSnak]), which are essentially property-value pairs.  But KIF also supports, some-value snaks ([SomeValueSnak][kif_lib.SomeValueSnak]) and no-value snaks ([NoValueSnak][kif_lib.NoValueSnak]), which carry only the predicated property.

**Some-value snaks** represent predications with an unknown value, while **no-value snaks** represent predications with an absent value.  For instance, the fact that the Greek poet Homer's place of birth is unknown is represented in Wikidata by the some-value statement:

> (**Statement** (**Item** [Homer](http://www.wikidata.org/entity/Q6691)) (**SomeValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19))))

Similarly, the fact that the natural number 1 has no prime factor is represented by the no-value statement:

> (**Statement** (**Item** [1](http://www.wikidata.org/entity/Q199)) (**NoValueSnak** (**Property** [prime factor](http://www.wikidata.org/entity/P5236))))

The kinds of snaks to be matched are determined by the filter parameter *snak_mask*:

=== "Python"

    ```py
    # (1) Subject is "Homer" and snak is some-value:
    it = kb.filter(subject=wd.Homer, snak_mask=Filter.SOME_VALUE_SNAK)
    print(next(it))

    # (2) Subject is "1" and snak is no-value:
    it = kb.filter(subject=wd._1, snak_mask=Filter.NO_VALUE_SNAK)
    print(next(it))

    # (3) Subject is "Adam" and snak is some- or no-value:
    it = kb.filter(subject=wd.Adam,
        snak_mask=Filter.SOME_VALUE_SNAK|Filter.NO_VALUE_SNAK, limit=2)
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # (1) Subject is "Homer" and snak is some-value:
    $ kif filter --subject=wd.Homer --snak-mask=Filter.SOME_VALUE_SNAK

    # (2) Subject is "1" and snak is no-value:
    $ kif filter --subject=wd._1 --snak-mask=Filter.NO_VALUE_SNAK

    # (3) Subject is "Adam" and snak is some- or no-value:
    $ kif filter --subject=wd.Adam
        --snak-mask="Filter.SOME_VALUE_SNAK|Filter.NO_VALUE_SNAK" --limit=2
    ```

> `(1 )` (**Statement** (**Item** [Homer](http://www.wikidata.org/entity/Q6691)) (**SomeValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19))))<br/>
> `(2 )` (**Statement** (**Item** [1](http://www.wikidata.org/entity/Q199)) (**NoValueSnak** (**Property** [prime factor](http://www.wikidata.org/entity/P5236))))<br/>
> `(3a)` (**Statement** (**Item** [Adam](http://www.wikidata.org/entity/Q70899)) (**SomeValueSnak** (**Property** [date of birth](http://www.wikidata.org/entity/P569))))<br/>
> `(3b)` (**Statement** (**Item** [Adam](http://www.wikidata.org/entity/Q70899)) (**NoValueSnak** (**Property** [father](http://www.wikidata.org/entity/P22))))

The last filter parameter we want to mention is *language*, which controls the language of the returned text values.  If *language* is not given, [`kb.filter()`][kif_lib.Store.filter] returns statements with text values in any language:

=== "Python"

    ```py
    # Subject is "Mario" and property is "catchphrase":
    it = kb.filter(subject=wd.Mario, property=wd.catchphrase)
    for stmt in it:
        print(next(it))
    ```

=== "CLI"

    ```sh
    $ kif filter --subject=wd.Mario --property=wd.catchphrase
    ```

> (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "It’s-a me, Mario!"@en))<br/>
> (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "Let’s-a go!"@en-us))<br/>
> (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "Mamma mia!"@it))

However, we can set the *language* to a specific language tag ("en", "it", "fr", "pt", etc.) to filter-out statements with text values in languages other than the desired one:

=== "Python"

    ```py
    # (1) Subject is "Mario", property is "catchphrase", value is in English:
    it = kb.filter(subject=wd.Mario, property=wd.catchphrase, language='en')
    print(next(it))

    # (2) Subject is "Mario", property is "catchphrase", value is in Italian:
    it = kb.filter(subject=wd.Mario, property=wd.catchphrase, language='it')
    print(next(it))
    ```

=== "CLI"

    ```sh
    # (1) Subject is "Mario", property is "catchphrase", value is in English:
    $ kif filter --subject=wd.Mario --property=wd.catchphrase  --language=en

    # (2) Subject is "Mario", property is "catchphrase", value is in Italian:
    $ kif filter --subject=wd.Mario --property=wd.catchphrase --language=it
    ```

> `(1)` (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "It’s-a me, Mario!"@en))
> `(2)` (**Statement** (**Item** [Mario](http://www.wikidata.org/entity/Q12379)) (**ValueSnak** (**Property** [catchphrase](http://www.wikidata.org/entity/P6251)) "Mamma mia!"@it))

### Pseudo-properties

KIF extends the Wikidata data-model with the notion of **pseudo-properties**.  These are property-like entities which are not represented as properties in Wikidata.  For instance, entity labels, aliases, and descriptions, are not represented as Wikidata properties but are made available in KIF through the pseudo-properties [LabelProperty][kif_lib.LabelProperty], [AliasProperty][kif_lib.AliasProperty], [DescriptionProperty][kif_lib.DescriptionProperty].

We can use pseudo-properties in filters as if they were ordinary properties:

```py
from kif_lib import DescriptionProperty
it = kb.filter(subject=wd.IBM, property=DescriptionProperty())
print(next(it))
```



## Ask, count, mix
