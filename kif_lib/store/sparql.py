# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools
import logging
import sys
from collections.abc import Collection, Hashable, Iterable, Mapping, Set
from typing import Any, Callable, cast, Iterator, Optional, TypeVar, Union

import more_itertools
import requests
import requests.exceptions
from rdflib import BNode, Graph, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.sparql import Query

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    DeepDataValue,
    Descriptor,
    Entity,
    FilterPattern,
    IRI,
    NoValueSnak,
    Property,
    Quantity,
    Rank,
    ReferenceRecord,
    Snak,
    SnakMask,
    SnakSet,
    Statement,
    String,
    Text,
    Time,
    Value,
    ValueSnak,
)
from .abc import Store
from .sparql_builder import SPARQL_Builder
from .sparql_results import SPARQL_Results

LOG = logging.getLogger(__name__)

T = TypeVar('T')
T_WDS = Hashable
TOpq = Union[BNode, URIRef]
TTrm = SPARQL_Builder.TTrm


class SPARQL_Store(Store, type='sparql', description='SPARQL endpoint'):
    """SPARQL store.

    Parameters:
       store_type: Type of concrete store to instantiate.
       iri: SPARQL endpoint IRI.
    """

    _headers = {
        # See <https://meta.wikimedia.org/wiki/User-Agent_policy>.
        'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; '
        'coolbot@example.org) generic-library/0.0',
        'Content-Type': 'application/sparql-query;charset=utf-8',
    }

    _construct_headers = {
        **_headers,
        'Accept': 'application/rdf+xml;charset=utf-8',

    }

    _select_headers = {
        **_headers,
        'Accept': 'application/sparql-results+json;charset=utf-8',
    }

    __slots__ = (
        '_iri',
    )

    _iri: IRI

    def __init__(
            self,
            store_type: str,
            iri: Union[IRI, str],
            **kwargs: Any):
        assert store_type == self.store_type
        super().__init__(**kwargs)
        self._iri = IRI(iri)

    @property
    def iri(self) -> IRI:
        """SPARQL endpoint IRI."""
        return self.get_iri()

    def get_iri(self) -> IRI:
        """Gets SPARQL endpoint IRI.

        Returns:
           SPARQL endpoint IRI.
        """
        return self._iri

    # -- Caching -----------------------------------------------------------

    def _cache_get_wdss(self, stmt: Statement) -> Optional[Set[T_WDS]]:
        return self._cache.get(stmt, 'wdss')

    def _cache_add_wds(self, stmt: Statement, wds: T_WDS) -> Set[T_WDS]:
        self._cache.set(wds, 'statement', stmt)
        wdss = self._cache.get(stmt, 'wdss')
        if wdss is None:
            wdss = self._cache.set(stmt, 'wdss', set())
        wdss.add(wds)
        return wdss

    # -- Query evaluation (internal) ---------------------------------------

    def _eval_construct_query(
            self,
            query: SPARQL_Builder,
            parse_results_fn: Callable[[Graph], Iterator[Optional[T]]],
            limit: int = sys.maxsize,
            trim: bool = False
    ) -> Iterator[T]:
        def eval_fn(
                eval_limit: Optional[int] = None,
                eval_offset: Optional[int] = None
        ) -> Iterator[Optional[T]]:
            return parse_results_fn(
                self._eval_construct_query_string(
                    query.construct(limit=eval_limit, offset=eval_offset)))
        return self._eval_query(query, eval_fn, limit, trim)

    def _eval_select_query(
            self,
            query: SPARQL_Builder,
            parse_results_fn: Callable[
                [SPARQL_Results], Iterator[Optional[T]]],
            vars: Collection[Union[TTrm, tuple[TTrm, TTrm]]] = [],
            order_by: Optional[TTrm] = None,
            limit: int = sys.maxsize,
            trim: bool = False
    ) -> Iterator[T]:
        def eval_fn(
                eval_limit: Optional[int] = None,
                eval_offset: Optional[int] = None
        ) -> Iterator[Optional[T]]:
            return parse_results_fn(
                self._eval_select_query_string(
                    query.select(
                        *vars, order_by=order_by,
                        limit=eval_limit, offset=eval_offset)))
        return self._eval_query(query, eval_fn, limit, trim)

    def _eval_query(
            self,
            query: SPARQL_Builder,
            eval_fn: Callable[
                [Optional[int], Optional[int]], Iterator[Optional[T]]],
            limit: int = sys.maxsize,
            trim: bool = False,
            page_size: Optional[int] = None,
            offset: Optional[int] = None
    ) -> Iterator[T]:
        assert limit > 0
        page_size = page_size or self.page_size
        offset = offset or 0
        if trim and limit < page_size:
            page_size = limit
        i = 0
        for obj in eval_fn(page_size, offset):
            i += 1
            if obj is not None:
                yield obj
                limit -= 1
                if limit <= 0:
                    assert limit == 0
                    return      # done
        assert i <= page_size
        if i == page_size:
            yield from self._eval_query(
                query, eval_fn, limit=limit, trim=trim,
                page_size=page_size, offset=offset + i)

    def _eval_construct_query_string(
            self,
            text: str,
            headers: Optional[dict[str, Any]] = None,
            **kwargs
    ) -> Graph:
        text = self._prepare_query_string_wrapper(text)
        res = self._eval_query_string(
            text, headers=headers or self._construct_headers, **kwargs)
        return Graph().parse(data=res.text, format='xml')

    def _eval_select_query_string(
            self,
            text: str,
            headers: Optional[dict[str, Any]] = None,
            **kwargs
    ) -> SPARQL_Results:
        text = self._prepare_query_string_wrapper(text)
        return SPARQL_Results(self._eval_query_string(
            text, headers=headers or self._select_headers, **kwargs).json())

    def _prepare_query_string_wrapper(self, text: str) -> str:
        return self._prepare_query_string(text)._original_args[0]

    def _prepare_query_string(self, text: str) -> Query:
        from pyparsing.exceptions import ParseException
        try:
            return prepareQuery(text, initNs=None)
        except ParseException as err:
            raise self._error_bad_query_string(
                err.args[0], err.lineno, err.column,
                err.explain()) from None

    def _error_bad_query_string(
            self,
            query: str,
            line: int,
            column: int,
            details: str
    ) -> SyntaxError:
        return SyntaxError(f'''\
bad query:
{query}
At line {line}, column {column}:
{details}''')

    def _eval_query_string(
            self,
            text: str,
            headers: dict[str, str] = dict(),
            timeout: Optional[int] = None) -> requests.Response:
        LOG.debug('%s():\n%s', self._eval_query_string.__qualname__, text)
        try:
            res = requests.post(
                cast(str, self.iri.value), data=text.encode('utf-8'),
                headers=headers, timeout=self.timeout)
            res.raise_for_status()
            return res
        except requests.exceptions.RequestException as err:
            raise err

    # -- Queries -----------------------------------------------------------

    def _contains(self, pat: FilterPattern) -> bool:
        it = self._filter(pat, limit=1)
        try:
            next(it)
            return True
        except StopIteration:
            return False

    def _count(self, pattern: FilterPattern) -> int:
        q = self._make_count_query(pattern)
        text = q.select('(count (*) as ?count)')
        res = self._eval_select_query_string(text)
        return self._parse_count_query_results(res)

    def _make_count_query(self, pattern: FilterPattern) -> SPARQL_Builder:
        if pattern.is_nonfull():
            return self._make_filter_query(pattern)
        else:
            q = SPARQL_Builder()
            with q.where():
                wds = q.var('wds')
                if self.has_flags(self.BEST_RANK):
                    q.triple(wds, self.rdf.type, self.wikibase.BestRank)
                else:
                    q.triple(wds, self.wikibase.rank, q.var('rank'))
            return q

    def _parse_count_query_results(self, results: SPARQL_Results) -> int:
        return int(next(results.bindings).check_literal('count'))

    _filter_vars = (
        '?property',
        '?qt_amount',
        '?qt_lower',
        '?qt_unit',
        '?qt_upper',
        '?subject',
        '?tm_calendar',
        '?tm_precision',
        '?tm_timezone',
        '?tm_value',
        '?value',
        '?wds',
    )

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        assert limit > 0
        q = self._make_filter_query(pattern)
        if (q.has_variable(q.var('subject'))
            and q.has_variable(q.var('property'))
                and q.has_variable(q.var('value'))):
            return self._eval_select_query(
                q, lambda res: self._parse_filter_results(res, pattern),
                vars=self._filter_vars, limit=limit, trim=True)
        else:
            LOG.debug(
                '%s(): nothing to select:\n%s', self._filter.__qualname__,
                q.select(*self._filter_vars))
            return iter([])     # query is empty

    def _parse_filter_results(
            self,
            results: SPARQL_Results,
            pattern: FilterPattern
    ) -> Iterator[Optional[Statement]]:
        for entry in results.bindings:
            stmt = entry.check_statement(
                'subject', 'property', 'value',
                'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
            wds = entry.check_bnode_or_uriref('wds')
            self._cache_add_wds(stmt, wds)
            if not self.has_flags(self.LATE_FILTER):
                yield stmt      # success
                continue
            # Snak mask mismatch.
            if not bool(pattern.snak_mask & stmt.snak.get_snak_mask()):
                yield None      # pragma: no cover
                continue        # pragma: no cover
            # Subject mismatch.
            if (pattern.subject is not None
                and pattern.subject.entity is not None
                    and pattern.subject.entity != stmt.subject):
                yield None      # pragma: no cover
                continue        # pragma: no cover
            # Property mismatch.
            if (pattern.property is not None
                and pattern.property.property is not None
                    and pattern.property.property != stmt.snak.property):
                yield None      # pragma: no cover
                continue        # pragma: no cover
            # Value mismatch.
            if (pattern.value is not None
                    and pattern.value.value is not None):
                assert stmt.snak.is_value_snak()
                value = cast(ValueSnak, stmt.snak).value
                if type(pattern.value.value) is not type(value):
                    yield None  # pragma: no cover
                    continue    # pragma: no cover
                if not value.is_deep_data_value():
                    if pattern.value.value != value:
                        yield None  # pragma: no cover
                        continue    # pragma: no cover
                elif value.is_quantity():
                    assert pattern.value.value.is_quantity()
                    pat_qt = cast(Quantity, pattern.value.value)
                    qt = cast(Quantity, value)
                    if (pat_qt.amount != qt.amount
                        or (pat_qt.unit is not None
                            and pat_qt.unit != qt.unit)
                        or (pat_qt.lower_bound is not None
                            and pat_qt.lower_bound != qt.lower_bound)
                        or (pat_qt.upper_bound is not None
                            and pat_qt.upper_bound != qt.upper_bound)):
                        yield None  # pragma: no cover
                        continue    # pragma: no cover
                elif value.is_time():
                    assert pattern.value.value.is_time()
                    pat_tm = cast(Time, pattern.value.value)
                    tm = cast(Time, value)
                    if (pat_tm.time != tm.time
                        or (pat_tm.precision is not None
                            and pat_tm.precision != tm.precision)
                        or (pat_tm.timezone is not None
                            and pat_tm.timezone != tm.timezone)
                        or (pat_tm.calendar_model is not None
                            and pat_tm.calendar_model != tm.calendar_model)):
                        yield None  # pragma: no cover
                        continue    # pragma: no cover
                else:
                    raise ShouldNotGetHere
            # Success.
            yield stmt

    def _make_filter_query(self, pattern: FilterPattern) -> SPARQL_Builder:
        q = SPARQL_Builder()
        t = self._make_filter_query_vars_dict(q)
        q.where_start()
        self._push_filter_pattern(q, t, pattern)
        q.where_end()
        return q

    def _make_filter_query_vars_dict(
            self,
            q: SPARQL_Builder
    ) -> Mapping[str, TTrm]:
        return q.vars_dict(
            'i',
            'p',
            'pname',
            'property',
            'ps',
            'psv',
            'qt_amount',
            'qt_lower',
            'qt_unit',
            'qt_upper',
            'subject',
            'tm_calendar',
            'tm_precision',
            'tm_timezone',
            'tm_value',
            'value',
            'wdno',
            'wds',
            'wdv',
        )

    def _push_filter_pattern(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            pat: FilterPattern
    ) -> SPARQL_Builder:
        # Push subject and property snak sets (if any).
        if pat.subject is not None and pat.subject.snak_set is not None:
            self._push_snak_set(q, t['subject'], pat.subject.snak_set)
        if pat.property is not None and pat.property.snak_set is not None:
            self._push_snak_set(q, t['property'], pat.property.snak_set)
        # Push wds.
        q.triples(
            (t['subject'], t['p'], t['wds']),
            (t['wds'], self.wikibase.rank, q.bnode()))
        if self.has_flags(self.BEST_RANK):
            q.triple(t['wds'], self.rdf.type, self.wikibase.BestRank)
        if pat.property is None or pat.property.property is None:
            if pat.property is not None:
                # Property is snak set: use ?property as basis.
                assert pat.property.snak_set is not None
                q.bind(
                    q.substr(q.str_(t['property']), len(self.wd) + 1),
                    cast(SPARQL_Builder.Variable, t['pname']))
                self._push_filter_pattern_bind_pname_as(
                    q, t, (self.p, 'p'))
            else:
                # Property is unknown: use ?p as basis.
                q.bind(
                    q.substr(q.str_(t['p']), len(self.p) + 1),
                    cast(SPARQL_Builder.Variable, t['pname']))
                self._push_filter_pattern_bind_pname_as(
                    q, t, (self.wd, 'property'))
            self._push_filter_pattern_bind_pname_as(
                q, t, (self.ps, 'ps'), (self.psv, 'psv'), (self.wdno, 'wdno'))
        # Value.
        if pat.value is not None and pat.value.snak_set is not None:
            # Push value snak set.
            q.triple(t['wds'], t['ps'], t['value'])
            self._push_snak_set(q, t['value'], pat.value.snak_set)
        else:
            # Push value.
            value_is_unknown = pat.value is None or pat.value.value is None
            try_value_snak = bool(
                pat.snak_mask & SnakMask.VALUE_SNAK
                and self.has_flags(self.VALUE_SNAK))
            try_some_value_snak = bool(
                value_is_unknown
                and pat.snak_mask & SnakMask.SOME_VALUE_SNAK
                and self.has_flags(self.SOME_VALUE_SNAK))
            try_no_value_snak = bool(
                value_is_unknown
                and pat.snak_mask & SnakMask.NO_VALUE_SNAK
                and self.has_flags(self.NO_VALUE_SNAK))
            cond = sum(
                (try_value_snak,
                 try_some_value_snak,
                 try_no_value_snak)) > 1
            with q.union(cond=cond) as cup:
                if try_value_snak or try_some_value_snak:
                    cup.branch()
                    q.triple(t['wds'], t['ps'], t['value'])
                    if self.has_flags(self.EARLY_FILTER):
                        if not try_value_snak:
                            self._push_some_value_filter(q, t['value'])
                        elif not try_some_value_snak:
                            self._push_some_value_filter(
                                q, t['value'], negate=True)
                    if try_value_snak:
                        with q.optional(cond=value_is_unknown):
                            if value_is_unknown:
                                self._push_deep_data_value(q, t)
                            else:
                                assert pat.value is not None
                                assert pat.value.value is not None
                                if pat.value.value.is_deep_data_value():
                                    deep = cast(DeepDataValue, pat.value.value)
                                    self._push_deep_data_value(q, t, deep)
                                else:
                                    pass  # nothing to do
                if try_no_value_snak:
                    cup.branch()
                    q.triple(t['wds'], self.rdf.type, t['wdno'])
        # Push subject, property, value entities/literals (if any).
        self._push_filter_patterns_as_values(q, t, [(0, pat)])
        return q

    def _push_filter_pattern_bind_pname_as(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            *args: tuple[NS.T_NS, str]
    ) -> Mapping[str, TTrm]:
        for ns, name in args:
            q.bind(q.uri(q.concat(String(str(ns)), t['pname'])), t[name])
        return t

    def _push_filter_patterns_as_values(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            pats: Iterable[tuple[int, FilterPattern]]
    ) -> Mapping[str, TTrm]:
        values = q.values(
            t['i'], t['subject'], t['property'],
            t['pname'], t['p'], t['ps'], t['psv'], t['wdno'], t['value'],
            t['qt_amount'], t['qt_unit'], t['qt_lower'], t['qt_upper'],
            t['tm_value'], t['tm_precision'],
            t['tm_timezone'], t['tm_calendar'])
        with values:
            for i, pat in pats:
                self._push_filter_patterns_as_values_helper(
                    q, values, pat, i)
        return t

    def _push_filter_patterns_as_values_helper(
            self,
            q: SPARQL_Builder,
            values: SPARQL_Builder.Values,
            pat: FilterPattern,
            i: int
    ) -> SPARQL_Builder:
        p: TTrm = q.UNDEF
        pname: TTrm = q.UNDEF
        prop: TTrm = q.UNDEF
        ps: TTrm = q.UNDEF
        psv: TTrm = q.UNDEF
        qt_amount: TTrm = q.UNDEF
        qt_lower: TTrm = q.UNDEF
        qt_unit: TTrm = q.UNDEF
        qt_upper: TTrm = q.UNDEF
        subj: TTrm = q.UNDEF
        tm_calendar: TTrm = q.UNDEF
        tm_precision: TTrm = q.UNDEF
        tm_timezone: TTrm = q.UNDEF
        tm_value: TTrm = q.UNDEF
        val: TTrm = q.UNDEF
        wdno: TTrm = q.UNDEF
        # Subject:
        if pat.subject is not None and pat.subject.entity is not None:
            subj = cast(Entity, pat.subject.entity)
        # Property:
        if pat.property is not None and pat.property.property is not None:
            prop_ = cast(Property, pat.property.property)
            name = NS.Wikidata.get_wikidata_name(prop_.iri.value)
            prop = prop_
            pname = String(name)
            p = self.p[name]
            ps = self.ps[name]
            psv = self.psv[name]
            wdno = self.wdno[name]
        # Value:
        if pat.value is not None and pat.value.value is not None:
            value = cast(Value, pat.value.value)
            val = value
            if value.is_deep_data_value():
                if value.is_quantity():
                    qt = cast(Quantity, value)
                    qt_amount = Quantity(qt.amount)
                    if qt.unit is not None:
                        qt_unit = qt.unit
                    if qt.lower_bound is not None:
                        qt_lower = Quantity(qt.lower_bound)
                    if qt.upper_bound is not None:
                        qt_upper = Quantity(qt.upper_bound)
                elif value.is_time():
                    tm = cast(Time, value)
                    tm_value = tm
                    if tm.precision is not None:
                        tm_precision = tm.precision.value
                    if tm.timezone is not None:
                        tm_timezone = tm.timezone
                    if tm.calendar_model is not None:
                        tm_calendar = tm.calendar_model
                else:
                    raise ShouldNotGetHere
        values.push(
            i, subj, prop, pname, p, ps, psv, wdno, val,
            qt_amount, qt_unit, qt_lower, qt_upper,
            tm_value, tm_precision, tm_timezone, tm_calendar)
        return q

    def _push_deep_data_value(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            value: Optional[DeepDataValue] = None,
            wds: str = 'wds',
            psv: str = 'psv',
            wdv: str = 'wdv',
            qt_amount: str = 'qt_amount',
            qt_unit: str = 'qt_unit',
            qt_lower: str = 'qt_lower',
            qt_upper: str = 'qt_upper',
            tm_value: str = 'tm_value',
            tm_precision: str = 'tm_precision',
            tm_timezone: str = 'tm_timezone',
            tm_calendar: str = 'tm_calendar',
    ) -> SPARQL_Builder:
        assert value is None or value.is_deep_data_value()
        with q.union(cond=value is None) as cup:
            if value is None or value.is_quantity():
                cup.branch()
                q.triples(
                    (t[wds], t[psv], t[wdv]),
                    (t[wdv], self.rdf.type, self.wikibase.QuantityValue),
                    (t[wdv], self.wikibase.quantityAmount, t[qt_amount]))
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).unit is None)):
                    q.triple(
                        t[wdv], self.wikibase.quantityUnit, t[qt_unit])
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).lower_bound is None)):
                    q.triple(
                        t[wdv], self.wikibase.quantityLowerBound, t[qt_lower])
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).upper_bound is None)):
                    q.triple(
                        t[wdv], self.wikibase.quantityUpperBound, t[qt_upper])
            if value is None or value.is_time():
                cup.branch()
                q.triples(
                    (t[wds], t[psv], t[wdv]),
                    (t[wdv], self.rdf.type, self.wikibase.TimeValue),
                    (t[wdv], self.wikibase.timeValue, t[tm_value]))
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).precision is None)):
                    q.triple(
                        t[wdv], self.wikibase.timePrecision, t[tm_precision])
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).timezone is None)):
                    q.triple(
                        t[wdv], self.wikibase.timeTimezone, t[tm_timezone])
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).calendar_model is None)):
                    q.triple(
                        t[wdv], self.wikibase.timeCalendarModel,
                        t[tm_calendar])
        return q

    def _push_snak_set(
            self,
            q: SPARQL_Builder,
            subj: TTrm,
            snaks: SnakSet
    ) -> SPARQL_Builder:
        for snak in snaks:
            pname = NS.Wikidata.get_wikidata_name(snak.property.iri.value)
            if snak.is_value_snak():
                val = cast(ValueSnak, snak).value
                q.triple(subj, self.wdt[pname], val)
            elif snak.is_some_value_snak():
                some = q.var()
                q.triple(subj, self.wdt[pname], some)
                self._push_some_value_filter(q, some)
            elif snak.is_no_value_snak():
                wds = q.bnode()
                q.triples(
                    (subj, self.p[pname], wds),
                    (wds, self.rdf.type, self.wdno[pname]))
            else:
                raise ShouldNotGetHere
        return q

    def _push_some_value_filter(
            self,
            q: SPARQL_Builder,
            val: TTrm,
            negate: bool = False,
    ) -> SPARQL_Builder:
        cond = q.or_(
            q.isBlank(val),
            q.and_(q.isURI(val), q.strstarts(
                q.str_(val), String(str(self.wdgenid)))))
        if negate:
            return q.filter(q.not_(cond))
        else:
            return q.filter(cond)

    def _get_wdss(
            self,
            stmts: Iterable[Statement],
            force_cache_update: bool = False,
            retries: int = 1,
            _vars: tuple[str, ...] = (
                '?i',
                '?property',
                '?qt_amount',
                '?qt_lower',
                '?qt_unit',
                '?qt_upper',
                '?subject',
                '?tm_calendar',
                '?tm_precision',
                '?tm_timezone',
                '?tm_value',
                '?value',
                '?wds',
            )
    ) -> Iterator[tuple[Statement, Optional[Set[T_WDS]]]]:
        batches = more_itertools.batched(stmts, self.page_size)
        for batch in batches:
            reduced_batch: list[Statement] = []
            stmt2wdss: dict[Statement, set[T_WDS]] = dict()
            for stmt in batch:
                wdss = self._cache_get_wdss(stmt)
                if not force_cache_update and wdss is not None:
                    stmt2wdss[stmt] = cast(set, wdss)
                else:
                    reduced_batch.append(stmt)
            if reduced_batch:
                q1, q2 = self._make_get_wdss_queries(enumerate(reduced_batch))
                if q1 is not None:
                    it1 = self._eval_select_query(
                        q1, lambda res: self._parse_get_wdss_results(res),
                        vars=_vars)
                else:
                    it1 = iter([])
                if q2 is not None:
                    it2 = self._eval_select_query(
                        q2, lambda res: self._parse_get_wdss_results(res),
                        vars=_vars)
                else:
                    it2 = iter([])
                seen = set()
                for (stmt, wds, i) in itertools.chain(it1, it2):
                    seen.add(i)
                    if stmt != reduced_batch[i]:
                        continue  # nothing to do
                    if stmt not in stmt2wdss:
                        stmt2wdss[stmt] = set()
                    stmt2wdss[stmt].add(wds)
                unseen = set(range(len(reduced_batch))) - seen
                if unseen and retries > 0:
                    unseen_stmts = list(map(
                        lambda i: reduced_batch[i], unseen))
                    LOG.debug(
                        '%s(): retrying (%d left)',
                        self._get_wdss.__qualname__, retries - 1)
                    for stmt, wds in self._get_wdss(
                            unseen_stmts, force_cache_update, retries - 1):
                        if wds is not None:
                            if stmt not in stmt2wdss:
                                stmt2wdss[stmt] = set()
                            stmt2wdss[stmt].add(wds)
            for stmt in batch:
                yield stmt, stmt2wdss.get(stmt, None)

    def _parse_get_wdss_results(
            self,
            results: SPARQL_Results,
    ) -> Iterator[Optional[tuple[Statement, T_WDS, int]]]:
        for entry in results.bindings:
            i = entry.check_integer('i')
            stmt = entry.check_statement(
                'subject', 'property', 'value',
                'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
            wds = entry.check_bnode_or_uriref('wds')
            yield stmt, wds, i

    def _make_get_wdss_queries(
            self,
            stmts: Iterator[tuple[int, Statement]]
    ) -> tuple[Optional[SPARQL_Builder], Optional[SPARQL_Builder]]:
        values: list[tuple[int, Statement]] = []
        no_values: list[tuple[int, Statement]] = []
        for i, stmt in stmts:
            if ((self.has_flags(self.VALUE_SNAK)
                and stmt.snak.is_value_snak())
                or (self.has_flags(self.SOME_VALUE_SNAK)
                    and stmt.snak.is_some_value_snak())):
                values.append((i, stmt))
            elif (self.has_flags(self.NO_VALUE_SNAK)
                  and stmt.snak.is_no_value_snak()):
                no_values.append((i, stmt))
        ###
        # FIXME: Find a way to do this using a single query.
        ###
        if values:              # q1 applies to (some) value stmts
            q1, t1 = self._make_get_wdss_query_start()
            with q1.union() as cup:
                if self.has_flags(self.VALUE_SNAK):
                    cup.branch()
                    q1.triple(t1['wds'], t1['ps'], t1['value'])
                    with q1.optional():
                        self._push_deep_data_value(q1, t1)
                if self.has_flags(self.SOME_VALUE_SNAK):
                    cup.branch()
                    q1.triple(t1['wds'], t1['ps'], t1['value'])
                    self._push_some_value_filter(q1, t1['value'])
            self._make_get_wdss_query_end(q1, t1, values)
        else:
            q1 = None
        if no_values:           # q2 applies to no value stmts
            q2, t2 = self._make_get_wdss_query_start()
            q2.triple(t2['wds'], self.rdf.type, t2['wdno'])
            self._make_get_wdss_query_end(q2, t2, no_values)
        else:
            q2 = None
        return q1, q2

    def _make_get_wdss_query_start(
            self,
    ) -> tuple[SPARQL_Builder, Mapping[str, TTrm]]:
        q = SPARQL_Builder()
        t = self._make_filter_query_vars_dict(q)
        q.where_start()
        q.triples(
            (t['subject'], t['p'], t['wds']),
            (t['wds'], self.wikibase.rank, q.bnode()))
        if self.has_flags(self.BEST_RANK):
            q.triple(t['wds'], self.rdf.type, self.wikibase.BestRank)
        return q, t

    def _make_get_wdss_query_end(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            stmts: Iterable[tuple[int, Statement]]
    ):
        self._push_filter_patterns_as_values(q, t, map(
            lambda x: (x[0], FilterPattern.from_statement(x[1])), stmts))
        q.where_end()

    # -- Annotations -------------------------------------------------------

    def _get_annotations(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        batches = more_itertools.batched(stmts, self.page_size)
        for batch in batches:
            wds_batch = []
            stmt2wdss: dict[Statement, Set[T_WDS]] = dict()
            wds2stmt: dict[T_WDS, Statement] = dict()
            for stmt, wdss in self._get_wdss(batch):
                if wdss is not None:
                    stmt2wdss[stmt] = wdss
                    for wds in wdss:
                        wds2stmt[wds] = stmt
                        wds_batch.append(wds)
            if not wds_batch:
                for stmt in batch:
                    yield stmt, None
                continue        # empty batch, nothing to do
            q = self._make_get_annotations_query(set(wds_batch))
            it = self._eval_select_query(
                q, lambda res: self._parse_get_annotations_results(res))
            wds2rank: dict[T_WDS, Rank] = dict()
            wds2quals: dict[T_WDS, set[Snak]] = dict()
            wds2refs: dict[T_WDS, dict[T_WDS, set[Snak]]] = dict()
            for wds, rank, wdref, snak in it:
                wds2rank[wds] = rank
                if snak is None:
                    continue
                assert snak is not None
                if wdref is None:
                    if wds not in wds2quals:
                        wds2quals[wds] = set()
                    if (snak.is_no_value_snak()
                            and snak == wds2stmt[wds].snak):
                        ###
                        # IMPORTANT: The representation of NoValueSnak's
                        # (via rdf:type) is ambiguous.  To be considered a
                        # qualifier, a NoValueSnak must be different from
                        # the snak of the statement.
                        ###
                        pass
                    else:
                        wds2quals[wds].add(snak)
                else:
                    if wds not in wds2refs:
                        wds2refs[wds] = dict()
                    if wdref not in wds2refs[wds]:
                        wds2refs[wds][wdref] = set()
                    wds2refs[wds][wdref].add(snak)
            for stmt in batch:
                if stmt in stmt2wdss:
                    wdss = stmt2wdss[stmt]
                    annots = []
                    for wds in wdss:
                        if wds not in wds2rank:
                            continue
                        if wds in wds2quals:
                            quals = wds2quals[wds]
                        else:
                            quals = set()
                        if wds in wds2refs:
                            refs = set(itertools.starmap(
                                ReferenceRecord, wds2refs[wds].values()))
                        else:
                            refs = set()
                        annots.append(AnnotationRecord(
                            quals, refs, wds2rank[wds]))
                    yield stmt, AnnotationRecordSet(*annots)
                else:
                    yield stmt, None

    def _parse_get_annotations_results(
            self,
            results: SPARQL_Results,
    ) -> Iterator[Optional[tuple[
            T_WDS, Rank, Optional[T_WDS], Optional[Snak]]]]:
        for entry in results.bindings:
            wds = entry.check_bnode_or_uriref('wds')
            rank = entry.check_rank('rank')
            if 'pq' in entry and 'qvalue' in entry:
                pq = entry.check_uriref('pq')
                if not NS.Wikidata.is_wikidata_uri(pq):
                    yield None
                    continue    # ignore unexpected prefix
                ns, name = NS.Wikidata.split_wikidata_uri(pq)
                if ns == self.pqn:
                    yield None
                    continue    # ignore normalized value
                if ns != self.pq and ns != self.pqv:
                    yield None
                    continue    # ignore unexpected prefix
                if 'datatype' in entry['qvalue']:
                    dt = entry['qvalue']['datatype']
                    if (dt == str(self.xsd.dateTime)
                            or dt == str(self.xsd.decimal)):
                        yield None
                        continue  # ignore simple value
                prop = Property(self.wd[name])
                snak = entry.check_snak(
                    prop, 'qvalue',
                    'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                    'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
                yield wds, rank, None, snak
            elif 'pq' not in entry and 'qvalue' in entry:
                qvalue = entry.check_uriref('qvalue')
                if not NS.Wikidata.is_wikidata_uri(qvalue):
                    yield None
                    continue    # ignore unexpected prefix
                ns, name = NS.Wikidata.split_wikidata_uri(qvalue)
                if ns != self.wdno:
                    yield None
                    continue    # ignore unexpected prefix
                prop = Property(self.wd[name])
                yield wds, rank, None, NoValueSnak(prop)
            elif 'pr' in entry and 'rvalue' in entry and 'wdref' in entry:
                wdref = entry.check_uriref('wdref')
                pr = entry.check_uriref('pr')
                ns, name = NS.Wikidata.split_wikidata_uri(pr)
                if ns == self.prn:
                    yield None
                    continue    # ignore normalized value
                if 'datatype' in entry['rvalue']:
                    dt = entry['rvalue']['datatype']
                    if (dt == str(self.xsd.dateTime)
                            or dt == str(self.xsd.decimal)):
                        yield None
                        continue  # ignore simple value
                prop = Property(self.wd[name])
                snak = entry.check_snak(
                    prop, 'rvalue',
                    'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                    'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
                yield wds, rank, wdref, snak
            else:
                yield wds, rank, None, None

    def _make_get_annotations_query(
            self,
            wdss: Collection[T_WDS]
    ) -> SPARQL_Builder:
        q = SPARQL_Builder()
        t = q.vars_dict(
            'pq',
            'pr',
            'psv',
            'qt_amount',
            'qt_lower',
            'qt_unit',
            'qt_upper',
            'qvalue',
            'rank',
            'rvalue',
            'tm_calendar',
            'tm_precision',
            'tm_timezone',
            'tm_value',
            'wdref',
            'wds',
            'wdv',
        )
        q.where_start()
        q.triple(t['wds'], self.wikibase.rank, t['rank'])
        with q.values(t['wds']) as values:
            for wds in wdss:
                values.push(wds)
        if self.has_flags(self.BEST_RANK):
            q.triple(t['wds'], self.rdf.type, self.wikibase.BestRank)
        q.optional_start()
        with q.union() as cup:
            # Qualifiers:
            cup.branch()
            q.triple(t['wds'], t['pq'], t['qvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(q.str_(t['pq']), String(str(self.pq))))
            with q.optional():
                self._push_deep_data_value(
                    q, t, None, 'wds', 'pq', 'qvalue')
            cup.branch()
            q.triple(t['wds'], self.rdf.type, t['qvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(
                    q.str_(t['qvalue']), String(str(self.wdno))))
            # References:
            cup.branch()
            q.triple(t['wds'], self.prov.wasDerivedFrom, t['wdref'])
            q.triple(t['wdref'], t['pr'], t['rvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(q.str_(t['pr']), String(str(self.pr))))
            with q.optional():
                self._push_deep_data_value(
                    q, t, None, 'wdref', 'pr', 'rvalue')
        q.optional_end()
        q.where_end()
        return q

    # -- Descriptors -------------------------------------------------------

    def _get_descriptor(
            self,
            entities: Iterable[Entity],
            lang: str
    ) -> Iterator[tuple[Entity, Descriptor]]:
        batches = more_itertools.batched(entities, self.page_size)
        for batch in batches:
            q = self._make_descriptor_query(set(batch), lang)
            it = self._eval_select_query(
                q, lambda res: self._parse_get_descriptor_results(res))
            entity2label: dict[Entity, Text] = dict()
            entity2aliases: dict[Entity, set[Text]] = dict()
            entity2desc: dict[Entity, Text] = dict()
            for entity, label, alias, desc in it:
                if label is not None:
                    entity2label[entity] = label
                elif alias is not None:
                    if entity not in entity2aliases:
                        entity2aliases[entity] = set()
                    entity2aliases[entity].add(alias)
                elif desc is not None:
                    entity2desc[entity] = desc
            for entity in batch:
                yield (entity, Descriptor(
                    entity2label.get(entity),
                    entity2aliases.get(entity, []),
                    entity2desc.get(entity, None)))

    def _parse_get_descriptor_results(
            self,
            results: SPARQL_Results,
    ) -> Iterator[Optional[tuple[
            Entity, Optional[Text], Optional[Text], Optional[Text]]]]:
        for entry in results.bindings:
            entity = entry.check_entity('subject')
            if 'label' in entry:
                yield entity, entry.check_text('label'), None, None
            elif 'alias' in entry:
                yield entity, None, entry.check_text('alias'), None
            elif 'description' in entry:
                yield entity, None, None, entry.check_text('description')
            else:
                yield None      # ignore

    def _make_descriptor_query(
            self,
            entities: Collection[Entity],
            lang: str
    ) -> SPARQL_Builder:
        q = SPARQL_Builder()
        t: Mapping[str, TTrm] = q.vars_dict(
            'alias',
            'description',
            'label',
            'subject',
        )
        language = String(lang)
        with q.where():
            with q.union() as cup:
                q.triple(t['subject'], self.rdfs.label, t['label'])
                q.filter(q.eq(q.lang(t['label']), language))
                cup.branch()
                q.triple(
                    t['subject'], self.schema.description, t['description'])
                q.filter(q.eq(q.lang(t['description']), language))
                cup.branch()
                q.triple(t['subject'], self.skos.altLabel, t['alias'])
                q.filter(q.eq(q.lang(t['alias']), language))
            with q.values(t['subject']) as values:
                for entity in entities:
                    values.push(entity.iri)
        return q
