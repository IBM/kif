# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import logging

import httpx
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.sparql import Query

from .. import itertools
from .. import namespace as NS
from ..compiler.sparql import SPARQL_FilterCompiler, SPARQL_PatternCompiler
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    ClosedPattern,
    ClosedTerm,
    Datatype,
    DeepDataValue,
    Descriptor,
    Entity,
    ExternalId,
    Filter,
    IRI,
    Item,
    ItemDescriptor,
    Lexeme,
    LexemeDescriptor,
    NoValueSnak,
    OpenPattern,
    Pattern,
    Property,
    PropertyDescriptor,
    Quantity,
    Rank,
    ReferenceRecord,
    Snak,
    SomeValueSnak,
    Statement,
    StatementVariable,
    String,
    T_IRI,
    TemplatePattern,
    Term,
    Text,
    Time,
    Value,
    ValueSnak,
    VariablePattern,
)
from ..rdflib import BNode, URIRef
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Collection,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    MutableSet,
    override,
    Set,
    TypeAlias,
    TypeVar,
    Union,
)
from ..version import __version__
from .abc import Store
from .sparql_builder import SPARQL_Builder
from .sparql_results import SPARQL_Results

LOG = logging.getLogger(__name__)

T = TypeVar('T')
T_WDS = Hashable
TOpq: TypeAlias = Union[BNode, URIRef]
TTrm = SPARQL_Builder.TTrm


class SPARQL_Store(
        Store,
        store_name='sparql',
        store_description='SPARQL endpoint'
):
    """SPARQL store.

    Parameters:
       store_name: Store plugin to instantiate.
       iri: SPARQL endpoint IRI.
    """

    _headers = {
        # See <https://meta.wikimedia.org/wiki/User-Agent_policy>.
        'User-Agent': f'KIF/{__version__} (https://github.com/IBM/kif/)',
        'Content-Type': 'application/sparql-query;charset=utf-8',
        'Accept': 'application/sparql-results+json;charset=utf-8',
    }

    __slots__ = (
        '_client',
        '_iri',
    )

    #: HTTP client.
    _client: httpx.Client

    #: IRI of the target SPARQL endpoint.
    _iri: IRI

    def __init__(self, store_name: str, iri: T_IRI, **kwargs: Any) -> None:
        assert store_name == self.store_name
        self._client = httpx.Client(headers=self._headers)
        super().__init__(**kwargs)
        self._iri = IRI.check(iri, type(self), 'iri', 2)

    def __del__(self) -> None:
        self._client.close()

    @override
    def set_timeout(self, timeout: float | None = None) -> None:
        super().set_timeout(timeout)
        self._client.timeout = httpx.Timeout(timeout)

    @property
    def iri(self) -> IRI:
        """The IRI of the target SPARQL endpoint."""
        return self.get_iri()

    def get_iri(self) -> IRI:
        """Gets the IRI of the target SPARQL endpoint.

        Returns:
           IRI.
        """
        return self._iri

# -- Caching ---------------------------------------------------------------

    def _cache_get_wdss(self, stmt: Statement) -> Set[T_WDS] | None:
        return self._cache.get(stmt, 'wdss')

    def _cache_add_wds(self, stmt: Statement, wds: T_WDS) -> Set[T_WDS]:
        self._cache.set(wds, 'statement', stmt)
        wdss = self._cache.get(stmt, 'wdss')
        if wdss is None:
            wdss = self._cache.set(stmt, 'wdss', set())
        wdss.add(wds)
        return wdss

