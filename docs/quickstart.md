---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Quickstart

KIF is a Wikidata-based framework for integrating knowledge sources.

This quickstart guide presents the basic API of KIF.

## Hello world!

We start by importing the `kif_lib` namespace:

```{code-cell}
from kif_lib import *
```

We'll also need the Wikidata vocabulary module `wd`:

```{code-cell}
from kif_lib.vocabulary import wd
```

Let us no we create a SPARQL store pointing to the official Wikidata query
service:

```{code-cell}
kb = Store('wdqs')
```

A KIF store is an inteface to a knowledge source.  It allows us to view the
source as a set of Wikidata-like statements.

The store `kb` we just created is an interface to Wikidata itself. We can
use it, for example, to fetch from Wikidata three statements about Brazil:

```{code-cell}
it = kb.filter(subject=wd.Brazil, limit=3)
for stmt in it:
    display(stmt)
```

## Filters

The `kb.filter(...)` call searches for statements in `kb` matching the
restrictions `...`.

The result of a filter call is a (lazy) iterator `it` of statements:

```{code-cell}
it = kb.filter(subject=wd.Brazil)
```

We can advance `it` to obtain statements:

```{code-cell}
next(it)
```

If no `limit` argument is given to `kb.filter()`, the returned iterator
contains all matching statements.

## Basic filters

We can filter statements by any combination of *subject*, *property*, and
*value*.

For example:

*match any statement*

```{code-cell}
next(kb.filter())
```

*match statements with subject "Brazil" and property "official website"*

```{code-cell}
next(kb.filter(subject=wd.Brazil, property=wd.official_website))
```

*match statements with property "official website" and value "https://www.ibm.com/"*

```{code-cell}
next(kb.filter(property=wd.official_website, value=IRI('https://www.ibm.com/')))
```

*match statements with value "78.046950192 dalton"*
```{code-cell}
next(kb.filter(value=Quantity('78.046950192', unit=wd.dalton)))
```

We can also match statements having *some* (unknown) value:

```{code-cell}
next(kb.filter(snak=wd.date_of_birth.some_value()))
```

Or *no* value:

```{code-cell}
next(kb.filter(snak=wd.date_of_death.no_value()))
```

## Fingerprints (indirect ids)

So far, we have been using the symbolic aliases defined in the `wd` module to
specify entities in filters:

```{code-cell}
display(wd.Brazil)
display(wd.continent)
```

Alternatively, we can use their numeric Wikidata ids:

*match statements with subject Q155 (Brazil) and property P30 (continent)*

```{code-cell}
next(kb.filter(subject=wd.Q(155), property=wd.P(30)))
```

Sometimes, however, ids are not enough.  We might need to specify an entity
indirectly by giving not its id but a property it satisfies.

In cases like this, we can use a *fingerprint*:

*match statemets whose subject "is a dog" and value "is a human"*

```{code-cell}
next(kb.filter(subject=wd.instance_of(wd.dog), value=wd.instance_of(wd.human)))
```

Properties themselves can also be specified using fingerprints:

*match statements whose property is "equivalent to Schema.org's 'weight'"*

```{code-cell}
next(kb.filter(property=wd.equivalent_property('https://schema.org/weight')))
```

The `-` (unary minus) operator can be used to invert the direction of the
property used in the fingerprint:

*match statements whose subject is "the continent of Brazil"*

```{code-cell}
next(kb.filter(subject=-(wd.continent(wd.Brazil))))
```

## And-ing and or-ing fingeprints

Entity ids and fingerpints can be combined using the operators `&` (and) and
`|` (or).

For example:

*match three statements such that:*
- *subject is "Brazil" or "Argentina"*
- *property is "continent" or "highest point"*

```{code-cell}
it = kb.filter(
        subject=wd.Brazil | wd.Argentina,
        property=wd.continent | wd.highest_point,
        limit=3)
for stmt in it:
    display(stmt)
```

*match three statements such that:*
- *subject "has continent South America" and "official language is Portuguese"*
- *value "is a river" or "is a mountain"*

```{code-cell}
it = kb.filter(
        subject=wd.continent(wd.South_America) & wd.official_language(wd.Portuguese),
        value=wd.instance_of(wd.river) | wd.instance_of(wd.mountain),
        limit=3)
for stmt in it:
    display(stmt)
```

*match three statements such that:*
- *subject "is a female" and ("was born in NYC" or "was born in Rio")*
- *property is "field of work" or "is equivalent to Schema.org's 'hasOccupation'"*

```{code-cell}
it = kb.filter(
        subject=wd.sex_or_gender(wd.female)\
        & (wd.place_of_birth(wd.New_York_City) | wd.place_of_birth(wd.Rio_de_Janeiro)),
        property=wd.field_of_work\
        | wd.equivalent_property(IRI('https://schema.org/hasOccupation')),
        limit=3)
for stmt in it:
    display(stmt)
```

## Count and contains

A variant of the filter call is `kb.count(...)` which, instead of
statements, counts the number of statements matching restrictions `...`:

```{code-cell}
kb.count(subject=wd.Brazil, property=wd.population | wd.official_language)
```

The `kb.contains()` call tests whether a given statement occurs in `kb`.

```{code-cell}
stmt1 = wd.official_language(wd.Brazil, wd.Portuguese)
kb.contains(stmt1)
```

```{code-cell}
stmt2 = wd.official_language(wd.Brazil, wd.Spanish)
kb.contains(stmt2)
```

## Final remarks

This concludes the quickstart guide.

There are many other calls in the Store API of KIF.  For more information
see, the [API Reference](<reference/index>).
