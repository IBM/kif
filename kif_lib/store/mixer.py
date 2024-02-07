# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import sys
from collections.abc import Callable, Collection, Iterable, Sequence
from itertools import cycle

import more_itertools

from ..model import AnnotationRecordSet, FilterPattern, KIF_Object, Statement
from ..typing import Any, Iterator, Optional, TypeVar
from .abc import Store, StoreFlags

T = TypeVar('T')
S = TypeVar('S')


class MixerStore(Store, type='mixer', description='Mixer store'):
    """Mixer store.

    Parameters:
       store_type: Type of concrete store to instantiate.
       sources: Sources to mix.
       sync_flags: Whether to sync flags.
    """

    __slots__ = (
        '_sources',
        '_sync_flags',
    )

    _sources: Sequence[Store]   # sources to mix
    _sync_flags: bool           # whether to sync flag changes

    def __init__(
            self,
            store_type: str,
            sources: Iterable[Store] = [],
            sync_flags: bool = True,
            **kwargs: Any
    ):
        assert store_type == self.store_type
        super().__init__(**kwargs)
        self._init_sources(sources)
        self._sync_flags = sync_flags

    def _init_sources(self, sources: Iterable[Store]):
        KIF_Object._check_arg_isinstance(
            sources, Iterable, self.__class__, 'sources')
        self._sources = list(map(
            lambda s: KIF_Object._check_arg_isinstance(
                s, Store, self.__class__, 'sources'), sources))

    @property
    def sources(self) -> Iterable[Store]:
        """Underlying sources."""
        return self.get_sources()

    def get_sources(self) -> Iterable[Store]:
        """Get underlying sources.

        Returns:
           Underlying sources.
        """
        return self._sources

    @property
    def sync_flags(self) -> bool:
        """Whether to sync flags."""
        return self.get_sync_flags()

    def get_sync_flags(self) -> bool:
        """Tests whether to sync flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self._sync_flags

    def _do_set_flags(self, old: StoreFlags, new: StoreFlags) -> bool:
        if not super()._do_set_flags(old, new):
            return False
        if self.sync_flags:
            for src in self.sources:
                src.flags = new
        return True

    # -- Queries -----------------------------------------------------------

    def _contains(self, pattern: FilterPattern) -> bool:
        return any(map(lambda kb: kb._contains(pattern), self._sources))

    def _count(self, pattern: FilterPattern) -> int:
        return sum(map(lambda kb: kb._count(pattern), self._sources))

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        its = map(lambda kb: kb._filter(pattern, limit), self._sources)
        return self._filter_mixed(list(its), limit)

    def _filter_mixed(
            self,
            its: Collection[Iterator[T]],
            limit: int = sys.maxsize
    ) -> Iterator[T]:
        cyc = cycle(its)
        exausted: set[Iterator[T]] = set()
        while limit > 0 and len(exausted) < len(its):
            try:
                src = next(cyc)
                if src in exausted:
                    continue    # skip
                yield next(src)
                limit -= 1
            except StopIteration:
                exausted.add(src)

    # -- Annotations -------------------------------------------------------

    def _get_annotations(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        return self._get_x_mixed(
            stmts, None, lambda kb, b: kb._get_annotations_tail(b),
            self._get_annotations_mixed)

    def _get_annotations_mixed(
            self,
            it: Iterator[tuple[Statement, Optional[AnnotationRecordSet]]],
    ) -> tuple[Statement, Optional[AnnotationRecordSet]]:
        stmt, annots = next(it)
        for stmti, annotsi in it:
            assert stmt == stmti
            if annots is not None and annotsi is not None:
                annots = annots.union(annotsi)
            elif annots is None:
                annots = annotsi
        return stmt, annots

    def _get_x_mixed(
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
            batches = more_itertools.batched(it, self.page_size)
            for batch in batches:
                its = list(map(lambda kb: get(kb, batch), self._sources))
                n = 0
                while True:
                    try:
                        yield mix(map(next, its))
                        n += 1
                    except StopIteration:
                        break
                assert len(batch) == n

    # -- Descriptor --------------------------------------------------------

    # def _get_descriptor(
    #         self,
    #         entities: Iterable[Entity],
    #         language: str
    # ) -> Iterator[tuple[Entity, Optional[Descriptor]]]:
    #     return self._get_x_mixed(
    #         entities, None,
    #         lambda kb, b: kb._get_descriptor(b, language),
    #         self._get_descriptor_mixed)

    # def _get_descriptor_mixed(
    #         self,
    #         it: Iterator[tuple[Entity, Optional[Descriptor]]],
    # ) -> tuple[Entity, Optional[Descriptor]]:
    #     entity0, desc = next(it)
    #     found = bool(desc)
    #     label = desc.label if desc is not None else None
    #     aliases = set(desc.aliases) if desc is not None else set()
    #     description = desc.description if desc is not None else None
    #     for entityi, desc in it:
    #         assert entity0 == entityi
    #         if desc is None:
    #             continue
    #         else:
    #             found |= bool(desc)
    #         if label is None and desc.label is not None:
    #             label = desc.label
    #         elif (label is not None
    #               and desc.label is not None and label != desc.label):
    #             aliases.add(desc.label)
    #         aliases.update(desc.aliases)
    #         if description is None and desc.description is not None:
    #             description = desc.description
    #     if found:
    #         return entity0, Descriptor(label, aliases, description)
    #     else:
    #         return entity0, None
