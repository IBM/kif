# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import re

from .... import itertools
from ....model import Item, Normal, Property, Text, Variables
from ....namespace import OWL, RDF, RDFS, Wikidata
from ....namespace.dbpedia import DBpedia
from ....typing import Final, TypeAlias
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M
from .wikidata import WikidataMapping

__all__ = (
    'DBpediaMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral
e, p, q, x, y, z = Variables(*'epqxyz')


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

    def _start_r(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, OWL.Thing), itertools.chain((x,), xs)))

    def _start_op(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, RDF.Property), itertools.chain((x,), xs)))

    def _p_text(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral
    ) -> None:
        if isinstance(y, Var):
            c.q.triples()((e, p, x))
            c.q.bind(c.q.lang(x), y)
        elif isinstance(x, Var):
            c.q.triples()((e, p, x))
            c.q.filter(c.q.eq(c.q.lang(x), y))
        else:
            c.q.triples()((e, p, c.q.Literal(x, y)))

    @M.register(
        [wd.label(Item(e), Text(x, y))],
        {e: CheckResource()},
        rank=Normal)
    def wd_label(self, c: C, e: V_URI, x: VLiteral, y: VLiteral) -> None:
        self._start_r(c, e)
        self._p_text(c, e, RDFS.label, x, y)

    @M.register(
        [wd.label(Property(e), Text(x, y))],
        {e: CheckOntology()},
        rank=Normal)
    def wd_label_op(self, c: C, e: V_URI, x: VLiteral, y: VLiteral) -> None:
        self._start_op(c, e)
        self._p_text(c, e, RDFS.label, x, y)

    @M.register(
        [wd.description(Item(e), Text(x, y))],
        {e: CheckResource()},
        rank=Normal)
    def wd_description(self, c: C, e: V_URI, x: VLiteral, y: VLiteral) -> None:
        self._start_r(c, e)
        self._p_text(c, e, RDFS.comment, x, y)

    @M.register(
        [Property(p)(Item(x), Item(y))],
        {p: CheckOntology(),
         x: CheckResource(),
         y: CheckResource()},
        rank=Normal)
    def op_r_r(self, c: C, p: V_URI, x: V_URI, y: V_URI) -> None:
        self._start_r(c, x, y)
        self._start_op(c, p)
        b = c.bnode()
        c.q.triples()(
            (x, p, y),
            (p, RDFS.range, b),
            (b, RDF.type, OWL.Class))

    @M.register(
        [Property(p)(Item(x), Item(y))],
        {p: CheckWikidataProperty(),
         x: CheckResource(),
         y: CheckResource()},
        rank=Normal)
    def p_r_r(self, c: C, p: V_URI, x: V_URI, y: V_URI) -> None:
        dbp = c.fresh_qvar()
        c.q.triples()((dbp, OWL.equivalentProperty, p))
        self.op_r_r(c, dbp, x, y)
        if isinstance(p, Var):
            c.q.filter(c.q.strstarts(c.q.str(p), str(Wikidata.WD)))
        elif str(p) == wd.said_to_be_the_same_as.iri.content:
            raise self.Skip

    @M.register(
        [wd.said_to_be_the_same_as(Item(x), Item(y))],
        {x: CheckResource(),
         y: CheckWikidataItem()},
        rank=Normal)
    def wd_said_to_be_the_same_as(self, c: C, x: V_URI, y: V_URI) -> None:
        self._start_r(c, x)
        c.q.triples()((x, OWL.sameAs, y))
        if isinstance(y, Var):
            c.q.filter(c.q.strstarts(c.q.str(y), str(Wikidata.WD)))
