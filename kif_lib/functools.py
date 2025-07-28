# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
from functools import cache, partial, reduce

from .typing import (
    Callable,
    Literal,
    ParamSpec,
    Protocol,
    runtime_checkable,
    TypeVar,
    TypeVarTuple,
    Unpack,
)

__all__ = (
    'cache',
    'compose',
    'fst',
    'id',
    'incr',
    'partial',
    'reduce',
    'snd',
)

P = ParamSpec('P')
S = TypeVar('S')
T = TypeVar('T')
Ts = TypeVarTuple('Ts')


def id(x: T) -> T:
    """Identity function."""
    return x


def fst(x: tuple[T, Unpack[Ts]]) -> T:
    """First projection."""
    return x[0]


def snd(x: tuple[S, T, Unpack[Ts]]) -> T:
    """Second projection."""
    return x[1]


def compose(g: Callable[[S], T], f: Callable[P, S]) -> Callable[P, T]:
    """Function composition."""
    return lambda *args, **kwargs: g(f(*args, **kwargs))


@runtime_checkable
class SupportsIncr(Protocol):
    """An ABC with one abstract method __add__ taking 1 as second argument."""

    __slots__ = ()

    @abc.abstractmethod
    def __add__(self: T, other: Literal[1]) -> T:
        pass


def incr(x: SupportsIncr) -> SupportsIncr:
    """The increment (successor) function."""
    return x + 1
