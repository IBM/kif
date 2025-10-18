# Quickstart

KIF is a knowledge integration framework based on [Wikidata](https://www.wikidata.org/).  The idea behind it is to use Wikidata to standardize the syntax and possibly the vocabulary of the integrated sources.  Users can then query the sources through filter patterns described in terms of the [Wikidata data model](https://www.wikidata.org/wiki/Wikidata:Data_model).

The integration done by KIF is *virtual* in the sense that syntax and vocabulary translations happen dynamically, at query time, guided by built-in or user-provided mappings.

## Hello world!

We start by importing the [Store][kif_lib.Store] class from the KIF library:

```pycon
>>> from kif_lib import Store
```

We'll also need the [Wikidata](https://www.wikidata.org/) vocabulary module `wd`:

```pycon
>>> from kif_lib.vocabulary import wd
```

Now, let's create a KIF store pointing to the official [Wikidata query service](https://query.wikidata.org/):

```pycon
>>> kb = Store('wikidata')
```

A KIF **store** is an interface to a knowledge source.  It allows us to query the source as if it were Wikidata and obtain Wikidata-like statements as a result.

The store `kb` we just created, in particular, is an interface to Wikidata itself.  We can use it, for example, to fetch from Wikidata three statements about Brazil:

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

    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))<br>
    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [inception](http://www.wikidata.org/entity/P571)) 7 September 1822))<br>
    > (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Portuguese](http://www.wikidata.org/entity/Q5146))))

    From now on, we'll use the pretty-printed format to display statements.

A KIF **statement** stands for an assertion and consists of two parts: a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  The snak associates a property with either a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates the property [shares border with (P47)](http://www.wikidata.org/entity/P47) with the value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).  This statement stands for the assertion "Brazil shares border with Argentina".

## Data model

KIF data-model objects, such as statements and their components, are immutable and are built using the data-model constructors (see the [data model guide](guides/data_model.md)).

For instance, we can construct the statement "Brazil shares border with Argentina" directly as follows:

```pycon
>>> from kif_lib import Item, Property, Statement, ValueSnak
>>> Brazil = Item('http://www.wikidata.org/entity/Q155')
>>> shares_border_with = Property('http://www.wikidata.org/entity/P47', Item)
>>> Argentina = Item('http://www.wikidata.org/entity/Q414')
>>> stmt = Statement(Brazil, ValueSnak(shares_border_with, Argentina))
>>> stmt
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

Alternatively, we can apply the property object `shares_border_with` as if it were a Python function to the arguments `Brazil` and `Argentina` to obtain the exactly same statement:

```pycon
>>> stmt_alt = shares_border_with(Brazil, Argentina)
>>> stmt_alt
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

!!! note

    Data-model object identity is completely determined by the objects' contents.  That is, two data-model objects constructed from the same arguments are equal.  Hence, `(stmt == stmt_alt) == True` above.

### Vocabulary

KIF comes with built-in vocabulary modules to ease the construction of entities in a given namespace.  For instance, instead of giving their full IRIs, we can use the convenience functions `wd.Q()` and `wd.P()` available in the Wikidata vocabulary module `wd` to construct the items [Brazil (Q155)](http://www.wikidata.org/entity/) and [Argentina (Q414)](http://www.wikidata.org/entity/Q414) and the property [shares border with (P47)](http://www.wikidata.org/entity/P47) as follows:

```pycon
>>> from kif_lib.vocabulary import wd
>>> Brazil = wd.Q(155); print(Brazil)
>>> Brazil
```

> (**Item** [Brazil](http://www.wikidata.org/entity/Q155))

```pycon
>>> Argentina = wd.Q(414); print(Argentina)
>>> Argentina
```

> (**Item** [Argentina](http://www.wikidata.org/entity/Q414))

```pycon
>>> shares_border_with = wd.P(47); print(shares_border_with)
>>> shares_border_with
```

> (**Property** [shares border with](http://www.wikidata.org/entity/P47))

```pycon
>>> shares_border_with(Brazil, Argentina)
```

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))

## Filters

Let's now return to the [Store][kif_lib.Store] API.

The [`kb.filter(...)`][kif_lib.Store.filter] call used previously searches for statements in `kb` such that matching the constraints `...`.  The result is a (lazy) iterator which when advanced produces the matched statements.  For example:

```pycon
>>> it = kb.filter(subject=wd.Alan_Turing)
>>> next(it)
```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

If no `limit` argument is given to `kb.filter()`, the returned iterator will eventually produce all matching statements.  For instance, if advanced indefinitely, iterator `it` will produce every statement about [Alan Turing (Q7251)](http://www.wikidata.org/entity/Q7251) in Wikidata.

### Basic filters

We can filter statements by any combination of *subject*, *property*, and *value*.  For example:

(1) Match any statement:

```pycon
>>> next(kb.filter())
```

> (**Statement** (**Item** [lion](http://www.wikidata.org/entity/Q140)) (**ValueSnak** (**Property** [parent taxon](http://www.wikidata.org/entity/P171)) (**Item** [Panthera](http://www.wikidata.org/entity/Q127960))))

(2) Match statement with snak "place of birth is Geneva":

```pycon
>>> next(kb.filter(snak=wd.place_of_birth(wd.Geneva))
```

> (**Statement** (**Item** [Jean-Jacques Rousseau](http://www.wikidata.org/entity/Q6527)) (**ValueSnak** (**Property** [place of birth](http://www.wikidata.org/entity/P19)) (**Item** [Geneva](http://www.wikidata.org/entity/Q71))))

(3) Match statements property "official language":

```pycon
>>> next(kb.filter(property=wd.official_language))
```

> (**Statement** (**Item** [Peru](http://www.wikidata.org/entity/Q419)) (**ValueSnak** (**Property** [official language](http://www.wikidata.org/entity/P37)) (**Item** [Spanish](http://www.wikidata.org/entity/Q1321))))


### More complex filters
