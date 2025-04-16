# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import functools
import logging
import pathlib

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

        def ask(self, query: str) -> SPARQL_ResultsAsk:
            """Evaluates ask query over back-end.

            Parameters:
               query: Query string.

            Returns:
               Ask query results.
            """
            _logger.debug('%s()\n%s', self.ask.__qualname__, query)
            return self._ask(query)

        @abc.abstractmethod
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            raise NotImplementedError

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
        self._init_mapping(mapping, type(self), 'mapping')
        self._init_backend(backend, args, kwargs, type(self), 'backend')
        super().__init__(**kwargs)

    @override
    def _set_timeout(self, old: float | None, new: float | None) -> bool:
        self.backend._set_timeout(new)
        return True

# -- Backend ---------------------------------------------------------------

    #: SPARQL store backend.
    _backend: _SPARQL_Store.Backend

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
    _mapping: SPARQL_Mapping

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
        return self._mapping

# -- Statements ------------------------------------------------------------

    @override
    def _ask(self, filter: Filter) -> bool:
        compiler = self._compile_filter(filter)
        res = self.backend.ask(str(compiler.query.ask()))
        assert 'boolean' in res
        return res['boolean']

    @override
    def _count(self, filter: Filter) -> int:
        compiler = self._compile_filter(filter.replace(annotated=False))
        q = compiler.query
        q.order_by = None
        count = q.fresh_var()
        res = self.backend.select(str(q.select((q.count(), count))))
        assert 'results' in res
        assert 'bindings' in res['results']
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
        assert isinstance(compiler.pattern, VariablePattern)
        assert isinstance(compiler.pattern.variable, StatementVariable)
        assert limit >= 0
        page_size = min(self.page_size, limit)
        offset, count = 0, 0
        while count <= limit:
            query = compiler.build_query(
                limit=page_size, offset=offset, distinct=distinct)
            assert isinstance(compiler.pattern, VariablePattern)
            assert isinstance(compiler.pattern.variable, StatementVariable)
            if query.where_is_empty():
                break           # nothing to do
            res = self.backend.select(str(query))
            if 'results' not in res:
                break           # nothing to do
            bindings = res['results']['bindings']
            if not bindings:
                break           # done
            push = compiler.build_results()
            bindings_it: Iterator[SPARQL_ResultsBinding] =\
                itertools.chain(bindings, ({},))  # {} is the sentinel
            for binding in bindings_it:
                thetas = push(binding)
                if thetas is None:
                    continue    # push more results
                for theta in thetas:
                    stmt = compiler.pattern.variable.instantiate(theta)
                    assert isinstance(stmt, Statement), stmt
                    yield stmt
                    count += 1
            assert count <= limit, (count, limit)
            if count < page_size or count == limit:
                break           # done
            offset += page_size

    def _compile_filter(self, filter: Filter) -> SPARQL_FilterCompiler:
        compiler = SPARQL_FilterCompiler(
            filter, self.mapping, SPARQL_FilterCompiler.default_flags)
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
