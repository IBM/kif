# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.11.1 (?)

- Added `describe_mask` option to RDF encoder.  This determines whether
  statements corresponding to entity descriptors should be included in the
  serialization automatically.  The boolean aliases `describe_aliases`,
  `describe_items`, `describe_lexemes` can also be used to control this in
  the `KIF_Object.to_rdf()` call.

## 0.11.0 (2025-07-15)

- Added support for the pseudo-properties `TypeProperty()` and
  `SubtypeProperty()`, with aliases `wd.type` / `wd.a` and `wd.subtype`.
  These correspond to the primitive ontological relations of class
  membership (∈) and (proper) containment (⊊) taking into account the
  transitivity of the later.  The expression `wd.type(x)` compiles to the
  restriction "an instance of some subclass of `x`", while the expression
  `wd.subtype` compiles to the restriction "some subclass of `x`".

- Added support for basic property path fingerprints — essentially,
  sequential paths.  For example, the fingerprint
  `(wd.occupation/wd.a)(wd.musician)` stands for the entities whose
  occupation is an instance of a subclass of musician.

- Added support for rank mask.  More precisely now rank mask is being
  honored by the SPARQL compiler.  See `--rank-mask` option of KIF CLI.

- Added support for splitting monolithic queries generated by the SPARQL
  compiler into multiple disjoint subqueries.  The maximum number of
  disjoint subqueries to generate is controlled by the `omega` store option.
  By default, `omega` is set to 2.  See also the `--omega` option to KIF
  CLI.

- Added `memory` store.  Keeps a set of statements in memory and uses
  shallow-matching to implement `filter()`.

- Added `Value.display()` method to pretty-print any value, not only
  entities.

- Added `--profile` option to KIF CLI.  Profile the command using cProfile.

- Moved `best_ranked` flag from store API to filter object.

## 0.10.0 (2025-06-26)

- Added projected variants of `count()` and `filter()` to the Store API,
  i.e., `count_s()`, `count_p()`, `filter_s()`, `filter_p()`, etc.

- Optimized the queries generated by the SPARQL compiler to include explicit
  projection variables.

- Fixed long standing bug in the implementation of `count()` in SPARQL
  store.  It now counts statements with the same (s,p,v) only once.

- Added support for shallow-filters in reader stores.  This means that now
  they only return statements shallow-matching the given filter.

- Added `distinct_window_size` option to the store base class.  This option
  determines the size of the look-back window used to implement the
  `distinct` option. By default, `distinct_window_size` is set to 10000
  statements.

- Added `--debug` and `--info` options to KIF CLI.  Enable debug and
  info logging.

- Renamed `--no-best-ranked` to `--non-best-ranked` in KIF CLI's ask, count,
  and filter.

- Added `--value-is-quantity`, `--value-is-time`, and `--value-is-value`
  options to KIF CLI ask, count, and filter commands.  More aliases to
  common value mask settings.

## 0.9.2 (2025-06-09)

- Optimized the queries generated by the Wikidata mappings.  When a property
  schema is available, we use it to resolve "p:", "ps:", etc., which avoid
  an extra indirection in the query.  Added option `use_schema` to Wikidata
  SPARQL mappings to enable/disable this optimization.  By default, it is
  enabled.

- Added `--snak-is-*`, `--subject-is-*`, and `--value-is-*` options to KIF
  CLI commands `ask`, `filter`, and `count`.  These are aliases to common
  snak, subject, and value mask settings.

- Added the `--no-best-ranked` option to KIF CLI to make it consider
  non-best ranked statements.

## 0.9.1 (2025-06-06)

- Moved `fcntl` import to the RDFox store constructor. (Windows doesn't have
  fcntl.)

- Updated SPARQL filter compiler to honor fine-grained subject mask
  settings.

## 0.9.0 (2025-06-03)

- Added a default RDF schema to RDF encoder.  Properties without schema are
  now serialized using the Wikidata RDF schema by default.  The default
  schema can be changed via `kif.codec.rdf.encoder.schema` or overriden via
  the parameter `schema` of `KIF_Object.to_rdf()`.  Note that this changes
  the meaning of parameter `schema`, which breaks compatibility with
  previous versions.

- Added convenience methods (preamble, postamble, describe, and register) to
  the base reader store.  These allow for a fine-grained control of
  statement generation.

- Fixed a bug in Wikidata mappings which was causing a runtime error when
  fetching annotations of statements with pseudo-property.

- Fixed bug in reader base store which was causing the eager evaluation of
  filters.

## 0.8.2 (2025-05-27)

- Added `sparql-rdfox` store, a local RDF store that uses RDFox to evaluate
  SPARQL queries.  The `sparql-rdfox` backend in now used by default by the
  `rdf` store if a working `RDFox` command is available.

- Fixed a design issue in the internal Store API: `_afilter()` is no longer
  marked as `async`.  It returns an async iterator but it might not need to
  await for anything.

- Fixed the mapping of `wd.chemical_formula` in the SPARQL mapping of
  PubChem.  Now we pre/post process the chemical formula strings to
  substitute 0-9 by their UTF-8 subscript counterparts, ₀₋₉.

- Fixed the mapping of `wd.mass` in the SPARQL mapping of PubChem.  Now
  `wd.mass` is mapped to "exact mass" whose unit is dalton (Da).

- Added support for overriding store options in `Store.ask`, `Store.count`,
  `Store.filter` and `Store.mix` (plus their async versions).

