# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import json
import logging
import pathlib

import httpx

from .. import itertools, rdflib
from ..compiler.sparql import SPARQL_Mapping, SPARQL_MappingFilterCompiler
from ..compiler.sparql.results import SPARQL_Results, SPARQL_ResultsBinding
from ..model import (
    Filter,
    Graph,
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
    ClassVar,
    Iterator,
    Location,
    TextIO,
    TypeAlias,
    cast,
    override,
)
from .sparql import NS, SPARQL_Store


HTTP_Headers: TypeAlias = httpx._types.HeaderTypes

LOG = logging.getLogger(__name__)


class SPARQL_Store2(
        SPARQL_Store,
        store_name='sparql2',
        store_description='SPARQL endpoint'
):
    """SPARQL store.

    Parameters:
       store_name: Store plugin to instantiate.
       iri: SPARQL endpoint IRI.
       mapping: SPARQL mapping.
    """

    __slots__ = (
        '_http_headers',
        '_mapping',
        '_rdflib_graph',
    )

    def __init__(
            self,
            store_name: str,
            iri: T_IRI | None = None,
            mapping: SPARQL_Mapping | None = None,
            publicID: str | None = None,
            format: str | None = None,
            path: pathlib.PurePath | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(store_name, iri or 'file:///dev/null', **kwargs)
        self._init_mapping(mapping, type(self), 'mapping')
        self._init_rdflib_graph(
            rdflib_graph=rdflib_graph, publicID=publicID,
            format=format, path=path, location=location, file=file,
            data=data, graph=graph)

# -- HTTP client -----------------------------------------------------------


# -- HTTP headers ----------------------------------------------------------

    #: HTTP headers.
    _http_headers: HTTP_Headers


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

    @property
    def default_mapping(self) -> SPARQL_Mapping:
        """The default value for :attr:`SPARQL_Store2.mapping`."""
        return self.get_default_mapping()

    def get_default_mapping(self) -> SPARQL_Mapping:
        """Gets the default value for :attr:`SPARQL_Store2.mapping`.

        Returns:
           Default mapping.
        """
        from ..compiler.sparql.mapping.wikidata import WikidataMapping
        return WikidataMapping()

    #: SPARQL mapping.
    _mapping: SPARQL_Mapping

    def _init_mapping(
            self,
            mapping: SPARQL_Mapping | None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        if mapping is None:
            self._mapping = self.default_mapping
        else:
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

# -- RDFlib graph ----------------------------------------------------------

    @classmethod
    def _check_rdflib_graph(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> rdflib.Graph:
        return KIF_Object._check_arg_isinstance(
            arg, rdflib.Graph, function, name, position)

    @classmethod
    def _check_optional_rdflib_graph(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> rdflib.Graph | None:
        return cls._do_check_optional(
            cls._check_rdflib_graph, arg, default, function, name, position)

    @property
    def default_rdflib_graph(self) -> rdflib.Graph | None:
        """The default value for :attr:`SPARQL_Store2.rdflib_graph`."""
        return self.get_default_rdflib_graph()

    def get_default_rdflib_graph(self) -> rdflib.Graph | None:
        """Gets the default value for :attr:`SPARQL_Store2.rdflib_graph`.

        Returns:
           RDFlib graph or ``None``.
        """
        return None

    #: RDFlib graph.
    _rdflib_graph: rdflib.Graph | None

    def _init_rdflib_graph(
            self,
            rdflib_graph: rdflib.Graph | None,
            publicID: str | None = None,
            format: str | None = None,
            path: pathlib.PurePath | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: str | bytes | None = None,
            graph: TGraph | None = None
    ) -> None:
        rdflib_graph = self._check_optional_rdflib_graph(
            rdflib_graph, None, type(self), 'rdflib_graph')
        graph = Graph.check_optional(graph, None, type(self), 'graph')
        try:
            if (path is not None
                    or location is not None
                    or file is not None
                    or data is not None
                    or graph is not None):
                if rdflib_graph is None:
                    rdflib_graph = rdflib.Graph()
                load = functools.partial(
                    rdflib_graph.parse, format=format, publicID=publicID)
                if path is not None:
                    load(path)
                if location is not None:
                    load(location=location)
                if file is not None:
                    load(file=file)
                if data is not None:
                    load(data=data)
                if graph is not None:
                    load(data=graph.to_rdf())
            if rdflib_graph is not None:
                rdflib_graph = rdflib_graph.skolemize()
            self._rdflib_graph = rdflib_graph
        except Exception as err:
            raise self._error(str(err)) from err

    @property
    def rdflib_graph(self) -> rdflib.Graph | None:
        """The RDFLib graph of SPARQL store (if any)."""
        return self.get_rdflib_graph()

    def get_rdflib_graph(self) -> rdflib.Graph | None:
        """Gets RDFLib graph of SPARQL store.

        Returns:
           RDFLib graph or ``None``.
        """
        return self._rdflib_graph

# -- Statements ------------------------------------------------------------

    def _eval(self, text: str) -> SPARQL_Results:
        if self._rdflib_graph is not None:
            LOG.debug('%s()\n%s', self._eval_query_string.__qualname__, text)
            res = self._rdflib_graph.query(self._prepare_query_string(text))
            data = cast(bytes, res.serialize(format='json'))
            assert data is not None
            return json.loads(data)
        else:
            return self._http_post(self.iri.content, text).json()

    def _http_post(self, iri: str, text: str) -> httpx.Response:
        LOG.debug('%s():\n%s', self._http_post.__qualname__, text)
        try:
            res = self._client.post(iri, content=text.encode('utf-8'))
            res.raise_for_status()
            return res
        except httpx.RequestError as err:
            raise err

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
            res = self._eval(str(query))
            if 'results' not in res:
                break           # nothing to do
            bindings = res['results']['bindings']
            if not bindings:
                break           # done
            push = compiler.build_results()
            bindings_it: Iterator[SPARQL_ResultsBinding] =\
                itertools.chain(bindings, ({},))  # {} is the sentinel
            for binding in bindings_it:
                ret = push(binding)
                if ret is None:
                    continue    # push more results
                for theta in ret:
                    stmt = compiler.pattern.variable.instantiate(theta)
                    assert isinstance(stmt, Statement), stmt
                    ###
                    # FIXME: Is this really needed?  It drops statements
                    # when property has ExternalId datatype and value is
                    # String.
                    ###
                    # if (self.has_flags(self.LATE_FILTER)
                    #         and not filter.match(stmt)):
                    #     LOG.debug('SKIPPED (late filter) %s', stmt)
                    #     continue
                    self._cache_add_wds(stmt, NS.WDS[stmt.digest])
                    yield stmt
                    count += 1
            assert count <= limit, (count, limit)
            if count < page_size or count == limit:
                break           # done
            offset += page_size

    #: Flags to be passed to filter compiler.
    _compile_filter_flags: ClassVar[SPARQL_MappingFilterCompiler.Flags] =\
        SPARQL_MappingFilterCompiler.default_flags

    def _compile_filter(self, filter: Filter) -> SPARQL_MappingFilterCompiler:
        compiler = SPARQL_MappingFilterCompiler(
            filter, self._mapping, self._compile_filter_flags)
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
