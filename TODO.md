# TODO

- CLI: Command-line version of the basic store API (`kif`).

- Internal module names should start with a "_".  Cf. the httpx package.

- Follow the approach to `__version__` used by httpx.

## Codec

### RDF encoder

- BUG: Add an option to escape URLs should (true by default).

## Context

### Entity registry

- Add support for property (RDF) schemas — one per IRI prefix.

## Model

- Revise the use of `NotImplemented` in dunders such as `__eq__`.

- Per-class, more convenient version of `KIF_Object.replace()`.

### Filter

- BUG: pseudo-properties should not match snak fingerprints.

- Add support for pseudo-property flag in `property_mask`.

- Add support for "negation".  We can compile the negation of an atomic `v`,
  i.e., `~v`, as `FILTER(?x != v)`.  And we can compile the negation of a
  snak `S`, i.e., `~S`, as a `FILTER NOT EXISTS`.

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

- Revise the use of `Text.TLanguage`.  Maybe we should create an alias
  `Text.Language` for `String`.

### Time

- BUG: Fix the internal representation of dates and times.  Find an
  alternative to Python's datetime or add a new field to the time values to
  store the `+` or `-` sign of Wikidata datetime strings.

- Time values with no month or day should default to `01-01`.

- `Time()` should default to `now()`.

## Compiler

- Filter compiler [optimization]: Aggregate snaks with the same property.

- Filter compiler: Use subqueries to implement fingerprints(?).

## Codec

### Repr

- Replace `eval()` by a proper parser (via lark).

## Store

- BUG: Bad bindings should be ignored when producing query results.  That
  is, they should be skipped with a warning.

- Add async API for Store.

### Mixer

- Revise the "sync" options.
