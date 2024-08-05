TODO
====

Model
-----

- Statement patterns: We could start introducing patterns via a statement
  pattern, i.e., a statement template together with a variable constraint.

- Add `AnnotatedStatement` object to carry statement together with its set
  of annotation records.

- BUG: Fix the internal representation of dates and times.  Maybe we
  shouldn't use Python's datatime.

- Filter (new feature): Add support for "negation".  We can compile the
  negation of an atomic `v`, i.e., `~v`, as `FILTER(?x != v)`.  And we can
  compile the negation of a snak `S`, i.e., `~S`, as a `FILTER NOT EXISTS`.

- Fingerprint (normalization): We can use the distributive laws to decompose
  complex fingerprint.  E.g., `𝜂[A∧(B∨(C∧(D∨E)))]` ⤳ `𝜂[A∧B]∨𝜂[A∧(C∧(D∨E))]`
  ⤳ `(A∧B)∨𝜂[(X≔A∧C)∧(D∨E)]` ⤳ `(A∧B)∨𝜂[X∧(D∨E)]` ⤳ `(A∧B)∨𝜂[X∧D]∨𝜂[X∧E]` ⤳
  `(A∧B)∨(A∧C∧D)∨(A∧C∧E)`. Now we know that the value mask of the original
  formula is equal to the mask of `(A∧B) | (A∧C∧D) | (A∧C∧E)`; also we can
  break the original query into three queries (executed in parallel).  We
  should restrict this type of normalization to non-VALUES clauses.  One
  possible way to do this is to introduce a new kind of fingerprint
  ValuesFingerprint/OneOfFingepprint which behaves as `|` but aggregates
  only or-ed value fingerprints.


Compiler
--------

- Filter compiler (optimization): Aggregate snaks with the same property.

Codec
-----

- Wikidata RDF: Write a new Wikidata RDF encoder for model classes.  The
  proposed `AnnotatedStatement` object (see above) can help us here.

- Repr: Replace `eval()` by a proper parser (via lark).

Store
-----

- Add async API for Store.  See the technique used in
  `kif_lib.vocabulary.wd.downloader`.

- Mapper: We could use statement templates as the unity of mappings.  That
  is, an entry in the mapping could be a pair `(p,push)` where `p` is a
  statement pattern and `push()` is a function that takes a query builder as
  argument and pushes the SPARQL fragment that matches `p` in the target
  graph.  The `push()` function should also update the substitution with
  variables that occur in `p`, so that the final substitution will
  automatically translate from the target graph to KIF model objects.

- RDF: Allow user to construct a store by passing statement objects
  (requires Wikidata RDF encoder).
