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
    NoValueSnak,
    Quantity,
    SomeValueSnak,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
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
from ...typing import Iterable, Optional, override, Union
from .builder import Query
from .compiler import SPARQL_Compiler


class SPARQL_FilterCompiler(SPARQL_Compiler):
    """SPARQL filter compiler."""

    class Error(SPARQL_Compiler.Error):
        """SPARQL filter compiler error."""

    class Results(SPARQL_Compiler.Results):
        """SPARQL filter compiler results."""

        __slots__ = (
            '_filter',
        )

        #: The source filter.
        _pattern: Filter

        def __init__(
                self,
                query: 'SPARQL_FilterCompiler.Query',
                filter: Filter,
        ):
            super().__init__(query)
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

    __slots__ = (
        '_filter',
        '_flags',
    )

    # The source filter.
    _filter: Filter

    def __init__(
            self,
            filter: Filter,
            debug: Optional[bool] = None
    ):
        super().__init__(debug)
        self._filter = filter

    @override
    def compile(self) -> 'SPARQL_FilterCompiler.Results':
        filter = self._filter.normalize()
        self._compile(filter)
        return self.Results(self._q, filter)

    def _compile(self, filter: Filter):
        if filter.is_empty():
            return              # nothing to do
        assert isinstance(filter.subject, Fp)
        assert isinstance(filter.property, Fp)
        assert isinstance(filter.value, Fp)
        subject, property, datatype, value = self._q.vars(
            'subject', 'property', 'datatype', 'value')
        p, ps, psv, wdno, wds = self._q.fresh_vars(5)
        self._q.triples()(
            (subject, p, wds),
            (property, NS.WIKIBASE.claim, p),
            (property, NS.WIKIBASE.novalue, wdno),
            (property, NS.WIKIBASE.propertyType, datatype),
            (property, NS.WIKIBASE.statementProperty, ps),
            (property, NS.WIKIBASE.statementValue, psv))
        ###
        # TODO: Best-ranked only?
        # if self.has_flags(self.BEST_RANK):
        #     self._q.triples()((wds, NS.RDF.type, NS.WIKIBASE.BestRank))
        ###
        # Push subject.
        self._push_fingerprint(filter.subject, subject, psv, wds)
        # Push property fingerprint.
        self._push_fingerprint(filter.property, property, psv, wds)

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
                                self._push_quantity(qt, dest, wdv, bind)
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
                                self._push_time(tm, dest, wdv, bind)

    def _push_quantity(
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

    def _push_time(
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

    def _push_some_value_filter(
            self,
            dest: Query.Variable
    ):
        ###
        # TODO: Use native test when available.
        ###
        # return q.call(NS.WIKIBASE.isSomeValue, dest)
        self._q.filter(
            self._q.is_blank(dest) | (
                self._q.is_uri(dest) & self._q.strstarts(
                    self._q.str(dest), str(NS.WDGENID))))

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