# -- Query evaluation (internal) -------------------------------------------

    def _eval_select_query(
            self,
            query: SPARQL_Builder,
            parse_results_fn: Callable[
                [SPARQL_Results], Iterator[T | None]],
            vars: Collection[TTrm | tuple[TTrm, TTrm]] = tuple(),
            order_by: TTrm | None = None,
            limit: int | None = None,
            distinct: bool = False,
            trim: bool = False
    ) -> Iterator[T]:
        def eval_fn(
                eval_limit: int | None = None,
                eval_offset: int | None = None
        ) -> Iterator[T | None]:
            return parse_results_fn(
                self._eval_select_query_string(
                    query.select(
                        *vars, distinct=distinct, order_by=order_by,
                        limit=eval_limit, offset=eval_offset)))
        return self._eval_query(query, eval_fn, limit, trim)

    def _eval_query(
            self,
            query: SPARQL_Builder,
            eval_fn: Callable[
                [int | None, int | None], Iterator[T | None]],
            limit: int | None = None,
            trim: bool = False,
            page_size: int | None = None,
            offset: int | None = None
    ) -> Iterator[T]:
        import sys
        if limit is None:
            limit = sys.maxsize
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

    def _eval_select_query_string(
            self,
            text: str,
            fake_results: bool = False,
            **kwargs: Any
    ) -> SPARQL_Results:
        # text = self._prepare_query_string_wrapper(text)
        results = self._eval_query_string(text, **kwargs).json()
        if fake_results:
            return cast(SPARQL_Results, results)
        else:
            return SPARQL_Results(results)

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
            **kwargs: Any
    ) -> httpx.Response:
        LOG.debug('%s():\n%s', self._eval_query_string.__qualname__, text)
        try:
            res = self._client.post(
                self.iri.content, content=text.encode('utf-8'), **kwargs)
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err

# -- Match -----------------------------------------------------------------

    @override
    def _match(
            self,
            pattern: Pattern,
            limit: int,
            distinct: bool
    ) -> Iterator[ClosedTerm]:
        assert isinstance(pattern, Pattern)
        assert limit >= 0
        compiler = self._compile_pattern(pattern)
        if isinstance(pattern, ClosedPattern):
            raise NotImplementedError
        elif isinstance(pattern, OpenPattern):
            page_size = min(self.page_size, limit)
            offset, count = 0, 0
            while count <= limit:
                query = compiler.query.select(
                    limit=page_size, offset=offset, distinct=distinct)
                res = self._eval_select_query_string(str(query))
                bindings = res['results']['bindings']
                if not bindings:
                    break           # done
                for binding in bindings:
                    theta = compiler.theta.instantiate(binding)
                    if isinstance(pattern, TemplatePattern):
                        term: Term | None = pattern.template.instantiate(theta)
                    elif isinstance(pattern, VariablePattern):
                        term = pattern.variable.instantiate(theta)
                    else:
                        raise self._should_not_get_here()
                    if isinstance(term, ClosedTerm):
                        yield term
                    count += 1
                if len(bindings) < page_size:
                    break           # done
                if count == limit:
                    break           # done
                offset += page_size
        else:
            raise self._should_not_get_here()

    #: Flags to be passed to filter compiler.
    _compile_pattern_flags: ClassVar[SPARQL_FilterCompiler.Flags] =\
        SPARQL_PatternCompiler.default_flags

    def _compile_pattern(
            self,
            pattern: Pattern
    ) -> SPARQL_PatternCompiler:
        compiler = SPARQL_PatternCompiler(pattern, self._compile_pattern_flags)
        if self.has_flags(self.DEBUG):
            compiler.set_flags(compiler.DEBUG)
        else:
            compiler.unset_flags(compiler.DEBUG)
        if self.has_flags(self.BEST_RANK):
            compiler.set_flags(compiler.BEST_RANK)
        else:
            compiler.unset_flags(compiler.BEST_RANK)
        compiler.compile()
        return compiler

