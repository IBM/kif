# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .... import functools, itertools
from ....context import Context
from ....model import IRI, Item, Normal, String, Text, Variables
from ....namespace import RDF, RDFS, SKOS
from ....namespace.uniprot import UniProt, UNIPROT
from ....typing import Final, TypeAlias
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M

if TYPE_CHECKING:  # pragma: no cover
    from .uniprot_options import UniProtMappingOptions

__all__ = (
    'UniProtMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral

#: Variables used in register patterns.
s, s0, p, v, v0 = Variables('s', 's0', 'p', 'v', 'v0')


class UniProtMapping(M):
    """UniProt SPARQL mapping."""

# -- Checks ----------------------------------------------------------------

    _re_taxonomy_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(UniProt.TAXONOMY)}.*$')

    #: Checks whether argument is a taxonomy URI.
    CheckTaxonomy: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_taxonomy_uri)

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    #: UniProt SPARQL mapping options.
    _options: UniProtMappingOptions

    def __init__(
            self,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()

    def _get_context_options(self) -> UniProtMappingOptions:
        return self.context.options.compiler.sparql.mapping.uniprot

    @property
    def options(self) -> UniProtMappingOptions:
        """The UniProt SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> UniProtMappingOptions:
        """Gets the UniProt SPARQL mapping options.

        Returns:
           UniProt SPARQL mapping options.
        """
        return self._options

    def _start_taxonomy(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (
                y, RDF.type, UNIPROT.Taxon), itertools.chain((x,), xs)))

    def _p_text(
            self,
            c: C,
            s: V_URI,
            p: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        if isinstance(v0, Var):
            c.q.triples()((s, p, v))
            c.q.bind(c.q.lang(v), v0)
        elif isinstance(v, Var):
            c.q.triples()((s, p, v))
            c.q.filter(c.q.eq(c.q.lang(v), v0))
        else:
            c.q.triples()((s, p, c.q.Literal(v, v0)))

# -- Taxonomy ---------------------------------------------------------------

    @M.register(
        [wd.instance_of(Item(s), wd.taxon),
         wd.a(Item(s), wd.taxon)],
        {s: CheckTaxonomy()},
        rank=Normal)
    def wd_instance_of_taxononmy(self, c: C, s: V_URI) -> None:
        self._start_taxonomy(c, s)

    @M.register(
        [wd.subclass_of(Item(s), Item(v)),
         wd.type(Item(s), Item(v))],
        {s: CheckTaxonomy(),
         v: CheckTaxonomy()},
        rank=Normal)
    def wd_subclass_of_taxononmy(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_taxonomy(c, s, v)
        c.q.triples()((s, RDFS.subClassOf, v))

    @M.register(
        [wd.label(Item(s), Text(v, 'en')),
         wd.taxon_name(Item(s), String(v))],
        {s: CheckTaxonomy()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_taxonomy(self, c: C, s: V_URI, v: VLiteral) -> None:
        self._start_taxonomy(c, s)
        c.q.triples()((s, UNIPROT.scientificName, v))

    @M.register(
        [wd.alias(Item(s), Text(v, 'en'))],
        {s: CheckTaxonomy()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_alias_taxonomy(self, c: C, s: V_URI, v: VLiteral) -> None:
        self._start_taxonomy(c, s)
        c.q.triples()((s, UNIPROT.otherName, v))

    @M.register(
        [wd.narrower_external_class(Item(s), IRI(v))],
        {s: CheckTaxonomy(),
         v: CheckTaxonomy()},
        rank=Normal)
    def wd_narrower_external_class_taxononmy(
            self,
            c: C,
            s: V_URI,
            v: V_URI
    ) -> None:
        self._start_taxonomy(c, s, v)
        c.q.triples()((s, SKOS.narrowerTransitive, v))

    _taxon_rank_repl: Final[dict[str, str]] = {
        k: v.iri.content for k, v in {
            UNIPROT.Taxonomic_Rank_Class: wd.class_,
            UNIPROT.Taxonomic_Rank_Domain: wd.domain,
            UNIPROT.Taxonomic_Rank_Genus: wd.genus,
            UNIPROT.Taxonomic_Rank_Kingdom: wd.kingdom,
            UNIPROT.Taxonomic_Rank_Order: wd.order,
            UNIPROT.Taxonomic_Rank_Phylum: wd.phylum,
            UNIPROT.Taxonomic_Rank_Species: wd.species,
            UNIPROT.Taxonomic_Rank_Strain: wd.strain,
        }.items()
    }

    @M.register(
        [wd.taxon_rank(Item(s), Item(v))],
        {s: CheckTaxonomy(),    # pre
         v: M.CheckURI(replace_inv=_taxon_rank_repl)},
        {v: M.CheckURI(replace=_taxon_rank_repl)},  # post
        rank=Normal)
    def wd_taxon_rank_taxononmy(
            self,
            c: C,
            s: V_URI,
            v: V_URI
    ) -> None:
        self._start_taxonomy(c, s)
        c.q.triples()((s, UNIPROT.rank, v))
