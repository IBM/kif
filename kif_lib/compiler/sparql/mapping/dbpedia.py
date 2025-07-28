# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .... import functools, itertools
from ....context import Context
from ....model import Item, Normal, Property, Quantity, Text, Time, Variables
from ....namespace import OWL, RDF, RDFS, Wikidata, XSD
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

    _re_class_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(DBpedia.ONTOLOGY)}[A-Z].*$')

    _re_property_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(DBpedia.ONTOLOGY)}[a-z].*$')

    _re_resource_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(DBpedia.RESOURCE)}.*$')

    #: Checks whether argument is a DBpedia ontology term.
    CheckClass: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_class_uri)

    #: Checks whether argument is a DBpedia ontology term.
    CheckProperty: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_property_uri)

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
        {s: CheckClass(),
         v: CheckClass()},
        priority=M.VERY_LOW_PRIORITY,
        rank=Normal)
    def wd_subtype(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_oc(c, s)
        subtype = RDFS.subClassOf * '+'  # type: ignore
        c.q.triples()((s, subtype, v))

    @M.register(
        [wd.label(Item(s), Text(v, v0))],
        {s: CheckClass()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_oc(self, c: C, s: V_URI, v: VLiteral, v0: VLiteral) -> None:
        self._start_oc(c, s)
        self._p_text(c, s, RDFS.label, v, v0)

    @M.register(
        [wd.label(Item(s), Text(v, v0))],
        {s: CheckResource()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_r(self, c: C, s: V_URI, v: VLiteral, v0: VLiteral) -> None:
        self._start_r(c, s)
        self._p_text(c, s, RDFS.label, v, v0)

    @M.register(
        [wd.label(Property(s, s0), Text(v, v0))],
        {s: CheckProperty()},
        defaults={s0: None},
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
    def wd_description_r(
            self,
            c: C,
            s: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        self._start_r(c, s)
        self._p_text(c, s, RDFS.comment, v, v0)

    # -- real properties --

    @M.register(
        [wd.instance_of(Item(s), Item(v))],
        {s: CheckResource(),
         v: CheckClass()},
        rank=Normal)
    def wd_instance_of_r_oc(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_r(c, s)
        self._start_oc(c, v)
        c.q.triples()((s, RDF.type, v))

    @M.register(
        [wd.subclass_of(Item(s), Item(v))],
        {s: CheckClass(),
         v: CheckClass()},
        rank=Normal)
    def wd_subclass_of_oc_oc(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_oc(c, s, v)
        c.q.triples()((s, RDFS.subClassOf, v))

    @M.register(
        [wd.subproperty_of(Property(s), Property(v))],
        {s: CheckProperty(),
         v: CheckProperty()},
        rank=Normal)
    def wd_subproperty_of_op_op(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_op(c, s, v)
        c.q.triples()((s, RDFS.subPropertyOf, v))

    @M.register(
        [Property(p)(Item(s), Item(v))],
        {p: CheckProperty(),
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
        [Property(p)(Item(s), Quantity(v))],
        {p: CheckProperty(),
         s: CheckResource()},
        rank=Normal)
    def op_r_quantity(
            self,
            c: C,
            p: V_URI,
            s: V_URI,
            v: VLiteral
    ) -> None:
        self._start_r(c, s)
        self._start_op(c, p)
        d = c.fresh_qvar()
        c.q.triples()(
            (s, p, v),
            (p, RDFS.range, d))
        c.q.values(d)(
            (XSD.decimal,),
            (XSD.double,),
            (XSD.integer,),
            (XSD.nonNegativeInteger,),
            (XSD.nonPositiveInteger,),
            # TODO: Bind the unit for H, M, S. (?)
            (XSD.hour,),
            (XSD.minute,),
            (XSD.second,))

    @M.register(
        [Property(p)(Item(s), Text(v, v0))],
        {p: CheckProperty(),
         s: CheckResource()},
        rank=Normal)
    def op_r_text(
            self,
            c: C,
            p: V_URI,
            s: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        self._start_r(c, s)
        self._start_op(c, p)
        c.q.triples()((p, RDFS.range, RDF.langString))
        self._p_text(c, s, p, v, v0)

    @M.register(
        [Property(p)(Item(s), Time(
            v, Time.DAY, 0, wd.proleptic_Gregorian_calendar))],
        {p: CheckProperty(),
         s: CheckResource()},
        rank=Normal)
    def op_r_time(self, c: C, p: V_URI, s: V_URI, v: VLiteral) -> None:
        self._start_r(c, s)
        self._start_op(c, p)
        c.q.triples()(
            (s, p, v),
            (p, RDFS.range, XSD.date))

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
        if not self.options.wikidata_properties:
            raise self.Skip     # nothing to do
        self._start_r(c, s)
        c.q.triples()((s, OWL.sameAs, v))
        if isinstance(v, Var):
            c.q.filter(c.q.strstarts(c.q.str(v), str(Wikidata.WD)))
