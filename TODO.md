# TODO

## Model

### Filter

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

### Time

- BUG: Fix the internal representation of dates and times.  Find an
  alternative to Python's datetime or add a new field to the time values to
  store the `+` or `-` sign of Wikidata datetime strings.

## Compiler

- Filter compiler (optimization): Aggregate snaks with the same property.

- Use subqueries to implement fingerprints(?).

## Codec

### Repr

- Replace `eval()` by a proper parser (via lark).

## Store

- Add async API for Store.
