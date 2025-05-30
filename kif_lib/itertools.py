# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import sys
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
    AsyncIterable,
    AsyncIterator,
    Callable,
    cast,
    Final,
    Hashable,
    Iterable,
    Iterator,
    Literal,
    TypeAlias,
    TypeVar,
    Union,
)

__all__ = [
    'achain',
    'aenumerate',
    'amix',
    'aroundrobin',
    'auniq',
    'batched',
    'chain',
    'count',
    'cycle',
    'groupby',
    'islice',
    'mix',
    'partition',
    'permutations',
    'product',
    'repeat',
    'roundrobin',
    'starmap',
    'take',
    'tee',
    'uniq',
]

H = TypeVar('H', bound=Hashable)
R = TypeVar('R')
T = TypeVar('T')

AnyIterable: TypeAlias = Union[Iterable[T], AsyncIterable[T]]


class _Sentinel:

    __slots__ = (
        'payload',
    )

    payload: Any

    def __init__(self, payload: Any = None) -> None:
        self.payload = payload


_SENTINEL: Final[_Sentinel] = _Sentinel()


async def achain(*its: AsyncIterable[T]) -> AsyncIterator[T]:
    """Async version of :func:`itertools.chain`."""
    for it in its:
        async for x in it:
            yield x


async def aenumerate(
        it: AsyncIterable[T],
        start: int = 0
) -> AsyncIterator[tuple[int, T]]:
    """Async version of :func:`enumerate`."""
    async for x in aiter(it):
        yield start, x
        start += 1


if sys.version_info < (3, 10):
    __all__.append('aiter')

    def aiter(it: AsyncIterable[T]) -> AsyncIterator[T]:
        """Async version of :func:`iter`."""
        return it.__aiter__()


async def amap(
        f: Callable[..., R],
        *args: AnyIterable[Any]
) -> AsyncIterable[R]:
    """Async version of :func:`map`."""
    for it in args:
        if hasattr(it, '__aiter__'):
            async for x in cast(AsyncIterable[Any], it):
                yield f(x)
        else:
            for x in cast(Iterable[Any], it):
                yield f(x)


def mix(
        *its: Iterable[H],
        distinct: bool | None = None,
        limit: int | None = None,
        method: Literal['chain'] | Literal['roundrobin'] = 'roundrobin'
) -> Iterator[H]:
    """Yields mixed elements.

    Parameters:
       its: Iterables of hashable elements.
       distinct: Whether to skip duplicates.
       limit: Limit (maximum number) of elements to yield.
       method: Mixing method.

    Returns:
       Iterator.
    """
    if method == 'roundrobin':
        it = roundrobin(*its)
    elif method == 'chain':
        it = chain(*its)
    else:
        raise ValueError(method)
    if distinct:
        it = uniq(it)
    if limit is not None:
        it = islice(it, max(limit, 0))
    return it


async def amix(
        *its: AsyncIterable[H],
        distinct: bool | None = None,
        limit: int | None = None,
        method: Literal['chain'] | Literal['roundrobin'] = 'roundrobin'
) -> AsyncIterator[H]:
    """Async version of :func:`mix`."""
    if method == 'roundrobin':
        it = aroundrobin(*its)
    elif method == 'chain':
        it = achain(*its)
    else:
        raise ValueError(method)
    if distinct:
        it = auniq(it)
    if limit is None:
        async for x in it:
            yield x
    else:
        limit = max(limit, 0)
        async for i, x in aenumerate(it, 1):
            yield x
            if i >= limit:
                break


if sys.version_info < (3, 10):
    __all__.append('anext')

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


async def aroundrobin(*its: AsyncIterable[T]) -> AsyncIterator[T]:
    """Async version of :func:`more_itertools.roundrobin`."""
    its_ = list(its)
    while its_:
        tasks = (asyncio.ensure_future(
            anext(aiter(it), _Sentinel(it))) for it in its_)
        for x in await asyncio.gather(*tasks):
            if isinstance(x, _Sentinel):
                its_.remove(x.payload)  # type: ignore
            else:
                yield x


async def atake(n: int, it: AsyncIterable[T]) -> list[T]:
    """Async version of :func:`more_itertools.take`."""
    it, result = aiter(it), []
    while n > 0:
        try:
            result.append(await it.__anext__())
            n -= 1
        except StopAsyncIteration:
            break
    return result


def uniq(it: Iterable[H], _key=lambda x: x) -> Iterator[H]:
    """Yields unique elements, preserves order.

    This is a hashable-only version of `more_itertools.unique_everseen`.

    Parameters:
       it: Iterable of hashable elements.

    Returns:
       The resulting iterator.
    """
    return unique_everseen(it, key=_key)


async def auniq(it: AsyncIterable[H]) -> AsyncIterator[H]:
    """Async version of :func:`uniq`."""
    seen: set[H] = set()
    async for x in aiter(it):
        if x not in seen:
            yield x
            seen.add(x)
