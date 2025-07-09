# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from ... import itertools
from ...context import Context
from ...model import (
    DatatypeVariable,
    IRI_Variable,
    QuantityVariable,
    StringVariable,
    TimeVariable,
    Variable,
)
from ...typing import cast, Final, Iterator, Sequence
from ..compiler import Compiler
from .builder import SelectQuery
from .options import SPARQL_CompilerOptions as Options


class SPARQL_Compiler(Compiler):
    """Abstract base class for SPARQL compilers."""

    class Query(SelectQuery):
        """Compiled SPARQL query."""

    __slots__ = (
        '_query_stack',
        '_debug',
    )

    #: The compiled queries.
    _query_stack: Sequence[SPARQL_Compiler.Query]

    #: Whether to enable debugging.
    _debug: bool

    @abc.abstractmethod
    def __init__(
            self,
            debug: bool | None = None,
            context: Context | None = None
    ) -> None:
        self._query_stack = [self.Query()]
        self._debug = debug or False

    @property
    def default_options(self) -> Options:
        """The default options of compiler."""
        return self.get_default_options()

    def get_default_options(self, context: Context | None = None) -> Options:
        """Gets the default options of compiler.

        Parameters:
           context: Context.

        Returns:
           Compiler options.
        """
        return self.get_context(context).options.compiler.sparql

    @property
    def query_stack(self) -> Sequence[Query]:
        """The compiled query stack."""
        return self.get_query_stack()

    def get_query_stack(self) -> Sequence[Query]:
        """Get the compiled query stack.

        Returns:
           Query stack.
        """
        return self._query_stack

    def push_query(self, query: Query | None = None) -> Query:
        """Pushes query onto query stack.

        If `query` is ``None``, pushes an empty query.

        Returns:
           The pushed query.
        """
        query = query or self.Query()
        cast(list, self._query_stack).append(query)
        return query

    def pop_query(self) -> Query:
        """Pops query from query stack.

        Returns:
           The popped query.
        """
        assert self._query_stack
        return cast(list, self._query_stack).pop()

    @property
    def q(self) -> Query:
        """The current query (top of query stack)."""
        return self.get_query()

    @property
    def query(self) -> Query:
        """The current query (top of query stack)."""
        return self.get_query()

    def get_query(self) -> Query:
        """Gets the current query (top of query stack).

        Returns:
           Query.
        """
        assert self._query_stack
        return self._query_stack[-1]

    @property
    def debug(self) -> bool:
        """Whether debugging is enabled."""
        return self.get_debug()

    def get_debug(self) -> bool:
        """Gets the debug flag.

        Returns:
           Debug flag.
        """
        return self._debug

    def uri(self, content: Query.T_URI) -> Query.URI:
        """Alias of :meth:`Query.uri`."""
        return self.q.uri(content)

    def bnode(self) -> Query.BNode:
        """Alias of :meth:`Query.BNode`."""
        return self.q.bnode()

    def literal(
            self,
            content: Query.TLiteral,
            language: str | None = None,
            datatype: str | None = None
    ) -> Query.Literal:
        """Alias of :meth:`Query.literal`."""
        return self.q.literal(content, language, datatype)

    def qvar(self, name: Query.TVariable) -> Query.Variable:
        """Alias of :meth:`Query.var`."""
        return self.q.var(name)

    def qvars(
            self,
            var: Query.TVariable,
            *vars: Query.Variable
    ) -> Iterator[Query.Variable]:
        """Alias of :meth:`Query.vars`."""
        return self.q.vars(var, *vars)

    def fresh_qvar(self) -> Query.Variable:
        """Alias of :meth:`Query.fresh_var`."""
        return self.q.fresh_var()

    def fresh_qvars(self, n: int) -> Iterator[Query.Variable]:
        """Alias of :meth:`Query.fresh_vars`."""
        return self.q.fresh_vars(n)

    def as_qvar(self, var: Variable) -> Query.Variable:
        """Constructs query variable from variable.

        Parameter:
           var: Variable.

        Returns:
           Query variable.
        """
        return self.qvar(var.name)

    def as_qvars(
            self,
            var: Variable,
            *vars: Variable
    ) -> Iterator[Query.Variable]:
        """Constructs one or more query variables from variables.

        Parameters:
           var: Variable.
           vars: Variables.

        Returns:
           Iterator of query variables.
        """
        return map(self.as_qvar, itertools.chain((var,), vars))

    #: Classes of variables corresponding to primitive SPARQL types.
    _primitive_var_classes: Final[tuple[type[Variable], ...]] = (
        DatatypeVariable,
        IRI_Variable,
        QuantityVariable,
        StringVariable,
        TimeVariable,
    )

    def as_safe_qvar(self, var: Variable) -> Query.Variable:
        """Constructs query variable from variable (safe).

        If variable is not of a primitive type, raises an error.

        Returns:
           Query variable.
        """
        if isinstance(var, self._primitive_var_classes):
            return self.as_qvar(var)
        else:
            raise TypeError

    def as_safe_qvars(
            self,
            var: Variable,
            *vars: Variable
    ) -> Iterator[Query.Variable]:
        """Constructs one or more query variables from variables (safe).

        If one of the variables is not of a primitive type, raises an error.

        Parameters:
           var: Variable.
           vars: Variables.

        Returns:
           Iterator of query variables.
        """
        return map(self.as_safe_qvar, itertools.chain((var,), vars))
