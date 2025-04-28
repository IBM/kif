# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from itertools import (
    chain,
    count,
    cycle,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    starmap,
    tee,
)

from more_itertools import batched, partition, take, unique_everseen

from .typing import AsyncIterator, cast, ClassVar, Final, TypeAlias, TypeVar

__all__ = (
    'anext',
    'batched',
    'chain',
    'count',
    'cycle',
    'groupby',
    'islice',
    'partition',
    'permutations',
    'product',
    'repeat',
    'starmap',
    'take',
    'tee',
    'unique_everseen',
)

T = TypeVar('T')


class _SentinelType:
    Sentinel: ClassVar[_SentinelType | None] = None

    def __new__(cls):
        if cls.Sentinel is None:
            cls.Sentinel = super().__new__(cls)
        return cls.Sentinel

    def __call__(self) -> _SentinelType:
        return self


_T_SENTINEL: TypeAlias = _SentinelType
_SENTINEL: Final[_SentinelType] = _SentinelType()


async def anext(
        it: AsyncIterator[T],
        default: T | _T_SENTINEL = _SENTINEL
) -> T:
    """Async version of :func:`next'."""
    try:
        return await it.__anext__()
    except StopAsyncIteration:
        if default is _SENTINEL:
            raise
        return cast(T, default)
