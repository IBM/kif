# Quickstart

We start by importing the [Store][kif_lib.Store] class from the KIF library:

```pycon
>>> from kif_lib import Store
```

We'll also need the Wikidata vocabulary module `wd`:

```pycon
>>> from kif_lib.vocabulary import wd
```

Now, let's create a KIF store pointing to the official [Wikidata query service](https://query.wikidata.org/):

```pycon
>>> kb = Store('wikidata')
```

A KIF **store** is an interface to a knowledge source.  It allows us to view the source as a set of Wikidata-like statements.

The store `kb` we just created is an interface to [Wikidata](https://www.wikidata.org/) itself.  We can use it, for example, to fetch from Wikidata three statements about Brazil:

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

A KIF **statement** stands for an assertion and consists of a subject and a snak.  The **subject** is the entity about which the assertion is made, while the **snak** (or predication) is what is asserted about the subject.  In KIF, the snak associates a property with either a specific value, some value, or no value.

Consider the first statement obtained from the store `kb` above:

> (**Statement** (**Item** [Brazil](http://www.wikidata.org/entity/Q155)) (**ValueSnak** (**Property** [shares border with](http://www.wikidata.org/entity/P47)) (**Item** [Argentina](http://www.wikidata.org/entity/Q414))))<br>

Its subject is the item [Brazil (Q155)](http://www.wikidata.org/entity/Q155) and its snak is a value snak which associates the property [shares border with (P47)](http://www.wikidata.org/entity/Q47) with the value [Argentina (Q414)](http://www.wikidata.org/entity/Q414).  This particular statement stands thus for the assertion "Brazil shares border with Argentina".

## Filters

The [`kb.filter(...)`][kif_lib.Store.filter] call searches for statements in `kb` such that `...`.  The result is a (lazy) iterator which when advanced produces the matched statements:

```pycon
>>> it = kb.filter(subject=wd.Alan_Turing)
>>> next(it)
```

> (**Statement** (**Item** [Alan Turing](http://www.wikidata.org/entity/Q7251)) (**ValueSnak** (**Property** [doctoral advisor](http://www.wikidata.org/entity/P184)) (**Item** [Alonzo Church](http://www.wikidata.org/entity/Q92741))))

If not `limit` argument is given to `kb.filter()`, the returned iterator will contains all matching statements.  For instance, if advanced indefinitely, iterator `it` above will eventually produce every statement about [Alan Turing (Q7251)](http://www.wikidata.org/entity/Q7251) in Wikidata.

### Basic filters
