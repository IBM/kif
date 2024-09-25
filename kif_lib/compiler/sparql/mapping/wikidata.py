# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import re

from ....model import (
    Datatype,
    EntityVariable,
    ExternalId,
    IRI,
    Item,
    ItemVariable,
    Lexeme,
    LexemeVariable,
    Property,
    PropertyVariable,
    Quantity,
    Statement,
    String,
    Text,
    TextVariable,
    Time,
    Variable,
    Variables,
    VEntity,
    VText,
)
from ....namespace import ONTOLEX, RDF, WIKIBASE, Wikidata
from ....typing import cast, Final, TypeAlias
from ..compiler import SPARQL_Compiler as C
from .mapping import SPARQL_Mapping as M

__all__ = (
    'WikidataMapping',
)

Arg: TypeAlias = M.EntryCallbackArg

Literal: TypeAlias = C.Query.Literal
VLiteral: TypeAlias = C.Query.VLiteral

URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI

Var: TypeAlias = C.Query.Variable
Var3: TypeAlias = tuple[Var, Var, Var]

e, p, w, x, y, z = Variables(*'epwxyz')


class WikidataMapping(M):
    """Wikidata SPARQL mapping.

    Parameters:
       strict: Whether to be strict (assume full Wikidata compatibility).
    """

    _re_item_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}Q[1-9][0-9]*$')

    _re_lexeme_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}L[1-9][0-9]*$')

    _re_property_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}P[1-9][0-9]*$')

    class CheckDatatype(M.EntryCallbackArgProcessor):
        """Checks whether argument is a datatype value."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            if isinstance(arg, Datatype):
                return arg._to_rdflib()
            else:
                return arg

    class CheckItem(M.CheckURI):
        """Checks whether argument is an item URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_item_uri if m.strict else None)(m, c, arg)

    class CheckProperty(M.CheckURI):
        """Checks whether argument is a property URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_property_uri if m.strict else None)(m, c, arg)

    class CheckLexeme(M.CheckURI):
        """Checks whether argument is a lexeme URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_lexeme_uri if m.strict else None)(m, c, arg)

    class CheckIRI(M.CheckStr):
        """Checks whether argument is a IRI content."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            super().__call__(m, c, arg)
            ###
            # TODO: Validate URI?
            ###
            return URI(arg)

    __slots__ = (
        '_strict',
    )

    #: Whether to be strict (assume full Wikidata compatibility).
    _strict: bool

    def __init__(self, strict: bool = False):
        self._strict = bool(strict)

    @property
    def relax(self) -> bool:
        """The negation of the value of the strict flag."""
        return not self.get_strict()

    @property
    def strict(self) -> bool:
        """The value of the strict flag."""
        return self.get_strict()

    def get_strict(self) -> bool:
        """Gets the value of the strict flag.

        Returns:
           Strict flag.
        """
        return self._strict

    def _push(self, c: C, e: VEntity, p: V_URI, dt: URI) -> Var3:
        from ..mapping_filter_compiler import SPARQL_MappingFilterCompiler
        assert isinstance(c, SPARQL_MappingFilterCompiler)
        if isinstance(e, Variable):
            v = c.as_qvar(e)
            t = self._push_preamble(c, v, p, dt)
            with c.q.union():
                if type(e) is ItemVariable or type(e) is EntityVariable:
                    with c.q.group():
                        item_iri = c._fresh_iri_variable()
                        c._theta_add(e@Item, Item(item_iri))
                        c.q.triples()((v, WIKIBASE.sitelinks, c.bnode()))
                        c.q.bind(v, c._theta_add_as_qvar(item_iri))
                if type(e) is LexemeVariable or type(e) is EntityVariable:
                    with c.q.group():
                        lex_iri = c._fresh_iri_variable()
                        c._theta_add(e@Lexeme, Lexeme(lex_iri))
                        c.q.triples()((v, RDF.type, ONTOLEX.LexicalEntry))
                        c.q.bind(v, c._theta_add_as_qvar(lex_iri))
                if type(e) is PropertyVariable or type(e) is EntityVariable:
                    with c.q.group():
                        prop_dt = c._fresh_datatype_variable()
                        prop_dt_iri = c._fresh_iri_variable()
                        prop_iri = c._fresh_iri_variable()
                        c._theta_add(prop_dt, prop_dt_iri)
                        c._theta_add(e@Property, Property(prop_iri, prop_dt))
                        c.q.triples()(
                            (v, RDF.type, WIKIBASE.Property),
                            (v, WIKIBASE.propertyType,
                             c._theta_add_as_qvar(prop_dt_iri)))
                        c.q.bind(v, c._theta_add_as_qvar(prop_iri))
            return t
        elif isinstance(e, URI):
            v = c.theta.get(EntityVariable('e'))
            if isinstance(v, Item):
                return self._push_preamble_Q(
                    c, cast(URI, self.CheckItem()(self, c, e)), p, dt)
            elif isinstance(v, Lexeme):
                return self._push_preamble_L(
                    c, cast(URI, self.CheckLexeme()(self, c, e)), p, dt)
            elif isinstance(v, Property):
                return self._push_preamble_P(
                    c, cast(URI, self.CheckProperty()(self, c, e)), p, dt)
            else:
                raise c._should_not_get_here()
        else:
            raise c._should_not_get_here()

    def _push_preamble_Q(self, c: C, x: V_URI, p: V_URI, dt: URI) -> Var3:
        t = self._push_preamble(c, x, p, dt)
        c.q.triples()((x, WIKIBASE.sitelinks, c.q.bnode()))
        return t

    def _push_preamble_L(self, c: C, x: V_URI, p: V_URI, dt: URI) -> Var3:
        t = self._push_preamble(c, x, p, dt)
        c.q.triples()((x, RDF.type, ONTOLEX.LexicalEntry))
        return t

    def _push_preamble_P(self, c: C, x: V_URI, p: V_URI, dt: URI) -> Var3:
        t = self._push_preamble(c, x, p, dt)
        c.q.triples()((x, RDF.type, WIKIBASE.Property))
        return t

    def _push_preamble(self, c: C, x: V_URI, p: V_URI, dt: URI) -> Var3:
        p_, ps, wds = c.fresh_qvars(3)
        c.q.triples()(
            (x, p_, wds),
            (p, RDF.type, WIKIBASE.Property),
            (p, WIKIBASE.claim, p_),
            (p, WIKIBASE.propertyType, dt),
            (p, WIKIBASE.statementProperty, ps))
        if c.has_flags(c.BEST_RANK):
            c.q.triples()((wds, RDF.type, WIKIBASE.BestRank))
        return p_, ps, wds

    @M.register(
        Statement(e, Property(p)(Item(x))),
        {p: CheckProperty(),
         x: CheckItem()})
    def p_item(self, c: C, e: VEntity, p: V_URI, x: V_URI):
        _, ps, wds = self._push(c, e, p, WIKIBASE.WikibaseItem)
        c.q.triples()(
            (wds, ps, x),
            (x, WIKIBASE.sitelinks, c.q.bnode()))

    @M.register(
        Statement(e, Property(p)(Property(x, y))),
        {p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_property(self, c: C, e: VEntity, p: V_URI, x: V_URI, y: V_URI):
        _, ps, wds = self._push(c, e, p, WIKIBASE.WikibaseProperty)
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, WIKIBASE.Property),
            (x, WIKIBASE.propertyType, y))

    @M.register(
        Statement(e, Property(p)(Lexeme(x))),
        {p: CheckProperty(),
         x: CheckLexeme()})
    def p_lexeme(self, c: C, e: VEntity, p: V_URI, x: V_URI):
        _, ps, wds = self._push(c, e, p, WIKIBASE.WikibaseLexeme)
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, ONTOLEX.LexicalEntry))

    @M.register(
        Statement(e, Property(p)(IRI(x))),
        {p: CheckProperty(),
         x: CheckIRI()})
    def p_iri(self, c: C, e: VEntity, p: V_URI, x: V_URI):
        _, ps, wds = self._push(c, e, p, WIKIBASE.Url)
        c.q.triples()((wds, ps, x))

    @M.register(
        Statement(e, Property(p)(x@Text)),
        {p: CheckProperty()})
    def p_text(self, c: C, e: VEntity, p: V_URI, x: VLiteral | VText):
        _, ps, wds = self._push(c, e, p, WIKIBASE.Monolingualtext)
        if isinstance(x, Literal):
            c.q.triples()((wds, ps, x))
        elif isinstance(x, TextVariable):
            from ..mapping_filter_compiler import SPARQL_MappingFilterCompiler
            assert isinstance(c, SPARQL_MappingFilterCompiler)
            cnt = c._fresh_string_variable()
            tag = c._fresh_string_variable()
            c._theta_add(x, Text(cnt, tag))
            x = c._theta_add_as_qvar(cnt)
            c.q.bind(c.q.lang(x), c._theta_add_as_qvar(tag))
            c.q.triples()((wds, ps, x))
        else:
            raise c._should_not_get_here()

    @M.register(
        Statement(e, Property(p)(String(x))),
        {p: CheckProperty()})
    def p_string(self, c: C, e: VEntity, p: V_URI, x: VLiteral):
        _, ps, wds = self._push(c, e, p, WIKIBASE.String)
        c.q.triples()((wds, ps, x))

    @M.register(
        Statement(e, Property(p)(ExternalId(x))),
        {p: CheckProperty()})
    def p_external_id(self, c: C, e: VEntity, p: V_URI, x: VLiteral):
        _, ps, wds = self._push(c, e, p, WIKIBASE.ExternalId)
        c.q.triples()((wds, ps, x))

    @M.register(
        Statement(e, Property(p)(Quantity(x, y@Item, z, w))),
        {p: CheckProperty()},
        defaults={y: None, z: None, w: None})
    def p_quantity(
            self,
            c: C,
            e: VEntity,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral
    ):
        _, ps, wds = self._push(c, e, p, WIKIBASE.Quantity)
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.QuantityValue),
            (wdv, WIKIBASE.quantityAmount, x))
        if isinstance(y, Literal):
            c.q.triples()(
                (wdv, WIKIBASE.quantityUnit, y))
        elif isinstance(y, ItemVariable):
            with c.q.optional_if(self.relax):
                from ..mapping_filter_compiler import (
                    SPARQL_MappingFilterCompiler,
                )
                assert isinstance(c, SPARQL_MappingFilterCompiler)
                iri = c._fresh_iri_variable()
                c._theta_add(y, Item(iri))
                c.q.triples()(
                    (wdv, WIKIBASE.quantityUnit, c._theta_add_as_qvar(iri)))
                c.q.bind(c.as_qvar(iri), c.as_qvar(y))
        else:
            raise c._should_not_get_here()
        with c.q.optional_if(isinstance(z, Var)):
            c.q.triples()((wdv, WIKIBASE.quantityLowerBound, z))
        with c.q.optional_if(isinstance(z, Var)):
            c.q.triples()((wdv, WIKIBASE.quantityUpperBound, w))

    @M.register(
        Statement(e, Property(p)(Time(x, y, z, w@Item))),
        {p: CheckProperty(),
         y: M.CheckInt(),
         z: M.CheckInt()},
        defaults={y: None, z: None})
    def p_time(
            self,
            c: C,
            e: VEntity,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            z: VLiteral,
            w: V_URI
    ):
        _, ps, wds = self._push(c, e, p, WIKIBASE.Time)
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.TimeValue),
            (wdv, WIKIBASE.timeValue, x))
        with c.q.optional_if(isinstance(y, Var) and self.relax):
            c.q.triples()((wdv, WIKIBASE.timePrecision, y))
        with c.q.optional_if(isinstance(z, Var) and self.relax):
            c.q.triples()((wdv, WIKIBASE.timeTimezone, z))
        if isinstance(w, Literal):
            c.q.triples()((wdv, WIKIBASE.timeCalendarModel, w))
        elif isinstance(w, ItemVariable):
            with c.q.optional_if(self.relax):
                from ..mapping_filter_compiler import (
                    SPARQL_MappingFilterCompiler,
                )
                assert isinstance(c, SPARQL_MappingFilterCompiler)
                iri = c._fresh_iri_variable()
                c._theta_add(w, Item(iri))
                c.q.triples()(
                    (wdv, WIKIBASE.timeCalendarModel,
                     c._theta_add_as_qvar(iri)))
                c.q.bind(c.as_qvar(iri), c.as_qvar(w))
        else:
            raise c._should_not_get_here()

    @M.register(
        Statement(e, Property(x, y).some_value()),
        {x: CheckProperty(),
         y: CheckDatatype()})
    def p_some_value(self, c: C, e: VEntity, x: V_URI, y: V_URI):
        _, ps, wds = self._push(c, e, x, y)
        some = c.fresh_qvar()
        c.q.triples()((wds, ps, some))
        if self.strict:
            c.q.filter(c.q.call(WIKIBASE.isSomeValue, some))
        else:
            c.q.filter(c.q.is_blank(some) | (
                c.q.is_uri(some) & c.q.strstarts(
                    c.q.str(some), str(Wikidata.WDGENID))))

    @M.register(
        Statement(e, Property(x, y).no_value()),
        {x: CheckProperty(),
         y: CheckDatatype()})
    def p_no_value(self, c: C, e: VEntity, x: V_URI, y: V_URI):
        _, ps, wds = self._push(c, e, x, y)
        wdno = c.fresh_qvar()
        c.q.triples()(
            (x, WIKIBASE.novalue, wdno),
            (x, WIKIBASE.propertyType, y),
            (wds, RDF.type, wdno))
