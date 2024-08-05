Release v0.4
============

- `Property.range`: We added a new `range` field (datatype) to `Property`.
  This information is now being retrieved automatically by most stores.

- `Property.some_value()` and `Propeprty.no_value()`: We added new, simpler
  APIs to construct `SomeValueSnak`'s and `NoValueSnaks`'s.

- `Filter`: We renamed the `FilterPattern` object to `Filter` to distinguish
  it from patterns.

- More expressive fingerprints: We redesigned the structure of fingerprints.
  We now distinguish between value and snak fingerprints and allow these to
  be composed using and's (`&`) and or's (`|`).

- Subject, property, and value masks in `filter()`: We added full support
   for entity masks to `Filter`.

- The `SPARQL_Store` is finally using the compiler infrastructure and
  template instantiation to generate the SPARQL query of `filter()` and
  parse the results.

- `vocabulary.wd.downloader`: We added a new entity description downloader
  module.  We also updated the format of the TSV files.
