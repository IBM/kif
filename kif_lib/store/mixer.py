# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import dataclasses
import functools

from .. import itertools
from ..model import Entity, Filter, KIF_Object, Statement
from ..model.flags import Flags as KIF_Flags
from ..typing import (
    Any,
    AsyncIterator,
    Callable,
    ClassVar,
    Collection,
    Final,
    Iterable,
    Iterator,
    Location,
    override,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
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
       sync_flags: Sync flags.
    """

    class SyncFlags(KIF_Flags):
        """Sync flags.

        The sync flags determine which option changes are propagated to the
        child stores.
        """

        #: Whether to propagate changes in base filter option.
        BASE_FILTER = KIF_Flags.auto()

        #: Whether to propagate changes in best-ranked option.
        BEST_RANKED = KIF_Flags.auto()

        #: Whether to propagate changes in debug option.
        DEBUG = KIF_Flags.auto()

        #: Whether to propagate changes in distinct option.
        DISTINCT = KIF_Flags.auto()

        #: Whether to propagate changes in distinct window-size option.
        DISTINCT_WINDOW_SIZE = KIF_Flags.auto()

        #: Whether to propagate changes in limit option.
        LIMIT = KIF_Flags.auto()

        #: Whether to propagate changes in lookahead option.
        LOOKAHEAD = KIF_Flags.auto()

        #: Whether to propagate changes in page size option.
        PAGE_SIZE = KIF_Flags.auto()

        #: Whether to propagate changes in timeout option.
        TIMEOUT = KIF_Flags.auto()

        #: All sync flags.
        ALL = (
            BASE_FILTER
            | BEST_RANKED
            | DEBUG
            | DISTINCT
            | DISTINCT_WINDOW_SIZE
            | LIMIT
            | LOOKAHEAD
            | PAGE_SIZE
            | TIMEOUT)

    #: Whether to propagate changes in base filter option.
    BASE_FILTER: Final[SyncFlags] = SyncFlags.BASE_FILTER

    #: Whether to propagate changes in best-ranked option.
    BEST_RANKED: Final[SyncFlags] = SyncFlags.BEST_RANKED

    #: Whether to propagate changes in debug option.
    DEBUG: Final[SyncFlags] = SyncFlags.DISTINCT

    #: Whether to propagate changes in distinct option.
    DISTINCT: Final[SyncFlags] = SyncFlags.DISTINCT

    #: Whether to propagate changes in distinct window-size option.
    DISTINCT_WINDOW_SIZE: Final[SyncFlags] = SyncFlags.DISTINCT

    #: Whether to propagate changes in limit option.
    LIMIT: Final[SyncFlags] = SyncFlags.LIMIT

    #: Whether to propagate changes in lookahead option.
    LOOKAHEAD: Final[SyncFlags] = SyncFlags.LOOKAHEAD

    #: Whether to propagate changes in page size option.
    PAGE_SIZE: Final[SyncFlags] = SyncFlags.PAGE_SIZE

    #: Whether to propagate changes in timeout option.
    TIMEOUT: Final[SyncFlags] = SyncFlags.TIMEOUT

    #: Type alias for types coercible to :class:`SyncFlags`.
    TSyncFlags: TypeAlias = Union[SyncFlags, int]

    @dataclasses.dataclass
    class _Options(Store.Options):

        _v_best_ranked: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_MIXER_STORE_BEST_RANKED',), None)

        _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_MIXER_STORE_DEBUG',), None)

        _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_MIXER_STORE_DISTINCT',), None)

        _v_max_distinct_window_size: ClassVar[
            tuple[Iterable[str], int | None]] = (
                (('KIF_MIXER_STORE_MAX_DISTINCT_WINDOW_SIZE',), None))

        _v_distinct_window_size: ClassVar[
            tuple[Iterable[str], int | None]] = (
                (('KIF_MIXER_STORE_DISTINCT_WINDOW_SIZE',), None))

        _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_MIXER_STORE_MAX_LIMIT',), None)

        _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_MIXER_STORE_LIMIT',), None)

        _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_MIXER_STORE_LOOKAHEAD',), None)

        _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_MIXER_STORE_MAX_PAGE_SIZE',), None)

        _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_MIXER_STORE_PAGE_SIZE',), None)

        _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_MIXER_STORE_MAX_TIMEOUT',), None)

        _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_MIXER_STORE_TIMEOUT',), None)

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self._init_sync_flags(kwargs)

        # -- sync_flags --

        #: The default value for the sync flags option
        DEFAULT_SYNC_FLAGS: ClassVar[int] = -1

        _sync_flags: MixerStore.SyncFlags | None

        def _init_sync_flags(self, kwargs: dict[str, Any]) -> None:
            self.sync_flags = kwargs.get(
                '_sync_flags', self.DEFAULT_SYNC_FLAGS)

        @property
        def sync_flags(self) -> MixerStore.SyncFlags:
            """Determines the option changes to propagate to children."""
            return self.get_sync_flags()

        @sync_flags.setter
        def sync_flags(self, sync_flags: MixerStore.TSyncFlags) -> None:
            self.set_sync_flags(sync_flags)

        def get_sync_flags(self) -> MixerStore.SyncFlags:
            """Gets the sync flags option.

            Returns:
               Sync flags.
            """
            assert self._sync_flags is not None
            return self._sync_flags

        def set_sync_flags(
                self,
                sync_flags: MixerStore.TSyncFlags,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the sync flags option.

            Parameters:
               sync_flags: Sync flags.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._sync_flags = MixerStore.SyncFlags.check(
                sync_flags, function, name, position)

    @dataclasses.dataclass
    class Options(_Options, name='mixer'):
        """Mixer store options."""

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)

        @override
        def get_sync_flags(self) -> MixerStore.SyncFlags:
            return self._do_get('_sync_flags', super().get_sync_flags)

        @override
        def set_sync_flags(
                self,
                sync_flags: MixerStore.TSyncFlags | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(sync_flags, '_sync_flags', functools.partial(
                super().set_sync_flags,
                function=function, name=name, position=position))

    __slots__ = (
        '_sources',
    )

    _sources: Sequence[Store]

    def __init__(
            self,
            store_name: str,
            sources: Iterable[Store] = tuple(),
            sync_flags: TSyncFlags | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        self._init_sources(sources)
        super().__init__(**kwargs)

    @property
    def default_options(self) -> Options:
        return super().default_options  # type: ignore

    @override
    def get_default_options(self) -> Options:
        return self.context.options.store.mixer

    @property
    def options(self) -> Options:
        return super().options  # type: ignore

    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'sync_flags' in kwargs:
            self.set_sync_flags(kwargs['sync_flags'])

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

# -- Sync flags ------------------------------------------------------------

    @property
    def default_sync_flags(self) -> SyncFlags:
        """The default value for :attr:`MixerStore.sync_flags`."""
        return self.get_default_sync_flags()

    def get_default_sync_flags(self) -> SyncFlags:
        """Gets the default value for :attr:`MixerStore.sync_flags`.

        Returns:
           Default sync flags.
        """
        return self.default_options.sync_flags

    @property
    def sync_flags(self) -> SyncFlags:
        """The sync flags of mixer."""
        return self.get_sync_flags()

    @sync_flags.setter
    def sync_flags(self, sync_flags: TSyncFlags | None = None) -> None:
        self.set_sync_flags(sync_flags)

    def get_sync_flags(self) -> SyncFlags:
        """Gets the sync flags of mixer.

        Returns:
           Sync flags.
        """
        return self.options.sync_flags

    def set_sync_flags(self, sync_flags: TSyncFlags | None = None) -> None:
        """Sets the sync flags of mixer.

        If `sync_flags` is ``None``, resets it to the default.

        Parameters:
           sync_flags: Sync flags.
        """
        self._set_option_with_hooks(
            sync_flags,
            self.options.get_sync_flags,
            functools.partial(
                self.options.set_sync_flags,
                function=self.set_sync_flags,
                name='sync_flags',
                position=1),
            self._set_sync_flags)

    def _set_sync_flags(self, sync_flags: SyncFlags) -> bool:
        return True

    @override
    def _set_base_filter(self, base_filter: Filter) -> bool:
        return self._set_x(
            Store.set_base_filter, base_filter, self.BASE_FILTER)

    @override
    def _set_best_ranked(self, best_ranked: bool) -> bool:
        return self._set_x(
            Store.set_best_ranked, best_ranked, self.BEST_RANKED)

    @override
    def _set_debug(self, debug: bool) -> bool:
        return self._set_x(Store.set_debug, debug, self.DEBUG)

    @override
    def _set_distinct(self, distinct: bool) -> bool:
        return self._set_x(Store.set_distinct, distinct, self.DISTINCT)

    @override
    def _set_distinct_window_size(self, distinct_window_size: int) -> bool:
        return self._set_x(
            Store.set_distinct_window_size,
            distinct_window_size, self.DISTINCT_WINDOW_SIZE)

    @override
    def _set_limit(self, limit: int | None) -> bool:
        return self._set_x(Store.set_limit, limit, self.LIMIT)

    @override
    def _set_lookahead(self, lookahead: int) -> bool:
        return self._set_x(Store.set_lookahead, lookahead, self.LOOKAHEAD)

    @override
    def _set_page_size(self, page_size: int) -> bool:
        return self._set_x(Store.set_page_size, page_size, self.PAGE_SIZE)

    @override
    def _set_timeout(self, timeout: float | None) -> bool:
        return self._set_x(Store.set_timeout, timeout, self.TIMEOUT)

    def _set_x(
            self,
            set_fn: Callable[[Store, T], None],
            value: T,
            sync_flag: SyncFlags
    ) -> bool:
        if self.sync_flags & sync_flag:
            for src in self.sources:
                set_fn(src, value)
        return True

# -- Ask -------------------------------------------------------------------

    @override
    def _ask(self, filter: Filter, options: Store.Options) -> bool:
        return any(map(lambda src: src._ask(filter, options), self._sources))

    @override
    async def _aask(self, filter: Filter, options: Store.Options) -> bool:
        tasks = (
            asyncio.ensure_future(src._aask(filter, options))
            for src in self._sources)
        return any(await asyncio.gather(*tasks))

# -- Count -----------------------------------------------------------------

    @override
    def _count(self, filter: Filter, options: Store.Options) -> int:
        return sum(map(
            lambda src: src._count(filter, options), self._sources))

    @override
    async def _acount(self, filter: Filter, options: Store.Options) -> int:
        tasks = (
            asyncio.ensure_future(src._acount(filter, options))
            for src in self._sources)
        return sum(await asyncio.gather(*tasks))

# -- Filter ----------------------------------------------------------------

    @override
    def _filter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Statement]:
        get_synced_options = functools.partial(
            self._filter_get_synced_source_options, options)
        return itertools.mix(
            *(src._filter_tail(filter, get_synced_options(src))
              for src in self.sources),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=options.limit)

    def _filter_get_synced_source_options(
            self,
            options: Store.Options,
            source: Store
    ) -> Store.Options:
        source_options = source.options.copy()
        if self.sync_flags & self.BASE_FILTER:
            source_options.base_filter = options.base_filter
        if self.sync_flags & self.BEST_RANKED:
            source_options.best_ranked = options.best_ranked
        if self.sync_flags & self.DEBUG:
            source_options.debug = options.debug
        if self.sync_flags & self.DISTINCT:
            source_options.distinct = options.distinct
        if self.sync_flags & self.DISTINCT_WINDOW_SIZE:
            source_options.distinct_window_size =\
                options.distinct_window_size
        if self.sync_flags & self.LIMIT:
            source_options.limit = options.limit
        if self.sync_flags & self.LOOKAHEAD:
            source_options.lookahead = options.lookahead
        if self.sync_flags & self.PAGE_SIZE:
            source_options.page_size = options.page_size
        if self.sync_flags & self.TIMEOUT:
            source_options.timeout = options.timeout
        return source_options

    @override
    def _filter_s(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Entity]:
        return self._filter_x_mix_sources(
            lambda s: s._filter_s, filter, options)

    def _filter_x_mix_sources(
            self,
            get_filter_x_fn: Callable[
                [Store], Callable[[Filter, Store.Options], Iterator[T]]],
            filter: Filter,
            options: Store.Options
    ) -> Iterator[T]:
        return itertools.mix(
            *(src._filter_x_tail(
                get_filter_x_fn(src), filter, src.options.copy())
              for src in self.sources),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=options.limit)

    @override
    def _afilter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Statement]:
        return itertools.amix(
            *(src._afilter_tail(filter, src.options.copy())
              for src in self.sources),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=options.limit)

    @override
    def _afilter_s(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Entity]:
        return self._afilter_x_mix_sources(
            lambda s: s._afilter_s, filter, options)

    def _afilter_x_mix_sources(
            self,
            get_afilter_x_fn: Callable[
                [Store], Callable[[Filter, Store.Options], AsyncIterator[T]]],
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[T]:
        return itertools.amix(
            *(src._afilter_x_tail(
                get_afilter_x_fn(src), filter, src.options.copy())
              for src in self.sources),
            distinct=options.distinct,
            distinct_window_size=options.distinct_window_size,
            limit=options.limit)
