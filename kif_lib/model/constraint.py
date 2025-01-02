# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import (
    Any,
    cast,
    Literal,
    Location,
    override,
    Self,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object

TConstraint: TypeAlias = Union['Constraint', 'TAtomicConstraint']

TAtomicConstraint: TypeAlias =\
    Union['AtomicConstraint', 'TTrueConstraint', 'TFalseConstraint']
TTrueConstraint: TypeAlias = Union['TrueConstraint', bool, Literal[None]]
TFalseConstraint: TypeAlias = Union['FalseConstraint', bool]


class Constraint(KIF_Object):
    """Abstract base class for constraint expressions."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        else:
            return cast(Self, AtomicConstraint.check(
                arg, function or cls.check, name, position))


class AtomicConstraint(Constraint):
    """Abstract base class for atomic constraint expressions."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif arg is None or arg is True:
            return cast(Self, TrueConstraint.check(
                arg, function or cls.check, name, position))
        elif arg is False:
            return cast(Self, FalseConstraint.check(
                arg, function or cls.check, name, position))
        else:
            raise cls._check_error(
                arg, function or cls.check, name, position)


class TrueConstraint(AtomicConstraint):
    """The true constraint."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif arg is True or arg is None:
            return cls()
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self) -> None:
        super().__init__()


class FalseConstraint(AtomicConstraint):
    """The false constraint."""

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif arg is False:
            return cls()
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self) -> None:
        super().__init__()
