# TODO

## CLI

- Add --output-format option.  It should support SVG (mathplotlib/graphviz),
  KIF JSON, KIF JSONL, markdown (the default), repr, table(?).

## Codec

### RDF encoder

- BUG: Add an option to escape URLs should (true by default).

## Compiler

### SPARQL

### PubChem mapping

- Add support for the use of QIDs as compound identifiers in subjects and
  values.

## Context

### Entity registry

- Cache the property-constraint(allowed-entity-types-constraint) of
  properties.  We could expose this as Property.domain (Item, Property, or
  Lexeme) and then use it to optimize the queries.

## Model

- Per-class, more convenient version of `KIF_Object.replace()`.

- Add `context` argument to model classes. (?)

### Filter

- BUG: Pseudo-properties should not match snak fingerprints.

- Add support for pseudo-property flag in `property_mask`.

- Add support for "negation".  We can compile the negation of an atomic `v`,
  i.e., `~v`, as `FILTER(?x != v)`.  And we can compile the negation of a
  snak `S`, i.e., `~S`, as a `FILTER NOT EXISTS`.

- Add support for compound filters.  E.g., we could add a FilterUnion to
  represent the union of two or more filters.  If no snak sets occur in the
  child patterns, then each child pattern becomes an entry in the VALUES
  clause of filter.  Otherwise, each child pattern becomes a separate call
  to filter() and these calls are merged by the union.

### Fingerprint

- Normalization: We can use the distributive laws to decompose complex
  fingerprints.  E.g., `𝜂[A∧(B∨(C∧(D∨E)))]` ⤳ `𝜂[A∧B]∨𝜂[A∧(C∧(D∨E))]` ⤳
  `(A∧B)∨𝜂[(X≔A∧C)∧(D∨E)]` ⤳ `(A∧B)∨𝜂[X∧(D∨E)]` ⤳ `(A∧B)∨𝜂[X∧D]∨𝜂[X∧E]` ⤳
  `(A∧B)∨(A∧C∧D)∨(A∧C∧E)`. Now we know that the value mask of the original
  formula is equal to the mask of `(A∧B) | (A∧C∧D) | (A∧C∧E)`; also we can
  break the original query into three queries (executed in parallel).  We
  should restrict this type of normalization to non-VALUES clauses.  One
  possible way to do this is to introduce a new kind of fingerprint
  ValuesFingerprint/OneOfFingepprint which behaves as `|` but aggregates
  only or-ed value fingerprints.

### Text

- Revise the use of `TTextLanguage`.  Maybe we should create an alias
  `Text.Language` for `String`.

### Time

- BUG: Fix the internal representation of dates and times.  Find an
  alternative to Python's datetime or add a new field to the time values to
  store the `+` or `-` sign of Wikidata datetime strings.

- Time values with no month or day should default to `01-01`.

- `Time()` should default to `now()`.

## Compiler

- Filter compiler [optimization]: Aggregate snaks with the same property.

- Filter compiler: Use subqueries to implement fingerprints. (?)

- Make the compiler return a stream of queries to be executed in parallel.

## Codec

### Repr

- Replace `eval()` by a proper parser (via lark).

### JSON

- Add support for generating JSON in standard Wikidata format.  See

## Store

- BUG: Bad bindings should be ignored when producing query results.  That
  is, they should be skipped with a warning.

- Remove store flags.

- Implement some notion of option stack.  This way `distinct`, `page_size`,
  etc., can be temporarily overriden using the context manager mechanism.

- Add support for matching annotations (qualifiers, references, rank) in
  `Store.filter()` and `Store.filter_annotated()`.

- Add `Store.multifilter(subject, p1, p2, ...pn)` which returns a table
  whose lines are matching subjects and columns are the desired properties.

- Add support for obtaining normalized values.  Some possibilities: (i) make
  `Statement` carry an extra (normalized) value or value set; (ii) make
  value carry an extra (normalized) value or value set.

- Add support for testing whether a given statement is best-ranked.

- Add support for pagination, projection, etc., via an explicit "results"
  object.  Given the results, one can skip pages, apply a projection, etc.

### CSV

- Add support for a CSV store using the local SPARQL backend.  One of the
  columns of the CSV should be used for the subject; the remaining columns
  should be used for properties.

### Mixer

- Add support for entity unification: When a fingerprint is used with an
  identifier property (external id) we could ask the mixer to perform entity
  unification, i.e., use one of the underlying stores as the source of
  canonical entity ids.

- Revise the "sync" options.  Rename them to "propagate". (?)

- Brainstorm: Add some notion of proportion.  For example, for the stores
  `(s1,s2)` we associate the proportion `(4,3)` meaning that at each cycle
  the mixer will return 4 statements from `s1` and 3 statements from `s2`.
  Note that this is equivalent to using `(s1,s1,s1,s2,s2,s2)` as children.

- Brainstorm: Exploit SPARQL federation in cases where children support the
  SPARQL protocol.
