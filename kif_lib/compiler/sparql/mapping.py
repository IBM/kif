# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import dataclasses

from ...model import (
    Statement,
    StatementTemplate,
    StatementVariable,
    Template,
    Variable,
    VStatement,
    VTStatement,
)
from ...typing import Any, Callable, MutableSequence, Sequence, TypeAlias
from .builder import Query

Callback: TypeAlias = Callable[
    ['SPARQL_Mapping', 'SPARQL_Mapping.Entry', Query, VStatement], None]


class SPARQL_Mapping(Sequence):
    """SPARQL mapping."""

    @dataclasses.dataclass(frozen=True)
    class Entry:
        """Entry in SPARQL mapping."""

        class Skip(BaseException):
            """Skip the current entry."""

        #: The statement pattern of entry.
        pattern: VStatement

        #: The compilation callback of entry.
        callback: Callback

    #: The registered entries.
    entries: MutableSequence[Entry]

    @classmethod
    def __init_subclass__(cls) -> None:
        cls.entries = []

    @classmethod
    def register(
            cls,
            pattern: VTStatement,
            **kwargs: Any
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           pattern: Statement, statement template, or statement variable.
        """
        pat: VStatement
        if isinstance(pattern, Template):
            pat = StatementTemplate.check(pattern, cls.register, 'pattern', 1)
        elif isinstance(pattern, Variable):
            pat = StatementVariable.check(pattern, cls.register, 'pattern', 1)
        else:
            pat = Statement.check(pattern, cls.register, 'statement', 1)
        return lambda callback: cls._register(
            cls.Entry(pat, callback, **kwargs))

    @classmethod
    def _register(cls, entry: Entry) -> None:
        cls.entries.append(entry)

    @abc.abstractmethod
    def __init__(self):
        pass

    def __getitem__(self, i: Any) -> Any:
        return self.entries[i]

    def __len__(self) -> int:
        return len(self.entries)
