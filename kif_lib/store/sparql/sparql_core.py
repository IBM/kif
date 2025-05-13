# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import asyncio
import functools
import logging
import pathlib
import threading

from ... import itertools, rdflib
from ...compiler.sparql import SPARQL_FilterCompiler, SPARQL_Mapping
from ...compiler.sparql.results import (
    SPARQL_Results,
    SPARQL_ResultsAsk,
    SPARQL_ResultsBinding,
)
from ...model import (
    Filter,
    Graph,
    KIF_Object,
    Statement,
    StatementVariable,
    TGraph,
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
    TextIO,
    TypeAlias,
    TypeVar,
    Union,
)
from ..abc import Store

T = TypeVar('T')

_logger: Final[logging.Logger] = logging.getLogger(__name__)
_py_filter = filter


class _SPARQL_Store(
        Store,
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
        _store: _SPARQL_Store

        def __init__(self, store: _SPARQL_Store) -> None:
            self._store = store

        def close(self) -> None:
            """Closes backend."""
            self._close()

        def _close(self) -> None:
            pass

        async def aclose(self) -> None:
            """Async version of :meth:`_SPARQL_Store.Backend.close()`."""
            await self._aclose()

        async def _aclose(self) -> None:
            pass

        def ask(self, query: str) -> SPARQL_ResultsAsk:
            """Evaluates ask query over back-end.

            Parameters:
               query: Query string.

            Returns:
               Ask query results.
            """
            _logger.debug('%s()\n%s', self.ask.__qualname__, query)
            return self._ask(query)

        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return cast(SPARQL_ResultsAsk, self._select(query))

        async def aask(self, query: str) -> SPARQL_ResultsAsk:
            """Async version of :meth:`_SPARQL_Store.Backend.ask`."""
            _logger.debug('%s()\n%s', self.aask.__qualname__, query)
            return await self._aask(query)

        async def _aask(self, query: str) -> SPARQL_ResultsAsk:
            return await asyncio.create_task(asyncio.to_thread(
                lambda: self._ask(query)))

        def select(self, query: str) -> SPARQL_Results:
            """Evaluates select query over back-end.

            Parameters:
               query: Query string.

            Returns:
               Select query results.
            """
            _logger.debug('%s()\n%s', self.select.__qualname__, query)
            return self._select(query)

        @abc.abstractmethod
        def _select(self, query: str) -> SPARQL_Results:
            raise NotImplementedError

        async def aselect(self, query: str) -> SPARQL_Results:
            """Async version of :meth:`_SPARQL_Store.Backend.select`."""
            _logger.debug('%s()\n%s', self.aselect.__qualname__, query)
            return await self._aselect(query)

        async def _aselect(self, query: str) -> SPARQL_Results:
            return await asyncio.create_task(asyncio.to_thread(
                lambda: self._select(query)))

        def _set_timeout(self, timeout: float | None = None) -> None:
            pass

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
                store: _SPARQL_Store,
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
            self._init(store, **kwargs)

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
                lambda s: isinstance(s, Statement), args))
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

        @abc.abstractmethod
        def _init(self, store: _SPARQL_Store, **kwargs: Any) -> None:
            raise NotImplementedError

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
                location: pathlib.PurePath | str,
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
            backend: type[_SPARQL_Store.Backend],
            *args: Any,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
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

    @override
    def _set_timeout(self, timeout: float | None) -> bool:
        self.backend._set_timeout(timeout)
        return True