# -- Statements ------------------------------------------------------------

    @override
    def _contains(self, filter: Filter) -> bool:
        compiler = self._compile_filter(filter)
        res = self._eval_select_query_string(
            str(compiler.query.ask()), fake_results=True)
        return res['boolean']

    @override
    def _count(self, filter: Filter) -> int:
        if not filter.is_full():
            compiler = self._compile_filter(filter)
            q = compiler.query
        else:
            q = SPARQL_FilterCompiler.Query()
            wds = q.fresh_var()
            if self.has_flags(self.BEST_RANK):
                q.triples()((wds, NS.RDF.type, NS.WIKIBASE.BestRank))
            else:
                q.triples()((wds, NS.WIKIBASE.rank, q.var('rank')))
        count = q.fresh_var()
        res = self._eval_select_query_string(
            str(q.select((q.count(), count))))
        assert len(res['results']['bindings']) == 1
        return int(res['results']['bindings'][0][str(count)]['value'])

    @override
    def _filter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        compiler = self._compile_filter(filter)
        assert limit >= 0
        page_size = min(self.page_size, limit)
        offset, count = 0, 0
        while count <= limit:
            query = compiler.query.select(
                limit=page_size, offset=offset, distinct=distinct)
            assert isinstance(compiler.pattern, VariablePattern)
            assert isinstance(compiler.pattern.variable, StatementVariable)
            if query.where_is_empty():
                break           # nothing to do
            var = compiler.pattern.variable
            wds = compiler.wds
            res = self._eval_select_query_string(str(query))
            bindings = res['results']['bindings']
            if not bindings:
                break           # done
            for binding in bindings:
                theta = compiler.theta.instantiate(binding)
                stmt = var.instantiate(theta)
                assert isinstance(stmt, Statement)
                if self.has_flags(self.LATE_FILTER) and not filter.match(stmt):
                    continue
                self._cache_add_wds(stmt, URIRef(binding[str(wds)]['value']))
                yield stmt
                count += 1
            if len(bindings) < page_size:
                break           # done
            if count == limit:
                break           # done
            offset += page_size

    #: Flags to be passed to filter compiler.
    _compile_filter_flags: ClassVar[SPARQL_FilterCompiler.Flags] =\
        SPARQL_FilterCompiler.default_flags

    def _compile_filter(
            self,
            filter: Filter
    ) -> SPARQL_FilterCompiler:
        compiler = SPARQL_FilterCompiler(filter, self._compile_filter_flags)
        if self.has_flags(self.DEBUG):
            compiler.set_flags(compiler.DEBUG)
        else:
            compiler.unset_flags(compiler.DEBUG)
        if self.has_flags(self.BEST_RANK):
            compiler.set_flags(compiler.BEST_RANK)
        else:
            compiler.unset_flags(compiler.BEST_RANK)
        compiler.compile()
        return compiler

    def _make_filter_query_vars_dict(
            self,
            q: SPARQL_Builder
    ) -> Mapping[str, TTrm]:
        return q.vars_dict(
            'datatype',
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

    def _push_filters_as_values(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            filters: Iterable[tuple[int, Filter]]
    ) -> Mapping[str, TTrm]:
        values = q.values(
            t['i'], t['subject'], t['property'],
            t['pname'], t['p'], t['ps'], t['psv'], t['wdno'], t['value'],
            t['qt_amount'], t['qt_unit'], t['qt_lower'], t['qt_upper'],
            t['tm_value'], t['tm_precision'],
            t['tm_timezone'], t['tm_calendar'])
        with values:
            for i, filter in filters:
                self._push_filters_as_values_helper(
                    q, values, filter, i)
        return t

    def _push_filters_as_values_helper(
            self,
            q: SPARQL_Builder,
            values: SPARQL_Builder.Values,
            filter: Filter,
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
        subject, property, value, _ = filter._unpack_legacy()
        # Subject:
        if subject is not None and isinstance(subject, Entity):
            subj = subject
        # Property:
        if property is not None and isinstance(property, Property):
            prop_ = property
            name = NS.Wikidata.get_wikidata_name(prop_.iri.content)
            prop = prop_
            pname = String(name)
            p = NS.P[name]
            ps = NS.PS[name]
            psv = NS.PSV[name]
            wdno = NS.WDNO[name]
        # Value:
        if value is not None and isinstance(value, Value):
            val = value
            if isinstance(value, DeepDataValue):
                if isinstance(value, Quantity):
                    qt = value
                    qt_amount = Quantity(qt.amount)
                    if qt.unit is not None:
                        qt_unit = qt.unit
                    if qt.lower_bound is not None:
                        qt_lower = Quantity(qt.lower_bound)
                    if qt.upper_bound is not None:
                        qt_upper = Quantity(qt.upper_bound)
                elif isinstance(value, Time):
                    tm = value
                    tm_value = tm
                    if tm.precision is not None:
                        tm_precision = tm.precision.value
                    if tm.timezone is not None:
                        tm_timezone = tm.timezone
                    if tm.calendar is not None:
                        tm_calendar = tm.calendar
                else:
                    raise self._should_not_get_here()
        values.push(
            i, subj, prop, pname, p, ps, psv, wdno, val,
            qt_amount, qt_unit, qt_lower, qt_upper,
            tm_value, tm_precision, tm_timezone, tm_calendar)
        return q

    def _push_deep_data_value(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            value: DeepDataValue | None = None,
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
        assert value is None or isinstance(value, DeepDataValue)
        with q.union(cond=value is None) as cup:
            if value is None or isinstance(value, Quantity):
                cup.branch()
                q.triples(
                    (t[wds], t[psv], t[wdv]),
                    (t[wdv], NS.RDF.type, NS.WIKIBASE.QuantityValue),
                    (t[wdv], NS.WIKIBASE.quantityAmount, t[qt_amount]))
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).unit is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.quantityUnit, t[qt_unit])
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).lower_bound is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.quantityLowerBound, t[qt_lower])
                with q.optional(
                        cond=(value is None or cast(
                            Quantity, value).upper_bound is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.quantityUpperBound, t[qt_upper])
            if value is None or isinstance(value, Time):
                cup.branch()
                q.triples(
                    (t[wds], t[psv], t[wdv]),
                    (t[wdv], NS.RDF.type, NS.WIKIBASE.TimeValue),
                    (t[wdv], NS.WIKIBASE.timeValue, t[tm_value]))
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).precision is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.timePrecision, t[tm_precision])
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).timezone is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.timeTimezone, t[tm_timezone])
                with q.optional(
                        cond=(value is None or cast(
                            Time, value).calendar is None)):
                    q.triple(
                        t[wdv], NS.WIKIBASE.timeCalendarModel,
                        t[tm_calendar])
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
                q.str_(val), String(str(NS.WDGENID)))))
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
    ) -> Iterator[tuple[Statement, Set[T_WDS] | None]]:
        for batch in self._batched(stmts):
            reduced_batch: list[Statement] = []
            stmt2wdss: dict[Statement, MutableSet[T_WDS]] = {}
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
                        q1, self._parse_get_wdss_results, vars=_vars)
                else:
                    it1 = iter(())
                if q2 is not None:
                    it2 = self._eval_select_query(
                        q2, self._parse_get_wdss_results, vars=_vars)
                else:
                    it2 = iter(())
                seen = set()
                for (stmt, wds, i) in itertools.chain(it1, it2):
                    ###
                    # FIXME: Compatibility with legacy queries.
                    ###
                    seen.add(i)
                    stmti = reduced_batch[i]
                    saved_stmti = stmti
                    if isinstance(stmt.snak, (SomeValueSnak, NoValueSnak)):
                        stmti = stmti.replace(stmti.KEEP, type(stmti.snak)(
                            stmti.snak.property.replace(stmti.KEEP, None)))
                    elif (isinstance(stmt.snak, ValueSnak)
                          and isinstance(stmti.snak, ValueSnak)
                          and isinstance(stmt.snak.value, String)
                          and isinstance(stmti.snak.value, ExternalId)):
                        stmti = stmti.replace(
                            stmti.KEEP,
                            stmti.snak.property.replace(stmti.KEEP, None)(
                                stmti.snak.value.content))
                    else:
                        self._should_not_get_here()
                    if stmt != stmti:
                        continue  # nothing to do
                    if stmt not in stmt2wdss:
                        stmt2wdss[saved_stmti] = set()
                    stmt2wdss[saved_stmti].add(wds)
                unseen = set(range(len(reduced_batch))) - seen
                if unseen and retries > 0:
                    f = functools.partial(lambda t, i: t[i], reduced_batch)
                    unseen_stmts = list(map(f, unseen))
                    LOG.debug(
                        '%s(): retrying (%d left)',
                        self._get_wdss.__qualname__, retries - 1)
                    for stmt, wdss in self._get_wdss(
                            unseen_stmts, force_cache_update, retries - 1):
                        if wdss is not None:
                            if stmt not in stmt2wdss:
                                stmt2wdss[stmt] = set()
                            for wds in wdss:
                                stmt2wdss[stmt].add(wds)
            for stmt in batch:
                yield stmt, stmt2wdss.get(stmt, None)

    def _make_get_wdss_queries(
            self,
            stmts: Iterator[tuple[int, Statement]]
    ) -> tuple[SPARQL_Builder | None, SPARQL_Builder | None]:
        values: list[tuple[int, Statement]] = []
        no_values: list[tuple[int, Statement]] = []
        for i, stmt in stmts:
            if ((self.has_flags(self.VALUE_SNAK)
                and isinstance(stmt.snak, ValueSnak))
                or (self.has_flags(self.SOME_VALUE_SNAK)
                    and isinstance(stmt.snak, SomeValueSnak))):
                values.append((i, stmt))
            elif (self.has_flags(self.NO_VALUE_SNAK)
                  and isinstance(stmt.snak, NoValueSnak)):
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
            q2.triple(t2['wds'], NS.RDF.type, t2['wdno'])
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
            (t['wds'], NS.WIKIBASE.rank, q.bnode()))
        if self.has_flags(self.BEST_RANK):
            q.triple(t['wds'], NS.RDF.type, NS.WIKIBASE.BestRank)
        return q, t

    def _make_get_wdss_query_end(
            self,
            q: SPARQL_Builder,
            t: Mapping[str, TTrm],
            stmts: Iterable[tuple[int, Statement]]
    ) -> None:
        self._push_filters_as_values(q, t, map(
            lambda x: (x[0], Filter.from_statement(x[1])), stmts))
        q.where_end()

    def _parse_get_wdss_results(
            self,
            results: SPARQL_Results,
    ) -> Iterator[tuple[Statement, T_WDS, int] | None]:
        for entry in results.bindings:
            i = entry.check_integer('i')
            stmt = entry.check_statement(
                'subject', 'property', 'value',
                'qt_amount', 'qt_unit', 'qt_lower', 'qt_upper',
                'tm_value', 'tm_precision', 'tm_timezone', 'tm_calendar')
            wds = entry.check_bnode_or_uriref('wds')
            yield stmt, wds, i

