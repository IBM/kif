# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import itertools
from ... import namespace as NS
from ...model import (
    DeepDataValue,
    Entity,
    ExternalId,
    ExternalIdVariable,
    Filter,
    IRI,
    IRI_Variable,
    Item,
    ItemVariable,
    Lexeme,
    LexemeVariable,
    NoValueSnak,
    NoValueSnakVariable,
    Property,
    PropertyVariable,
    Quantity,
    QuantityVariable,
    SomeValueSnak,
    SomeValueSnakVariable,
    Statement,
    StatementVariable,
    String,
    StringVariable,
    Text,
    TextVariable,
    Time,
    TimeVariable,
    Value,
    ValueSnak,
    ValueSnakVariable,
    Variable,
    VariablePattern,
)
from ...model.fingerprint import (
    AndFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    Fingerprint,
    FullFingerprint,
    OrFingerprint,
    SnakFingerprint,
    ValueFingerprint,
)
from ...typing import Any, cast, Iterable, override, Self
from .builder import Query
from .pattern_compiler import SPARQL_PatternCompiler


class SPARQL_FilterCompiler(SPARQL_PatternCompiler):
    """SPARQL filter compiler."""

    __slots__ = (
        '_filter',
        '_wds',
    )

    #: The source filter.
    _filter: Filter

    #: The query variable holding the wds.
    _wds: Query.Variable

    def __init__(
            self,
            filter: Filter,
            flags: SPARQL_FilterCompiler.Flags | None = None
    ) -> None:
        super().__init__(Variable('_', Statement), flags)
        self._filter = filter
        self._wds = self.q.fresh_var()

    @property
    def filter(self) -> Filter:
        """The source filter."""
        return self.get_filter()

    def get_filter(self) -> Filter:
        """Gets the source filter.

        Returns:
           Filter.
        """
        return self._filter

    @property
    def wds(self) -> Query.Variable:
        """The variable storing the statement id."""
        return self.get_wds()

    def get_wds(self) -> Query.Variable:
        """Gets the variable storing the statement id.

        Returns:
           Query.Variable.
        """
        return self._wds

    @override
    def compile(self) -> Self:
        filter = self._filter.normalize()
        if not filter.is_empty():
            self._push_filter(filter)
        return self

    def _push_filter(self, filter: Filter) -> None:
        assert isinstance(self.pattern, VariablePattern)
        assert isinstance(self.pattern.variable, StatementVariable)
        # Subject variable.
        subject = self._fresh_entity_variable()
        if isinstance(filter.subject, ValueFingerprint):
            assert isinstance(filter.subject.value, Entity)
            v_subject: Query.V_URI = cast(Query.V_URI, self._as_simple_value(
                filter.subject.value))
        else:
            v_subject = self.as_qvar(subject)
        # Snak variable.
        snak = self._fresh_snak_variable()
        self._theta_add(self.pattern.variable, Statement(subject, snak))
        # Property variable.
        property = self._fresh_property_variable()
        if isinstance(filter.property, ValueFingerprint):
            assert isinstance(filter.property.value, Property)
            v_property: Query.V_URI = cast(Query.V_URI, self._as_simple_value(
                filter.property.value))
        else:
            v_property = self.as_qvar(property)
        wds = self.wds
        p = self.q.fresh_var()
        ###
        # IMPORTANT: Some SPARQL engines are sensitive to the place where a
        # variable is bound.  As a rule of thumb, we should bind variables
        # as late as possible, i.e., as close as possible to where they are
        # actually used.  This is why we do not bind the `ps`, `wdno`, etc.,
        # here.
        ###
        self.q.triples()(
            (v_subject, p, wds),
            (v_property, NS.WIKIBASE.claim, p))
        # Best-ranked only?
        best_ranked = self.has_flags(self.BEST_RANK)
        if best_ranked:
            self.q.triples()((wds, NS.RDF.type, NS.WIKIBASE.BestRank))
        # Push subject.
        with self.q.group():
            with self.q.union():
                if bool(filter.subject_mask & filter.ITEM):
                    with self.q.group():
                        self._bind_as_item(
                            v_subject, ItemVariable(subject.name))
                if bool(filter.subject_mask & filter.PROPERTY):
                    with self.q.group():
                        self._bind_as_property(
                            v_subject, PropertyVariable(subject.name))
                if bool(filter.subject_mask & filter.LEXEME):
                    with self.q.group():
                        self._bind_as_lexeme(
                            v_subject, LexemeVariable(subject.name))
            if isinstance(v_subject, Query.Variable):
                self._push_fingerprint(
                    filter.subject, v_subject, v_property, wds)
        # Push property.
        with self.q.group():
            self._bind_as_property(v_property, property)
            if isinstance(v_property, Query.Variable):
                self._push_fingerprint(
                    filter.property, v_property, v_property, wds)
        # Push value.
        try_value_snak = bool(
            filter.snak_mask & Filter.VALUE_SNAK
            and self.has_flags(self.VALUE_SNAK))
        try_some_value_snak = bool(
            filter.snak_mask & Filter.SOME_VALUE_SNAK
            and self.has_flags(self.SOME_VALUE_SNAK))
        try_no_value_snak = bool(
            filter.snak_mask & Filter.NO_VALUE_SNAK
            and self.has_flags(self.NO_VALUE_SNAK))
        assert try_value_snak or try_some_value_snak or try_no_value_snak
        with self.q.union():
            if try_value_snak:
                value_mask = filter.value_mask\
                    & filter.property.range_datatype_mask
                with self.q.group():
                    value = self._fresh_value_variable()
                    v_value: Query.VTerm
                    if isinstance(filter.value, ValueFingerprint):
                        assert isinstance(filter.value.value, Value)
                        v_value = self._as_simple_value(filter.value.value)
                    else:
                        v_value = self.as_qvar(value)
                    self._theta_add(
                        ValueSnakVariable(snak.name),
                        ValueSnak(property, value))
                    ps = self.q.fresh_var()
                    self.q.triples()(
                        (v_property, NS.WIKIBASE.statementProperty, ps),
                        (wds, ps, v_value))
                    with self.q.group():
                        with self.q.union():
                            if value_mask & filter.ITEM:
                                with self.q.group():  # item?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.WikibaseItem))
                                    assert not isinstance(
                                        v_value, Query.Literal)
                                    self._bind_as_item(
                                        v_value, ItemVariable(value.name))
                            if value_mask & filter.PROPERTY:
                                with self.q.group():  # property?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.WikibaseProperty))
                                    assert not isinstance(
                                        v_value, Query.Literal)
                                    self._bind_as_property(
                                        v_value, PropertyVariable(value.name))
                            if value_mask & filter.LEXEME:
                                with self.q.group():  # lexeme?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.WikibaseLexeme))
                                    assert not isinstance(
                                        v_value, Query.Literal)
                                    self._bind_as_lexeme(
                                        v_value, LexemeVariable(value.name))
                            if value_mask & filter.IRI:
                                with self.q.group():  # iri?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.Url),
                                        (wds, ps, v_value))
                                    assert not isinstance(
                                        v_value, Query.Literal)
                                    self._bind_as_iri(
                                        v_value, IRI_Variable(value.name))
                            if value_mask & filter.TEXT:
                                with self.q.group():  # text?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.Monolingualtext),
                                        (wds, ps, v_value))
                                    assert not isinstance(v_value, Query.URI)
                                    self._bind_as_text(
                                        v_value, TextVariable(value.name))
                            if value_mask & filter.STRING:
                                with self.q.group():  # string?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.String),
                                        (wds, ps, v_value))
                                    assert not isinstance(v_value, Query.URI)
                                    self._bind_as_string(
                                        v_value, StringVariable(value.name))
                            if value_mask & (
                                    filter.STRING | filter.EXTERNAL_ID):
                                with self.q.group():  # external id?
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.ExternalId),
                                        (wds, ps, v_value))
                                    assert not isinstance(v_value, Query.URI)
                                    self._bind_as_external_id(
                                        v_value,
                                        ExternalIdVariable(value.name))
                            if value_mask & filter.QUANTITY:
                                with self.q.group():  # quantity?
                                    psv, wdv = self.q.fresh_vars(2)
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.Quantity),
                                        (v_property,
                                         NS.WIKIBASE.statementValue,
                                         psv),
                                        (wds, psv, wdv),
                                        (wdv, NS.RDF.type,
                                         NS.WIKIBASE.QuantityValue))
                                    assert not isinstance(v_value, Query.URI)
                                    qt: Quantity | None = None
                                    if isinstance(
                                            filter.value, ValueFingerprint):
                                        assert isinstance(
                                            filter.value.value, Quantity)
                                        qt = filter.value.value
                                    self._bind_as_quantity(
                                        v_value, wdv,
                                        QuantityVariable(value.name), qt)
                            if value_mask & filter.TIME:
                                with self.q.group():  # time?
                                    psv, wdv = self.q.fresh_vars(2)
                                    self.q.triples()(
                                        (v_property,
                                         NS.WIKIBASE.propertyType,
                                         NS.WIKIBASE.Time),
                                        (v_property,
                                         NS.WIKIBASE.statementValue,
                                         psv),
                                        (wds, psv, wdv),
                                        (wdv, NS.RDF.type,
                                         NS.WIKIBASE.TimeValue))
                                    assert not isinstance(v_value, Query.URI)
                                    tm: Time | None = None
                                    if isinstance(
                                            filter.value, ValueFingerprint):
                                        assert isinstance(
                                            filter.value.value, Time)
                                        tm = filter.value.value
                                    self._bind_as_time(
                                        v_value, wdv,
                                        TimeVariable(value.name), tm)
                        if isinstance(v_value, Query.Variable):
                            self._push_fingerprint(
                                filter.value, v_value, v_property, wds)
            if try_some_value_snak:
                with self.q.group():
                    prop_some_datatype = self._fresh_datatype_variable()
                    prop_some_datatype_iri = self._fresh_iri_variable()
                    self._theta_add(
                        prop_some_datatype_iri,
                        self.as_qvar(prop_some_datatype_iri))
                    self._theta_add(
                        prop_some_datatype, prop_some_datatype_iri)
                    prop_some = self._fresh_property_variable()
                    prop_some_iri = self._fresh_iri_variable()
                    self._theta_add(
                        prop_some_iri, self.as_qvar(prop_some_iri))
                    self._theta_add(
                        prop_some, Property(prop_some_iri, prop_some_datatype))
                    self._theta_add(
                        SomeValueSnakVariable(snak.name),
                        SomeValueSnak(prop_some))
                    ps, v_some = self.q.fresh_vars(2)
                    self.q.triples()(
                        (v_property, NS.WIKIBASE.statementProperty, ps),
                        (v_property, NS.WIKIBASE.propertyType,
                         self.as_qvar(prop_some_datatype_iri)),
                        (wds, ps, v_some))
                    self.q.bind(v_property, self.as_qvar(prop_some_iri))
                    self._push_some_value_filter(v_some)
            if try_no_value_snak:
                with self.q.group():
                    prop_no_datatype = self._fresh_datatype_variable()
                    prop_no_datatype_iri = self._fresh_iri_variable()
                    self._theta_add(
                        prop_no_datatype_iri,
                        self.as_qvar(prop_no_datatype_iri))
                    self._theta_add(
                        prop_no_datatype, prop_no_datatype_iri)
                    prop_no = self._fresh_property_variable()
                    prop_no_iri = self._fresh_iri_variable()
                    self._theta_add(
                        prop_no_iri, self.as_qvar(prop_no_iri))
                    self._theta_add(
                        prop_no, Property(prop_no_iri, prop_no_datatype))
                    self._theta_add(
                        NoValueSnakVariable(snak.name),
                        NoValueSnak(prop_no))
                    wdno = self.q.fresh_var()
                    self.q.triples()(
                        (v_property, NS.WIKIBASE.novalue, wdno),
                        (v_property, NS.WIKIBASE.propertyType,
                         self.as_qvar(prop_no_datatype_iri)),
                        (wds, NS.RDF.type, wdno))
                    self.q.bind(v_property, self.as_qvar(prop_no_iri))

    def _bind_as_item(
            self,
            dest: Query.V_URI,
            var: ItemVariable | None = None
    ) -> None:
        var = var or ItemVariable(str(dest))
        iri = self._fresh_iri_variable()
        self._theta_add(var, Item(iri))
        self.q.triples()((dest, NS.WIKIBASE.sitelinks, self.bnode()))
        self.q.bind(dest, self._theta_add(iri, self.as_qvar(iri)))

    def _bind_as_property(
            self,
            dest: Query.V_URI,
            var: PropertyVariable | None = None
    ) -> None:
        var = var or PropertyVariable(str(dest))
        datatype = self._fresh_datatype_variable()
        datatype_iri = self._fresh_iri_variable()
        iri = self._fresh_iri_variable()
        self._theta_add(datatype, datatype_iri)
        self._theta_add(var, Property(iri, datatype))
        self.q.triples()(
            (dest, NS.RDF.type, NS.WIKIBASE.Property),
            (dest, NS.WIKIBASE.propertyType, self._theta_add(
                datatype_iri, self.as_qvar(datatype_iri))))
        self.q.bind(dest, self._theta_add(iri, self.as_qvar(iri)))

    def _bind_as_lexeme(
            self,
            dest: Query.V_URI,
            var: LexemeVariable | None = None
    ) -> None:
        var = var or LexemeVariable(str(dest))
        iri = self._fresh_iri_variable()
        self._theta_add(var, Lexeme(iri))
        self.q.triples()((dest, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        self.q.bind(dest, self._theta_add(iri, self.as_qvar(iri)))

    def _bind_as_iri(
            self,
            dest: Query.V_URI,
            var: IRI_Variable | None = None
    ) -> None:
        var = var or IRI_Variable(str(dest))
        content = self._fresh_string_variable()
        self._theta_add(var, IRI(content))
        self.q.bind(dest, self._theta_add(content, self.as_qvar(content)))

    def _bind_as_text(
            self,
            dest: Query.VLiteral,
            var: TextVariable | None = None
    ) -> None:
        var = var or TextVariable(str(dest))
        content = self._fresh_string_variable()
        lang = self._fresh_string_variable()
        self._theta_add(var, Text(content, lang))
        self.q.bind(dest, self._theta_add(content, self.as_qvar(content)))
        self.q.bind(self.q.lang(dest), self._theta_add(
            lang, self.as_qvar(lang)))

    def _bind_as_string(
            self,
            dest: Query.VLiteral,
            var: StringVariable | None = None
    ) -> None:
        var = var or StringVariable(str(dest))
        content = self._fresh_string_variable()
        self._theta_add(var, String(content))
        self.q.bind(dest, self._theta_add(content, self.as_qvar(content)))

    def _bind_as_external_id(
            self,
            dest: Query.VLiteral,
            var: ExternalIdVariable | None = None
    ) -> None:
        var = var or ExternalIdVariable(str(dest))
        content = self._fresh_string_variable()
        self._theta_add(var, ExternalId(content))
        self.q.bind(dest, self._theta_add(content, self.as_qvar(content)))

    def _bind_as_quantity(
            self,
            dest: Query.VLiteral,
            wdv: Query.Variable,
            var: QuantityVariable | None = None,
            qt: Quantity | None = None
    ) -> None:
        var = var or QuantityVariable(str(dest))
        amount = self._fresh_quantity_variable()
        unit = self._theta_add_default(self._fresh_item_variable(), None)
        lower = self._theta_add_default(self._fresh_quantity_variable(), None)
        upper = self._theta_add_default(self._fresh_quantity_variable(), None)
        self._theta_add(var, Quantity(amount, unit, lower, upper))
        # Push amount.
        if qt is not None:
            v_amount: Query.VLiteral = cast(
                Query.Literal, self._as_simple_value(Quantity(qt.amount)))
            self.q.bind(
                v_amount, self._theta_add(amount, self.as_qvar(amount)))
        else:
            v_amount = self.as_qvar(amount)
            self._theta_add(amount, v_amount)
        self.q.triples()((wdv, NS.WIKIBASE.quantityAmount, v_amount))
        # Push unit.
        if qt is not None and qt.unit is not None:
            v_unit: Query.V_URI = cast(
                Query.URI, self._as_simple_value(qt.unit))
            self.q.bind(
                v_unit, self._theta_add(unit, self.as_qvar(unit)))
        else:
            v_unit = self.as_qvar(unit)
            self._theta_add(unit, v_unit)
        with self.q.optional_if(isinstance(v_unit, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.quantityUnit, v_unit))
        # Push lower-bound.
        if qt is not None and qt.lower_bound is not None:
            v_lower: Query.VLiteral = cast(
                Query.Literal, self._as_simple_value(Quantity(qt.lower_bound)))
            self.q.bind(
                v_lower, self._theta_add(lower, self.as_qvar(lower)))
        else:
            v_lower = self.as_qvar(lower)
            self._theta_add(lower, v_lower)
        with self.q.optional_if(isinstance(v_lower, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.quantityLowerBound, v_lower))
        # Push upper-bound.
        if qt is not None and qt.upper_bound is not None:
            v_upper: Query.VLiteral = cast(
                Query.Literal, self._as_simple_value(Quantity(qt.upper_bound)))
            self.q.bind(
                v_upper, self._theta_add(upper, self.as_qvar(upper)))
        else:
            v_upper = self.as_qvar(upper)
            self._theta_add(upper, v_upper)
        with self.q.optional_if(isinstance(v_upper, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.quantityUpperBound, v_upper))

    def _bind_as_time(
            self,
            dest: Query.VLiteral,
            wdv: Query.Variable,
            var: TimeVariable | None = None,
            tm: Time | None = None
    ) -> None:
        var = var or TimeVariable(str(dest))
        time = self._fresh_time_variable()
        prec = self._theta_add_default(self._fresh_quantity_variable(), None)
        tz = self._theta_add_default(self._fresh_quantity_variable(), None)
        cal = self._theta_add_default(self._fresh_item_variable(), None)
        self._theta_add(var, Time(time, prec, tz, cal))
        # Push time.
        if tm is not None:
            v_time: Query.VLiteral = cast(
                Query.Literal, self._as_simple_value(Time(tm.time)))
            self.q.bind(v_time, self._theta_add(time, self.as_qvar(time)))
        else:
            v_time = self.as_qvar(time)
            self._theta_add(time, v_time)
        self.q.triples()((wdv, NS.WIKIBASE.timeValue, v_time))
        # Push precision.
        if tm is not None and tm.precision is not None:
            v_prec: Query.VLiteral = Query.Literal(tm.precision.value)
            self.q.bind(v_prec, self._theta_add(prec, self.as_qvar(prec)))
        else:
            v_prec = self.as_qvar(prec)
            self._theta_add(prec, v_prec)
        with self.q.optional_if(isinstance(v_prec, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.timePrecision, v_prec))
        # Push timezone.
        if tm is not None and tm.timezone is not None:
            v_tz: Query.VLiteral = Query.Literal(tm.timezone)
            self.q.bind(v_tz, self._theta_add(tz, self.as_qvar(tz)))
        else:
            v_tz = self.as_qvar(tz)
            self._theta_add(tz, v_tz)
        with self.q.optional_if(isinstance(v_tz, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.timeTimezone, v_tz))
        # Push calendar.
        if tm is not None and tm.calendar is not None:
            v_cal: Query.V_URI = cast(
                Query.URI, self._as_simple_value(tm.calendar))
            self.q.bind(v_cal, self._theta_add(cal, self.as_qvar(cal)))
        else:
            v_cal = self.as_qvar(cal)
            self._theta_add(cal, v_cal)
        with self.q.optional_if(isinstance(v_cal, Query.Variable)):
            self.q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, v_cal))

    def _push_fingerprint(
            self,
            fp: Fingerprint,
            dest: Query.Variable,
            property: Query.V_URI,
            wds: Query.Variable
    ) -> None:
        assert not fp.is_empty()
        if isinstance(fp, CompoundFingerprint):
            with self.q.group():
                self.q.comments()(f'{dest} =~ {type(fp).__qualname__}')
                self._push_compound_fingerprint(fp, dest, property, wds)
        elif isinstance(fp, SnakFingerprint):
            with self.q.group():
                self.q.comments()(f'{dest} =~ {fp}')
                self._push_snak_fingerprint(fp, dest)
        elif isinstance(fp, ValueFingerprint):
            with self.q.group():
                self.q.comments()(f'{dest} =~ {fp}')
                self._push_value_fingerprints((fp,), dest, property, wds)
        elif isinstance(fp, FullFingerprint):
            pass                # nothing to do
        else:
            raise self._should_not_get_here()

    def _push_compound_fingerprint(
            self,
            fp: CompoundFingerprint,
            dest: Query.Variable,
            property: Query.V_URI,
            wds: Query.Variable
    ) -> None:
        atoms, comps = map(list, itertools.partition(
            lambda x: isinstance(x, CompoundFingerprint), fp.args))
        snaks, values = map(list, itertools.partition(
            lambda x: isinstance(x, ValueFingerprint), atoms))
        if isinstance(fp, AndFingerprint):
            for child in itertools.chain(snaks, comps):
                ###
                # TODO: Aggregate snaks with the same property.
                ###
                self._push_fingerprint(child, dest, property, wds)
            if values:
                self._push_value_fingerprints(values, dest, property, wds)
        elif isinstance(fp, OrFingerprint):
            with self.q.union():
                for child in itertools.chain(snaks, comps):
                    with self.q.group():
                        self._push_fingerprint(child, dest, property, wds)
                if values:
                    with self.q.group():
                        self._push_value_fingerprints(
                            values, dest, property, wds)
        else:
            raise self._should_not_get_here()

    def _push_snak_fingerprint(
            self,
            fp: SnakFingerprint,
            dest: Query.Variable,
    ) -> None:
        prop = self.uri(fp.snak.property.iri.content)
        if isinstance(fp, ConverseSnakFingerprint):
            assert isinstance(fp.snak, ValueSnak)
            assert isinstance(fp.snak.value, Entity)
            wdt = self.q.fresh_var()
            value = self._as_simple_value(fp.snak.value)
            assert isinstance(value, Query._mk_uri)
            self.q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (value, wdt, dest))
        elif isinstance(fp.snak, ValueSnak):
            wdt = self.q.fresh_var()
            value = self._as_simple_value(fp.snak.value)
            self.q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (dest, wdt, value))
            if isinstance(fp.snak.value, DeepDataValue):
                p, ps, wds = self.q.fresh_vars(3)
                self.q.triples()(
                    (prop, NS.WIKIBASE.claim, p),
                    (prop, NS.WIKIBASE.statementProperty, ps),
                    (dest, p, wds),
                    (wds, ps, value))
                self._push_value_fingerprints(
                    (ValueFingerprint(fp.snak.value),), self.q.fresh_var(),
                    prop, wds)
        elif isinstance(fp.snak, SomeValueSnak):
            some, wdt = self.q.fresh_vars(2)
            self.q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (dest, wdt, some))
            self._push_some_value_filter(some)
        elif isinstance(fp.snak, NoValueSnak):
            p, wdno, wds, wdt = self.q.fresh_vars(4)
            self.q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (prop, NS.WIKIBASE.claim, p),
                (prop, NS.WIKIBASE.novalue, wdno),
                (dest, p, wds),
                (wds, NS.RDF.type, wdno))
        else:
            raise self._should_not_get_here()

    def _push_value_fingerprints(
            self,
            fps: Iterable[ValueFingerprint],
            dest: Query.Variable,
            property: Query.V_URI,
            wds: Query.Variable
    ) -> None:
        values = map(lambda fp: fp.value, fps)
        shallow, deep = map(list, itertools.partition(
            lambda v: isinstance(v, DeepDataValue), values))
        tms, qts = map(list, itertools.partition(
            lambda v: isinstance(v, Quantity), deep))
        with self.q.union():
            if shallow:
                with self.q.group():
                    self.q.values(dest)(*map(
                        lambda v: (self._as_simple_value(v),),
                        shallow))
            if qts:
                with self.q.group():
                    ps, psv, wdv = self.q.fresh_vars(3)
                    self.q.triples()(
                        (property, NS.WIKIBASE.statementProperty, ps),
                        (property, NS.WIKIBASE.statementValue, psv),
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue))
                    with self.q.union():
                        for qt in qts:
                            assert isinstance(qt, Quantity)
                            with self.q.group():
                                self.q.triples()(
                                    (wds, ps, self.literal(qt.amount)))
                                self._push_quantity_value(qt, dest, wdv)
            if tms:
                with self.q.group():
                    ps, psv, wdv = self.q.fresh_vars(3)
                    self.q.triples()(
                        (property, NS.WIKIBASE.statementProperty, ps),
                        (property, NS.WIKIBASE.statementValue, psv),
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.TimeValue))
                    with self.q.union():
                        for tm in tms:
                            assert isinstance(tm, Time)
                            with self.q.group():
                                self.q.triples()(
                                    (wds, ps, self.literal(tm.time)))
                                self._push_time_value(tm, dest, wdv)

    def _push_quantity_value(
            self,
            qt: Quantity,
            dest: Query.Variable,
            wdv: Query.Variable
    ) -> None:
        amount = self.literal(qt.amount)
        self.q.triples()((wdv, NS.WIKIBASE.quantityAmount, amount))
        if qt.unit is not None:
            unit = self.uri(qt.unit.iri.content)
            self.q.triples()((wdv, NS.WIKIBASE.quantityUnit, unit))
        if qt.lower_bound is not None:
            lower = self.literal(qt.lower_bound)
            self.q.triples()(
                (wdv, NS.WIKIBASE.quantityLowerBound, lower))
        if qt.upper_bound is not None:
            upper = self.literal(qt.upper_bound)
            self.q.triples()(
                (wdv, NS.WIKIBASE.quantityUpperBound, upper))

    def _push_time_value(
            self,
            tm: Time,
            dest: Query.Variable,
            wdv: Query.Variable,
    ) -> None:
        time = self.literal(tm.time)
        self.q.triples()((wdv, NS.WIKIBASE.timeValue, time))
        if tm.precision is not None:
            precision = self.literal(tm.precision.value)
            self.q.triples()(
                (wdv, NS.WIKIBASE.timePrecision, precision))
        if tm.timezone is not None:
            timezone = self.literal(tm.timezone)
            self.q.triples()(
                (wdv, NS.WIKIBASE.timeTimezone, timezone))
        if tm.calendar is not None:
            calendar = self.uri(tm.calendar.iri.content)
            self.q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, calendar))

    def _push_some_value_filter(
            self,
            dest: Query.Variable,
            negate: bool = False
    ) -> None:
        if self.has_flags(self.WIKIDATA_EXTENSIONS):
            cond: Any = self.q.call(NS.WIKIBASE.isSomeValue, dest)
        else:
            cond = self.q.is_blank(dest) | (
                self.q.is_uri(dest) & self.q.strstarts(
                    self.q.str(dest), str(NS.WDGENID)))
        self.q.filter(cond if not negate else ~cond)
