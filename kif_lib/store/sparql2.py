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
from ..typing import Any, cast, ClassVar, Iterator, override
from .sparql import NS, SPARQL_Store

LOG = logging.getLogger(__name__)


class SPARQL_Store2(
        SPARQL_Store,
        store_name='sparql2',
        store_description='SPARQL endpoint'):
    """SPARQL store.

    Parameters:
       store_name: Store plugin to instantiate.
       iri: SPARQL endpoint IRI.
       mapping: SPARQL mapping.
    """

    __slots__ = (
        '_mapping',
        '_rdflib_graph',
    )

    #: SPARQL mapping.
    _mapping: SPARQL_Mapping

    #: RDFlib graph.
    _rdflib_graph: rdflib.Graph | None

    def __init__(
            self,
            store_name: str,
            iri: T_IRI | None = None,
            mapping: SPARQL_Mapping | None = None,
            publicID: str | None = None,
            format: str | None = None,
            path: pathlib.PurePath | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(store_name, iri or '', **kwargs)
        self._init_mapping(
            mapping=KIF_Object._check_optional_arg_isinstance(
                mapping, SPARQL_Mapping, None, type(self), 'mapping'))
        self._init_rdflib_graph(
            rdflib_graph=KIF_Object._check_optional_arg_isinstance(
                rdflib_graph, rdflib.Graph, None, type(self), 'rdflib_graph'),
            publicID=publicID,
            format=format,
            path=path,
            graph=Graph.check_optional(graph, None, type(self), 'graph'))

    def _init_mapping(self, mapping: SPARQL_Mapping | None) -> None:
        if mapping is not None:
            self._mapping = mapping
        else:
            from ..compiler.sparql.mapping.wikidata import WikidataMapping
            self._mapping = WikidataMapping()

    def _init_rdflib_graph(
            self,
            rdflib_graph: rdflib.Graph | None,
            publicID: str | None = None,
            format: str | None = None,
            path: pathlib.PurePath | None = None,
            graph: Graph | None = None
    ) -> None:
        if path is not None or graph is not None:
            if rdflib_graph is None:
                rdflib_graph = rdflib.Graph()
            load = functools.partial(
                rdflib_graph.parse, format=format, publicID=publicID)
            if path is not None:
                load(path)
            if graph is not None:
                graph = Graph.check(graph, type(self), 'graph')
                assert graph is not None
                load(data=graph.to_rdf())
        if rdflib_graph is not None:
            rdflib_graph = rdflib_graph.skolemize()
        self._rdflib_graph = rdflib_graph

    @property
    def mapping(self) -> SPARQL_Mapping:
        """SPARQL mapping."""
        return self.get_mapping()

    def get_mapping(self) -> SPARQL_Mapping:
        """Gets SPARQL mapping.

        Returns:
           SPARQL mapping.
        """
        return self._mapping

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