# -- Annotations -----------------------------------------------------------

    @override
    def _get_annotations(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        for batch in self._batched(stmts):
            wds_batch: list[T_WDS] = []
            stmt2wdss: dict[Statement, Set[T_WDS]] = {}
            wds2stmt: dict[T_WDS, Statement] = {}
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
                q, self._parse_get_annotations_results)
            wds2rank: dict[T_WDS, Rank] = {}
            wds2quals: dict[T_WDS, set[Snak]] = {}
            wds2refs: dict[T_WDS, dict[T_WDS, set[Snak]]] = {}
            for wds, rank, wdref, snak in it:
                wds2rank[wds] = rank
                if snak is None:
                    continue
                assert snak is not None
                if wdref is None:
                    if wds not in wds2quals:
                        wds2quals[wds] = set()
                    if (isinstance(snak, NoValueSnak)
                        and isinstance(wds2stmt[wds].snak, NoValueSnak)
                            and snak.property.iri == wds2stmt[
                                wds].snak.property.iri):
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
                        wds2refs[wds] = {}
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
                        quals = wds2quals.get(wds, set())
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
    ) -> Iterator[tuple[T_WDS, Rank, T_WDS | None, Snak | None] | None]:
        for entry in results.bindings:
            wds = entry.check_bnode_or_uriref('wds')
            rank = entry.check_rank('rank')
            if 'pq' in entry and 'qvalue' in entry:
                pq = entry.check_uriref('pq')
                if not NS.Wikidata.is_wikidata_uri(pq):
                    yield None
                    continue    # ignore unexpected prefix
                ns, name = NS.Wikidata.split_wikidata_uri(pq)
                if ns == NS.PQN:
                    yield None
                    continue    # ignore normalized value
                if ns != NS.PQ and ns != NS.PQV:
                    yield None
                    continue    # ignore unexpected prefix
                if 'datatype' in entry['qvalue']:
                    dt = entry['qvalue']['datatype']
                    if (dt == str(NS.XSD.dateTime)
                            or dt == str(NS.XSD.decimal)):
                        yield None
                        continue  # ignore simple value
                prop = Property(NS.WD[name])
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
                if ns != NS.WDNO:
                    yield None
                    continue    # ignore unexpected prefix
                prop = Property(NS.WD[name])
                yield wds, rank, None, NoValueSnak(prop)
            elif 'pr' in entry and 'rvalue' in entry and 'wdref' in entry:
                wdref = entry.check_uriref('wdref')
                pr = entry.check_uriref('pr')
                ns, name = NS.Wikidata.split_wikidata_uri(pr)
                if ns == NS.PRN:
                    yield None
                    continue    # ignore normalized value
                if 'datatype' in entry['rvalue']:
                    dt = entry['rvalue']['datatype']
                    if (dt == str(NS.XSD.dateTime)
                            or dt == str(NS.XSD.decimal)):
                        yield None
                        continue  # ignore simple value
                prop = Property(NS.WD[name])
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
        q.triple(t['wds'], NS.WIKIBASE.rank, t['rank'])
        with q.values(t['wds']) as values:
            for wds in wdss:
                values.push(cast(TTrm, wds))
        if self.has_flags(self.BEST_RANK):
            q.triple(t['wds'], NS.RDF.type, NS.WIKIBASE.BestRank)
        q.optional_start()
        with q.union() as cup:
            # Qualifiers:
            cup.branch()
            q.triple(t['wds'], t['pq'], t['qvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(q.str_(t['pq']), String(str(NS.PQ))))
            with q.optional():
                self._push_deep_data_value(
                    q, t, None, 'wds', 'pq', 'qvalue')
            cup.branch()
            q.triple(t['wds'], NS.RDF.type, t['qvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(
                    q.str_(t['qvalue']), String(str(NS.WDNO))))
            # References:
            cup.branch()
            q.triple(t['wds'], NS.PROV.wasDerivedFrom, t['wdref'])
            q.triple(t['wdref'], t['pr'], t['rvalue'])
            if self.has_flags(self.EARLY_FILTER):
                q.filter(q.strstarts(q.str_(t['pr']), String(str(NS.PR))))
            with q.optional():
                self._push_deep_data_value(
                    q, t, None, 'wdref', 'pr', 'rvalue')
        q.optional_end()
        q.where_end()
        return q

# -- Descriptors -----------------------------------------------------------

    @override
    def _get_item_descriptor(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, ItemDescriptor | None]]:
        return cast(
            Iterator[tuple[Item, Union[ItemDescriptor, None]]],
            self._get_item_or_property_descriptor(Item, items, language, mask))

    @override
    def _get_property_descriptor(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, PropertyDescriptor | None]]:
        return cast(
            Iterator[tuple[Property, Union[PropertyDescriptor, None]]],
            self._get_item_or_property_descriptor(
                Property, properties, language, mask))

    def _get_item_or_property_descriptor(
            self,
            cls: type[Entity],
            entities: Iterable[Item | Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[
            Item | Property,
            ItemDescriptor | PropertyDescriptor | None]]:
        q = self._make_item_or_property_descriptor_query(
            set(entities), cls, language, mask)
        if q.has_variable(q.var('subject')):
            it = self._eval_select_query(
                q, lambda res:
                self._parse_get_item_or_property_descriptor_results(
                    res, cls, language, mask))
        else:
            it = iter(())
            LOG.debug(
                '%s(): nothing to select:\n%s',
                self._filter.__qualname__, q.select())
        desc: dict[IRI | Property, dict[str, Any]] = {}
        ###
        # FIXME: Compatibility with legacy queries.
        ###
        for entity, label, alias, description, datatype in it:
            if entity.iri not in desc:
                desc[entity.iri] = {
                    'label': None,
                    'aliases': [],
                    'description': None,
                    'datatype': None
                }
            if label is not None:
                desc[entity.iri]['label'] = label
            if alias is not None:
                desc[entity.iri]['aliases'].append(alias)
            if description is not None:
                desc[entity.iri]['description'] = description
            if datatype is not None:
                desc[entity.iri]['datatype'] = datatype
        for entity in entities:
            if entity.iri in desc:
                if isinstance(entity, Item) and cls is Item:
                    yield (cast(Item, entity), ItemDescriptor(
                        desc[entity.iri].get('label'),
                        desc[entity.iri].get('aliases'),
                        desc[entity.iri].get('description')))
                elif isinstance(entity, Property) and cls is Property:
                    yield (cast(Property, entity), PropertyDescriptor(
                        desc[entity.iri].get('label'),
                        desc[entity.iri].get('aliases'),
                        desc[entity.iri].get('description'),
                        desc[entity.iri].get('datatype')))
                else:
                    raise self._should_not_get_here()
            else:
                yield entity, None

    def _make_item_or_property_descriptor_query(
            self,
            entities: Collection[Item | Property],
            cls: type[Entity],
            lang: str,
            mask: Descriptor.AttributeMask
    ) -> SPARQL_Builder:
        q = SPARQL_Builder()
        t: Mapping[str, TTrm] = q.vars_dict(
            'alias',
            'datatype',
            'description',
            'label',
            'subject')
        language = String(lang)
        if self.has_flags(self.EARLY_FILTER):
            get_label = bool(mask & Descriptor.LABEL)
            get_aliases = bool(mask & Descriptor.ALIASES)
            get_description = bool(mask & Descriptor.DESCRIPTION)
            get_datatype = cls is Property and bool(mask & Descriptor.DATATYPE)
        else:
            get_label = True
            get_aliases = True
            get_description = True
            get_datatype = cls is Property
        with q.where():
            # We use schema:version check whether ?subject exists.
            with q.union() as cup:
                q.triple(t['subject'], NS.WIKIBASE.sitelinks, q.bnode())
                cup.branch()
                q.triple(t['subject'], NS.RDF.type, NS.WIKIBASE.Property)
            if get_datatype:
                q.triple(t['subject'], NS.WIKIBASE.propertyType, t['datatype'])
            with q.optional(cond=get_label or get_aliases or get_description):
                with q.union() as cup:
                    if get_label:
                        q.triple(t['subject'], NS.RDFS.label, t['label'])
                        q.filter(q.eq(q.lang(t['label']), language))
                    if get_aliases:
                        cup.branch()
                        q.triple(
                            t['subject'], NS.SKOS.altLabel, t['alias'])
                        q.filter(q.eq(q.lang(t['alias']), language))
                    if get_description:
                        cup.branch()
                        q.triple(
                            t['subject'],
                            NS.SCHEMA.description, t['description'])
                        q.filter(q.eq(q.lang(t['description']), language))
            with q.values(t['subject']) as values:
                for entity in entities:
                    if isinstance(entity, cls):
                        values.push(entity.iri)
        return q

    def _parse_get_item_or_property_descriptor_results(
            self,
            results: SPARQL_Results,
            cls: type[Entity],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[
            Item | Property,
            Text | None,
            Text | None,
            Text | None,
            Datatype | None] | None]:
        if self.has_flags(self.LATE_FILTER):
            late_filter = True
            get_label = bool(mask & Descriptor.LABEL)
            get_aliases = bool(mask & Descriptor.ALIASES)
            get_description = bool(mask & Descriptor.DESCRIPTION)
            get_datatype = cls is Property and bool(mask & Descriptor.DATATYPE)
        else:
            late_filter = False
            get_label = True
            get_aliases = True
            get_description = True
            get_datatype = cls is Property
        for entry in results.bindings:
            if cls is Item:
                entity: Item | Property = entry.check_item('subject')
            elif cls is Property:
                entity = entry.check_property('subject')
            else:
                raise self._should_not_get_here()
            if get_datatype and 'datatype' in entry:
                datatype: Datatype | None = entry.check_datatype('datatype')
            else:
                datatype = None
            if get_label and 'label' in entry:
                label = entry.check_text('label')
                if label.language == language or not late_filter:
                    yield entity, label, None, None, datatype
                    continue    # found label
            elif get_aliases and 'alias' in entry:
                alias = entry.check_text('alias')
                if alias.language == language or not late_filter:
                    yield entity, None, alias, None, datatype
                    continue    # found alias
            elif get_description and 'description' in entry:
                description = entry.check_text('description')
                if description.language == language or not late_filter:
                    yield entity, None, None, description, datatype
                    continue    # found description
            yield entity, None, None, None, datatype  # fallback

    @override
    def _get_lexeme_descriptor(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, LexemeDescriptor | None]]:
        for batch in self._batched(lexemes):
            q = self._make_lexeme_descriptor_query(set(batch), mask)
            if q.has_variable(q.var('subject')):
                it = self._eval_select_query(
                    q, lambda res:
                    self._parse_get_lexeme_descriptor_results(res, mask))
            else:
                it = iter(())
                LOG.debug(
                    '%s(): nothing to select:\n%s',
                    self._filter.__qualname__, q.select())
            desc: dict[Lexeme, dict[str, Any]] = {}
            for lexeme, lemma, category, language in it:
                desc[lexeme] = {
                    'lemma': lemma,
                    'category': category,
                    'language': language,
                }
            for lexeme in batch:
                if lexeme in desc:
                    yield (lexeme, LexemeDescriptor(
                        desc[lexeme]['lemma'],
                        desc[lexeme]['category'],
                        desc[lexeme]['language']
                    ))
                else:
                    yield lexeme, None

    def _make_lexeme_descriptor_query(
            self,
            lexemes: Collection[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> SPARQL_Builder:
        q = SPARQL_Builder()
        t: Mapping[str, TTrm] = q.vars_dict(
            'lemma',
            'category',
            'language',
            'subject')
        if self.has_flags(self.EARLY_FILTER):
            get_lemma = bool(mask & Descriptor.LEMMA)
            get_category = bool(mask & Descriptor.CATEGORY)
            get_language = bool(mask & Descriptor.LANGUAGE)
        else:
            get_lemma = True
            get_category = True
            get_language = True
        with q.where():
            q.triple(t['subject'], NS.RDF.type, NS.ONTOLEX.LexicalEntry)
            if get_lemma:
                q.triple(t['subject'], NS.WIKIBASE.lemma, t['lemma'])
            if get_category:
                q.triple(
                    t['subject'], NS.WIKIBASE.lexicalCategory, t['category'])
            if get_language:
                q.triple(t['subject'], NS.DCT.language, t['language'])
            with q.values(t['subject']) as values:
                for lexeme in lexemes:
                    if isinstance(lexeme, Lexeme):
                        values.push(lexeme.iri)
        return q

    def _parse_get_lexeme_descriptor_results(
            self,
            results: SPARQL_Results,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, Text | None, Item | None, Item | None]]:
        if self.has_flags(self.LATE_FILTER):
            get_lemma = bool(mask & Descriptor.LEMMA)
            get_category = bool(mask & Descriptor.CATEGORY)
            get_language = bool(mask & Descriptor.LANGUAGE)
        else:
            get_lemma = True
            get_category = True
            get_language = True
        for entry in results.bindings:
            subject = entry.check_lexeme('subject')
            if get_lemma and 'lemma' in entry:
                lemma = entry.check_text('lemma')
            else:
                lemma = None
            if get_category and 'category' in entry:
                category = entry.check_item('category')
            else:
                category = None
            if get_language and 'language' in entry:
                language = entry.check_item('language')
            else:
                language = None
            yield subject, lemma, category, language
