# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import itertools
from ... import namespace as NS
from ...model import (
    DeepDataValue,
    Entity,
    ExternalId,
    Filter,
    IRI,
    Item,
    ItemVariable,
    Lexeme,
    LexemeVariable,
    NoValueSnak,
    Property,
    PropertyVariable,
    Quantity,
    SomeValueSnak,
    Statement,
    StatementVariable,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
    Variable,
)
from ...model.fingerprint import (
    AndFp,
    CompoundFp,
    ConverseSnakFp,
    Fp,
    FullFp,
    OrFp,
    SnakFp,
    ValueFp,
)
from ...typing import Iterable, Optional, override, Self, Union
from .builder import Query
from .pattern_compiler import SPARQL_PatternCompiler


class SPARQL_FilterCompiler(SPARQL_PatternCompiler):
    """SPARQL filter compiler."""

    __slots__ = (
        '_filter',
    )

    # The source filter.
    _filter: Filter

    def __init__(
            self,
            filter: Filter,
            flags: Optional['SPARQL_FilterCompiler.Flags'] = None
    ):
        super().__init__(Variable('_', Statement), flags)
        self._filter = filter

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

    @override
    def compile(self) -> Self:
        filter = self._filter.normalize()
        self._push_filter(filter)
        return self

    def _push_filter(self, filter: Filter):
        if filter.is_empty():
            return              # nothing to do
        assert isinstance(filter.subject, Fp)
        assert isinstance(filter.property, Fp)
        assert isinstance(filter.value, Fp)
        assert isinstance(self.pattern, StatementVariable)
        subject = self._fresh_entity_variable()
        snak = self._fresh_snak_variable()
        property = self._fresh_property_variable()
        self._theta_add(self.pattern, Statement(subject, snak))
        v_subject, v_property = self._as_qvars(subject, property)
        v_value = self._q.var('value')
        p, ps, psv, wdno, wds = self._q.fresh_vars(5)
        self._q.triples()(
            (v_subject, p, wds),
            (v_property, NS.WIKIBASE.claim, p),
            (v_property, NS.WIKIBASE.novalue, wdno),
            (v_property, NS.WIKIBASE.statementProperty, ps),
            (v_property, NS.WIKIBASE.statementValue, psv))
        # Best-ranked only?
        if self.has_flags(self.BEST_RANK):
            self._q.triples()((wds, NS.RDF.type, NS.WIKIBASE.BestRank))
        # Push subject.
        with self._q.group():
            with self._q.union():
                with self._q.group():
                    self._bind_as_item(v_subject)
                with self._q.group():
                    self._bind_as_property(v_subject)
                with self._q.group():
                    self._bind_as_lexeme(v_subject)
            self._push_fingerprint(filter.subject, v_subject, psv, wds)
        # Push property.
        with self._q.group():
            self._bind_as_property(v_property)
            self._push_fingerprint(filter.property, v_property, psv, wds)
        # Push value.
        if (not filter.value.is_empty()
                and not filter.value.is_full()):  # specified value?
            self._q.triples()((wds, ps, v_value))
            self._push_fingerprint(filter.value, v_value, psv, wds)
        else:                   # no/some value or unspecified value
            try_value_snak = bool(
                not filter.value.is_empty()
                and filter.snak_mask & Filter.VALUE_SNAK
                and self.has_flags(self.VALUE_SNAK))
            try_some_value_snak = bool(
                filter.snak_mask & Filter.SOME_VALUE_SNAK
                and self.has_flags(self.SOME_VALUE_SNAK))
            try_no_value_snak = bool(
                filter.snak_mask & Filter.NO_VALUE_SNAK
                and self.has_flags(self.NO_VALUE_SNAK))
            with self._q.union():
                if try_value_snak or try_some_value_snak:
                    with self._q.group():
                        self._q.triples()((wds, ps, v_value))
                        if self.has_flags(self.EARLY_FILTER):
                            if not try_value_snak:
                                self._push_some_value_filter(v_value)
                            elif not try_some_value_snak:
                                self._push_some_value_filter(
                                    v_value, negate=True)
                        if try_value_snak:  # deep data value?
                            with self._q.optional():
                                self._push_unknown_deep_data_value(
                                    v_value, psv, wds)
                if try_no_value_snak:
                    with self._q.group():
                        self._q.triples()((wds, NS.RDF.type, wdno))

    def _bind_as_item(self, dest: Query.Variable):
        iri = self._fresh_iri_variable()
        self._theta_add(ItemVariable(str(dest)), Item(iri))
        self._q.triples()((dest, NS.WIKIBASE.sitelinks, self._q.bnode()))
        self._q.bind(dest, self._theta_add(iri, self._as_qvar(iri)))

    def _bind_as_property(self, dest: Query.Variable):
        datatype = self._fresh_datatype_variable()
        datatype_iri = self._fresh_iri_variable()
        iri = self._fresh_iri_variable()
        self._theta_add(datatype, datatype_iri)
        self._theta_add(PropertyVariable(str(dest)), Property(iri, datatype))
        self._q.triples()(
            (dest, NS.RDF.type, NS.WIKIBASE.Property),
            (dest, NS.WIKIBASE.propertyType, self._theta_add(
                datatype_iri, self._as_qvar(datatype_iri))))
        self._q.bind(dest, self._theta_add(iri, self._as_qvar(iri)))

    def _bind_as_lexeme(self, dest: Query.Variable):
        iri = self._fresh_iri_variable()
        self._theta_add(LexemeVariable(str(dest)), Lexeme(iri))
        self._q.triples()((dest, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        self._q.bind(dest, self._theta_add(iri, self._as_qvar(iri)))

    def _push_fingerprint(
            self,
            fp: Fp,
            dest: Query.Variable,
            psv: Query.Variable,
            wds: Query.Variable
    ):
        assert not fp.is_empty()
        if isinstance(fp, CompoundFp):
            with self._q.group():
                self._q.comments()(f'?{dest} := {type(fp).__qualname__}')
                self._push_compound_fingerprint(fp, dest, psv, wds)
        elif isinstance(fp, SnakFp):
            with self._q.group():
                self._q.comments()(f'?{dest} := {fp}')
                self._push_snak_fingerprint(fp, dest)
        elif isinstance(fp, ValueFp):
            with self._q.group():
                self._q.comments()(f'?{dest} := {fp}')
                self._push_value_fingerprints((fp,), dest, psv, wds)
        elif isinstance(fp, FullFp):
            pass                # nothing to do
        else:
            raise self._should_not_get_here()

    def _push_compound_fingerprint(
            self,
            fp: CompoundFp,
            dest: Query.Variable,
            psv: Query.Variable,
            wds: Query.Variable
    ):
        atoms, comps = map(list, itertools.partition(
            lambda x: isinstance(x, CompoundFp), fp.args))
        snaks, values = map(list, itertools.partition(
            lambda x: isinstance(x, ValueFp), atoms))
        if isinstance(fp, AndFp):
            for child in itertools.chain(snaks, comps):
                ###
                # TODO: Aggregate snaks with the same property.
                ###
                self._push_fingerprint(child, dest, psv, wds)
            if values:
                self._push_value_fingerprints(values, dest, psv, wds)
        elif isinstance(fp, OrFp):
            with self._q.union():
                for child in itertools.chain(snaks, comps):
                    with self._q.group():
                        self._push_fingerprint(child, dest, psv, wds)
                if values:
                    with self._q.group():
                        self._push_value_fingerprints(values, dest, psv, wds)
        else:
            raise self._should_not_get_here()

    def _push_snak_fingerprint(
            self,
            fp: SnakFp,
            dest: Query.Variable,
    ):
        prop = self._q.uri(fp.snak.property.iri.value)
        if isinstance(fp, ConverseSnakFp):
            assert isinstance(fp.snak, ValueSnak)
            assert isinstance(fp.snak.value, Entity)
            wdt = self._q.fresh_var()
            value = self._as_simple_value(fp.snak.value)
            assert isinstance(value, Query._mk_uri)
            self._q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (value, wdt, dest))
        elif isinstance(fp.snak, ValueSnak):
            wdt = self._q.fresh_var()
            value = self._as_simple_value(fp.snak.value)
            self._q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (dest, wdt, value))
            if isinstance(fp.snak.value, DeepDataValue):
                p, ps, psv, wds = self._q.fresh_vars(4)
                self._q.triples()(
                    (prop, NS.WIKIBASE.claim, p),
                    (prop, NS.WIKIBASE.statementProperty, ps),
                    (prop, NS.WIKIBASE.statementValue, psv),
                    (dest, p, wds),
                    (wds, ps, value))
                self._push_value_fingerprints(
                    (ValueFp(fp.snak.value),),
                    self._q.fresh_var(), psv, wds, bind=False)
        elif isinstance(fp.snak, SomeValueSnak):
            some, wdt = self._q.fresh_vars(2)
            self._q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (dest, wdt, some))
            self._push_some_value_filter(some)
        elif isinstance(fp.snak, NoValueSnak):
            p, wdno, wds, wdt = self._q.fresh_vars(4)
            self._q.triples()(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (prop, NS.WIKIBASE.claim, p),
                (prop, NS.WIKIBASE.novalue, wdno),
                (dest, p, wds),
                (wds, NS.RDF.type, wdno))
        else:
            raise self._should_not_get_here()

    def _push_value_fingerprints(
            self,
            fps: Iterable[ValueFp],
            dest: Query.Variable,
            psv: Query.Variable,
            wds: Query.Variable,
            bind: bool = True
    ):
        values = map(lambda fp: fp.value, fps)
        shallow, deep = map(list, itertools.partition(
            lambda v: isinstance(v, DeepDataValue), values))
        tms, qts = map(list, itertools.partition(
            lambda v: isinstance(v, Quantity), deep))
        with self._q.union():
            if shallow:
                with self._q.group():
                    self._q.values(dest)(*map(
                        lambda v: (self._as_simple_value(v),),
                        shallow))
            if qts:
                with self._q.group():
                    wdv = self._q.fresh_var()
                    self._q.triples()(
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue))
                    with self._q.union():
                        for qt in qts:
                            assert isinstance(qt, Quantity)
                            with self._q.group():
                                self._push_quantity_value(qt, dest, wdv, bind)
            if tms:
                with self._q.group():
                    wdv = self._q.fresh_var()
                    self._q.triples()(
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.TimeValue))
                    with self._q.union():
                        for tm in tms:
                            assert isinstance(tm, Time)
                            with self._q.group():
                                self._push_time_value(tm, dest, wdv, bind)

    def _push_quantity_value(
            self,
            qt: Quantity,
            dest: Query.Variable,
            wdv: Query.Variable,
            bind: bool = True
    ):
        v_qt_amount, v_qt_unit, v_qt_lower, v_qt_upper = self._q.vars(
            f'{dest}_qt_amount',
            f'{dest}_qt_unit',
            f'{dest}_qt_lower',
            f'{dest}_qt_upper')
        amount = self._q.literal(qt.amount)
        self._q.triples()((wdv, NS.WIKIBASE.quantityAmount, amount))
        if bind:
            self._q.bind(amount, dest)
            self._q.bind(amount, v_qt_amount)
        if qt.unit is not None:
            unit = self._q.uri(qt.unit.iri.value)
            self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, unit))
            if bind:
                self._q.bind(unit, v_qt_unit)
        elif bind:
            with self._q.optional():
                self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, v_qt_unit))
        if qt.lower_bound is not None:
            lower = self._q.literal(qt.lower_bound)
            self._q.triples()(
                (wdv, NS.WIKIBASE.quantityLowerBound, lower))
            if bind:
                self._q.bind(lower, v_qt_lower)
        elif bind:
            with self._q.optional():
                self._q.triples()(
                    (wdv, NS.WIKIBASE.quantityLowerBound, v_qt_lower))
        if qt.upper_bound is not None:
            upper = self._q.literal(qt.upper_bound)
            self._q.triples()(
                (wdv, NS.WIKIBASE.quantityUpperBound, upper))
            if bind:
                self._q.bind(upper, v_qt_upper)
        elif bind:
            with self._q.optional():
                self._q.triples()(
                    (wdv, NS.WIKIBASE.quantityUpperBound, v_qt_upper))

    def _push_time_value(
            self,
            tm: Time,
            dest: Query.Variable,
            wdv: Query.Variable,
            bind: bool = True
    ):
        v_tm_time, v_tm_precision, v_tm_timezone, v_tm_calendar = self._q.vars(
            f'{dest}_tm_time',
            f'{dest}_tm_precision',
            f'{dest}_tm_timezone',
            f'{dest}_tm_calendar')
        time = self._q.literal(tm.time)
        self._q.triples()((wdv, NS.WIKIBASE.timeValue, time))
        if bind:
            self._q.bind(time, dest)
            self._q.bind(time, v_tm_time)
        if tm.precision is not None:
            precision = self._q.literal(tm.precision.value)
            self._q.triples()(
                (wdv, NS.WIKIBASE.timePrecision, precision))
            if bind:
                self._q.bind(precision, v_tm_precision)
        elif bind:
            with self._q.optional():
                self._q.triples()(
                    (wdv, NS.WIKIBASE.timePrecision, v_tm_precision))
        if tm.timezone is not None:
            timezone = self._q.literal(tm.timezone)
            self._q.triples()(
                (wdv, NS.WIKIBASE.timeTimezone, timezone))
            if bind:
                self._q.bind(timezone, v_tm_timezone)
        elif bind:
            with self._q.optional():
                self._q.triples()(
                    (wdv, NS.WIKIBASE.timeTimezone, v_tm_timezone))
        if tm.calendar is not None:
            calendar = self._q.uri(tm.calendar.iri.value)
            self._q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, calendar))
            if bind:
                self._q.bind(calendar, v_tm_calendar)
        elif bind:
            with self._q.optional():
                self._q.triples()(
                    (wdv, NS.WIKIBASE.timeCalendarModel, v_tm_calendar))

    def _push_unknown_deep_data_value(
            self,
            dest: Query.Variable,
            psv: Query.Variable,
            wds: Query.Variable
    ):
        wdv = self._q.fresh_var()
        with self._q.union():
            with self._q.group():     # quantity?
                v_qt_amount, v_qt_unit, v_qt_lower, v_qt_upper = self._q.vars(
                    f'{dest}_qt_amount',
                    f'{dest}_qt_unit',
                    f'{dest}_qt_lower',
                    f'{dest}_qt_upper')
                self._q.triples()(
                    (wds, psv, wdv),
                    (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue),
                    (wdv, NS.WIKIBASE.quantityAmount, v_qt_amount))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.quantityUnit, v_qt_unit))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.quantityLowerBound, v_qt_lower))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.quantityUpperBound, v_qt_upper))
            with self._q.group():     # time?
                v_tm_time, v_tm_precision, v_tm_timezone, v_tm_calendar\
                    = self._q.vars(
                        f'{dest}_tm_time',
                        f'{dest}_tm_precision',
                        f'{dest}_tm_timezone',
                        f'{dest}_tm_calendar')
                self._q.triples()(
                    (wds, psv, wdv),
                    (wdv, NS.RDF.type, NS.WIKIBASE.TimeValue),
                    (wdv, NS.WIKIBASE.timeValue, v_tm_time))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.timePrecision, v_tm_precision))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.timeTimezone, v_tm_timezone))
                with self._q.optional():
                    self._q.triples()(
                        (wdv, NS.WIKIBASE.timeCalendarModel, v_tm_calendar))

    def _push_some_value_filter(
            self,
            dest: Query.Variable,
            negate: bool = False
    ):
        ###
        # TODO: Use native test when available.
        ###
        # return q.call(NS.WIKIBASE.isSomeValue, dest)
        cond = self._q.is_blank(dest) | (
            self._q.is_uri(dest) & self._q.strstarts(
                self._q.str(dest), str(NS.WDGENID)))
        self._q.filter(cond if not negate else ~cond)

    def _as_simple_value(
            self,
            value: Value
    ) -> Union[Query.URI, Query.Literal]:
        if isinstance(value, Entity):
            return self._q.uri(value.iri.value)
        elif isinstance(value, IRI):
            return self._q.uri(value.content)
        elif isinstance(value, Text):
            return self._q.literal(value.content, value.language)
        elif isinstance(value, (String, ExternalId)):
            return self._q.literal(value.content)
        elif isinstance(value, Quantity):
            return self._q.literal(value.amount)
        elif isinstance(value, Time):
            return self._q.literal(value.time)
        else:
            raise self._should_not_get_here()
