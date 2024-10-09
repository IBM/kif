# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging

from ..compiler.sparql import SPARQL_Mapping, SPARQL_MappingFilterCompiler
from ..model import (
    Filter,
    KIF_Object,
    Statement,
    StatementVariable,
    T_IRI,
    VariablePattern,
)
from ..typing import Any, ClassVar, Iterator, override
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
    )

    #: SPARQL mapping.
    _mapping: SPARQL_Mapping

    def __init__(
            self,
            store_name: str,
            iri: T_IRI,
            mapping: SPARQL_Mapping,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(store_name, iri, **kwargs)
        self._mapping = KIF_Object._check_arg_isinstance(
            mapping, SPARQL_Mapping, self.__class__, 'mapping', 3)

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
            res = self._eval_select_query_string(str(query))
            bindings = res['results']['bindings']
            if not bindings:
                break           # done
            for binding in bindings:
                for theta in compiler._binding_to_thetas(binding):
                    stmt = compiler.pattern.variable.instantiate(theta)
                    assert isinstance(stmt, Statement), stmt
                    ###
                    # FIXME: Is this really needed?  It drops statements
                    # when property has ExternalId datatype and value is
                    # String.
                    ###
                    if (self.has_flags(self.LATE_FILTER)
                            and not filter.match(stmt)):
                        LOG.debug('SKIPPED (late filter) %s', stmt)
                        continue
                    self._cache_add_wds(stmt, NS.WDS[stmt.digest])
                    yield stmt
                    count += 1
            if len(bindings) < page_size:
                break           # done
            if count == limit:
                break           # done
            offset += page_size

    #: Flags to be passed to filter compiler.
    _compile_filter_flags: ClassVar[SPARQL_MappingFilterCompiler.Flags] =\
        SPARQL_MappingFilterCompiler.default_flags

    def _compile_filter(
            self,
            filter: Filter
    ) -> SPARQL_MappingFilterCompiler:
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
