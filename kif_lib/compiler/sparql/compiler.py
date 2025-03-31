# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from ... import itertools
from ...model import (
    DatatypeVariable,
    IRI_Variable,
    QuantityVariable,
    StringVariable,
    TimeVariable,
    Variable,
)
from ...model.flags import Flags as KIF_Flags
from ...typing import Final, Iterator
from ..compiler import Compiler
from .builder import SelectQuery


class SPARQL_Compiler(Compiler):
    """Abstract base class for SPARQL compilers."""

    class Query(SelectQuery):
        """Compiled SPARQL query."""

    class Flags(KIF_Flags):
        """Compilation flags."""

        #: Whether to generate debugging information.
        DEBUG = KIF_Flags.auto()

        #: Whether to match only the best ranked statements.
        BEST_RANK = KIF_Flags.auto()

        #: Whether to match value snaks.
        VALUE_SNAK = KIF_Flags.auto()

        #: Whether to match some-value snaks.
        SOME_VALUE_SNAK = KIF_Flags.auto()

        #: Whether to match no-value snaks.
        NO_VALUE_SNAK = KIF_Flags.auto()

        #: All flags.
        ALL = (
            DEBUG
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK)

    #: The default flags.
    default_flags: Final[Flags] = (Flags.ALL & ~Flags.DEBUG)

    DEBUG = Flags.DEBUG
    BEST_RANK = Flags.BEST_RANK
    VALUE_SNAK = Flags.VALUE_SNAK
    SOME_VALUE_SNAK = Flags.SOME_VALUE_SNAK
    NO_VALUE_SNAK = Flags.NO_VALUE_SNAK

    __slots__ = (
        '_q',
        '_flags',
    )

    #: The compiled query.
    _q: SPARQL_Compiler.Query

    #: The compilation flags.
    _flags: SPARQL_Compiler.Flags

    @abc.abstractmethod
    def __init__(self, flags: Flags | None = None) -> None:
        super().__init__()
        self._q = self.Query()
        if flags is None:
            self._flags = self.default_flags
        else:
            self._flags = self.Flags(flags)

    @property
    def flags(self) -> Flags:
        """The flags set in compiler."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Flags) -> None:
        if flags != self._flags:
            self._flags = self.Flags(flags)

    def get_flags(self) -> Flags:
        """Gets the flags set in compiler.

        Returns:
           Compiler flags.
        """
        return self._flags

    def has_flags(self, flags: Flags) -> bool:
        """Tests whether `flags` are set in compiler.

        Parameters:
           flags: Compiler flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return bool(self.flags & flags)

    def set_flags(self, flags: Flags) -> None:
        """Sets `flags` in compiler.

        Parameters:
           flags: Compiler flags.
        """
        self.flags |= flags

    def unset_flags(self, flags: Flags) -> None:
        """Unsets `flags` in compiler.

        Parameters:
           flags: Compiler flags.
        """
        self.flags &= ~flags

    @property
    def q(self) -> Query:
        """The compiled query."""
        return self.get_query()

    @property
    def query(self) -> Query:
        """The compiled query."""
        return self.get_query()

    def get_query(self) -> Query:
        """Gets the compiled query.

        Returns:
           SPARQL query.
        """
        return self._q

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
