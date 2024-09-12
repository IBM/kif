# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools

from ...model import Statement, StatementTemplate, Template, VTStatement
from ...typing import Any, Callable, ClassVar, Final, MutableSequence, Sequence


class SPARQL_Mapping(Sequence):
    """SPARQL mapping."""

    @dataclasses.dataclass(frozen=True)
    class Entry:
        """Entry in SPARQL mapping."""

        class Skip(BaseException):
            """Skip the current entry."""

        #: The statement pattern of entry.
        pattern: Statement | StatementTemplate

        #: The compilation callback of entry.
        callback: Callable[..., Any]

    #: The registered entries.
    _entries: ClassVar[Sequence[Entry]]

    #: Entries to be registered by the next __init_subclass__() call.
    _scheduled_entries: ClassVar[MutableSequence[
        tuple[Statement | StatementTemplate, Callable[..., Any]]]] = []

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._entries = list(map(
            lambda t: cls.Entry(t[0], functools.partial(t[1], cls)),
            SPARQL_Mapping._scheduled_entries))
        SPARQL_Mapping._scheduled_entries = []

    @classmethod
    def register(
            cls,
            pattern: VTStatement
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           pattern: Statement, statement template, or statement variable.
        """
        pat: Statement | StatementTemplate
        if isinstance(pattern, Template):
            pat = StatementTemplate.check(pattern, cls.register, 'pattern', 1)
        else:
            pat = Statement.check(pattern, cls.register, 'statement', 1)
        return lambda f: cls._scheduled_entries.append((pat, f))

    def __getitem__(self, i: Any) -> Any:
        return self._entries[i]

    def __len__(self) -> int:
        return len(self._entries)


register: Final[Callable[[VTStatement], Callable[..., Any]]] =\
    SPARQL_Mapping.register
