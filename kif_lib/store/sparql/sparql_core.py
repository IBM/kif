# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import asyncio
import logging
import pathlib
import threading

from ... import functools, itertools, rdflib
from ...compiler.sparql import SPARQL_FilterCompiler, SPARQL_Mapping
from ...compiler.sparql.results import (
    SPARQL_Results,
    SPARQL_ResultsAsk,
    SPARQL_ResultsBinding,
)
from ...model import (
    ClosedTerm,
    Entity,
    Filter,
    Graph,
    KIF_Object,
    Property,
    Snak,
    SnakTemplate,
    Statement,
    StatementTemplate,
    StatementVariable,
    Term,
    TGraph,
    Value,
    ValuePair,
    ValueSnak,
    ValueSnakTemplate,
    VariablePattern,
)
from ...typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Callable,
    cast,
    Final,
    Iterable,
    Iterator,
    Location,
    Mapping,
    override,
    Sequence,
    Set,
    TextIO,
    TypeAlias,
    TypeVar,
    Union,
)
from ..abc import Store, StoreOptions, TOptions

_TOptions = TypeVar('_TOptions', bound=StoreOptions)
T = TypeVar('T')
TLocation: TypeAlias = Union[pathlib.PurePath, str]

_logger: Final[logging.Logger] = logging.getLogger(__name__)
_py_filter = filter


