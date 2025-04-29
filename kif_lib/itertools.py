# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
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

from more_itertools import (
    batched,
    partition,
    roundrobin,
    take,
    unique_everseen,
)

from .typing import (
    Any,
    AsyncIterator,
    cast,
    Final,
    Iterable,
    Iterator,
    TypeVar,
)

__all__ = (
    'aenumerate',
    'anext',
    'aroundrobin',
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
    'roundrobin',
    'starmap',
    'take',
    'tee',
    'unique_everseen',
)

T = TypeVar('T')


class _Sentinel:

    __slots__ = (
        'payload',
    )

    def __init__(self, payload: Any = None) -> None:
        self.payload = payload


_SENTINEL: Final[_Sentinel] = _Sentinel()


async def aenumerate(
        it: AsyncIterator[T],
        start: int = 0
) -> AsyncIterator[tuple[int, T]]:
    """Async version of :func:`enumerate`."""
    async for x in it:
        yield start, x
        start += 1


async def anext(
        it: AsyncIterator[T],
        default: T | _Sentinel = _SENTINEL
) -> T:
    """Async version of :func:`next'."""
    try:
        return await it.__anext__()
    except StopAsyncIteration:
        if default is _SENTINEL:
            raise
        return cast(T, default)


async def aroundrobin(*its: AsyncIterator[T]) -> AsyncIterator[T]:
    """Async version of :func:`roundrobin`."""
    its_ = list(its)
    while its_:
        tasks = (asyncio.ensure_future(
            anext(it, _Sentinel(it))) for it in its_)
        for x in await asyncio.gather(*tasks):
            if isinstance(x, _Sentinel):
                its_.remove(x.payload)  # type: ignore
            else:
                yield x


def uniq(it: Iterable[T]) -> Iterator[T]:
    """Yields unique elements, preserves order.

    it: Iterable of hashable elements.

    Returns:
       An corresponding iterator without duplicates.
    """
    seen: set[T] = set()
    for x in it:
        if x not in seen:
            yield x
            seen.add(x)


async def auniq(it: AsyncIterator[T]) -> AsyncIterator[T]:
    """Async version of :func:`uniq`."""
    seen: set[T] = set()
    async for x in it:
        if x not in seen:
            yield x
            seen.add(x)
