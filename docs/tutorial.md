# Tutorial

Before we start, let's use the command-line to create and activate a fresh Python virtual environment:

```console
$ python -m env tutorial
$ source tutorial/bin/activate
(tutorial) $
```

Next, we use [pip](https://pypi.org/project/pip/) to install the latest release of [kif-lib](https://pypi.org/project/kif-lib/) (with [KIF CLI](guides/cli.md) support) and then start an interactive Python session:

```console
(tutorial) $ pip install kif-lib[cli]
(tutorial) $ python
>>>
```

The rest of the tutorial will take place inside this interactive session.  From now on, we will omit the session prompt string (`>>>`).

## 1 First steps

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

    ```console
    $ kif filter --store=wikidata --subject=wd.Brazil --limit=3
    (Statement (Item Brazil) (ValueSnak (Property shares border with) (Item Argentina)))
    (Statement (Item Brazil) (ValueSnak (Property inception) 7 September 1822))
    (Statement (Item Brazil) (ValueSnak (Property official language) (Item Portuguese)))
    ```

!!! note

    Most Python examples shown in this tutorial can be reproduced on the command-line using [KIF CLI](guides/cli.md).  Click on the "CLI" tab above to see the equivalent KIF CLI shell invocation.

If you run the previous Python code in Jupyter and use `display()` instead of `print()`, then the three statements will be pretty-printed in [S-expression](https://en.wikipedia.org/wiki/S-expression) format as follows:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 7 September 1822))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Portuguese](http://www.wikidata.org/entity/Q5146))))

From now on, we'll use this pretty-printed format to display statements and their components.  (Note that KIF CLI uses this format by default.)

A KIF **statement** represents an assertion and consists of two parts: a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  The snak associates a property with a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

This statement stands for the assertion "Brazil shares border with Argentina".  Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates property [shares border with (P47)](http://www.wikidata.org/entity/P47) with value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).

## 2 Data model

KIF data-model objects, such as statements and their components, are built using the data-model object constructors (see [Data Model](guides/data_model.md)).  For instance, we can construct the statement "Brazil shares border with Argentina" as follows:

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

    KIF data-model objects are immutable: once constructed, they cannot be changed.  Also, data-model object identity is completely determined by the object contents.  This means that two data-model objects constructed from the same arguments will always test equal.  For example, `(stmt == stmt_alt) == True` above.

To access the contents of statement objects, we can use the fields `subject` and `snak`:

```py
print(stmt.subject, stmt.snak)
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))<br/>
> (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414)))

Other data-model objects, such as entities, data values, and snaks, have analogous content-accessing fields (see [Data Model](guides/data_model.md)):

```py
print(stmt.subject.iri, stmt.snak.property, stmt.snak.value)
```

> http://www.wikidata.org/entity/Q155<br/>
> (**Property** [shares border with](http://www.wikidata.org/entity/P47))<br/>
> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))


### 2.1 Vocabulary

KIF comes with built-in vocabulary modules that ease the construction of entities in certain namespaces.  For instance, instead of writing the full IRI of Wikidata entities, we can use the convenience functions [`wd.Q`][kif_lib.vocabulary.wd.Q] and [`wd.P`][kif_lib.vocabulary.wd] from the Wikidata vocabulary module [wd][kif_lib.vocabulary.wd] to construct the items [Brazil (Q155)](http://www.wikidata.org/entity/) and [Argentina (Q414)](http://www.wikidata.org/entity/Q414) and the property [shares border with (P47)](http://www.wikidata.org/entity/P47):

```py
from kif_lib.vocabulary import wd

Brazil = wd.Q(155)
Argentina = wd.Q(414)
shares_border_with = wd.P(47)

print(Brazil, Argentina, shares_border_with)
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))<br/>
> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))<br/>
> (**Property** [shares border with](http://www.wikidata.org/entity/P47))

As before, we can apply `shares_border_with` to `Brazil` and `Argentina` to obtain the statement "Brazil shares border with Argentina":

```py
stmt = shares_border_with(Brazil, Argentina)
print(stmt)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

The [wd][kif_lib.vocabulary.wd] vocabulary module defines symbolic aliases for popular entities.  So, instead of writing `wd.Q(155)` and `wd.Q(414)` for Brazil and Argentina, we can write `wd.Brazil` and `wd.Argentina`.  Similarly, instead of writing `wd.P(47)` for "shares border with", we can write `wd.shares_border_with`.  Most Wikidata properties have symbolic aliases defined in [wd][kif_lib.vocabulary.wd].

```py
print(wd.Brazil, wd.Argentina, wd.shares_border_with, wd.capital)
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))<br/>
> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))<br/>
> (**Property** [shares border with](http://www.wikidata.org/entity/P47))<br/>
> (**Property** [capital](http://www.wikidata.org/entity/P36))

!!! note

    Besides [wd][kif_lib.vocabulary.wd], KIF comes with the vocabulary modules [db][kif_lib.vocabulary.db] for [DBpedia](https://www.dbpedia.org/), [fg][kif_lib.vocabulary.fg] for [FactGrid](https://database.factgrid.de/), [pc][kif_lib.vocabulary.pc] for [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [up][kif_lib.vocabulary.up] for [UniProt](https://www.uniprot.org/), among others.

## 3 Store

Let's now turn to the [Store][kif_lib.Store] API.

As we said earlier, a KIF store is an interface to a knowledge source, typically but not necessarily a knowledge graph.  A store is created using the [Store][kif_lib.Store] constructor which takes as arguments the name of the store plugin to instantiate followed by zero or more arguments to be passed to the plugin.  For instance:

```py
kb = Store('wikidata')
```

This instantiates and assigns to `kb` a new store using the "wikidata" plugin.  This plugin creates a [SPARQL store][kif_lib.store.SPARQL_Store], loads it with the Wikidata SPARQL mappings, and points it at the official Wikidata SPARQL endpoint.  ([SPARQL](https://en.wikipedia.org/wiki/SPARQL) is the query language of [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework), a standard format for knowledge graphs; see [RDF](guides/rdf.md).)

Alternatively, we could have specified the target SPARQL endpoint explicitly, as the second argument to the [`Store()`][kif_lib.Store] call:

```py
kb = Store('wikidata', 'https://query.wikidata.org/sparql')
```

!!! note

    The available store plugins can be shown using KIF CLI:

    ```console
    $ kif show-plugins --store
    ...
    dbpedia         : DBpedia SPARQL store
    europa          : Europa (data.europa.eu) SPARQL store
    factgrid        : FactGrid SPARQL store
    pubchem         : PubChem SPARQL store
    uniprot         : UniProt SPARQL store
    wikidata        : Wikidata query service store
    ...
    ```

## 4 Filter

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

    # Note: We can omit --store=wikidata, as it is the default.
    ```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

If no *limit* argument is given to [kb.filter()][kif_lib.Store.filter], the returned iterator will eventually produce all matching statements.  For instance, iterator `it` above will produce every statement with subject [Alan Turing (Q7251)](http://www.wikidata.org/entity/Q7251) in Wikidata before it is exhausted.

### 4.1 Basic filters

We can filter statements by specifying any combination of *subject*, *property*, *value* (or *snak*) to match—none of these are required though.  For example:

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

    In example (3) above, `wd.place_of_birth(wd.Athens)` is another way of construcing the snak `ValueSnak(wd.place_of_birth, wd.Athens)`, while in example (5), `733@wd.kilogram` is another way of constructing the quantity value `Quantity(733, wd.kilogram)` (see [Data Model](guides/data_model.md)).

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

The [Or][kif_lib.Or] constructor can be used to construct alternatives more conveniently from collection of values.  For example:

```py
from kif_lib import Or

south_america_countries = [wd.Brazil, wd.Argentina, wd.Uruguay, ...]
it = kb.filter(subject=Or(*south_america_countries), property=wd.capital)
for stmt in it:
    print(stmt)
```

> (**Statement** (**Item** [Argentina](http://www.wikidata.org/entity/Q414)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Buenos Aires](http://www.wikidata.org/entity/Q1486))))<br/>
> (**Statement** (**Item** [Uruguay](http://www.wikidata.org/entity/Q77)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Montevideo](http://www.wikidata.org/entity/Q1335))))<br/>
> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [capital](http://www.wikidata.org/entity/P36)) (**Item** [Brasília](http://www.wikidata.org/entity/Q2844))))<br/>
> ⋮

### 4.2 More complex filters

Suppose we want to match statements whose subjects are any items that "share border with Argentina".  If we know the subjects beforehand, we can specify them explicitly using the `|` operator:

```py
it = kb.filter(subject=wd.Brazil|wd.Uruguay|wd.Chile|...))
```

Sometimes, however, we do not know the subjects beforehand.  In such cases, we can use a snak that captures the desired constraint, such as:

```py
snak = wd.shares_border_with(wd.Argentina)
print(snak)
```

> (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414)))

The filter below matches statements such that the subject is any item that "shares border with Argentina", that is, any item `x` such that there is a statement `wd.shares_border_with(x, wd.Argentina)` in the store `kb`.

=== "Python"

    ```py
    it = kb.filter(subject=wd.shares_border_with(wd.Argentina))
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    $ kif filter  --subject="wd.shares_border_with(wd.Argentina)"

    # Note: The double quotes (") prevent the shell from interpreting the
    #       parentheses in the argument of --subject as a subshell invocation.
    ```

> (**Statement** (**Item** [Uruguay](http://www.wikidata.org/entity/Q77)) (**ValueSnak** (**Property** [public holiday](http://www.wikidata.org/entity/P832)) (**Item** [Tourism Week](http://www.wikidata.org/entity/Q6124629))))<br/>
> (**Statement** (**Item** [Bolivia](http://www.wikidata.org/entity/Q750)) (**ValueSnak** (**Property** [highest point](http://www.wikidata.org/entity/P610)) (**Item** [Nevado Sajama](http://www.wikidata.org/entity/Q272593))))<br/>
> (**Statement** (**Item** [Paraguay](http://www.wikidata.org/entity/Q733)) (**ValueSnak** (**Property** [electrical plug type](http://www.wikidata.org/entity/P2853)) (**Item** [Europlug](http://www.wikidata.org/entity/Q1378312))))<br/>
> ⋮

These statements may seem random at first but they all have subjects matching the constraint "shares border with Argentina".

**Snak constraints** such as `wd.shares_border_with(wd.Argentina)` can be given as subject, property, or value arguments to [`kb.filter()`][kif_lib.Store.filter].  Moreover, they can be combined with other constraints using the bitwise "and" (`&`) and "or" (`|`) infix operators (or their prefixed versions [And][kif_lib.And] and [Or][kif_lib.Or]).  For example:

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

Constraints that require traversing property paths of length greater than one can be specified using the **sequencing operator** `/`.  For example, the filter below matches statements such that:

- the subject "has some notable work in a collection which is part of the Louvre"; and

- the property is "handedness".

=== "Python"

    ```py
    it = kb.filter(
        subject=(wd.notable_work/wd.collection/wd.part_of)(wd.Louvre_Museum),
        property=wd.handedness)
    print(next(it))
    ```

=== "CLI"

    ```sh
    $ kif filter\
        --subject="(wd.notable_work/wd.collection/wd.part_of)(wd.Louvre_Museum)"\
        --property=wd.handedness
    ```

> (**Statement** (**Item** [Leonardo da Vinci](http://www.wikidata.org/entity/Q762)) (**ValueSnak** (**Property** [handedness](http://www.wikidata.org/entity/P552)) (**Item** [left-handedness](http://www.wikidata.org/entity/Q789447))))

### 4.3 Masks and language

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

    As illustrated in example (3) above, masks can be operated through the usual bitwise operations.  See [Filter][kif_lib.Filter] for the available mask types and values.

Another mask parameter of [`kb.filter()`][kif_lib.Store.filter] is *snak_mask* which determines the kinds of snaks to be matched.  So far, we have dealt only with value snaks ([ValueSnak][kif_lib.ValueSnak]), which are essentially property-value pairs.  But KIF also supports, some-value snaks ([SomeValueSnak][kif_lib.SomeValueSnak]) and no-value snaks ([NoValueSnak][kif_lib.NoValueSnak]), which carry only the predicated property.

**Some-value snaks** represent predications with an unknown value, while **no-value snaks** represent predications with an absent value.  For instance, the fact that the Greek poet Homer's place of birth is unknown is represented in Wikidata by the some-value statement:

> (**Statement** (**Item** [Homer](http://www.wikidata.org/entity/Q6691)) (**SomeValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19))))

Similarly, the fact that the natural number 1 has no prime factor is represented by the no-value statement:

> (**Statement** (**Item** [1](http://www.wikidata.org/entity/Q199)) (**NoValueSnak** (**Property** [prime factor](http://www.wikidata.org/entity/P5236))))

The kinds of snaks to be matched in filters are determined by the parameter *snak_mask*:

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

However, we can set the *language* parameter to a language tag ("en", "it", "fr", "pt", etc.) to match only the statements with text values in the desired language:

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

## 5 Pseudo-properties

KIF extends the Wikidata data-model with the notion of **pseudo-properties**.  These are property-like entities which are not represented as properties in Wikidata.  For instance, labels, aliases, and descriptions are not represented as properties in Wikidata but are made available in KIF through the pseudo-properties [LabelProperty][kif_lib.LabelProperty], [AliasProperty][kif_lib.AliasProperty], [DescriptionProperty][kif_lib.DescriptionProperty].

We can use pseudo-properties in filters as if they were ordinary properties:

=== "Python"

    ```py
    from kif_lib import LabelProperty, AliasProperty, DescriptionProperty

    # (1) Get the Spanish label of Mars:
    it = kb.filter(subject=wd.Mars, property=LabelProperty(), language='es')
    print(next(it))

    # (2) Get a French alias of Mars:
    it = kb.filter(subject=wd.Mars, property=AliasProperty(), language='fr')
    print(next(it))

    # (3) Get the English description of Mars:
    it = kb.filter(subject=wd.Mars, property=DescriptionProperty(), language='en')
    print(next(it))
    ```

=== "CLI"

    ```sh
    # (1) Get the Spanish label of Mars:
    $ kif filter --subject=wd.Mars --property="LabelProperty()" --language=es

    # (2) Get a French alias of Mars:
    $ kif filter --subject=wd.Mars --property="AliasProperty()" --language=fr

    # (3) Get the English description of Mars:
    $ kif filter --subject=wd.Mars --property="DescriptionProperty" --language=en
    ```

> `(1)` (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **LabelProperty** "Marte"@es))<br/>
> `(2)` (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **AliasProperty** "Planète rouge"@fr))<br/>
> `(3)` (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **DescriptionProperty** "fourth planet in the Solar System from the Sun"@en))

The Wikidata vocabulary module [wd][kif_lib.vocabulary.wd] defines the aliases `wd.label`, `wd.alias`, `wd.description` for the pseudo-properties [`LabelProperty()`][kif_lib.LabelProperty], [`AliasProperty()`][kif_lib.AliasProperty], [`DescriptionProperty()`][kif_lib.DescriptionProperty].  These can be used to write less verbose filter calls:

=== "Python"

    ```py
    # Get the label, aliases, and description of Mars in Portuguese:
    it = kb.filter(
        subject=wd.Mars, property=wd.label|wd.alias|wd.description, language='pt')
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # Get the label, aliases, and description of Mars in Portuguese:
    $ kif filter --subject=wd.Mars\
        --property="wd.label|wd.alias|wd.description" --language='pt'
    ```

> (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **LabelProperty** "Marte"@pt))<br/>
> (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **AliasProperty** "planeta Marte"@pt))<br/>
> (**Statement** (**Item** [Mars](http://www.wikidata.org/entity/Q111)) (**ValueSnak** **DescriptionProperty** "quarto planeta a partir do Sol no System Solar"@pt))

!!! note

    In KIF, information such as labels, aliases, and descriptions are referred to collectively as **descriptors**.  Descriptor values can be registered (saved) in the current KIF context so that, for example, they don't need to be retrieved every time an entity is pretty-printed (see [Context](guides/context.md)).  Most vocabulary modules register in the context the English label of the entities they predefine.  This cached label can be conveniently accessed through the `label` field of item and property objects:

    ```py
    print(wd.Q(111).label, wd.P(2583).label)
    ```

    > "Mars"@en<br/>
    > "distance from Earth"@en

    The aliases and description can be accessed through the fields `aliases` and `descriptions`.  These are usually left undefined by the vocabulary modules:

    ```py
    print(wd.Q(111).aliases, wd.P(2583).aliases)          # None None
    print(wd.Q(111).description, wd.P(2583).description)  # None None
    ```

    However, KIF can be instructed to resolve them automatically using the vocabulary module's resolver.  This is done by setting option "entities.resolve" to `True` in the context:

    ```py
    # Enable automatic entity descriptor resolution:
    from kif_lib import Context
    Context.top().options.entities.resolve = True

    # (1)
    print(wd.Q(111).aliases, wd.P(2583).aliases)

    # (2)
    print(wd.Q(111).description, wd.P(2583).description)
    ```

    > `(1a)` {"Planet Mars"@en, "Red Planet"@en}<br/>
    > `(1b)` {"angular diameter distance"@en, "proper distance"@en, ...}<br/>
    > `(2a)` "fourth planet in the Solar System from the Sun"@en<br/>
    > `(2b)` "estimated distance to astronomical objects"@en

    Automatic entity descriptor resolution can also be enabled by setting the value of the environment variable `KIF_RESOLVE_ENTITIES` to 1 (or any other literal that evaluates to `True` in Python).  See [Context](guides/context.md) for details.

Some KIF pseudo-properties have no direct counterpart in Wikidata.  This is the case of the pseudo-properties [TypeProperty][kif_lib.TypeProperty] and [SubtypeProperty][kif_lib.SubtypeProperty], whose [wd][kif_lib.vocabulary.wd] aliases are `wd.a` and `wd.subtype`.  These pseudo-properties stand for the ontological relations "is a" and "subclass of", respectively, and can be seen as more powerful (transitivity-enabled) versions of the Wikidata properties [instance of (P31)](http://www.wikidata.org/entity/P31) and [subclass of P(279)](http://www.wikidata.org/entity/P279).

To see the difference, consider the filter below, which gets statements that assert the classes of which [rabbit (Q9394)](http://www.wikidata.org/entity/Q9394) is an instance:

=== "Python"

    ```py
    # Get the classes such that "rabbit" is an instance of:
    it = kb.filter(subject=wd.rabbit, property=wd.instance_of)
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # Get the classes such that "rabbit" is an instance of:
    $ kif filter --subject=wd.rabbit --property=wd.instance_of
    ```

> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** (**Property** [instance of](http://www.wikidata.org/entity/P31)) (**Item** [organisms known by a particular common name](http://www.wikidata.org/entity/Q55983715))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** (**Property** [instance of](http://www.wikidata.org/entity/P31)) (**Item** [taxon](http://www.wikidata.org/entity/Q16521))))

If replace `wd.instance_of` by `wd.a`, we get three times more results:

=== "Python"

    ```py
    # Get the classes such that "rabbit" is an instance of (with transitivity):
    it = kb.filter(subject=wd.rabbit, property=wd.a)
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # Get the classes such that "rabbit" is an instance of (with transitivity):
    $ kif filter --subject=wd.rabbit --property=wd.a
    ```

> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [group or class of living things](http://www.wikidata.org/entity/Q21871294))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [organisms known by a particular common name](http://www.wikidata.org/entity/Q55983715))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [group or class of physical objects](http://www.wikidata.org/entity/Q98119401))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [collective entity](http://www.wikidata.org/entity/Q99527517))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [taxon](http://www.wikidata.org/entity/Q16521))))<br/>
> (**Statement** (**Item** [rabbit](http://www.wikidata.org/entity/Q9394)) (**ValueSnak** **TypeProperty** (**Item** [entity](http://www.wikidata.org/entity/Q35120))))

What is happening here is that the latter version will consider as classes such that rabbit is an instance not only [organisms known by a particular common name (Q55983715)](http://www.wikidata.org/entity/Q55983715) and [taxon (Q16521)](http://www.wikidata.org/entity/Q16521) but also any super-classes of these two.  In other words, while `wd.instance_of` looks only to the immediate class, `wd.a` traverses the whole class hierarchy.

The pseudo-property `wd.subtype`, which is the transitive counterpart of `wd.subclass_of`, behaves similarly:

=== "Python"

    ```py
    # (1) Get the subclasses of "mammal":
    it = kif.filter(subject=wd.mammal, --property=wd.subclass_of)
    for stmt in it:
        print(stmt)

    # (2) Get the subclasses of "mammal" (with transitivity):
    for stmt in it:
        print(stmt)
    ```

=== "CLI"

    ```sh
    # (1) Get the subclasses of "mammal":
    $ kif filter --subject=wd.mammal --property=wd.subclass_of

    # (2) Get the subclasses of "mammal" (with transitivity):
    $ kif filter --subject=wd.mammal --property=wd.subtype
    ```

> `(1 )` (**Statement** (**Item** [mammal](http://www.wikidata.org/entity/Q7377)) (**ValueSnak** (**Property** [subclass of](http://www.wikidata.org/entity/P279)) (**Item** [Vertebrata](http://www.wikidata.org/entity/Q25241))))<br/>
> `(2a)` (**Statement** (**Item** [mammal](http://www.wikidata.org/entity/Q7377)) (**ValueSnak** **SubtypeProperty** (**Item** [animal](http://www.wikidata.org/entity/Q729))))<br/>
> `(2b)` (**Statement** (**Item** [mammal](http://www.wikidata.org/entity/Q7377)) (**ValueSnak** **SubtypeProperty** (**Item** [Vertebrata](http://www.wikidata.org/entity/Q25241))))<br/>
> `(2c)` (**Statement** (**Item** [mammal](http://www.wikidata.org/entity/Q7377)) (**ValueSnak** **SubtypeProperty** (**Item** [organism](http://www.wikidata.org/entity/Q7239))))<br/>
> ⋮

## 6 Statement annotations

Up to now, we have dealt only with plain statements ([Statement][kif_lib.Statement]).  These are statements consisting of a subject, a snak, and nothing else.  In KIF, statements can also carry extra information referred to collectively as **annotations**.  These statements with annotations ([AnnotatedStatement][kif_lib.AnnotatedStatement]) behave exactly as plain statements but besides a subject and a snak also carry a set of qualifiers, a set of reference records, and a rank.  The **qualifiers** qualify the statement assertion, the **reference records** contain provenance information, and the **rank** indicates the quality of the statement.

The boolean parameter *annotated* instructs the [`kb.filter()`][kif_lib.Store.filter] method to obtain the annotations associated with each returned statement.  The variant [`kb.filter_annotated()`][kif_lib.Store.filter_annotated] can also be used to filter annotated statements.  (It behaves exactly as [`kb.filter()`][kif_lib.Store.filter] with the *annotated* flag set to `True` but its return type is [AnnotatedStatement][kif_lib.AnnotatedStatement] instead of [Statement][kif_lib.Statement].)

The difference between [`kb.filter()`][kif_lib.Store.filter] and [`kb.filter_annotated()`][kif_lib.Store.filter_annotated] is illustrated in examples (1) and (2) below:

=== "Python"

    ```py
    # (1) Get the "density" of "benzene":
    it = kb.filter(subject=wd.benzene, property=wd.density)
    print(next(it))

    # (2) Get the "density" of "benzene" (with annotations):
    it = kb.filter_annotated(subject=wd.benzene, property=wd.density)
    print(next(it))
    ```

=== "CLI"

    ```sh
    # (1) Get the "density" of "benzene":
    $ kif filter --subject=wd.benzene --property=wd.density

    # (2) Get the "density" of "benzene" (with annotations):
    $ kif filter --subject=wd.benzene --property=wd.density --annotated

    # Note: The --annotated flag instructs KIF CLI to fetch annotations.
    ```

> `(1)` (**Statement** (**Item** [benzene](http://www.wikidata.org/entity/Q2270)) (**ValueSnak** (**Property** [density](http://www.wikidata.org/entity/P2054)) 0.88 ±0.01 [gram per cubic centimetre](http://www.wikidata.org/entity/Q13147228)))<br/>
> `(2)` (**AnnotatedStatement** (**Item** [benzene](http://www.wikidata.org/entity/Q2270)) (**ValueSnak** (**Property** [density](http://www.wikidata.org/entity/P2054)) 0.88 ±0.01 [gram per cubic centimetre](http://www.wikidata.org/entity/Q13147228))<br/>
>  (**QualifierRecord**<br/>
>   (**ValueSnak** (**Property** [temperature](http://www.wikidata.org/entity/P2076)) 20 ±1 [degree Celsius](http://www.wikidata.org/entity/Q25267))<br/>
>   (**ValueSnak** (**Property** [phase of matter](http://www.wikidata.org/entity/P515)) (**Item** [liquid](http://www.wikidata.org/entity/Q11435))))<br/>
>  (**ReferenceRecordSet**<br/>
>    (**ReferenceRecord**<br/>
>     (**ValueSnak** (**Property** [HSDB ID](http://www.wikidata.org/entity/P2062)) "35#section=TSCA-Test-Submissions")<br/>
>     (**ValueSnak** (**Property** [stated in](http://www.wikidata.org/entity/P248)) (**Item** [Hazardous Substances Data Bank](http://www.wikidata.org/entity/Q5687720)))))<br/>
>  **NormalRank**)<br/>

Both statements, (1) and (2), assert that "benzene's density is 0.88±0.01 g/cm".  But statement (2), which is annotated, carries more information.  Its qualifier record qualifies the assertion, i.e., says in addition that this is the case when "the temperature is 20±1 ℃" and "the phase of matter is liquid".  Its reference record set contains a single reference record which indicates the provenance of the statement, namely, the entry with the given HSDB ID in the Hazardous Substances Data Bank.  Finally, its rank is "normal" which is the default one and means that its status is neutral (neither preferred nor deprecated).

!!! note

    The [QualifierRecord][kif_lib.QualifierRecord] is essentially a set of snaks, while the reference record set is a set of [ReferenceRecord][kif_lib.ReferenceRecord] objects, each of which is itself a snak set.  See [Data Model](guides/data_model.md) for details.

As plain statements, annotated statements can be constructed directly using data-model object constructors.  For instance, `stmt1` and `stmt2` below correspond exactly to statement (2) above.

```py
from kif_lib import (AnnotatedStatement, NormalRank,
                     QualifierRecord, Quantity,
                     ReferenceRecord, ReferenceRecordSet, ValueSnak)

stmt1 = AnnotatedStatement(
    wd.benzene,
    ValueSnak(
        wd.density,
        Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89')),
    QualifierRecord(
        wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
        wd.phase_of_matter(wd.liquid)),
    ReferenceRecordSet(
        ReferenceRecord(
            wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
        wd.stated_in(wd.Hazardous_Substances_Data_Bank))),
    NormalRank())

stmt2 = wd.density(
    wd.benzene, Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89'),
    qualifiers=[
        wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
        wd.phase_of_matter(wd.liquid)],
    references=[[
        wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
        wd.stated_in(wd.Hazardous_Substances_Data_Bank)]],
    rank=NormalRank())

print(stmt1 == stmt2)             # True
```

If you already have a statement, then you can use the method [`annotate()`][kif_lib.Statement.annotate] to create an annotated version of it.  For example:

```py
stmt3 = wd.density(
    wd.benzene, Quantity('.88', wd.gram_per_cubic_centimetre, '.87', '.89'))

stmt4 = stmt3.annotate(
    qualifiers=[
        wd.temperature(Quantity(20, wd.degree_Celsius, 19, 21)),
        wd.phase_of_matter(wd.liquid)],
    references=[[
        wd.HSDB_ID('35#section=TSCA-Test-Submissions'),
        wd.stated_in(wd.Hazardous_Substances_Data_Bank)]],
    rank=NormalRank())

print(stmt1 == stmt2 == stmt4)    # True
print(stmt3 == stmt4)             # False
```

Conversely, if you have an annotated statement you can use the method [`unannotated`][kif_lib.AnnotatedStatement.unannotate] to obtain its plain version:

```py
print(stmt3 == stmt4.unannotate() # True
```

## 7 Ask, count, mix

## 8 Beyond Wikidata

## 9 Entity search

## 10 Final remarks
