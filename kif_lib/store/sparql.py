# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import functools
import json
import logging
import pathlib
import re

import httpx

from .. import itertools, rdflib
from ..compiler.sparql import SPARQL_FilterCompiler, SPARQL_Mapping
from ..compiler.sparql.results import (
    SPARQL_Results,
    SPARQL_ResultsAsk,
    SPARQL_ResultsBinding,
)
from ..model import (
    Filter,
    Graph,
    IRI,
    KIF_Object,
    Statement,
    StatementVariable,
    T_IRI,
    TGraph,
    VariablePattern,
)
from ..typing import (
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
from ..version import __version__
from . import jena
from .abc import Store
from .mixer import MixerStore

T = TypeVar('T')

LOG = logging.getLogger(__name__)


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
       args: Backend arguments.
       kwargs: Backend keyword arguments.
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
            LOG.debug('%s()\n%s', self.ask.__qualname__, query)
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
            LOG.debug('%s()\n%s', self.select.__qualname__, query)
            return self._select(query)

        @abc.abstractmethod
        def _select(self, query: str) -> SPARQL_Results:
            raise NotImplementedError

        def _set_timeout(self, timeout: float | None = None) -> None:
            pass

    class HttpxBackend(Backend):
        """Httpx backend.

        Parameters:
           store: Parent SPARQL store.
           iri: IRI of the target SPARQL endpoint.
           headers: HTTP headers.
           kwargs: Other keyword arguments (ignored).
        """

        HTTP_Headers: TypeAlias = Mapping[str, str]

        _default_headers: Final[HTTP_Headers] = {
            ###
            # See <https://meta.wikimedia.org/wiki/User-Agent_policy>.
            ###
            'User-Agent': f'KIF/{__version__} (https://github.com/IBM/kif/)',
            'Content-Type': 'application/sparql-query;charset=utf-8',
            'Accept': 'application/sparql-results+json;charset=utf-8',
        }

        __slots__ = (
            '_client',
            '_headers',
            '_iri',
        )

        #: HTTP client.
        _client: httpx.Client | None

        #: HTTP headers.
        _headers: HTTP_Headers

        #: IRI of the target SPARQL endpoint.
        _iri: IRI

        def __init__(
                self,
                store: _SPARQL_Store,
                iri: T_IRI,
                *,
                headers: HTTP_Headers | None = None,
                **kwargs: Any
        ) -> None:
            super().__init__(store)
            self._client = None
            self._iri = IRI.check(iri, type(store), 'iri')
            try:
                self._headers = cast(_SPARQL_Store.HttpxBackend.HTTP_Headers, {
                    **dict(self._default_headers),
                    **dict(headers or {})
                })
            except Exception as err:
                raise KIF_Object._arg_error(
                    str(err), type(store), 'headers', exception=store.Error)
            self._client = httpx.Client(headers=self._headers)

        def __del__(self) -> None:
            if self._client is not None:
                self._client.close()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return cast(SPARQL_ResultsAsk, self._select(query))

        @override
        def _select(self, query: str) -> SPARQL_Results:
            return self._http_post(query).json()

        def _http_post(self, text: str) -> httpx.Response:
            assert self._client is not None
            try:
                res = self._client.post(
                    self._iri.content, content=text.encode('utf-8'))
                res.raise_for_status()
                return res
            except httpx.RequestError as err:
                raise err

        @override
        def _set_timeout(self, timeout: float | None = None) -> None:
            if self._client is not None:
                self._client.timeout = httpx.Timeout(timeout)

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

    class JenaBackend(LocalBackend):
        """Jena backend.

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
           kwargs: Other keyword arguments (ignored).
        """

        __slots__ = (
            '_jena',
        )

        #: Jena handle.
        _jena: jena.Jena

        @override
        def _init(
                self,
                store: _SPARQL_Store,
                **kwargs: Any
        ) -> None:
            jena_home = IRI.check_optional(
                kwargs.get('jena_home'), None, type(store), 'jena_home')
            try:
                self._jena = jena.Jena(
                    jena_home.content if jena_home is not None else None)
            except BaseException as err:
                raise store._error(
                    f'failed to create Jena backend ({err})') from err

        @override
        def _load_location(
                self,
                location: pathlib.PurePath | str,
                format: str | None = None
        ) -> None:
            self._jena.load(location, format)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            self._jena.loads(data, format)

        @override
        def _skolemize(self) -> None:
            self._jena.skolemize()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return {'boolean': cast(bool, self._jena.query(query))}

        @override
        def _select(self, query: str) -> SPARQL_Results:
            return cast(SPARQL_Results, self._jena.query(query))

    class RDFLibBackend(LocalBackend):
        """RDFLib backend.

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
           kwargs: Other keyword arguments (ignored).
        """

        __slots__ = (
            '_rdflib_graph',
        )

        #: RDFLib graph.
        _rdflib_graph: rdflib.Graph

        def _init(
                self,
                store: _SPARQL_Store,
                **kwargs: Any
        ) -> None:
            self._rdflib_graph = rdflib.Graph()

        @override
        def _load_arg_unknown(
                self,
                arg: Any,
                format: str | None = None
        ) -> None:
            self._rdflib_graph.parse(arg, format=format)  # type: ignore

        @override
        def _load_location(
                self,
                location: pathlib.PurePath | str,
                format: str | None = None
        ) -> None:
            self._rdflib_graph.parse(location=str(location), format=format)

        @override
        def _load_file(
                self,
                file: BinaryIO | TextIO,
                format: str | None = None
        ) -> None:
            self._rdflib_graph.parse(file=file, format=format)

        @override
        def _load_data(
                self,
                data: bytes | str,
                format: str | None = None
        ) -> None:
            self._rdflib_graph.parse(data=data, format=format)

        @override
        def _skolemize(self) -> None:
            self._rdflib_graph = self._rdflib_graph.skolemize()

        @override
        def _ask(self, query: str) -> SPARQL_ResultsAsk:
            return cast(SPARQL_ResultsAsk, self._select(query))

        @override
        def _select(self, query: str) -> SPARQL_Results:
            return json.loads(cast(bytes, self._rdflib_graph.query(
                query).serialize(format='json')))

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
        from ..compiler.sparql.mapping.dbpedia import DBpediaMapping
        return DBpediaMapping(*args, **kwargs)

    @classmethod
    def _pubchem_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ..compiler.sparql.mapping.pubchem import PubChemMapping
        return PubChemMapping(*args, **kwargs)

    @classmethod
    def _wikidata_mapping_constructor(
            cls,
            *args: Any,
            **kwargs: Any
    ) -> SPARQL_Mapping:
        from ..compiler.sparql.mapping.wikidata import WikidataMapping
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


# == Httpx SPARQL store ====================================================

class HttpxSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-httpx',
        store_description='SPARQL store with httpx backend'
):
    """SPARQL store with httpx backend.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       iri: IRI of the target SPARQL endpoint.
       headers: HTTP headers.
       mapping: SPARQL mapping.
       kwargs: Extra keyword arguments.
    """

    def __init__(
            self,
            store_name: str,
            iri: T_IRI,
            headers: _SPARQL_Store.HttpxBackend.HTTP_Headers | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(
            store_name,
            (mapping if mapping is not None
             else self._wikidata_mapping_constructor()),
            self.HttpxBackend, iri=iri, headers=headers, **kwargs)


# == Jena SPARQL store =====================================================

class JenaSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-jena',
        store_description='SPARQL store with Jena backend'
):
    """SPARQL store with Jena backend.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources, files, paths, strings, or statements.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Other keyword arguments.
    """

    #: Type alias for Jena SPARQL store arguments.
    Args: TypeAlias = _SPARQL_Store.JenaBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(
            store_name,
            (mapping if mapping is not None
             else self._wikidata_mapping_constructor()),
            self.JenaBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)


