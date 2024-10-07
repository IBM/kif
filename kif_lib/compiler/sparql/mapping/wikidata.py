# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re

from ....context import Section
from ....model import (
    Datatype,
    DatatypeVariable,
    EntityVariable,
    ExternalId,
    Filter,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    Statement,
    StatementTemplate,
    String,
    Term,
    Text,
    TextVariable,
    Time,
    Variable,
    Variables,
    VEntity,
    VText,
)
from ....namespace import ONTOLEX, RDF, WIKIBASE, Wikidata
from ....typing import (
    Any,
    cast,
    ClassVar,
    Final,
    Iterable,
    override,
    TypeAlias,
)
from ..mapping_filter_compiler import SPARQL_MappingFilterCompiler as C
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


@dataclasses.dataclass
class WikidataOptions(Section, name='wikidata'):
    """Wikidata SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_strict(kwargs)
        self._init_truthy(kwargs)

    # -- strict --

    _v_strict: ClassVar[tuple[str, bool | None]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_STRICT', None)

    _strict: bool | None

    def _init_strict(self, kwargs: dict[str, Any]) -> None:
        self.strict = kwargs.get('_strict', self.getenv(*self._v_strict))

    @property
    def strict(self) -> bool:
        """Whether to assume full Wikidata SPARQL compatibility."""
        return self.get_strict()

    @strict.setter
    def strict(self, strict: bool | None) -> None:
        self.set_strict(strict)

    @property
    def relax(self) -> bool:
        """Whether to assume only standard SPARQL compatibility."""
        return not self.strict

    def get_strict(self) -> bool:
        """Gets the value of the strict flag.

        Returns:
           Strict flag value.
        """
        return bool(self._strict)

    def set_strict(self, strict: bool | None) -> None:
        """Sets the value of the strict flag.

        Parameters:
           strict: Strict flag value or ``None``.
        """
        self._strict = bool(strict)

    # -- truthy --

    _v_truthy: ClassVar[tuple[str, Filter.DatatypeMask]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_TRUTHY',
         Filter.DatatypeMask(0))

    _truthy: Filter.DatatypeMask

    def _init_truthy(self, kwargs: dict[str, Any]) -> None:
        self.truthy = kwargs.get(
            '_truthy', int(self.getenv(
                self._v_truthy[0], self._v_truthy[1].value)))

    @property
    def truthy(self) -> Filter.DatatypeMask:
        """The truthy mask for filter compilation phase."""
        return self.get_truthy()

    @truthy.setter
    def truthy(self, truthy: Filter.TDatatypeMask) -> None:
        self.set_truthy(truthy)

    def get_truthy(self) -> Filter.DatatypeMask:
        """Gets the truthy mask for the filter compilation phase.

        Returns:
           Datatype mask.
        """
        return self._truthy

    def set_truthy(self, truthy: Filter.TDatatypeMask) -> None:
        """Sets the truthy mask for the filter compilation phase.

        Parameters:
           truthy: Datatype mask.
        """
        self._truthy = Filter.DatatypeMask.check(
            truthy, self.set_truthy, 'truthy', 1)


class WikidataMapping(M):
    """Wikidata SPARQL mapping.

    Parameters:
       strict: Whether to be strict (assume full Wikidata compatibility).
       truthy: Truthy mask to be used in the filter compilation phase.
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
                match=m._re_item_uri if m.options.strict else None)(
                m, c, arg)

    class CheckProperty(M.CheckURI):
        """Checks whether argument is a property URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_property_uri if m.options.strict else None)(
                m, c, arg)

    class CheckLexeme(M.CheckURI):
        """Checks whether argument is a lexeme URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_lexeme_uri if m.options.strict else None)(
                m, c, arg)

    class CheckIRI(M.CheckStr):
        """Checks whether argument is a IRI content."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            return URI(str(super().__call__(m, c, arg)))

    __slots__ = (
        '_options',
    )

    #: Wikidata SPARQL mapping options.
    _options: WikidataOptions

    def __init__(
            self,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None
    ) -> None:
        self._options = dataclasses.replace(
            self.context.options.compiler.sparql.mapping.wikidata)
        if strict is not None:
            self.options.set_strict(strict)
        if truthy is not None:
            self.options.set_truthy(truthy)

    @property
    def options(self) -> WikidataOptions:
        """The Wikidata SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> WikidataOptions:
        """Gets the Wikidata SPARQL mapping options.

        Returns:
           Wikidata SPARQL mapping options.
        """
        return self._options

    @override
    def postamble(self, c: C, targets: Iterable[M.EntryPattern]) -> None:
        subject_of_all_targets_is_fixed = all(map(lambda s: (
            isinstance(s, (Statement, StatementTemplate))
            and Term.is_closed(s.subject)), targets))
        if subject_of_all_targets_is_fixed:
            ###
            # IMPORTANT: We use ORDER BY(?wds) only if the subject of all
            # target patterns is fixed.  We do this to ensure that the
            # expected number of results is not too large.
            ###
            c.q.set_order_by(c.wds)

    def _start(self, c: C, e: VEntity, p: V_URI, dt: V_URI) -> Var3:
        if isinstance(e, Variable):
            v = c.as_qvar(e)
            t = self._start_any(c, v, p, dt)
            if not c.is_compiling_filter():
                return t        # nothing else to do
            with c.q.union():
                if type(e) is ItemVariable or type(e) is EntityVariable:
                    with c.q.group():
                        item_iri = c._fresh_iri_variable()
                        c.theta_add(e@Item, Item(item_iri))
                        c.q.triples()((v, WIKIBASE.sitelinks, c.bnode()))
                        c.q.bind(v, c.theta_add_as_qvar(item_iri))
                if type(e) is LexemeVariable or type(e) is EntityVariable:
                    with c.q.group():
                        lex_iri = c._fresh_iri_variable()
                        c.theta_add(e@Lexeme, Lexeme(lex_iri))
                        c.q.triples()((v, RDF.type, ONTOLEX.LexicalEntry))
                        c.q.bind(v, c.theta_add_as_qvar(lex_iri))
                if (type(e) is PropertyVariable
                        or type(e) is EntityVariable):
                    with c.q.group():
                        prop_dt = c._fresh_datatype_variable()
                        prop_dt_iri = c._fresh_iri_variable()
                        prop_iri = c._fresh_iri_variable()
                        c.theta_add(prop_dt, prop_dt_iri)
                        c.theta_add(
                            e@Property, Property(prop_iri, prop_dt))
                        c.q.triples()(
                            (v, RDF.type, WIKIBASE.Property),
                            (v, WIKIBASE.propertyType,
                             c.theta_add_as_qvar(prop_dt_iri)))
                        c.q.bind(v, c.theta_add_as_qvar(prop_iri))
            return t
        elif isinstance(e, ItemTemplate):
            assert isinstance(e.iri, IRI_Variable)
            return self._start_Q(c, c.as_qvar(e.iri), p, dt)
        elif isinstance(e, LexemeTemplate):
            assert isinstance(e.iri, IRI_Variable)
            return self._start_L(c, c.as_qvar(e.iri), p, dt)
        elif isinstance(e, PropertyTemplate):
            if isinstance(e.iri, IRI):
                s: V_URI = cast(URI, self.CheckProperty()(
                    self, c, URI(e.iri.content)))
            elif isinstance(e.iri, IRI_Variable):
                s = c.as_qvar(e.iri)
            else:
                raise c._should_not_get_here()
            assert e.range is not None
            prop_tpl_dt = e.range
            if isinstance(prop_tpl_dt, Datatype):
                v_prop_tpl_dt_iri: V_URI = prop_tpl_dt._to_rdflib()
            elif isinstance(prop_tpl_dt, DatatypeVariable):
                v_prop_tpl_dt_iri = c.theta_add(
                    prop_tpl_dt, c.fresh_qvar())
            else:
                raise c._should_not_get_here()
            t = self._start_P(c, s, p, dt)
            if c.is_compiling_filter():
                c.q.triples()((s, WIKIBASE.propertyType, v_prop_tpl_dt_iri))
            return t
        elif isinstance(e, URI):
            assert isinstance(c.target, (Statement, StatementTemplate))
            subject = c.target.subject
            assert subject is not None
            if isinstance(subject, (Item, ItemVariable)):
                return self._start_Q(
                    c, cast(URI, self.CheckItem()(self, c, e)), p, dt)
            elif isinstance(subject, (Lexeme, LexemeVariable)):
                return self._start_L(
                    c, cast(URI, self.CheckLexeme()(self, c, e)), p, dt)
            elif isinstance(subject, (Property, PropertyVariable)):
                return self._start_P(
                    c, cast(URI, self.CheckProperty()(self, c, e)), p, dt)
            else:
                raise c._should_not_get_here()
        else:
            raise c._should_not_get_here()

    def _start_Q(self, c: C, x: V_URI, p: V_URI, dt: V_URI) -> Var3:
        t = self._start_any(c, x, p, dt)
        if c.is_compiling_filter():
            c.q.triples()((x, WIKIBASE.sitelinks, c.q.bnode()))
        return t

    def _start_L(self, c: C, x: V_URI, p: V_URI, dt: V_URI) -> Var3:
        t = self._start_any(c, x, p, dt)
        if c.is_compiling_filter():
            c.q.triples()((x, RDF.type, ONTOLEX.LexicalEntry))
        return t

    def _start_P(self, c: C, x: V_URI, p: V_URI, dt: V_URI) -> Var3:
        t = self._start_any(c, x, p, dt)
        if c.is_compiling_filter():
            c.q.triples()((x, RDF.type, WIKIBASE.Property))
        return t

    def _start_any(self, c: C, x: V_URI, p: V_URI, dt: V_URI) -> Var3:
        wds = c.wds
        p_, ps = c.fresh_qvars(2)
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
        _, ps, wds = self._start(c, e, p, WIKIBASE.WikibaseItem)
        c.q.triples()(
            (wds, ps, x),
            (x, WIKIBASE.sitelinks, c.q.bnode()))

    @M.register(
        Statement(e, Property(p)(Property(x, y))),
        {p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_property(self, c: C, e: VEntity, p: V_URI, x: V_URI, y: V_URI):
        _, ps, wds = self._start(c, e, p, WIKIBASE.WikibaseProperty)
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, WIKIBASE.Property),
            (x, WIKIBASE.propertyType, y))

    @M.register(
        Statement(e, Property(p)(Lexeme(x))),
        {p: CheckProperty(),
         x: CheckLexeme()})
    def p_lexeme(self, c: C, e: VEntity, p: V_URI, x: V_URI):
        _, ps, wds = self._start(c, e, p, WIKIBASE.WikibaseLexeme)
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, ONTOLEX.LexicalEntry))

    @M.register(
        Statement(e, Property(p)(IRI(x))),
        {p: CheckProperty(),
         x: CheckIRI()})
    def p_iri(self, c: C, e: VEntity, p: V_URI, x: V_URI):
        _, ps, wds = self._start(c, e, p, WIKIBASE.Url)
        c.q.triples()((wds, ps, x))

    @M.register(
        Statement(e, Property(p)(x@Text)),
        {p: CheckProperty()})
    def p_text(self, c: C, e: VEntity, p: V_URI, x: VLiteral | VText):
        _, ps, wds = self._start(c, e, p, WIKIBASE.Monolingualtext)
        if isinstance(x, Literal):
            c.q.triples()((wds, ps, x))
        elif isinstance(x, TextVariable):
            cnt = c._fresh_string_variable()
            tag = c._fresh_string_variable()
            c.theta_add(x, Text(cnt, tag))
            x = c.theta_add_as_qvar(cnt)
            c.q.bind(c.q.lang(x), c.theta_add_as_qvar(tag))
            c.q.triples()((wds, ps, x))
        else:
            raise c._should_not_get_here()

    @M.register(
        Statement(e, Property(p)(String(x))),
        {p: CheckProperty()})
    def p_string(self, c: C, e: VEntity, p: V_URI, x: VLiteral):
        _, ps, wds = self._start(c, e, p, WIKIBASE.String)
        c.q.triples()((wds, ps, x))

    @M.register(
        Statement(e, Property(p)(ExternalId(x))),
        {p: CheckProperty()})
    def p_external_id(self, c: C, e: VEntity, p: V_URI, x: VLiteral):
        _, ps, wds = self._start(c, e, p, WIKIBASE.ExternalId)
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
        self._p_quantity(
            c, p, x, y, z, w, self._start(c, e, p, WIKIBASE.Quantity))

    def _p_quantity(
            self,
            c: C,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral,
            var3: Var3
    ) -> None:
        _, ps, wds = var3
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.QuantityValue),
            (wdv, WIKIBASE.quantityAmount, x))
        if isinstance(y, URI):
            c.q.triples()(
                (wdv, WIKIBASE.quantityUnit, y))
        elif isinstance(y, ItemVariable):
            if not c.is_compiling_fingerprint():
                with c.q.optional_if(self.options.relax):
                    iri = c._fresh_iri_variable()
                    c.theta_add(y, Item(iri))
                    c.q.triples()(
                        (wdv, WIKIBASE.quantityUnit,
                         c.theta_add_as_qvar(iri)))
                    c.q.bind(c.as_qvar(iri), c.as_qvar(y))
        else:
            raise c._should_not_get_here()
        if not (isinstance(z, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(z, Var)):
                c.q.triples()((wdv, WIKIBASE.quantityLowerBound, z))
        if not (isinstance(w, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(w, Var)):
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
        _, ps, wds = self._start(c, e, p, WIKIBASE.Time)
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.TimeValue),
            (wdv, WIKIBASE.timeValue, x))
        if not (isinstance(y, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(y, Var) and self.options.relax):
                c.q.triples()((wdv, WIKIBASE.timePrecision, y))
        if not (isinstance(z, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(z, Var) and self.options.relax):
                c.q.triples()((wdv, WIKIBASE.timeTimezone, z))
        if isinstance(w, URI):
            c.q.triples()((wdv, WIKIBASE.timeCalendarModel, w))
        elif isinstance(w, ItemVariable):
            if not c.is_compiling_fingerprint():
                with c.q.optional_if(self.options.relax):
                    iri = c._fresh_iri_variable()
                    c.theta_add(w, Item(iri))
                    c.q.triples()(
                        (wdv, WIKIBASE.timeCalendarModel,
                         c.theta_add_as_qvar(iri)))
                    c.q.bind(c.as_qvar(iri), c.as_qvar(w))
        else:
            raise c._should_not_get_here()

    @M.register(
        Statement(e, Property(x, y).some_value()),
        {x: CheckProperty(),
         y: CheckDatatype()})
    def p_some_value(self, c: C, e: VEntity, x: V_URI, y: V_URI):
        _, ps, wds = self._start(c, e, x, y)
        some = c.fresh_qvar()
        c.q.triples()((wds, ps, some))
        if self.options.strict:
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
        _, ps, wds = self._start(c, e, x, y)
        wdno = c.fresh_qvar()
        c.q.triples()(
            (x, WIKIBASE.novalue, wdno),
            (x, WIKIBASE.propertyType, y),
            (wds, RDF.type, wdno))
