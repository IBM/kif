# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import enum

from ... import itertools
from ...model import Variable
from ...typing import Final, Iterator
from ..compiler import Compiler
from .builder import SelectQuery


class SPARQL_Compiler(Compiler):
    """Abstract base class for SPARQL compilers."""

    class Query(SelectQuery):
        """Compiled SPARQL query."""

    class Flags(enum.Flag):
        """Compilation flags."""

        #: Whether to generate debugging information.
        DEBUG = enum.auto()

        #: Whether to match only the best ranked statements.
        BEST_RANK = enum.auto()

        #: Whether to match value snaks.
        VALUE_SNAK = enum.auto()

        #: Whether to match some-value snaks.
        SOME_VALUE_SNAK = enum.auto()

        #: Whether to match no-value snaks.
        NO_VALUE_SNAK = enum.auto()

        #: Whether to push early filters.
        EARLY_FILTER = enum.auto()

        #: Whether to use Wikidata RDF extensions.
        WIKIDATA_EXTENSIONS = enum.auto()

        #: All flags.
        ALL = (
            DEBUG
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK
            | EARLY_FILTER
            | WIKIDATA_EXTENSIONS)

    #: The default flags.
    default_flags: Final[Flags] = (
        Flags.ALL & ~(Flags.DEBUG | Flags.WIKIDATA_EXTENSIONS))

    DEBUG = Flags.DEBUG
    BEST_RANK = Flags.BEST_RANK
    VALUE_SNAK = Flags.VALUE_SNAK
    SOME_VALUE_SNAK = Flags.SOME_VALUE_SNAK
    NO_VALUE_SNAK = Flags.NO_VALUE_SNAK
    EARLY_FILTER = Flags.EARLY_FILTER
    WIKIDATA_EXTENSIONS = Flags.WIKIDATA_EXTENSIONS

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
           Variable.
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
           Iterator of variables.
        """
        return map(self.as_qvar, itertools.chain((var,), vars))