- Changed KIF CLI to use async calls by default.  Added the `--no-async`
  option to force it to use sync calls.

- Added support for multiple names (separated by ";") in KIF CLI's `--store`
  option.

- Added optional `name` argument and `--describe` option to KIF CLI's
  `list-options` command.

## 0.8.1 (2025-05-15)

- Fixed support for distinct flag in reader stores.  It is now honored.

- Added support for `Encoder` expressions in `--encoder` in KIF CLI.

- Fixed handling of `--no-resolved` in KIF CLI.

## 0.8.0 (2025-05-14)

- Re-implemented store options using the option infrastructure.  Now the
  store options are kept in a stack, which allows the current options to be
  temporarily overriden using a `with` clause.

- Removed the legacy `Store.Flags` (superseded by options).

- Added reader stores: `json-reader`, `jsonl-reader`, and `csv-reader`.
  These are "pseudo-stores" used to quickly read statements from data files.

- Added `list-options` command to the KIF CLI tool.  Lists the all options
  in KIF context.

- Added `--module` option to the KIF CLI tool.  Loads module before running
  the tool.

- Added `--encoder` option to the `filter` command of KIF CLI tool.  Uses
  encoder to encode the statements before outputting them.

## 0.7.8 (2025-04-29)

- Added async support to the Store API.  Now there are async versions of the
  core methods: `acontains()`, `aask()`, `acount()`, `afilter()`.

- Added the `Store.lookahead` option to determine the number of non-blocking
  requests done in parallel by `afilter()` when advancing its results.

- Added the convenience methods `Store.mix` and `Store.amix` to mix the
  results of multiple filter evaluations.

## 0.7.7 (2025-04-24)

- Added support for registering property schemas for whole IRI namespaces.
  See `IRI.register`.  Updated the RDF encoder use the registered schema
  when no schema is provided for a given property.

- Added CLI tool (kif) with support for the filter call.

## 0.7.6 (2025-04-17)

- Fixed setup.py.  It was broken by the previous release due to the renaming
  of the version module.

## 0.7.5 (2025-04-17)

- Added support for customizing the opaque ids (wdref, wds, and wdv)
  generated by the RDF encoder.  This can be done via parameters
  `gen_wdref`, `gen_wds`, and `gen_wdv` of `KIF_Object.to_rdf()`.

- Added store-level `Store.distict` flag (analogous to `Store.limit`,
  `Store.page_size`, etc.).

- Fixed a bug in the `mixer` store that was causing the timeout property of
  child stores not to be properly initialized.

## 0.7.4 (2025-04-16)

- Added the `sparql-jena` store, a local RDF store that uses Jena to
  evaluate SPARQL queries.  The `sparql-jena` backend is now used by default
  by the `rdf` store if Jena is available.

- Added a base filter to `Store` API.  Now every store has a base filter
  which is &-ed with the filter supplied as an argument to the
  `Store.filter()` call.

- Fixed a bug in `mixer` that was causing it to not honor
  `Store.extra_references`.

- Fixed a bug in the SPARQL compiler that was causing RDFLib to generate the
  wrong results in `Store.filter_annotated`.

## 0.7.3 (2025-04-01)

- Fixed wds when compiling Wikidata filters.  When not collecting
  annotations, we now use a blank node for wds instead of a variable.  This
  way statements with the same (s,p,v) will *not* be counted as distinct.

## 0.7.2 (2025-04-01)

- Added a new encoder, `Dot`.  This is useful for displaying graphs.

## v0.7.1 (2025-03-31)

- Updated quickstart and API reference.  Removed legacy stuff.

## v0.7.0

- All SPARQL-based stores suffered a major refactoring.  Now they all derive
  from a base SPARQL store which supports multiple back-ends (currently,
  Httpx and RDFLib).  Also, the SPARQL-based stores now use the new SPARQL
  compilation pipeline, which is completely parameterized by SPARQL
  mappings.  The old SPARQL compilation code was removed.

- The code of other stores, including the common code in `abc`, was
  simplified.

- The Wikidata mappings now generate a single query to resolve
  `Store.filter_annotated()`.

- Legacy descriptor classes were removed, as these were superseded by
  pseudo-properties.

## 0.6.3 (2025-03-14)

- Fixed bug (regression) that was causing
  `Store.extra_references` to not be honored.

## 0.6.2 (2025-03-11)

- Fixed the query that was being generated by `get_annotations()` in the
  `SPARQL_Store`.  Now the query no longer assumes that properties occurring
  in qualifier and reference snaks adopt the Wikidata RDF schema.

## 0.4

- Added a new `range` field (datatype) to `Property`.  This information is
  now being retrieved automatically by most stores.

- Added new, simpler APIs to construct `SomeValueSnak`'s and
  `NoValueSnaks`'s.  That is, `Property.some_value()` and
  `Propeprty.no_value()`

- Renamed the `FilterPattern` object to `Filter` to distinguish it from
  patterns.

- Added support for more expressive fingerprints.  We now distinguish
  between value and snak fingerprints and allow these to be composed using
  and's (`&`) and or's (`|`).

- Added full support for entity masks to `Filter`.

- Updated the `SPARQL_Store` to use the compiler infrastructure and template
  instantiation mechanism to generate the query of `filter()` and parse the
  results.

- Added a new entity description downloader module/tool
  (`vocabulary.wd.downloader`).  Also, updated the format of the TSV files.
