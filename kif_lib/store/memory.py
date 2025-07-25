# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import dataclasses
import functools
import logging

from .. import itertools
from ..model import Filter, Graph, Statement, TGraph
from ..typing import (
    Any,
    AsyncIterator,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    override,
    Sequence,
    TypeAlias,
)
from .abc import Store, StoreOptions

_logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclasses.dataclass
class MemoryStoreOptions(StoreOptions, name='memory'):
    """Memory store options."""

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_MEMORY_STORE_DEBUG',), None)

    _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_MEMORY_STORE_DISTINCT',), None)

    _v_max_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            (('KIF_MEMORY_STORE_MAX_DISTINCT_WINDOW_SIZE',), None))

    _v_distinct_window_size: ClassVar[
        tuple[Iterable[str], int | None]] = (
            (('KIF_MEMORY_STORE_DISTINCT_WINDOW_SIZE',), None))

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_LOOKAHEAD',), None)

    _v_omega: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_OMEGA',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_MEMORY_STORE_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_MEMORY_STORE_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_MEMORY_STORE_TIMEOUT',), None)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


# == Memory store ==========================================================

TOptions: TypeAlias = MemoryStoreOptions


class MemoryStore(
        Store[TOptions],
        store_name='memory',
        store_description='Memory store'
):
    """Memory store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
    """

    __slots__ = (
        '_statements',
    )

    #: Statement storage.
    _statements: set[Statement]

    def __init__(
            self,
            store_name: str,
            *args: Statement,
            graph: TGraph | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(*args, **kwargs)
        self._statements = set(itertools.chain(
            map(functools.partial(
                Statement.check, function=type(self), name='args'), args),
            Graph.check(graph, type(self), 'graph')
            if graph is not None else ()))

    @override
    def _filter(
            self,
            filter: Filter,
            options: TOptions
    ) -> Iterator[Statement]:
        return itertools.filter(
            filter.match, self._filter_it_statements(filter))

    def _filter_it_statements(
            self,
            filter: Filter
    ) -> Iterator[Statement]:
        if filter.annotated:
            return map(lambda stmt: stmt.annotate(), self._statements)
        else:
            return map(lambda stmt: stmt.unannotate(), self._statements)

    @override
    def _afilter(
            self,
            filter: Filter,
            options: TOptions
    ) -> AsyncIterator[Statement]:
        limit = options.limit
        if limit is None:
            limit = options.max_limit
        assert limit is not None
        batches = itertools.batched(
            self._filter_it_statements(filter), options.page_size)
        return itertools.amix(
            self._afilter_helper(filter, batches),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=limit, method='chain')

    async def _afilter_helper(
            self,
            filter: Filter,
            batches: Iterator[Sequence[Statement]]
    ) -> AsyncIterator[Statement]:
        async def task(
                batch: Sequence[Statement]
        ) -> Sequence[Statement]:
            _logger.debug(
                '%s():filtering %d statements asynchronously',
                task.__qualname__, len(batch))
            return await asyncio.to_thread(
                lambda: list(itertools.filter(filter.match, batch)))
        for batch in await asyncio.gather(*map(task, batches)):
            for stmt in batch:
                yield stmt
