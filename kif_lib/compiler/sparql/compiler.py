# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc
import itertools

from ...typing import Iterator, Optional
from ..compiler import Compiler
from .builder import SelectQuery


class SPARQL_Compiler(Compiler):
    """Abstract base class for SPARQL compilers."""

    class Query(SelectQuery):
        """Compiled query."""

    class Error(Compiler.Error):
        """Base class for SPARQL compiler errors."""

    class Results(Compiler.Results):
        """SPARQL compiler results."""

        __slots__ = (
            '_query',
        )

        #: The query that produced these results.
        _query: 'SPARQL_Compiler.Query'

        def __init__(
                self,
                query: 'SPARQL_Compiler.Query'
        ):
            self._query = query

        @property
        def query(self) -> 'SPARQL_Compiler.Query':
            """The SPARQL query that produced these results."""
            return self.get_query()

        def get_query(self) -> 'SPARQL_Compiler.Query':
            """Gets the SPARQL query that produced these results.

            Returns:
               SPARQL query.
            """
            return self._query

    __slots__ = (
        '_q',
        '_debug',
    )

    #: The compiled query.
    _q: 'SPARQL_Compiler.Query'

    #: Whether to enable debugging.
    _debug: bool

    @abc.abstractmethod
    def __init__(self, debug: Optional[bool] = None):
        super().__init__()
        self._q = self.Query()
        self._debug = debug if debug is not None else False

    def _qvar(self, var: Query.TVariable) -> Query.Variable:
        return self._q.var(var)

    def _qvars(
            self,
            var: Query.TVariable,
            *vars_: Query.Variable
    ) -> Iterator[Query.Variable]:
        return map(self._qvar, itertools.chain((var,), vars_))

    def _fresh_qvar(self) -> Query.Variable:
        return self._q.fresh_var()

    def _fresh_qvars(self, n: int) -> Iterator[Query.Variable]:
        return self._q.fresh_vars(n)
