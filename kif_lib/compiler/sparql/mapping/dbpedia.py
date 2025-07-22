# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

from .... import itertools
from ....context import Context
from ....model import Item, Normal, Property, Text, Variables
from ....namespace import OWL, RDF, RDFS, Wikidata
from ....namespace.dbpedia import DBpedia
from ....typing import Final, TypeAlias
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M
from .wikidata import WikidataMapping

if TYPE_CHECKING:  # pragma: no cover
    from .dbpedia_options import DBpediaMappingOptions

__all__ = (
    'DBpediaMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral

#: Variables used in register patterns.
s, s0, p, v, v0 = Variables('s', 's0', 'p', 'v', 'v0')


class DBpediaMapping(M):
    """DBpedia SPARQL mapping."""

    _re_ontology_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(DBpedia.ONTOLOGY)}.*$')

    _re_resource_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(DBpedia.RESOURCE)}.*$')

    #: Checks whether argument is a DBpedia ontology term.
    CheckOntology: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_ontology_uri)

    #: Checks whether argument is a DBpedia resource.
    CheckResource: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_resource_uri)

    #: Checks whether argument is a Wikidata item.
    CheckWikidataItem: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=WikidataMapping._re_item_uri)

    #: Checks whether argument is a Wikidata property.
    CheckWikidataProperty: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=WikidataMapping._re_property_uri)

    __slots__ = (
        '_options',
    )

    #: DBpedia SPARQL mapping options.
    _options: DBpediaMappingOptions

    def __init__(
            self,
            wikidata_properties: bool | None = None,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()
        if wikidata_properties is not None:
            self.options.set_wikidata_properties(wikidata_properties)

    def _get_context_options(self) -> DBpediaMappingOptions:
        return self.context.options.compiler.sparql.mapping.dbpedia

    @property
    def options(self) -> DBpediaMappingOptions:
        """The DBpedia SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> DBpediaMappingOptions:
        """Gets the DBpedia SPARQL mapping options.

        Returns:
           DBpedia SPARQL mapping options.
        """
        return self._options

    def _start_r(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, OWL.Thing), itertools.chain((x,), xs)))

    def _start_oc(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, OWL.Class), itertools.chain((x,), xs)))

    def _start_op(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, RDF.Property), itertools.chain((x,), xs)))

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

    # -- pseudo-properties --

    @M.register(
        [wd.type(Item(s), Item(v))],
        {s: CheckResource()},
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_type(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_r(c, s)
        ty = RDF.type / (RDFS.subClassOf * '*')  # type: ignore
        c.q.triples()((s, ty, v))

    @M.register(
        [wd.subtype(Item(s), Item(v))],
        {s: CheckOntology(),
         v: CheckOntology()},
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_subtype(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_oc(c, s)
        subtype = RDFS.subClassOf * '+'  # type: ignore
        c.q.triples()((s, subtype, v))

    @M.register(
        [wd.label(Item(s), Text(v, v0))],
        {s: CheckResource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label(self, c: C, s: V_URI, v: VLiteral, v0: VLiteral) -> None:
        self._start_r(c, s)
        self._p_text(c, s, RDFS.label, v, v0)

    @M.register(
        [wd.label(Property(s, s0), Text(v, v0))],
        {s: CheckOntology()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_op(
            self,
            c: C,
            s: V_URI,
            s0: V_URI,
            v: VLiteral,
            v0: VLiteral) -> None:
        self._start_op(c, s)
        self._p_text(c, s, RDFS.label, v, v0)

    @M.register(
        [wd.description(Item(s), Text(v, v0))],
        {s: CheckResource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_description(
            self,
            c: C,
            s: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        self._start_r(c, s)
        self._p_text(c, s, RDFS.comment, v, v0)

    @M.register(
        [Property(p)(Item(s), Item(v))],
        {p: CheckOntology(),
         s: CheckResource(),
         v: CheckResource()},
        rank=Normal)
    def op_r_r(self, c: C, p: V_URI, s: V_URI, v: V_URI) -> None:
        self._start_r(c, s, v)
        self._start_op(c, p)
        b = c.bnode()
        c.q.triples()(
            (s, p, v),
            (p, RDFS.range, b),
            (b, RDF.type, OWL.Class))

    @M.register(
        [Property(p)(Item(s), Item(v))],
        {p: CheckWikidataProperty(),
         s: CheckResource(),
         v: CheckResource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def p_r_r(self, c: C, p: V_URI, s: V_URI, v: V_URI) -> None:
        if not self.options.wikidata_properties:
            raise self.Skip     # nothing to do
        dbp = c.fresh_qvar()
        c.q.triples()((dbp, OWL.equivalentProperty, p))
        self.op_r_r(c, dbp, s, v)
        if isinstance(p, Var):
            c.q.filter(c.q.strstarts(c.q.str(p), str(Wikidata.WD)))
        elif str(p) == wd.said_to_be_the_same_as.iri.content:
            raise self.Skip

    @M.register(
        [wd.said_to_be_the_same_as(Item(s), Item(v))],
        {s: CheckResource(),
         v: CheckWikidataItem()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_said_to_be_the_same_as(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_r(c, s)
        c.q.triples()((s, OWL.sameAs, v))
        if isinstance(v, Var):
            c.q.filter(c.q.strstarts(c.q.str(v), str(Wikidata.WD)))
