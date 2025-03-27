# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..model import Filter, KIF_Object, Statement
from ..typing import (
    Any,
    Callable,
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
       sync_page_size: Whether to sync page size.
    """

    __slots__ = (
        '_sources',
        '_sync_flags',
        '_sync_page_size',
    )

    _sources: Sequence[Store]
    _sync_flags: bool
    _sync_page_size: bool

    def __init__(
            self,
            store_name: str,
            sources: Iterable[Store] = tuple(),
            sync_flags: bool = True,
            sync_page_size: bool = True,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(**kwargs)
        self._init_sources(sources)
        self._sync_flags = sync_flags
        self._sync_page_size = sync_page_size

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
    def _do_set_flags(self, old: Store.Flags, new: Store.Flags) -> bool:
        if not super()._do_set_flags(old, new):
            return False
        if self.sync_flags:
            for src in self.sources:
                src.flags = new
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
    def _do_set_page_size(self, old: int | None, new: int | None) -> bool:
        if not super()._do_set_page_size(old, new):
            return False
        if self.sync_page_size:
            for src in self.sources:
                src.set_page_size(new)
        return True

    def _mix_get_x(
            self,
            it: Iterable[T],
            empty: S,
            get: Callable[[Store, Iterable[T]], Iterator[tuple[T, S]]],
            mix: Callable[[Iterator[tuple[T, S]]], tuple[T, S]]
    ) -> Iterator[tuple[T, S]]:
        if not self._sources:
            for t in it:
                yield t, empty
        else:
            for batch in self._batched(it):
                its = list(map(lambda kb: get(kb, batch), self._sources))
                n = 0
                while True:
                    try:
                        yield mix(map(next, its))
                        n += 1
                    except StopIteration:
                        break
                assert len(batch) == n

    @override
    def _contains(self, filter: Filter) -> bool:
        return any(map(lambda kb: kb._contains(filter), self._sources))

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
        its = map(
            lambda kb: kb._filter_with_hooks(
                filter, limit, distinct), self._sources)
        return self._filter_mixed(list(its), limit, distinct)

    def _filter_mixed(
            self,
            its: Collection[Iterator[Statement]],
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        cyc = itertools.cycle(its)
        exausted: set[Iterator[Statement]] = set()
        seen: set[Statement] = set()
        while limit > 0 and len(exausted) < len(its):
            src: Iterator[Statement] | None = None
            try:
                src = next(cyc)
                if src in exausted:
                    continue    # skip source
                stmt = next(src)
                if distinct:
                    if stmt in seen:
                        continue  # skip statement
                    seen.add(stmt)
                yield stmt
                limit -= 1
            except StopIteration:
                assert src is not None
                exausted.add(src)
