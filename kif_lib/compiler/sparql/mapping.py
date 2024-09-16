# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from ...model import (
    KIF_Object,
    Statement,
    StatementTemplate,
    StatementVariable,
    Template,
    Term,
    Theta,
    Variable,
    VStatement,
    VTStatement,
)
from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterator,
    Mapping,
    MutableSequence,
    Optional,
    Protocol,
    TypeAlias,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from .compiler import SPARQL_Compiler


class SPARQL_Mapping(Mapping):
    """SPARQL mapping."""

    #: The type of entry ids.
    EntryId: TypeAlias = str

    #: The type of entry patterns.
    EntryPattern: TypeAlias = VStatement

    #: The type of things coercible to entry patterns.
    EntryTPattern: TypeAlias = VTStatement

    #: The type of entry callback argument.
    EntryCallbackArg: TypeAlias =\
        Optional[Union[Term, 'SPARQL_Compiler.Query.VTerm']]

    #: The type of entry callbacks.
    class EntryCallback(Protocol):
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                *args: SPARQL_Mapping.EntryCallbackArg
        ) -> Any:
            ...

    @dataclasses.dataclass(frozen=True)
    class Entry:
        """Entry in SPARQL mapping."""

        #: The pattern of entry.
        pattern: SPARQL_Mapping.EntryPattern

        #: The (compilation) callback of entry.
        callback: SPARQL_Mapping.EntryCallback

        @property
        def id(self) -> SPARQL_Mapping.EntryId:
            """The id of entry."""
            return self.get_id()

        def get_id(self) -> SPARQL_Mapping.EntryId:
            """Gets the id of entry.

            Returns:
               Entry id.
            """
            return self.pattern.digest

        def get_pattern(self) -> SPARQL_Mapping.EntryPattern:
            """Gets the pattern of entry.

            Returns:
               Entry pattern.
            """
            return self.pattern

        def get_callback(self) -> SPARQL_Mapping.EntryCallback:
            """Gets the callback of entry.

            Returns:
               Entry callback.
            """
            return self.callback

    class Skip(BaseException):
        """Skip the current entry."""

    #: The registered entries indexed by id (digest of pattern).
    _entries: ClassVar[Mapping[
        SPARQL_Mapping.EntryId, SPARQL_Mapping.Entry]]

    #: Entries to be registered by the next __init_subclass__() call.
    _scheduled_entries: ClassVar[MutableSequence[tuple[
        SPARQL_Mapping.EntryPattern, SPARQL_Mapping.EntryCallback]]] = []

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._entries = {
            pat.digest: cls.Entry(pat, f)
            for pat, f in SPARQL_Mapping._scheduled_entries}
        SPARQL_Mapping._scheduled_entries = []

    @classmethod
    def register(
            cls,
            pattern: SPARQL_Mapping.EntryTPattern
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           pattern: Statement, statement template, or statement variable.

        Returns:
           The wrapped callback.
        """
        pat: SPARQL_Mapping.EntryPattern
        if isinstance(pattern, Template):
            pat = StatementTemplate.check(pattern, cls.register, 'pattern', 1)
        elif isinstance(pattern, Variable):
            pat = StatementVariable.check(pattern, cls.register, 'pattern', 1)
        else:
            pat = Statement.check(pattern, cls.register, 'pattern', 1)

        ###
        # TODO: Rename variables in `pat` to avoid conflicts.
        ###
        def wrapper(f):
            cls._scheduled_entries.append((pat, f))
            return f
        return wrapper

    def __getitem__(
            self,
            k: SPARQL_Mapping.EntryId | SPARQL_Mapping.EntryPattern
    ) -> SPARQL_Mapping.Entry:
        if isinstance(k, KIF_Object):
            k = k.digest
        return self._entries[k]

    def __iter__(self) -> Iterator[SPARQL_Mapping.EntryPattern]:
        return iter(map(self.Entry.get_pattern, self._entries.values()))

    def __len__(self) -> int:
        return len(self._entries)

    def match(
            self,
            pattern: SPARQL_Mapping.EntryPattern
    ) -> Iterator[tuple[
            SPARQL_Mapping.EntryPattern, Theta, SPARQL_Mapping.Entry]]:
        """Searches for entries matching `pattern`.

        Parameters:
           pattern: Statement, statement template, or statement variable.

        Returns:
           An iterator of triples "(pattern, theta, entry)".
        """
        for _, entry in self._entries.items():
            theta = pattern.match(entry.pattern)
            if theta is None:
                continue
            target = pattern.instantiate(theta)
            assert target is not None
            yield (
                cast(SPARQL_Mapping.EntryPattern, target),
                {v: v.instantiate(theta)
                 for v in entry.pattern._iterate_variables()},
                entry)


register: Final[Callable[
    [SPARQL_Mapping.EntryTPattern], SPARQL_Mapping.EntryCallback]] =\
    SPARQL_Mapping.register
