# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..model import Filter, KIF_Object, Statement
from ..typing import (
    Any,
    AsyncIterator,
    Collection,
    Iterable,
    Iterator,
    override,
    Sequence,
    TypeVar,
)
from .abc import Store

T = TypeVar('T')
S = TypeVar('S')


class MixerStore(
        Store,
        store_name='mixer',
        store_description='Mixer store'
):
    """Mixer store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       sources: Sources to mix.
       sync_flags: Whether to sync store flags.
       sync_limit: Whether to sync store limit.
       sync_page_size: Whether to sync page size.
       sync_timeout: Whether to sync timeout.
    """

    __slots__ = (
        '_sources',
        '_sync_flags',
        '_sync_limit',
        '_sync_page_size',
        '_sync_timeout',
    )

    _sources: Sequence[Store]
    _sync_flags: bool
    _sync_limit: bool
    _sync_page_size: bool
    _sync_timeout: bool

    def __init__(
            self,
            store_name: str,
            sources: Iterable[Store] = tuple(),
            sync_flags: bool = True,
            sync_limit: bool = True,
            sync_page_size: bool = True,
            sync_timeout: bool = True,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        self._init_sources(sources)
        self._sync_flags = bool(sync_flags)
        self._sync_limit = bool(sync_limit)
        self._sync_page_size = bool(sync_page_size)
        self._sync_timeout = bool(sync_timeout)
        super().__init__(**kwargs)

    def _init_sources(self, sources: Iterable[Store]) -> None:
        KIF_Object._check_arg_isinstance(
            sources, Iterable, type(self), 'sources', 2)
        self._sources = [
            KIF_Object._check_arg(
                src, isinstance(src, Store),
                'expected Iterable[Store]',
                type(self), 'sources', 2, TypeError)
            for src in sources]

    @property
    def sources(self) -> Collection[Store]:
        """The mixed sources."""
        return self.get_sources()

    def get_sources(self) -> Collection[Store]:
        """Gets the mixed underlying sources.

        Returns:
           Mixed sources.
        """
        return self._sources

    @property
    def sync_flags(self) -> bool:
        """Whether to sync store flags."""
        return self.get_sync_flags()

    def get_sync_flags(self) -> bool:
        """Tests whether to sync store flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._sync_flags

    @override
    def _set_flags(
            self,
            old: Store.Flags | None,
            new: Store.Flags | None
    ) -> bool:
        if not super()._set_flags(old, new):
            return False
        if self.sync_flags:
            for src in self.sources:
                src.flags = new  # type: ignore
        return True

    @property
    def sync_limit(self) -> bool:
        """Whether to sync store limit."""
        return self.get_sync_limit()

    def get_sync_limit(self) -> bool:
        """Tests whether to sync store limit.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._sync_limit

    @override
    def _set_limit(self, old: int | None, new: int | None) -> bool:
        if not super()._set_limit(old, new):
            return False
        if self.sync_limit:
            for src in self.sources:
                src.set_limit(new)
        return True

    @property
    def sync_page_size(self) -> bool:
        """Whether to sync store page size."""
        return self.get_sync_flags()

    def get_sync_page_size(self) -> bool:
        """Tests whether to sync store page size.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._sync_page_size

    @override
    def _set_page_size(self, old: int | None, new: int | None) -> bool:
        if not super()._set_page_size(old, new):
            return False
        if self.sync_page_size:
            for src in self.sources:
                src.set_page_size(new)
        return True

    @property
    def sync_timeout(self) -> bool:
        """Whether to sync store timeout."""
        return self.get_sync_timeout()

    def get_sync_timeout(self) -> bool:
        """Tests whether to sync store timeout.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._sync_timeout

    @override
    def _set_timeout(self, old: float | None, new: float | None) -> bool:
        if not super()._set_timeout(old, new):
            return False
        if self.sync_timeout:
            for src in self.sources:
                src.set_timeout(new)
        return True

    @override
    def _ask(self, filter: Filter) -> bool:
        return any(map(lambda kb: kb._ask(filter), self._sources))

    @override
    def _count(self, filter: Filter) -> int:
        return sum(map(lambda kb: kb._count(filter), self._sources))

    @override
    def _filter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        its: list[Iterator[Statement]] = [kb._filter_tail(
            filter, limit, distinct) for kb in self._sources]
        count = 0
        seen: set[Statement] = set()
        exausted: set[Iterator[Statement]] = set()
        while count < limit and its:
            for it in its:
                try:
                    stmt = next(it)
                    if stmt not in seen:
                        yield stmt
                        seen.add(stmt)
                        count += 1
                except StopIteration:
                    exausted.add(it)
                    continue
            while exausted:
                its.remove(exausted.pop())

    @override
    async def _afilter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> AsyncIterator[Statement]:
        its: list[AsyncIterator[Statement]] = [kb._afilter_tail(
            filter, limit, distinct) for kb in self._sources]
        count = 0
        exausted: set[AsyncIterator[Statement]] = set()
        while count < limit and its:
            for it in its:
                try:
                    stmt = await it.__anext__()
                    yield stmt
                    count += 1
                except StopAsyncIteration:
                    exausted.add(it)
                    continue
            while exausted:
                its.remove(exausted.pop())