# == RDFLib SPARQL store ===================================================

class RDFLibSPARQL_Store(
        _SPARQL_Store,
        store_name='sparql-rdflib',
        store_description='SPARQL store with RDFLib backend'
):
    """SPARQL store with RDFLib backend.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources, files, paths, strings, or statements.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Other keyword arguments.
    """

    #: Type alias for RDFLib SPARQL store arguments.
    Args: TypeAlias = _SPARQL_Store.RDFLibBackend.Args

    def __init__(
            self,
            store_name: str,
            *args: Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(
            store_name,
            (mapping if mapping is not None
             else self._wikidata_mapping_constructor()),
            self.RDFLibBackend, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize, **kwargs)


class RDF_Store(
        RDFLibSPARQL_Store,
        store_name='rdf',
        store_description='RDF store'
):
    """RDF store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources, files, paths, strings, or statements.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Extra keyword arguments.
    """


class DBpediaRDF_Store(
        RDF_Store,
        store_name='dbpedia-rdf',
        store_description='DBpedia RDF store'
):
    """Alias for :class:`RDF_Store` with DBpedia mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._dbpedia_mapping_constructor()
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class PubChemRDF_Store(
        RDF_Store,
        store_name='pubchem-rdf',
        store_description='PubChem RDF store'
):
    """Alias for :class:`RDF_Store` with PubChem mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            normalize_casrn: bool | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._pubchem_mapping_constructor(
                normalize_casrn=normalize_casrn)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WikidataRDF_Store(
        RDF_Store,
        store_name='wikidata-rdf',
        store_description='Wikidata RDF store'
):
    """Alias for :class:`RDF_Store` with Wikidata mappings."""

    def __init__(
            self,
            store_name: str,
            *args: RDF_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=False,  # force
                strict=strict,
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


# == SPARQL Store ==========================================================

class SPARQL_Store(
        MixerStore,
        store_name='sparql',
        store_description='SPARQL store'
):
    """SPARQL store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: IRIs, input sources, files, paths, strings, or statements.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Extra keyword arguments.
    """

    #: Type alias for SPARQL Store arguments.
    Args: TypeAlias = T_IRI | _SPARQL_Store.RDFLibBackend.Args

    @classmethod
    def _is_http_or_https_iri(
            cls,
            arg: Args,
            _re: re.Pattern = re.compile(r'^http[s]?://')
    ) -> bool:
        content: str
        if isinstance(arg, IRI):
            content = arg.content
        elif isinstance(arg, rdflib.URIRef):
            content = str(arg)
        elif isinstance(arg, str):
            content = arg
        else:
            return False
        return bool(_re.match(content))

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        other, iris = map(list, itertools.partition(
            self._is_http_or_https_iri, args))

        def it() -> Iterator[Store]:
            for iri in iris:
                yield Store('sparql-httpx', iri, mapping=mapping, **kwargs)
            if (other
                    or location is not None
                    or file is not None
                    or data is not None
                    or graph is not None
                    or rdflib_graph is not None):
                yield Store(
                    'rdf', *other, format=format,
                    location=location, file=file, data=data, graph=graph,
                    rdflib_graph=rdflib_graph, skolemize=skolemize,
                    mapping=mapping, **kwargs)
        super().__init__(store_name, list(it()), **kwargs)


class DBpediaSPARQL_Store(
        SPARQL_Store,
        store_name='dbpedia-sparql',
        store_description='DBpedia SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with DBpedia mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.db.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._dbpedia_mapping_constructor()
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class PubChemSPARQL_Store(
        SPARQL_Store,
        store_name='pubchem-sparql',
        store_description='PubChem SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with PubChem mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            normalize_casrn: bool | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.pc.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._pubchem_mapping_constructor(
                normalize_casrn=normalize_casrn)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WikidataSPARQL_Store(
        SPARQL_Store,
        store_name='wikidata-sparql',
        store_description='Wikidata SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with Wikidata mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            blazegraph: bool | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.wd.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=blazegraph,
                strict=strict,
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WDQS_Store(
        WikidataSPARQL_Store,
        store_name='wdqs',
        store_description='Wikidata query service store'
):
    """Alias for :class:`WikidataSPARQL_Store` with stricter mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=True,  # force
                strict=True,      # force
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)
