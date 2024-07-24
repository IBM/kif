# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

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
        '_wds',
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
        self._wds = self._q.fresh_var()

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
        self._theta_add(self.pattern, Statement(subject, snak))
        property = self._fresh_property_variable()
        v_subject, v_property = self._as_qvars(subject, property)
        wds = self.wds
        p, wdt = self._q.fresh_vars(2)
        ###
        # IMPORTANT: Some SPARQL engines are sensitive to the place a
        # variable is bound.  As a rule of thumb, we should bound a variable
        # as close as possible to the place where it is actually used.  This
        # is why we do not bind the `ps`, `wdno`, etc., here.
        ###
        self._q.triples()(
            (v_subject, p, wds),
            (v_property, NS.WIKIBASE.claim, p),
            (v_property, NS.WIKIBASE.directClaim, wdt))
        # Best-ranked only?
        best_ranked = self.has_flags(self.BEST_RANK)
        if best_ranked:
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
            self._push_fingerprint(
                filter.subject, v_subject, v_property, wds)
        # Push property.
        with self._q.group():
            self._bind_as_property(v_property)
            self._push_fingerprint(
                filter.property, v_property, v_property, wds)
        # Push value.
        try_value_snak = bool(
            not filter.value.is_empty()
            and filter.snak_mask & Filter.VALUE_SNAK
            and self.has_flags(self.VALUE_SNAK))
        try_some_value_snak = bool(
            (filter.value.is_empty() or filter.value.is_full())
            and filter.snak_mask & Filter.SOME_VALUE_SNAK
            and self.has_flags(self.SOME_VALUE_SNAK))
        try_no_value_snak = bool(
            (filter.value.is_empty() or filter.value.is_full())
            and filter.snak_mask & Filter.NO_VALUE_SNAK
            and self.has_flags(self.NO_VALUE_SNAK))
        assert try_value_snak or try_some_value_snak or try_no_value_snak
        with self._q.union():
            if try_value_snak:
                with self._q.group():
                    value = self._fresh_value_variable()
                    v_value = self._as_qvar(value)
                    self._theta_add(
                        ValueSnakVariable(snak.name),
                        ValueSnak(property, value))
                    ps = self._q.fresh_var()
                    self._q.triples()(
                        (v_property, NS.WIKIBASE.statementProperty, ps),
                        (wds, ps, v_value))
                    with self._q.group():
                        with self._q.union():
                            with self._q.group():  # item?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.WikibaseItem))
                                self._bind_as_item(v_value)
                            with self._q.group():  # property?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.WikibaseProperty))
                                self._bind_as_property(v_value)
                            with self._q.group():  # lexeme?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.WikibaseLexeme))
                                self._bind_as_lexeme(v_value)
                            with self._q.group():  # iri?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.Url),
                                    (wds, ps, v_value))
                                self._bind_as_iri(v_value)
                            with self._q.group():  # text?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.Monolingualtext),
                                    (wds, ps, v_value))
                                self._bind_as_text(v_value)
                            with self._q.group():  # string?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.String),
                                    (wds, ps, v_value))
                                self._bind_as_string(v_value)
                            with self._q.group():  # external id?
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.ExternalId),
                                    (wds, ps, v_value))
                                self._bind_as_external_id(v_value)
                            with self._q.group():  # quantity?
                                psv, wdv = self._q.fresh_vars(2)
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.Quantity),
                                    (v_property,
                                     NS.WIKIBASE.statementValue,
                                     psv),
                                    (wds, psv, wdv),
                                    (wdv, NS.RDF.type,
                                     NS.WIKIBASE.QuantityValue))
                                self._bind_as_quantity(v_value, wdv)
                            with self._q.group():  # time?
                                psv, wdv = self._q.fresh_vars(2)
                                self._q.triples()(
                                    (v_property,
                                     NS.WIKIBASE.propertyType,
                                     NS.WIKIBASE.Time),
                                    (v_property,
                                     NS.WIKIBASE.statementValue,
                                     psv),
                                    (wds, psv, wdv),
                                    (wdv, NS.RDF.type,
                                     NS.WIKIBASE.TimeValue))
                                self._bind_as_time(v_value, wdv)
                        self._push_fingerprint(
                            filter.value, v_value, v_property, wds)
            if try_some_value_snak:
                with self._q.group():
                    some_prop = self._fresh_property_variable()
                    self._bind_as_property(self._as_qvar(some_prop))
                    self._theta_add(
                        SomeValueSnakVariable(snak.name),
                        SomeValueSnak(some_prop))
                    ps, v_some = self._q.fresh_vars(2)
                    self._q.triples()(
                        (v_property, NS.WIKIBASE.statementProperty, ps),
                        (self._as_qvar(some_prop),
                         NS.WIKIBASE.statementProperty, ps),
                        (wds, ps, v_some))
                    self._push_some_value_filter(v_some)
            if try_no_value_snak:
                with self._q.group():
                    wdno = self._q.fresh_var()
                    no_prop = self._fresh_property_variable()
                    self._bind_as_property(self._as_qvar(no_prop))
                    self._theta_add(
                        NoValueSnakVariable(snak.name), NoValueSnak(no_prop))
                    self._q.triples()(
                        (v_property, NS.WIKIBASE.novalue, wdno),
                        (self._as_qvar(no_prop), NS.WIKIBASE.novalue, wdno),
                        (wds, NS.RDF.type, wdno))

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

    def _bind_as_iri(self, dest: Query.Variable):
        content = self._fresh_string_variable()
        self._theta_add(IRI_Variable(str(dest)), IRI(content))
        self._q.bind(dest, self._theta_add(content, self._as_qvar(content)))

    def _bind_as_text(self, dest: Query.Variable):
        content = self._fresh_string_variable()
        lang = self._fresh_string_variable()
        self._theta_add(TextVariable(str(dest)), Text(content, lang))
        self._q.bind(dest, self._theta_add(content, self._as_qvar(content)))
        self._q.bind(self._q.lang(dest), self._theta_add(
            lang, self._as_qvar(lang)))

    def _bind_as_string(self, dest: Query.Variable):
        content = self._fresh_string_variable()
        self._theta_add(StringVariable(str(dest)), String(content))
        self._q.bind(dest, self._theta_add(content, self._as_qvar(content)))

    def _bind_as_external_id(self, dest: Query.Variable):
        content = self._fresh_string_variable()
        self._theta_add(ExternalIdVariable(str(dest)), ExternalId(content))
        self._q.bind(dest, self._theta_add(content, self._as_qvar(content)))

    def _bind_as_quantity(self, dest: Query.Variable, wdv: Query.Variable):
        amount = self._fresh_quantity_variable()
        unit = self._theta_add_default(self._fresh_item_variable(), None)
        lower = self._theta_add_default(self._fresh_quantity_variable(), None)
        upper = self._theta_add_default(self._fresh_quantity_variable(), None)
        self._theta_add(
            QuantityVariable(str(dest)), Quantity(amount, unit, lower, upper))
        v_amount, v_unit, v_lower, v_upper = self._as_qvars(
            amount, unit, lower, upper)
        self._theta_add(amount, v_amount)
        self._q.triples()((wdv, NS.WIKIBASE.quantityAmount, v_amount))
        self._theta_add(unit, v_unit)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, v_unit))
        self._theta_add(lower, v_lower)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.quantityLowerBound, v_lower))
        self._theta_add(upper, v_upper)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.quantityUpperBound, v_upper))

    def _bind_as_time(self, dest: Query.Variable, wdv: Query.Variable):
        time = self._fresh_time_variable()
        prec = self._theta_add_default(self._fresh_quantity_variable(), None)
        tz = self._theta_add_default(self._fresh_quantity_variable(), None)
        cal = self._theta_add_default(self._fresh_item_variable(), None)
        self._theta_add(TimeVariable(str(dest)), Time(time, prec, tz, cal))
        v_time, v_prec, v_tz, v_cal = self._as_qvars(time, prec, tz, cal)
        self._theta_add(time, v_time)
        self._q.triples()((wdv, NS.WIKIBASE.timeValue, v_time))
        self._theta_add(prec, v_prec)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.timePrecision, v_prec))
        self._theta_add(tz, v_tz)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.timeTimezone, v_tz))
        self._theta_add(cal, v_cal)
        with self._q.optional():
            self._q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, v_cal))

    def _push_fingerprint(
            self,
            fp: Fp,
            dest: Query.Variable,
            property: Union[Query.URI, Query.Variable],
            wds: Query.Variable
    ):
        assert not fp.is_empty()
        if isinstance(fp, CompoundFp):
            with self._q.group():
                self._q.comments()(f'{dest} := {type(fp).__qualname__}')
                self._push_compound_fingerprint(fp, dest, property, wds)
        elif isinstance(fp, SnakFp):
            with self._q.group():
                self._q.comments()(f'{dest} := {fp}')
                self._push_snak_fingerprint(fp, dest)
        elif isinstance(fp, ValueFp):
            with self._q.group():
                self._q.comments()(f'{dest} := {fp}')
                self._push_value_fingerprints((fp,), dest, property, wds)
        elif isinstance(fp, FullFp):
            pass                # nothing to do
        else:
            raise self._should_not_get_here()

    def _push_compound_fingerprint(
            self,
            fp: CompoundFp,
            dest: Query.Variable,
            property: Union[Query.URI, Query.Variable],
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
                self._push_fingerprint(child, dest, property, wds)
            if values:
                self._push_value_fingerprints(values, dest, property, wds)
        elif isinstance(fp, OrFp):
            with self._q.union():
                for child in itertools.chain(snaks, comps):
                    with self._q.group():
                        self._push_fingerprint(child, dest, property, wds)
                if values:
                    with self._q.group():
                        self._push_value_fingerprints(
                            values, dest, property, wds)
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
                p, ps, wds = self._q.fresh_vars(3)
                self._q.triples()(
                    (prop, NS.WIKIBASE.claim, p),
                    (prop, NS.WIKIBASE.statementProperty, ps),
                    (dest, p, wds),
                    (wds, ps, value))
                self._push_value_fingerprints(
                    (ValueFp(fp.snak.value),), self._q.fresh_var(),
                    prop, wds)
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
            property: Union[Query.URI, Query.Variable],
            wds: Query.Variable
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
                    psv, wdv = self._q.fresh_vars(2)
                    self._q.triples()(
                        (property, NS.WIKIBASE.statementValue, psv),
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue))
                    with self._q.union():
                        for qt in qts:
                            assert isinstance(qt, Quantity)
                            with self._q.group():
                                self._push_quantity_value(qt, dest, wdv)
            if tms:
                with self._q.group():
                    psv, wdv = self._q.fresh_vars(2)
                    self._q.triples()(
                        (property, NS.WIKIBASE.statementValue, psv),
                        (wds, psv, wdv),
                        (wdv, NS.RDF.type, NS.WIKIBASE.TimeValue))
                    with self._q.union():
                        for tm in tms:
                            assert isinstance(tm, Time)
                            with self._q.group():
                                self._push_time_value(tm, dest, wdv)

    def _push_quantity_value(
            self,
            qt: Quantity,
            dest: Query.Variable,
            wdv: Query.Variable
    ):
        amount = self._q.literal(qt.amount)
        self._q.triples()((wdv, NS.WIKIBASE.quantityAmount, amount))
        if qt.unit is not None:
            unit = self._q.uri(qt.unit.iri.value)
            self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, unit))
        if qt.lower_bound is not None:
            lower = self._q.literal(qt.lower_bound)
            self._q.triples()(
                (wdv, NS.WIKIBASE.quantityLowerBound, lower))
        if qt.upper_bound is not None:
            upper = self._q.literal(qt.upper_bound)
            self._q.triples()(
                (wdv, NS.WIKIBASE.quantityUpperBound, upper))

    def _push_time_value(
            self,
            tm: Time,
            dest: Query.Variable,
            wdv: Query.Variable,
    ):
        time = self._q.literal(tm.time)
        self._q.triples()((wdv, NS.WIKIBASE.timeValue, time))
        if tm.precision is not None:
            precision = self._q.literal(tm.precision.value)
            self._q.triples()(
                (wdv, NS.WIKIBASE.timePrecision, precision))
        if tm.timezone is not None:
            timezone = self._q.literal(tm.timezone)
            self._q.triples()(
                (wdv, NS.WIKIBASE.timeTimezone, timezone))
        if tm.calendar is not None:
            calendar = self._q.uri(tm.calendar.iri.value)
            self._q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, calendar))

    def _push_some_value_filter(
            self,
            dest: Query.Variable,
            negate: bool = False
    ):
        if self.has_flags(self.WIKIDATA_EXTENSIONS):
            cond = self._q.call(NS.WIKIBASE.isSomeValue, dest)
        else:
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
