# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..model import (
    AnnotationRecordSet,
    Descriptor,
    Filter,
    Item,
    ItemDescriptor,
    KIF_Object,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Statement,
)
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


class MixerStore(Store, store_name='mixer', store_description='Mixer store'):
    """Mixer store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       sources: Sources to mix.
       sync_flags: Whether to sync store flags.
    """

    __slots__ = (
        '_sources',
        '_sync_flags',
    )

    _sources: Sequence[Store]
    _sync_flags: bool

    def __init__(
            self,
            store_name: str,
            sources: Iterable[Store] = tuple(),
            sync_flags: bool = True,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(**kwargs)
        self._init_sources(sources)
        self._sync_flags = sync_flags

    def _init_sources(self, sources: Iterable[Store]) -> None:
        KIF_Object._check_arg_isinstance(
            sources, Iterable, self.__class__, 'sources', 2)
        self._sources = [
            KIF_Object._check_arg(
                src, isinstance(src, Store),
                'expected Iterable[Store]',
                self.__class__, 'sources', 2, TypeError)
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

    def _do_set_flags(self, old: Store.Flags, new: Store.Flags) -> bool:
        if not super()._do_set_flags(old, new):
            return False
        if self.sync_flags:
            for src in self.sources:
                src.flags = new
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

# -- Statements ------------------------------------------------------------

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
            lambda kb: kb._filter_with_hooks(filter, limit, distinct),
            self._sources)
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

# -- Annotations -----------------------------------------------------------

    @override
    def _get_annotations(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        return self._mix_get_x(
            stmts, None, lambda kb, b: kb._get_annotations_tail(b),
            self._get_annotations_mixed)

    def _get_annotations_mixed(
            self,
            it: Iterator[tuple[Statement, AnnotationRecordSet | None]],
    ) -> tuple[Statement, AnnotationRecordSet | None]:
        stmt, annots = next(it)
        for stmti, annotsi in it:
            assert stmt == stmti
            if annots is not None and annotsi is not None:
                annots = annots.union(annotsi)
            elif annots is None:
                annots = annotsi
        return stmt, annots

# -- Descriptors -----------------------------------------------------------

    @override
    def _get_item_descriptor(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, ItemDescriptor | None]]:
        return self._get_x_descriptor(
            items,
            lambda kb, batch: kb._get_item_descriptor(batch, language, mask),
            self._merge_item_descriptors)

    def _merge_item_descriptors(
            self,
            d1: ItemDescriptor | None,
            d2: ItemDescriptor | None
    ) -> ItemDescriptor:
        assert d1 is not None
        assert d2 is not None
        return ItemDescriptor(
            d1.label if d1.label is not None else d2.label,
            d1.aliases.union(d2.aliases),
            d1.description if d1.description is not None else d2.description)

    @override
    def _get_property_descriptor(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, PropertyDescriptor | None]]:
        return self._get_x_descriptor(
            properties,
            lambda kb, batch:
            kb._get_property_descriptor(batch, language, mask),
            self._merge_property_descriptors)

    def _merge_property_descriptors(
            self,
            d1: PropertyDescriptor | None,
            d2: PropertyDescriptor | None
    ) -> PropertyDescriptor:
        assert d1 is not None
        assert d2 is not None
        return PropertyDescriptor(
            d1.label if d1.label is not None else d2.label,
            d1.aliases.union(d2.aliases),
            d1.description if d1.description is not None else d2.description,
            d1.datatype if d1.datatype is not None else d2.datatype)

    @override
    def _get_lexeme_descriptor(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, LexemeDescriptor | None]]:
        return self._get_x_descriptor(
            lexemes,
            lambda kb, batch: kb._get_lexeme_descriptor(batch, mask),
            self._merge_lexeme_descriptors)

    def _merge_lexeme_descriptors(
            self,
            d1: LexemeDescriptor | None,
            d2: LexemeDescriptor | None
    ) -> LexemeDescriptor:
        assert d1 is not None
        assert d2 is not None
        return LexemeDescriptor(
            d1.lemma if d1.lemma is not None else d2.lemma,
            d1.category if d1.category is not None else d2.category,
            d1.language if d1.language is not None else d2.language)

    def _get_x_descriptor(
            self,
            entities: Iterable[T],
            get: Callable[[Store, Iterable[T]],
                          Iterator[tuple[T, S | None]]],
            merge: Callable[[S, S], S]
    ) -> Iterator[tuple[T, S | None]]:
        desc: dict[T, S] = {}
        for kb in self._sources:
            for entity, entity_desc in get(kb, entities):
                if entity_desc is None:
                    continue
                if entity not in desc:
                    desc[entity] = entity_desc
                else:
                    desc[entity] = merge(desc[entity], entity_desc)
        for entity in entities:
            if entity in desc:
                yield entity, desc[entity]
            else:
                yield entity, None