# -- Backend ---------------------------------------------------------------

    #: SPARQL store backend.
    _backend: _SPARQL_Store.Backend | None

    def _init_backend(
            self,
            backend: type[_SPARQL_Store.Backend],
            args: Sequence[Any],
            kwargs: Mapping[str, Any],
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        backend = KIF_Object._check_arg_issubclass(
            backend, self.Backend, function, name, position)
        self._backend = backend(self, *args, **kwargs)

    @property
    def backend(self) -> _SPARQL_Store.Backend:
        """The backend of SPARQL store."""
        return self.get_backend()

    def get_backend(self) -> _SPARQL_Store.Backend:
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
    def _pubchem_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ...compiler.sparql.mapping.pubchem import PubChemMapping
        return PubChemMapping(*args, **kwargs)

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

# -- Statements ------------------------------------------------------------

    @override
    def _ask(self, filter: Filter) -> bool:
        query = self._build_ask_query_from_filter(filter)
        if query.where_is_nonempty():
            return self._parse_ask_results(
                self.backend.ask(str(query.ask())))
        else:
            return False

    @override
    async def _aask(self, filter: Filter) -> bool:
        query = self._build_ask_query_from_filter(filter)
        if query.where_is_nonempty():
            return self._parse_ask_results(
                await self.backend.aask(str(query.ask())))
        else:
            return False

    def _build_ask_query_from_filter(
            self,
            filter: Filter
    ) -> SPARQL_FilterCompiler.Query:
        compiler, _, _ = self._compile_filter(filter)
        return compiler.query

    def _parse_ask_results(self, results: SPARQL_ResultsAsk) -> bool:
        assert 'boolean' in results
        return results['boolean']

    @override
    def _count(self, filter: Filter) -> int:
        count, query = self._build_count_query_from_filter(filter)
        if query.where_is_nonempty():
            return self._parse_count_results(
                count, self.backend.select(str(query)))
        else:
            return 0

    @override
    async def _acount(self, filter: Filter) -> int:
        count, query = self._build_count_query_from_filter(filter)
        if query.where_is_nonempty():
            return self._parse_count_results(
                count, await self.backend.aselect(str(query)))
        else:
            return 0

    def _build_count_query_from_filter(
            self,
            filter: Filter
    ) -> tuple[SPARQL_FilterCompiler.Query.Variable,
               SPARQL_FilterCompiler.Query]:
        compiler, _, _ = self._compile_filter(
            filter.replace(annotated=False))
        q = compiler.query
        count = q.fresh_var()
        return count, q.select((q.count(), count))  # type: ignore

    def _parse_count_results(
            self,
            count: SPARQL_FilterCompiler.Query.Variable,
            results: SPARQL_Results
    ) -> int:
        assert 'results' in results
        assert 'bindings' in results['results']
        assert len(results['results']['bindings']) == 1
        return int(results['results']['bindings'][0][str(count)]['value'])

    @override
    def _filter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Statement]:
        compiler, _, variable = self._compile_filter(filter)
        push = compiler.build_results()
        if options.limit is not None:
            limit = options.limit
        else:
            limit = options.max_limit
        query_stream = self._build_filter_query_stream(
            compiler, options.distinct, limit, options.page_size)
        count = 0
        for query in query_stream:
            bindings = list(self._build_filter_result_binding_stream((
                self.backend.select(str(query)),)))
            for binding in itertools.chain(bindings, ({},)):
                if not bindings:
                    return      # done
                thetas = push(binding)
                if thetas is None:
                    continue    # push more results
                for theta in thetas:
                    stmt = variable.instantiate(theta)
                    assert isinstance(stmt, Statement), stmt
                    yield stmt
                    count += 1
                    assert count <= limit, (count, limit)
                    if count == limit:
                        return  # done
            if count < options.page_size:
                break           # done

    @override
    async def _afilter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Statement]:
        compiler, _, variable = self._compile_filter(filter)
        push = compiler.build_results()
        if options.limit is not None:
            limit = options.limit
        else:
            limit = options.max_limit
        query_stream = self._build_filter_query_stream(
            compiler, options.distinct, limit, options.page_size)
        count = 0
        for batch in itertools.batched(query_stream, self.lookahead):
            tasks = (
                asyncio.ensure_future(self.backend.aselect(str(q)))
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
                    assert isinstance(stmt, Statement), stmt
                    yield stmt
                    count += 1
                    assert count <= limit, (count, limit)
                    if count == limit:
                        return  # done
            if count % self.page_size != 0:
                break           # done

    def _compile_filter(self, filter: Filter) -> tuple[
            SPARQL_FilterCompiler, VariablePattern, StatementVariable]:
        compiler = SPARQL_FilterCompiler(
            filter, self.mapping, SPARQL_FilterCompiler.default_flags)
        if self.debug:
            compiler.set_flags(compiler.DEBUG)
        if self.best_ranked:
            compiler.set_flags(compiler.BEST_RANK)
        else:
            compiler.unset_flags(compiler.BEST_RANK)
        compiler.compile()
        assert isinstance(compiler.pattern, VariablePattern)
        assert isinstance(compiler.pattern.variable, StatementVariable)
        return compiler, compiler.pattern, compiler.pattern.variable

    def _build_filter_query_stream(
            self,
            compiler: SPARQL_FilterCompiler,
            distinct: bool,
            limit: int,
            page_size: int
    ) -> Iterator[SPARQL_FilterCompiler.Query]:
        query_stream = self._build_filter_query_stream_tail(
            compiler, distinct, limit, page_size)
        for query in query_stream:
            if query.where_is_empty():
                break
            yield query

    def _build_filter_query_stream_tail(
            self,
            compiler: SPARQL_FilterCompiler,
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
                        distinct=distinct, limit=remaining, offset=offset)
                    break
                yield compiler.build_query(
                    distinct=distinct, limit=page_size, offset=offset)

    def _build_filter_result_binding_stream(
            self,
            results: Iterable[SPARQL_Results]
    ) -> Iterable[SPARQL_ResultsBinding]:
        for result in results:
            try:
                yield from result['results']['bindings']  # type: ignore
            except KeyError:
                pass