class _CoreSPARQL_Store(
        Store[TOptions],
        store_name='_sparql',
        store_description='SPARQL store (core)'
):
    """SPARQL store (core).

    Parameters:
       store_name: Name of the store plugin to instantiate.
       backend: SPARQL store backend.
       mapping: SPARQL mapping.
       args: Other arguments.
       kwargs: Other keyword arguments.
    """

    class Backend(abc.ABC):
        """SPARQL store back-end.

        Parameters:
           store: Parent SPARQL store.
        """

        __slots__ = (
            '_store',
        )

        #: The parent SPARQL store.
        _store: _CoreSPARQL_Store

        def __init__(self, store: _CoreSPARQL_Store[_TOptions]) -> None:
            self._store = store  # type: ignore

        def close(self) -> None:
            """Closes backend."""
            self._close()

        def _close(self) -> None:
            pass

        async def aclose(self) -> None:
            """Async version of :meth:`_CoreSPARQL_Store.Backend.close()`."""
            await self._aclose()

        async def _aclose(self) -> None:
            pass

        def ask(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_ResultsAsk:
            """Evaluates ask query over back-end.

            Parameters:
               query: Query string.
               timeout: Timeout.

            Returns:
               Ask query results.
            """
            _logger.debug('%s()\n%s', self.ask.__qualname__, query)
            return self._ask(query)

        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return cast(SPARQL_ResultsAsk, self._select(query))

        async def aask(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_ResultsAsk:
            """Async version of :meth:`_CoreSPARQL_Store.Backend.ask`."""
            _logger.debug('%s()\n%s', self.aask.__qualname__, query)
            return await self._aask(query)

        async def _aask(self, query: str) -> SPARQL_ResultsAsk:
            return await asyncio.create_task(asyncio.to_thread(
                lambda: self._ask(query)))

        def select(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_Results:
            """Evaluates select query over back-end.

            Parameters:
               query: Query string.
               timeout: Timeout.

            Returns:
               Select query results.
            """
            _logger.debug('%s()\n%s', self.select.__qualname__, query)
            return self._select(query, timeout)

        @abc.abstractmethod
        def _select(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_Results:
            raise NotImplementedError

        async def aselect(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_Results:
            """Async version of :meth:`_CoreSPARQL_Store.Backend.select`."""
            _logger.debug('%s()\n%s', self.aselect.__qualname__, query)
            return await self._aselect(query, timeout)

        async def _aselect(
                self,
                query: str,
                timeout: float | None = None
        ) -> SPARQL_Results:
            return await asyncio.create_task(asyncio.to_thread(
                lambda: self._select(query, timeout)))

    class LocalBackend(Backend):
        """Abstract base class for local backends.

        Parameters:
           store: Parent SPARQL store.
           args: Input sources, files, paths, strings, or statements.
           format: Input source format (file extension or media type).
           location: Relative or absolute URL of the input source.
           file: File-like object to be used as input source.
           data: Data to be used as input source.
           graph: KIF graph to used as input source.
           rdflib_graph: RDFLib graph to be used as input source.
           skolemize: Whether to skolemize the resulting graph.
           kwargs: Other keyword arguments.
        """

        #: Type alias for local backend arguments.
        Args: TypeAlias = Union[
            BinaryIO, TextIO, rdflib.InputSource,
            str, bytes, pathlib.PurePath, Statement]

        __slots__ = (
            '_lock',
        )

        #: Reentrant lock to sync access shared resources.
        _lock: threading.RLock

        def __init__(
                self,
                store: _CoreSPARQL_Store[_TOptions],
                *args: Args,
                format: str | None = None,
                location: str | None = None,
                file: BinaryIO | TextIO | None = None,
                data: bytes | str | None = None,
                graph: TGraph | None = None,
                rdflib_graph: rdflib.Graph | None = None,
                skolemize: bool | None = None,
                **kwargs: Any
        ) -> None:
            super().__init__(store)
            self._lock = threading.RLock()
            self._pre_init(store, **kwargs)

            def load(name: str | None, f: Callable[[T], None], x: T) -> None:
                try:
                    f(x)
                except Exception as err:
                    raise KIF_Object._arg_error(
                        str(err), type(store), name,
                        exception=store.Error) from err
            _load_arg = functools.partial(self._load_arg, format=format)
            _load_location = functools.partial(
                self._load_location, format=format)
            _load_file = functools.partial(self._load_file, format=format)
            _load_data = functools.partial(self._load_data, format=format)
            if location is not None:
                load('location', _load_location, location)
            if file is not None:
                load('file', _load_file, file)
            if data is not None:
                load('data', _load_data, data)
            if graph is not None:
                load('graph', self._load_graph,
                     Graph.check(graph, type(store), 'graph'))
            other, stmts = map(list, itertools.partition(
                Statement.test, args))
            if stmts:
                load('graph', self._load_graph,
                     Graph(*cast(Iterable[Statement], stmts)))
            if rdflib_graph is not None:
                load('rdflib_graph', self._load_rdflib_graph, rdflib_graph)
            for src in other:
                load('args', _load_arg, src)
            skolemize = skolemize if skolemize is not None else True
            if skolemize:
                self._skolemize()
            self._post_init(store)

        @abc.abstractmethod
        def _pre_init(
                self,
                store: _CoreSPARQL_Store[_TOptions],
                **kwargs: Any
        ) -> None:
            raise NotImplementedError

        def _post_init(
                self,
                store: _CoreSPARQL_Store[_TOptions]
        ) -> None:
            pass

        def _load_arg(self, arg: Args, format: str | None = None) -> None:
            if isinstance(arg, (pathlib.PurePath, str)):
                self._load_location(arg, format)
            elif isinstance(arg, (BinaryIO, TextIO)):
                self._load_file(arg, format)
            elif isinstance(arg, bytes):
                self._load_data(arg, format)
            elif isinstance(arg, Graph):
                self._load_graph(arg)
            elif isinstance(arg, rdflib.Graph):
                self._load_rdflib_graph(arg)
            else:
                self._load_arg_unknown(arg, format)

        def _load_arg_unknown(
                self,
                arg: Any,
                format: str | None = None
        ) -> None:
            raise TypeError(
                f'{type(self).__qualname__} does not support '
                f'{type(arg).__qualname__}')

        def _load_location(
                self,
                location: TLocation,
                format: str | None = None
        ) -> None:
            self._load_arg_unknown(location, format)

        def _load_file(
                self,
                file: BinaryIO | TextIO,
                format: str | None = None
        ) -> None:
            self._load_arg_unknown(file, format)

        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            self._load_arg_unknown(data, format)

        def _load_graph(self, graph: Graph) -> None:
            self._load_data(graph.to_rdf(), 'n3')

        def _load_rdflib_graph(self, rdflib_graph: rdflib.Graph) -> None:
            self._load_data(rdflib_graph.serialize(), 'n3')

        @abc.abstractmethod
        def _skolemize(self) -> None:
            raise NotImplementedError

    __slots__ = (
        '_backend',
        '_mapping',
    )

    def __init__(
            self,
            store_name: str,
            mapping: SPARQL_Mapping,
            backend: type[_CoreSPARQL_Store.Backend],
            *args: Any,
            **kwargs: Any
    ) -> None:
        self._mapping = None
        self._init_mapping(mapping, type(self), 'mapping')
        self._backend = None
        self._init_backend(backend, args, kwargs, type(self), 'backend')
        super().__init__(store_name, **kwargs)

    @override
    def _close(self) -> None:
        if self._backend is not None:
            self.backend.close()

    @override
    async def _aclose(self) -> None:
        if self._backend is not None:
            await self.backend.aclose()

# -- Backend ---------------------------------------------------------------

    #: SPARQL store backend.
    _backend: _CoreSPARQL_Store.Backend | None

    def _init_backend(
            self,
            backend: type[_CoreSPARQL_Store.Backend],
            args: Sequence[Any],
            kwargs: Mapping[str, Any],
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        backend = KIF_Object._check_arg_issubclass(
            backend, self.Backend, function, name, position)
        self._backend = backend(self, *args, **kwargs)  # type: ignore

    @property
    def backend(self) -> _CoreSPARQL_Store.Backend:
        """The backend of SPARQL store."""
        return self.get_backend()

    def get_backend(self) -> _CoreSPARQL_Store.Backend:
        """Gets the backend of SPARQL store.

        Returns:
           SPARQL store backend.
        """
        assert self._backend is not None
        return self._backend

# -- SPARQL mapping --------------------------------------------------------

    @classmethod
    def _check_mapping(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> SPARQL_Mapping:
        return KIF_Object._check_arg_isinstance(
            arg, SPARQL_Mapping, function, name, position)

    @classmethod
    def _check_optional_mapping(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> SPARQL_Mapping | None:
        return cls._do_check_optional(  # pragma: no cover
            cls._check_mapping, arg, default, function, name, position)

    @classmethod
    def _do_check_optional(
            cls,
            check: Callable[
                [Any, Location | None, str | None, int | None], T],
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> T | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return check(arg, function, name, position)

    @classmethod
    def _dbpedia_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.dbpedia import DBpediaMapping
        return DBpediaMapping(*args, **kwargs)

    @classmethod
    def _europa_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.europa import EuropaMapping
        return EuropaMapping(*args, **kwargs)

    @classmethod
    def _factgrid_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.factgrid import FactGridMapping
        return FactGridMapping(*args, **kwargs)

    @classmethod
    def _pubchem_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.pubchem import PubChemMapping
        return PubChemMapping(*args, **kwargs)

    @classmethod
    def _uniprot_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.uniprot import UniProtMapping
        return UniProtMapping(*args, **kwargs)

    @classmethod
    def _wikidata_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.wikidata import WikidataMapping
        return WikidataMapping(*args, **kwargs)

    #: SPARQL mapping.
    _mapping: SPARQL_Mapping | None

    def _init_mapping(
            self,
            mapping: SPARQL_Mapping | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        self._mapping = self._check_mapping(
            mapping, function, name, position)

    @property
    def mapping(self) -> SPARQL_Mapping:
        """The mapping of SPARQL store."""
        return self.get_mapping()

    def get_mapping(self) -> SPARQL_Mapping:
        """Gets the mapping of SPARQL store.

        Returns:
           SPARQL mapping.
        """
        assert self._mapping is not None
        return self._mapping

# -- Ask -------------------------------------------------------------------

    @override
    def _ask(self, filter: Filter, options: TOptions) -> bool:
        it = self._build_ask_query_stream_from_filter(filter, options)
        return any(
            self._parse_ask_results(self.backend.ask(str(query.ask())))
            for query in it)

    @override
    async def _aask(self, filter: Filter, options: TOptions) -> bool:
        it = list(self._build_ask_query_stream_from_filter(filter, options))
        tasks = (
            asyncio.ensure_future(self.backend.aask(str(query.ask())))
            for query in it)
        return any(
            self._parse_ask_results(results)
            for results in await asyncio.gather(*tasks))

    def _build_ask_query_stream_from_filter(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[SPARQL_FilterCompiler.Query]:
        compiler, _, _ = self._compile_filter(
            filter, options, SPARQL_FilterCompiler.Projection.ALL)
        yield from compiler.query_stack

    def _parse_ask_results(self, results: SPARQL_ResultsAsk) -> bool:
        assert 'boolean' in results
        return results['boolean']

# -- Count -----------------------------------------------------------------

    @override
    def _count(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.ALL)

    @override
    def _count_s(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.SUBJECT)

    @override
    def _count_p(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.PROPERTY)

    @override
    def _count_v(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.VALUE)

    @override
    def _count_sp(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.SUBJECT
            | SPARQL_FilterCompiler.Projection.PROPERTY)

    @override
    def _count_sv(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.SUBJECT
            | SPARQL_FilterCompiler.Projection.VALUE)

    @override
    def _count_pv(self, filter: Filter, options: TOptions) -> int:
        return self._count_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.PROPERTY
            | SPARQL_FilterCompiler.Projection.VALUE)

    def _count_with_projection(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection
    ) -> int:
        it = self._build_count_query_stream_from_filter(
            filter, options, projection)
        return sum(
            self._parse_count_results(
                count, self.backend.select(str(query), options.timeout))
            for count, query in it)

    @override
    async def _acount(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.ALL)

    @override
    async def _acount_s(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.SUBJECT)

    @override
    async def _acount_p(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.PROPERTY)

    @override
    async def _acount_v(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.VALUE)

    @override
    async def _acount_sp(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.SUBJECT
            | SPARQL_FilterCompiler.Projection.PROPERTY)

    @override
    async def _acount_sv(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.SUBJECT
            | SPARQL_FilterCompiler.Projection.VALUE)

    @override
    async def _acount_pv(self, filter: Filter, options: TOptions) -> int:
        return await self._acount_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.PROPERTY
            | SPARQL_FilterCompiler.Projection.VALUE)

    async def _acount_with_projection(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection
    ) -> int:
        it = list(self._build_count_query_stream_from_filter(
            filter, options, projection))
        tasks = (
            asyncio.ensure_future(
                self.backend.aselect(str(query), options.timeout))
            for _, query in it)
        return sum(
            self._parse_count_results(count, results)
            for (count, _), results in zip(
                it, await asyncio.gather(*tasks)))

    def _build_count_query_stream_from_filter(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection
    ) -> Iterator[tuple[SPARQL_FilterCompiler.Query.Variable,
                        SPARQL_FilterCompiler.Query]]:
        compiler, _, _ = self._compile_filter(
            filter.replace(annotated=False), options, projection)
        for disjoint_query in compiler.query_stack:
            try:
                q = next(self._build_filter_query_stream(
                    compiler, disjoint_query, projection, True, 1, 1))
            except StopIteration as err:
                raise self._should_not_get_here() from err
            q.set_limit(None)
            q.set_offset(None)
            count = compiler.fresh_qvar()
            query = compiler.Query()
            query.subquery(q)()
            yield count, query.select((q.count(), count))  # type: ignore

    def _parse_count_results(
            self,
            count: SPARQL_FilterCompiler.Query.Variable,
            results: SPARQL_Results
    ) -> int:
        assert 'results' in results
        assert 'bindings' in results['results']
        assert len(results['results']['bindings']) == 1
        return int(results['results']['bindings'][0][str(count)]['value'])

# -- Filter ----------------------------------------------------------------

    @override
    def _filter(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Statement]:
        return cast(Iterator[Statement], self._filter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.ALL))

    @override
    def _filter_s(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Entity]:
        return cast(Iterator[Entity], self._filter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.SUBJECT))

    @override
    def _filter_p(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Property]:
        return cast(Iterator[Property], self._filter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.PROPERTY))

    @override
    def _filter_v(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Value]:
        return cast(Iterator[Value], self._filter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.VALUE))

    @override
    def _filter_sp(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Property]]:
        return cast(
            Iterator[ValuePair[Entity, Property]],
            self._filter_with_projection(
                filter, options,
                SPARQL_FilterCompiler.Projection.SUBJECT
                | SPARQL_FilterCompiler.Projection.PROPERTY))

    @override
    def _filter_sv(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValuePair[Entity, Value]]:
        return cast(
            Iterator[ValuePair[Entity, Value]],
            self._filter_with_projection(
                filter, options,
                SPARQL_FilterCompiler.Projection.SUBJECT
                | SPARQL_FilterCompiler.Projection.VALUE))

    @override
    def _filter_pv(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[ValueSnak]:
        return cast(Iterator[ValueSnak], self._filter_with_projection(
            filter, options,
            SPARQL_FilterCompiler.Projection.PROPERTY
            | SPARQL_FilterCompiler.Projection.VALUE))

    def _filter_with_projection(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection
    ) -> Iterator[ClosedTerm]:
        compiler, _, variable = self._compile_filter(
            filter, options, projection)
        push = compiler.build_results()
        select = functools.partial(
            self._filter_with_projection_select, compiler, projection)
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        assert limit is not None
        timeout = options.timeout
        total_count = 0

        def process(
                disjoint_query: SPARQL_FilterCompiler.Query
        ) -> Iterator[ClosedTerm]:
            stream = self._build_filter_query_stream(
                compiler, disjoint_query, projection,
                options.distinct, limit, options.page_size)
            nonlocal total_count
            count = 0
            for query in stream:
                bindings = list(self._build_filter_result_binding_stream((
                    self.backend.select(str(query), timeout),)))
                for binding in itertools.chain(bindings, ({},)):
                    if not bindings:
                        return      # done
                    thetas = push(binding)
                    if thetas is None:
                        continue    # push more results
                    for theta in thetas:
                        stmt = variable.instantiate(theta)
                        assert isinstance(stmt, (Statement, StatementTemplate))
                        yield select(stmt)
                        count += 1
                        total_count += 1
                        assert total_count <= limit, (count, limit)
                        if total_count == limit:
                            return  # done
                if count < options.page_size:
                    break           # done
        return itertools.chain(*map(process, compiler.query_stack))

    def _filter_with_projection_select(
            self,
            compiler: SPARQL_FilterCompiler,
            projection: SPARQL_FilterCompiler.Projection,
            stmt: Statement | StatementTemplate,
    ) -> ClosedTerm:
        if projection == compiler.Projection.ALL:
            term: Term = stmt
        elif projection == compiler.Projection.SUBJECT:
            term = stmt.subject
        elif projection == compiler.Projection.PROPERTY:
            assert isinstance(
                stmt.snak, (Snak, SnakTemplate)), stmt.snak
            term = stmt.snak.property
        elif projection == compiler.Projection.VALUE:
            assert isinstance(
                stmt.snak, (ValueSnak, ValueSnakTemplate)), stmt.snak
            term = stmt.snak.value
        elif projection == (
                compiler.Projection.SUBJECT | compiler.Projection.PROPERTY):
            assert isinstance(stmt.subject, Entity), stmt.subject
            assert isinstance(stmt.snak, (Snak, SnakTemplate))
            assert isinstance(
                stmt.snak.property, Property), stmt.snak.property
            term = ValuePair(stmt.subject, stmt.snak.property)
        elif projection == (
                compiler.Projection.SUBJECT | compiler.Projection.VALUE):
            assert isinstance(
                stmt.snak, (ValueSnak, ValueSnakTemplate)), stmt.snak
            assert isinstance(stmt.subject, Entity)
            assert isinstance(stmt.snak.value, Value)
            term = ValuePair(stmt.subject, stmt.snak.value)
        elif projection == (
                compiler.Projection.PROPERTY | compiler.Projection.VALUE):
            assert isinstance(
                stmt.snak, (ValueSnak, ValueSnakTemplate)), stmt.snak
            term = stmt.snak
        else:
            raise self._should_not_get_here()
        assert isinstance(term, ClosedTerm), term
        return term

    @override
    def _afilter(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Statement]:
        return cast(AsyncIterator[Statement], self._afilter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.ALL))

    @override
    def _afilter_s(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Entity]:
        return cast(AsyncIterator[Entity], self._afilter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.SUBJECT))

    @override
    def _afilter_p(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Property]:
        return cast(AsyncIterator[Property], self._afilter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.PROPERTY))

    @override
    def _afilter_v(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Value]:
        return cast(AsyncIterator[Value], self._afilter_with_projection(
            filter, options, SPARQL_FilterCompiler.Projection.VALUE))

    @override
    def _afilter_sp(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Property]]:
        return cast(
            AsyncIterator[ValuePair[Entity, Property]],
            self._afilter_with_projection(
                filter, options,
                SPARQL_FilterCompiler.Projection.SUBJECT
                | SPARQL_FilterCompiler.Projection.PROPERTY))

    @override
    def _afilter_sv(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValuePair[Entity, Value]]:
        return cast(
            AsyncIterator[ValuePair[Entity, Value]],
            self._afilter_with_projection(
                filter, options,
                SPARQL_FilterCompiler.Projection.SUBJECT
                | SPARQL_FilterCompiler.Projection.VALUE))

    @override
    def _afilter_pv(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[ValueSnak]:
        return cast(
            AsyncIterator[ValueSnak],
            self._afilter_with_projection(
                filter, options,
                SPARQL_FilterCompiler.Projection.PROPERTY
                | SPARQL_FilterCompiler.Projection.VALUE))

    async def _afilter_with_projection(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection
    ) -> AsyncIterator[ClosedTerm]:
        compiler, _, variable = self._compile_filter(
            filter, options, projection)
        push = compiler.build_results()
        select = functools.partial(
            self._filter_with_projection_select, compiler, projection)
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        assert limit is not None
        timeout = options.timeout
        total_count = 0

        async def aprocess(
                disjoint_query: SPARQL_FilterCompiler.Query
        ) -> AsyncIterator[ClosedTerm]:
            stream = self._build_filter_query_stream(
                compiler, disjoint_query, projection,
                options.distinct, limit, options.page_size)
            nonlocal total_count
            count = 0
            for batch in itertools.batched(stream, self.lookahead):
                tasks = (
                    asyncio.ensure_future(self.backend.aselect(
                        str(q), timeout))
                    for q in batch)
                bindings = list(self._build_filter_result_binding_stream(
                    await asyncio.gather(*tasks)))
                if not bindings:
                    break           # done
                for binding in itertools.chain(bindings, ({},)):
                    thetas = push(binding)
                    if thetas is None:
                        continue    # push more results
                    for theta in thetas:
                        stmt = variable.instantiate(theta)
                        assert isinstance(stmt, (Statement, StatementTemplate))
                        yield select(stmt)
                        count += 1
                        total_count += 1
                        assert total_count <= limit, (count, limit)
                        if total_count == limit:
                            return  # done
                if count % self.page_size != 0:
                    break           # done
        async for term in itertools.achain(*map(
                aprocess, compiler.query_stack)):
            yield term

    def _compile_filter(
            self,
            filter: Filter,
            options: TOptions,
            projection: SPARQL_FilterCompiler.Projection,
            _projection_v_sv_pv: Set[SPARQL_FilterCompiler.Projection] = {
                SPARQL_FilterCompiler.Projection.VALUE,
                (SPARQL_FilterCompiler.Projection.SUBJECT
                 | SPARQL_FilterCompiler.Projection.VALUE),
                (SPARQL_FilterCompiler.Projection.PROPERTY
                 | SPARQL_FilterCompiler.Projection.VALUE),
            }
    ) -> tuple[
            SPARQL_FilterCompiler, VariablePattern, StatementVariable]:
        assert projection.value != 0
        if projection in _projection_v_sv_pv:
            ###
            # If we're projecting on value, there's no need to consider
            # some- or no-value snaks.
            ###
            assert filter.snak_mask & Filter.VALUE_SNAK
            filter = filter.replace(snak_mask=Filter.VALUE_SNAK)
        compiler = SPARQL_FilterCompiler(
            filter, self.mapping, debug=options.debug, omega=options.omega)
        compiler.compile()
        assert isinstance(compiler.pattern, VariablePattern)
        assert isinstance(compiler.pattern.variable, StatementVariable)
        return compiler, compiler.pattern, compiler.pattern.variable

    def _build_filter_query_stream(
            self,
            compiler: SPARQL_FilterCompiler,
            query: SPARQL_FilterCompiler.Query,
            projection: SPARQL_FilterCompiler.Projection,
            distinct: bool,
            limit: int,
            page_size: int
    ) -> Iterator[SPARQL_FilterCompiler.Query]:
        assert limit >= 0
        if limit > 0:
            page_size = min(page_size, limit)
            for offset in range(0, limit, page_size):
                remaining = limit - offset
                if remaining < page_size:
                    yield compiler.build_query(
                        query=query,
                        projection=projection,
                        distinct=distinct,
                        limit=remaining,
                        offset=offset)
                    break
                yield compiler.build_query(
                    query=query,
                    projection=projection,
                    distinct=distinct,
                    limit=page_size,
                    offset=offset)

    def _build_filter_result_binding_stream(
            self,
            results: Iterable[SPARQL_Results]
    ) -> Iterator[SPARQL_ResultsBinding]:
        for result in results:
            try:
                yield from result['results']['bindings']  # type: ignore
            except KeyError:
                pass


TCoreSPARQL_Store: TypeAlias = _CoreSPARQL_Store[_TOptions]
