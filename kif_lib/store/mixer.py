# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import dataclasses
import functools

from .. import itertools
from ..model import Filter, KIF_Object, Statement
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

# -- Statements ------------------------------------------------------------

    @override
    def _ask(self, filter: Filter) -> bool:
        return any(map(lambda src: src._ask(filter), self._sources))

    @override
    async def _aask(self, filter: Filter) -> bool:
        tasks = (
            asyncio.ensure_future(src._aask(filter))
            for src in self._sources)
        return any(await asyncio.gather(*tasks))

    @override
    def _count(self, filter: Filter) -> int:
        return sum(map(lambda src: src._count(filter), self._sources))

    @override
    async def _acount(self, filter: Filter) -> int:
        tasks = (
            asyncio.ensure_future(src._acount(filter))
            for src in self._sources)
        return sum(await asyncio.gather(*tasks))

    @override
    def _filter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> Iterator[Statement]:
        return itertools.mix(
            *(src._filter_tail(filter, src.options.copy())
              for src in self.sources),
            distinct=options.distinct, limit=options.limit)

    @override
    def _afilter(
            self,
            filter: Filter,
            options: Store.Options
    ) -> AsyncIterator[Statement]:
        return itertools.amix(
            *(src._afilter_tail(filter, src.options.copy())
              for src in self.sources),
            distinct=options.distinct, limit=options.limit)
