# TODO

## Code

- Make sure that `get_context()` methods are defined as class-methods.

- Revise the use of `logger.exception()`.

### CLI

- Add `--set` option to the top-level command set KIF context options.

### Codec

- dict/JSON codec: For generating dicts/JSON in standard Wikidata format or
  a simplified JSON format.

- RDF encoder: Add an option to escape URLs.  (BUG?)

- Repr decoder: Replace `eval()` by a proper parser (via lark).

### Compiler

- PubChem mapping: Add support for the use of QIDs as compound identifiers
  in subjects and values. (?)

- SPARQL compiler: Add support for variables in fingerprints, e.g.,
  `filter(subject=x)`, `filter(subject=wd.shares_border_with(x))`,
  `filter(subject=p(wd.Brazil)`.

- SPARQL compiler: Aggregate snaks with the same property (optimization).

- SPARQL compiler: Use subqueries to implement fingerprints. (?)

- SPARQL compiler: Add support for matching annotations in filters.  For
  example, `filter(references=[wd.stated_in(wd.PubChem)])`.

- Add initial support for non-SPARQL query languages (SQL and Cypher).

### Context

- Entity registry: Cache the property-constraint
  (allowed-entity-types-constraint) of properties.  We could expose this as
  Property.domain (Item, Property, or Lexeme) and then use it to optimize
  the queries.

- Options: Allow KIF-object values in environment variables.  For example,
  one could set `WIKIDATA` to `IRI('https://www.wikidata.org/sparql')`. (?)

### Model

- Add support for per-class, more convenient version of
  `KIF_Object.replace()` which can handle `kwargs`.

- Add `context` argument to model classes, including `Filter`. (?)

- Extend support for generics to `OpenTerm` subclasses.

- Filter: Add "normalized" flag to instruct KIF to obtain the normalized
  value (when it exists).

- Filter: Add support for pseudo-property flag in `property_mask`.

- Filter: Add support for "negation".  We can compile the negation of an
  atomic `v`, i.e., `~v`, as `FILTER(?x != v)`.  And we can compile the
  negation of a snak `S`, i.e., `~S`, as a `FILTER NOT EXISTS`.

- Filter: Add support for compound filters.  E.g., we could add a
  FilterUnion to represent the union of two or more filters.  If no snak
  sets occur in the child patterns, then each child pattern becomes an entry
  in the VALUES clause of filter.  Otherwise, each child pattern becomes a
  separate call to filter() and these calls are merged by the union.

- Fingerprint: Normalization: We can use the distributive laws to decompose
  complex fingerprints.  E.g., `𝜂[A∧(B∨(C∧(D∨E)))]` ⤳
  `𝜂[A∧B]∨𝜂[A∧(C∧(D∨E))]` ⤳ `(A∧B)∨𝜂[(X≔A∧C)∧(D∨E)]` ⤳ `(A∧B)∨𝜂[X∧(D∨E)]` ⤳
  `(A∧B)∨𝜂[X∧D]∨𝜂[X∧E]` ⤳ `(A∧B)∨(A∧C∧D)∨(A∧C∧E)`. Now we know that the
  value mask of the original formula is equal to the mask of `(A∧B) |
  (A∧C∧D) | (A∧C∧E)`; also we can break the original query into three
  queries (executed in parallel).  We should restrict this type of
  normalization to non-VALUES clauses.  One possible way to do this is to
  introduce a new kind of fingerprint ValuesFingerprint/OneOfFingepprint
  which behaves as `|` but aggregates only or-ed value fingerprints.

- Text: Revise the use of `TTextLanguage`.  Maybe we should create an alias
  `Text.Language` for `String`.

- Time: BUG: Fix the internal representation of dates and times.  Find an
  alternative to Python's datetime or add a new field to the time values to
  store the `+` or `-` sign of Wikidata datetime strings.

- Time: Time values with no month or day should default to `01-01`.

- Time: `Time()` should default to `now()`.

### Store

- BUG: Bad bindings should be ignored when producing query results.  That
  is, they should be skipped with a warning.

- Sync via async: See Jupyter core's
  [run_sync()](https://github.com/jupyter/jupyter_core/blob/main/jupyter_core/utils/__init__.py).

- Add support for matching annotations (qualifiers, references, rank) in
  `Store.filter()` and `Store.filter_annotated()`.

- Add `Store.multifilter(subject, p1, p2, ...pn)` which returns a table
  whose lines are matching subjects and columns are the desired properties.

- Add support for obtaining normalized values.  Some possibilities: (i) make
  `Statement` carry an extra (normalized) value or value set; (ii) make
  value carry an extra (normalized) value or value set.  See comment about
  adding a "normalized" flag to `Filter`.

- Add support for testing whether a given statement is best-ranked.

- Add support for pagination, projection, etc., via an explicit "results"
  object.  Given the results, one can skip pages, apply a projection, etc.

- CSV store: Add support for a CSV store using the local SPARQL backend.
  One of the columns of the CSV should be used for the subject; the
  remaining columns should be used for properties.

- TTL/n3 reader: Use a state machine to read triples and construct
  statements progressively.

- Mixer: Add new types of mixers, e.g., chain, interleave, and, or.

- Mixer: Add support for entity unification: When a fingerprint is used with
  an identifier property (external id) we could ask the mixer to perform
  entity unification, i.e., use one of the underlying stores as the source
  of canonical entity ids.

- Mixer: Brainstorm: Add some notion of proportion.  For example, for the
  stores `(s1,s2)` we associate the proportion `(4,3)` meaning that at each
  cycle the mixer will return 4 statements from `s1` and 3 statements from
  `s2`.  Note that this is equivalent to using `(s1,s1,s1,s2,s2,s2)` as
  children.

- Mixer: Brainstorm: Exploit SPARQL federation in cases where children
  support the SPARQL protocol.

- RDFox: Rename `rdfox_pipe` to `rdfox_process`.

### Vocabulary

- Make vocabulary first-class objects.  The loaded vocabularies should be
  stored in the library context and the user should be able to load parts of
  a vocabulary, e.g., `wd.load('chemistry')`.

## Docs

- Revise the use of doc-strings to document class constructors, cf. `Store`
  and `Search`.
