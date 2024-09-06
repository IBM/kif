# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..cache import Cache
from ..context import Context
from ..error import Error as KIF_Error
from ..error import ShouldNotGetHere
from ..model import (
    AnnotationRecord,
    AnnotationRecordSet,
    ClosedTerm,
    Descriptor,
    Entity,
    Filter,
    Fingerprint,
    Item,
    ItemDescriptor,
    KIF_Object,
    Lexeme,
    LexemeDescriptor,
    Pattern,
    Property,
    PropertyDescriptor,
    Quantity,
    ReferenceRecordSet,
    Snak,
    Statement,
    TFingerprint,
    TPattern,
    TReferenceRecordSet,
)
from ..model.flags import Flags as KIF_Flags
from ..typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Location,
    Sequence,
    Set,
    TypeVar,
)

T = TypeVar('T')
S = TypeVar('S')


class Store(Set):
    """Abstract base class for stores."""

    #: The store plugin registry.
    registry: Final[dict[str, type[Store]]] = {}

    #: The name of this store plugin.
    store_name: ClassVar[str]

    #: The description of this store plugin.
    store_description: ClassVar[str]

    @classmethod
    def _register(
            cls,
            store: type[Store],
            store_name: str,
            store_description: str
    ) -> None:
        store.store_name = store_name
        store.store_description = store_description
        cls.registry[store.store_name] = store

    @classmethod
    def __init_subclass__(
            cls,
            store_name: str,
            store_description: str
    ) -> None:
        Store._register(cls, store_name, store_description)

    def __new__(cls, store_name: str, *args: Any, **kwargs: Any):
        KIF_Object._check_arg(
            store_name, store_name in cls.registry,
            f"no such store plugin '{store_name}'",
            Store, 'store_name', 1, ValueError)
        return super().__new__(cls.registry[store_name])  # pyright: ignore

    class Error(KIF_Error):
        """Base class for store errors."""

    @classmethod
    def _error(cls, details: str) -> Error:
        """Makes a store error.

        Parameters:
           details: Details.

        Returns:
           :class:`Error`.
        """
        return cls.Error(details)

    @classmethod
    def _should_not_get_here(
            cls,
            details: str | None = None
    ) -> ShouldNotGetHere:
        """Makes a "should not get here" error.

        Parameters:
           details: Details.

        Returns:
           :class:`ShouldNotGetHere`.
        """
        return KIF_Object._should_not_get_here(details)

    __slots__ = (
        '_cache',
        '_context',
        '_extra_references',
        '_flags',
        '_limit',
        '_page_size',
        '_timeout',
    )

    def __init__(
            self,
            *args: Any,
            extra_references: TReferenceRecordSet | None = None,
            flags: Flags | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            timeout: int | None = None,
            **kwargs: Any
    ) -> None:
        """
        Initializes :class:`Store`.

        Parameters:
           store_name: Name of the store plugin to instantiate.
           args: Arguments to store plugin.
           extra_references: Extra references to attach to statements.
           flags: Store flags.
           limit: Limit (maximum number) of responses.
           page_size: Page size of paginated responses.
           timeout: Timeout of responses (in seconds).
           kwargs: Keyword arguments to store plugin.
        """
        self._init_flags(flags)
        self._init_cache(self.has_flags(self.CACHE))
        self._init_extra_references(extra_references)
        self._init_limit(limit)
        self._init_page_size(page_size)
        self._init_timeout(timeout)

    @property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        return Context.top(context)

# -- Caching ---------------------------------------------------------------

    #: The store cache.
    _cache: Cache

    def _init_cache(self, enabled: bool) -> None:
        self._cache = Cache(enabled)

    def _cache_get_presence(self, obj: Entity | Statement) -> bool | None:
        """Gets the status of `obj` presence in cache.

        Returns:
           ``True`` if `obj` is present;
           ``False`` if `obj` is not present;
           ``None`` otherwise (`obj` presence is unknown).
        """
        return self._cache.get(obj, 'presence')

    def _cache_set_presence(
            self,
            obj: Entity | Statement,
            status: bool | None = None
    ) -> bool | None:
        """Sets the status of `obj` presence in cache.

        Parameter:
           status: Presence status.

        Returns:
           Status.
        """
        if status is None:
            self._cache.unset(obj, 'presence')
            return None
        else:
            return self._cache.set(obj, 'presence', status)

# -- Extra references ------------------------------------------------------

    @property
    def default_extra_references(self) -> ReferenceRecordSet:
        """The default value for :attr:`Store.extra_references`."""
        return self.get_default_extra_references()

    def get_default_extra_references(self) -> ReferenceRecordSet:
        """Gets the default value for :attr:`Store.extra_references`.

        Returns:
           Reference record set.
        """
        return self.context.options.store.extra_references

    #: Extra references.
    _extra_references: ReferenceRecordSet | None

    def _init_extra_references(
            self,
            extra_references: TReferenceRecordSet | None
    ) -> None:
        self.extra_references = extra_references  # type: ignore

    @property
    def extra_references(self) -> ReferenceRecordSet:
        """The extra references to attach to statements."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(
            self,
            references: TReferenceRecordSet | None = None
    ) -> None:
        self.set_extra_references(references)

    def get_extra_references(
            self,
            default: ReferenceRecordSet | None = None
    ) -> ReferenceRecordSet:
        """Gets the extra references to attach to statements.

        If the extra references is ``None``, returns `default`.

        If `default` is ``None``,
        assumes :attr:`Store.default_extra_references`.

        Parameters:
           default: Default reference record set.

        Returns:
           Reference record set.
        """
        if self._extra_references is not None:
            extra_references: ReferenceRecordSet = self._extra_references
        elif default is not None:
            extra_references = default
        else:
            extra_references = self.default_extra_references
        return extra_references

    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None = None
    ) -> None:
        """Sets the extra references to attach to statements.

        If `extra_references` is ``None``,
        assumes :attr:`Store.default_extra_references`.

        Parameters:
           references: Reference record set.
        """
        self._extra_references =\
            ReferenceRecordSet.check_optional(
                extra_references, None, self.set_extra_references,
                'extra_references', 1)

# -- Flags -----------------------------------------------------------------

    class Flags(KIF_Flags):
        """Store flags."""

        #: Whether to enable cache.
        CACHE = KIF_Flags.auto()

        #: Whether to enable debugging.
        DEBUG = KIF_Flags.auto()

        #: Whether to remove duplicates.
        DISTINCT = KIF_Flags.auto()

        #: Whether to force some ordering.
        ORDER = KIF_Flags.auto()

        #: Whether to fetch only the best ranked statements.
        BEST_RANK = KIF_Flags.auto()

        #: Whether to fetch value snaks.
        VALUE_SNAK = KIF_Flags.auto()

        #: Whether to fetch some-value snaks.
        SOME_VALUE_SNAK = KIF_Flags.auto()

        #: Whether to fetch no-value snaks.
        NO_VALUE_SNAK = KIF_Flags.auto()

        #: Whether to enable early filtering.
        EARLY_FILTER = KIF_Flags.auto()

        #: Whether to enable late filtering.
        LATE_FILTER = KIF_Flags.auto()

        #: All flags.
        ALL = (
            CACHE
            | DEBUG
            | DISTINCT
            | ORDER
            | BEST_RANK
            | VALUE_SNAK
            | SOME_VALUE_SNAK
            | NO_VALUE_SNAK
            | EARLY_FILTER
            | LATE_FILTER)

    #: Whether to enable cache.
    CACHE: Final[Flags] = Flags.CACHE

    #: Whether to enable debugging.
    DEBUG: Final[Flags] = Flags.DEBUG

    #: Whether to remove duplicates.
    DISTINCT: Final[Flags] = Flags.DISTINCT

    #: Whether to force some ordering.
    ORDER: Final[Flags] = Flags.ORDER

    #: Whether to fetch only the best ranked statements.
    BEST_RANK: Final[Flags] = Flags.BEST_RANK

    #: Whether to fetch value snaks.
    VALUE_SNAK: Final[Flags] = Flags.VALUE_SNAK

    #: Whether to fetch some-value snaks.
    SOME_VALUE_SNAK: Final[Flags] = Flags.SOME_VALUE_SNAK

    #: Whether to fetch no-value snaks.
    NO_VALUE_SNAK: Final[Flags] = Flags.NO_VALUE_SNAK

    #: Whether to enable early filtering.
    EARLY_FILTER: Final[Flags] = Flags.EARLY_FILTER

    #: Whether to enable late filtering.
    LATE_FILTER: Final[Flags] = Flags.LATE_FILTER

    @property
    def default_flags(self) -> Flags:
        """The default value for :attr:`Store.flags`."""
        return self.get_default_flags()

    def get_default_flags(self) -> Flags:
        """Gets the default value for :attr:`Store.flags`.

        Returns:
           Default store flags.
        """
        return self.context.options.store.flags

    #: Store flags.
    _flags: Flags

    def _init_flags(self, flags: Flags | None = None) -> None:
        flags = self.Flags.check_optional(
            flags, self.default_flags, type(self), 'flags')
        assert flags is not None
        self._flags = flags

    @property
    def flags(self) -> Flags:
        """The store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Flags) -> None:
        if flags != self._flags and self._do_set_flags(self._flags, flags):
            self._flags = self.Flags(flags)

    def _do_set_flags(self, old: Flags, new: Flags) -> bool:
        self._cache.clear()
        return True

    def get_flags(self) -> Flags:
        """Gets the store flags.

        Returns:
           Store flags.
        """
        return self._flags

    def has_flags(self, flags: Flags) -> bool:
        """Tests whether `flags` are set in store.

        Parameters:
           flags: Store flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return bool(self.flags & flags)

    def set_flags(self, flags: Flags) -> None:
        """Sets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        self.flags |= flags

    def unset_flags(self, flags: Flags) -> None:
        """Unsets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        self.flags &= ~flags

# -- Limit -----------------------------------------------------------------

    @classmethod
    def _check_limit(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(int(Quantity.check(
            arg, function, name, position).amount), 0)

    @classmethod
    def _check_optional_limit(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return cls._check_limit(arg, function, name, position)

    @property
    def max_limit(self) -> int:
        """The maximum value for :attr:`Store.limit`."""
        return self.get_max_limit()

    def get_max_limit(self) -> int:
        """Gets the maximum value for :attr:`Store.limit`.

        Returns:
           Maximum limit.
        """
        return self.context.options.store.max_limit

    @property
    def default_limit(self) -> int | None:
        """The default value for :attr:`Store.limit`."""
        return self.get_default_limit()

    def get_default_limit(self) -> int | None:
        """Gets the default value for :attr:`Store.limit`.

        Returns:
           Default limit or ``None``.
        """
        return self.context.options.store.limit

    #: Limit.
    _limit: int | None

    def _init_limit(self, limit: int | None = None) -> None:
        self.limit = limit  # type: ignore

    @property
    def limit(self) -> int | None:
        """The limit (maximum number) of responses."""
        return self.get_limit()

    @limit.setter
    def limit(self, limit: int | None = None) -> None:
        self.set_limit(limit)

    def get_limit(
            self,
            default: int | None = None
    ) -> int | None:
        """Gets the limit (maximum number) of responses.

        If the limit is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_limit`.

        Parameters:
           default: Default limit.

        Returns:
           Limit or ``None``.
        """
        if self._limit is not None:
            limit: int | None = self._limit
        elif default is not None:
            limit = default
        else:
            limit = self.default_limit
        if limit is None:
            return limit
        else:
            return min(limit, self.max_limit)

    def set_limit(
            self,
            limit: int | None = None
    ) -> None:
        """Sets the limit (maximum number) of responses.

        If `limit` is negative, assumes zero.

        If `limit` is ``None``, assumes: attr: `Store.default_limit`.

        Parameters:
           limit: Limit.
        """
        self._limit = self._check_optional_limit(
            limit, None, self.set_limit, 'limit', 1)

# -- Page size -------------------------------------------------------------

    @classmethod
    def _check_page_size(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        return max(int(Quantity.check(
            arg, function, name, position).amount), 0)

    @classmethod
    def _check_optional_page_size(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return cls._check_page_size(arg, function, name, position)

    @property
    def max_page_size(self) -> int:
        """The maximum value for :attr:`Store.page_size`."""
        return self.get_max_page_size()

    def get_max_page_size(self) -> int:
        """Gets the maximum value for :attr:`Store.page_size`.

        Returns:
           Maximum page size.
        """
        return self.context.options.store.max_page_size

    @property
    def default_page_size(self) -> int:
        """The default value for :attr:`Store.page_size`."""
        return self.get_default_page_size()

    def get_default_page_size(self) -> int:
        """Gets the default value for :attr:`Store.page_size`.

        Returns:
           Default page size.
        """
        return self.context.options.store.page_size

    #: Page size.
    _page_size: int | None

    def _init_page_size(self, page_size: int | None = None) -> None:
        self.page_size = page_size  # type: ignore

    @property
    def page_size(self) -> int:
        """The page size of paginated responses."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: int | None = None) -> None:
        self.set_page_size(page_size)

    def get_page_size(
            self,
            default: int | None = None
    ) -> int:
        """Gets the page size of paginated responses.

        If the page size is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_page_size`.

        Parameters:
           default: Default page size.

        Returns:
           Page size.
        """
        if self._page_size is not None:
            page_size: int = self._page_size
        elif default is not None:
            page_size = default
        else:
            page_size = self.default_page_size
        return min(page_size, self.max_page_size)

    def set_page_size(
            self,
            page_size: int | None = None
    ) -> None:
        """Sets page size of paginated responses.

        If `page_size` is negative, assumes zero.

        If `page_size` is ``None``, assumes: attr: `Store.default_page_size`.

        Parameters:
           page_size: Page size.
        """
        self._page_size = self._check_optional_page_size(
            page_size, None, self.set_page_size, 'page_size', 1)

    def _batched(
            self,
            it: Iterable[T],
            page_size: int | None = None
    ) -> Iterator[Sequence[T]]:
        """Batches `it` into tuples of at most page-size length.

        If `page_size` is ``None``, assumes :attr:`Store.page_size`.

        Parameters:
           it: Iterable.
           page_size: Page size.

        Returns:
           The resulting tuples.
        """
        return itertools.batched(
            it, page_size if page_size is not None else self.page_size)

    def _chain_map_batched(
            self,
            op: Callable[[Iterable[T]], Iterator[S]],
            it: Iterable[T],
            page_size: int | None = None
    ) -> Iterator[S]:
        """Batches `it`, applies `op` to the batches, and chain them.

        If `page_size` is ``None``, assumes :attr:`Store.page_size`.

        Parameters:
           op: Callable.
           it: Iterable.
           page_size: Page size.

        Returns:
           The resulting iterator.
        """
        return itertools.chain.from_iterable(
            map(op, self._batched(it, page_size)))

# -- Timeout ---------------------------------------------------------------

    @classmethod
    def _check_timeout(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float:
        return max(float(Quantity.check(
            arg, function, name, position).amount), 0.)

    @classmethod
    def _check_optional_timeout(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> float | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return cls._check_timeout(arg, function, name, position)

    @property
    def max_timeout(self) -> float:
        """The maximum value for :attr:`Store.timeout`."""
        return self.get_max_timeout()

    def get_max_timeout(self) -> float:
        """Gets the maximum value for :attr:`Store.timeout`.

        Returns:
           Maximum timeout (in seconds).
        """
        return self.context.options.store.max_timeout

    @property
    def default_timeout(self) -> float | None:
        """The default value for :attr:`Store.timeout`."""
        return self.get_default_timeout()

    def get_default_timeout(self) -> float | None:
        """Gets the default value for :attr:`Store.timeout`.

        Returns:
           Timeout or ``None``.
        """
        return self.context.options.store.timeout

    #: Timeout (in seconds).
    _timeout: float | None

    def _init_timeout(self, timeout: float | None = None) -> None:
        self.timeout = timeout  # type: ignore

    @property
    def timeout(self) -> float | None:
        """The timeout of responses (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: float | None = None) -> None:
        self.set_timeout(timeout)

    def get_timeout(
            self,
            default: float | None = None
    ) -> float | None:
        """Gets the timeout of responses (in seconds).

        If the timeout is ``None``, returns `default`.

        If `default` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           default: Default timeout.

        Returns:
           Timeout or ``None``.
        """
        if self._timeout is not None:
            timeout: float | None = self._timeout
        elif default is not None:
            timeout = default
        else:
            timeout = self.default_timeout
        if timeout is None:
            return timeout
        else:
            return min(timeout, self.max_timeout)

    def set_timeout(
            self,
            timeout: float | None = None
    ) -> None:
        """Sets the timeout of responses (in seconds).

        If `timeout` is negative, assumes zero.

        If `timeout` is ``None``, assumes :attr:`Store.default_timeout`.

        Parameters:
           timeout: Timeout.
        """
        self._timeout = self._check_optional_timeout(
            timeout, None, self.set_timeout, 'timeout', 1)

# -- Match -----------------------------------------------------------------

    def match(
            self,
            pattern: TPattern,
            limit: int | None = None,
            distinct: bool | None = None
    ) -> Iterator[ClosedTerm]:
        """Searches for terms matching `pattern`.

        Parameters:
           pattern: Pattern.
           limit: Limit (maximum number) of matches to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of closed-terms matching pattern.
        """
        pattern = Pattern.check(pattern, self.match, 'pattern', 1)
        limit = self._as_limit(limit, self.match, 'limit', 2)
        distinct = self._as_distinct(distinct, self.match, 'distinct', 3)
        return self._match(pattern, limit, distinct)

    def _match(
            self,
            pattern: Pattern,
            limit: int,
            distinct: bool
    ) -> Iterator[ClosedTerm]:
        return iter(())

    def _as_limit(
            self,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        limit = self._check_optional_limit(
            arg, self.default_limit, function, name, position)
        return self.max_limit if limit is None else limit

    def _as_distinct(
            self,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> bool:
        distinct = KIF_Object._check_optional_arg_bool(
            arg, self.has_flags(self.DISTINCT), function, name, position)
        assert isinstance(distinct, bool)
        return distinct

# -- Set interface ---------------------------------------------------------

    def __contains__(self, v: Any) -> bool:
        return self.contains(v) if isinstance(v, Statement) else False

    def __iter__(self) -> Iterator[Statement]:
        return self.filter()

    def __len__(self) -> int:
        return self.count()

# -- Statements ------------------------------------------------------------

    def contains(self, stmt: Statement) -> bool:
        """Tests whether statement is in store.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        Statement.check(stmt, self.contains, 'stmt', 1)
        status = self._cache_get_presence(stmt)
        if status is None:
            filter = self._normalize_filter(
                Filter.from_statement(stmt))
            status = self._contains_tail(filter)
            status = self._cache_set_presence(stmt, status)
        assert status is not None
        return status

    def _contains_tail(self, filter: Filter) -> bool:
        if filter.is_nonempty():
            return self._contains(filter)
        else:
            return False

    def _contains(self, filter: Filter) -> bool:
        return False

    def count(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None
    ) -> int:
        """Counts statements matching filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           snak: Snak.
           filter: Filter.

        Returns:
           The number of statements matching filter.
        """
        return self._count_tail(self._check_filter(
            subject, property, value, snak_mask, snak, filter, self.count))

    def _count_tail(self, filter: Filter) -> int:
        if filter.is_nonempty():
            return self._count(filter)
        else:
            return 0

    def _count(self, filter: Filter) -> int:
        return 0

    def _check_filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            function: Location | None = None
    ) -> Filter:
        subj = Fingerprint.check_optional(
            subject, None, function, 'subject', 1)
        prop = Fingerprint.check_optional(
            property, None, function, 'property', 2)
        val = Fingerprint.check_optional(
            value, None, function, 'value', 3)
        mask = Filter.SnakMask.check_optional(
            snak_mask, Filter.SnakMask.ALL, function, 'snak_mask', 4)
        if filter is None:
            filter = Filter(subj, prop, val, mask)
        else:
            filter = Filter.check(filter, function, 'filter', 6).combine(
                Filter(subj, prop, val, mask))
        if snak is not None:
            filter = filter.combine(Filter.from_snak(None, Snak.check(
                snak, function, 'snak', 5)))
        return self._normalize_filter(filter)

    def _normalize_filter(
            self,
            filter: Filter
    ) -> Filter:
        store_snak_mask = Filter.SnakMask(0)
        if self.has_flags(self.VALUE_SNAK):
            store_snak_mask |= Filter.VALUE_SNAK
        if self.has_flags(self.SOME_VALUE_SNAK):
            store_snak_mask |= Filter.SOME_VALUE_SNAK
        if self.has_flags(self.NO_VALUE_SNAK):
            store_snak_mask |= Filter.NO_VALUE_SNAK
        return filter.normalize().replace(
            filter.KEEP, filter.KEEP, filter.KEEP,
            filter.snak_mask & store_snak_mask)

    def filter(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            limit: int | None = None,
            distinct: bool | None = None
    ) -> Iterator[Statement]:
        """Searches for statements matching filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           snak: Snak.
           filter: Filter filter.
           limit: Limit (maximum number) of statements to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of statements matching filter.
        """
        filter = self._check_filter(
            subject, property, value, snak_mask, snak, filter, self.filter)
        limit = self._as_limit(limit, self.filter, 'limit', 7)
        distinct = self._as_distinct(distinct, self.filter, 'distinct', 8)
        return self._filter_with_hooks(filter, limit, distinct)

    def _filter_with_hooks(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        filter, limit, distinct, data = self._filter_pre_hook(
            filter, limit, distinct)
        it_in: Iterator[Statement]
        it_out: Iterator[Statement]
        if limit > 0 and filter.is_nonempty():
            it_in = self._filter(filter, limit, distinct)
        else:
            it_in = iter(())
        it_out = self._filter_post_hook(filter, limit, distinct, data, it_in)
        if distinct:
            it_out = itertools.unique_everseen(it_out)
        return itertools.islice(it_out, limit)

    def _filter_pre_hook(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> tuple[Filter, int, bool, Any]:
        return filter, limit, distinct, None

    def _filter_post_hook(
            self,
            filter: Filter,
            limit: int,
            distinct: bool,
            data: Any,
            it: Iterator[Statement]
    ) -> Iterator[Statement]:
        return it

    def _filter(
            self,
            filter: Filter,
            limit: int,
            distinct: bool
    ) -> Iterator[Statement]:
        return iter(())

# -- Annotations -----------------------------------------------------------

    def filter_annotated(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            limit: int | None = None
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        """:meth:`Store.filter` with annotations.

        Same as :meth:`Store.filter` followed by
        :meth:`Store.get_annotations`.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           snak: Snak.
           filter: Filter.
           limit: Maximum number of statements to return .

        Returns:
           An iterator of pairs "(statement, annotation record set)".
        """
        return self._filter_annotated_tail(self.filter(
            subject, property, value, snak_mask, snak, filter, limit))

    def _filter_annotated_tail(
            self,
            it: Iterator[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet]]:
        for stmt, annots in self.get_annotations(it):
            assert annots is not None
            yield stmt, annots

    def get_annotations(
            self,
            stmts: Statement | Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        """Gets annotation records of statements.

        Parameters:
           stmts: Statements.

        Returns:
           An iterator of pairs "(statement, annotation record set)".
        """
        KIF_Object._check_arg_isinstance(
            stmts, (Statement, Iterable), self.get_annotations, 'stmts', 1)
        return self._get_annotations_tail(stmts)

    def _get_annotations_tail(
            self,
            stmts: Statement | Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        if isinstance(stmts, Statement):
            it = self._get_annotations_with_hooks((stmts,))
        else:
            it = self._get_annotations_with_hooks(map(
                lambda s: cast(Statement, Statement.check(
                    s, self.get_annotations)), stmts))
        if self.extra_references:
            return self._get_annotations_attach_extra_references(it)
        else:
            return it

    def _get_annotations_attach_extra_references(
            self,
            it: Iterator[tuple[Statement, AnnotationRecordSet | None]]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        for stmt, annots in it:
            if annots is None:
                yield stmt, annots
            else:
                def patch(a: AnnotationRecord):
                    return AnnotationRecord(
                        a.qualifiers,
                        a.references.union(self.extra_references),
                        a.rank)
                yield stmt, AnnotationRecordSet(*map(patch, annots))

    def _get_annotations_with_hooks(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        return self._get_annotations_post_hook(
            *self._get_annotations_pre_hook(stmts),
            self._get_annotations(stmts))

    def _get_annotations_pre_hook(
            self,
            stmts: Iterable[Statement]
    ) -> tuple[Iterable[Statement], Any]:
        return stmts, None

    def _get_annotations_post_hook(
            self,
            stmts: Iterable[Statement],
            data: Any,
            it: Iterator[tuple[Statement, AnnotationRecordSet | None]]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        return it

    def _get_annotations(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[tuple[Statement, AnnotationRecordSet | None]]:
        return map(lambda stmt: (stmt, None), stmts)

# -- Descriptors -----------------------------------------------------------

    def get_descriptor(
            self,
            entities: Entity | Iterable[Entity],
            language: str | None = None,
            mask: Descriptor.TAttributeMask | None = None
    ) -> Iterator[tuple[Entity, Descriptor | None]]:
        """Gets the descriptor of `entities`.

        Parameters:
           entities: Entities.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(entity, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            entities, (Entity, Iterable), self.get_descriptor, 'entities', 1)
        language = KIF_Object._check_optional_arg_str(
            language, self.context.options.language,
            self.get_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor.AttributeMask.check_optional(
            mask, Descriptor.ALL, self.get_descriptor, 'mask', 3)
        assert mask is not None
        if isinstance(entities, Entity):
            return self._get_descriptor_tail((entities,), language, mask)
        else:
            return self._get_descriptor_tail(map(
                lambda e: cast(Entity, Entity.check(
                    e, self.get_descriptor)), entities), language, mask)

    def _get_descriptor_tail(
            self,
            entities: Iterable[Entity],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Entity, Descriptor | None]]:
        return self._chain_map_batched(
            lambda batch: self._get_descriptor(batch, language, mask),
            entities, min(3 * self.page_size, self.max_page_size))

    def _get_descriptor(
            self,
            entities: Iterable[Entity],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Entity, Descriptor | None]]:
        items: list[Item] = []
        properties: list[Property] = []
        lexemes: list[Lexeme] = []
        for entity in entities:
            if isinstance(entity, Item):
                items.append(entity)
            elif isinstance(entity, Property):
                properties.append(entity)
            elif isinstance(entity, Lexeme):
                lexemes.append(entity)
            else:
                raise self._should_not_get_here()
        desc = dict(itertools.chain(
            self._get_item_descriptor(items, language, mask)
            if items else iter(()),
            self._get_property_descriptor(properties, language, mask)
            if properties else iter(()),
            self._get_lexeme_descriptor(lexemes, mask)
            if lexemes else iter(())))
        for entity in entities:
            assert entity in desc
            yield entity, desc[entity]

    def get_item_descriptor(
            self,
            items: Item | Iterable[Item],
            language: str | None = None,
            mask: Descriptor.TAttributeMask | None = None
    ) -> Iterator[tuple[Item, ItemDescriptor | None]]:
        """Gets the descriptor of `items`.

        Parameters:
           items: Items.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(item, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            items, (Item, Iterable),
            self.get_item_descriptor, 'items', 1)
        language = KIF_Object._check_optional_arg_str(
            language, self.context.options.language,
            self.get_item_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor.AttributeMask.check_optional(
            mask, Descriptor.ALL, self.get_item_descriptor, 'mask', 3)
        assert mask is not None
        if isinstance(items, Item):
            return self._get_item_descriptor_tail((items,), language, mask)
        else:
            return self._get_item_descriptor_tail(map(
                lambda e: cast(Item, Item.check(
                    e, self.get_item_descriptor)), items), language, mask)

    def _get_item_descriptor_tail(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, ItemDescriptor | None]]:
        return self._chain_map_batched(
            lambda batch: self._get_item_descriptor(batch, language, mask),
            items)

    def _get_item_descriptor(
            self,
            items: Iterable[Item],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Item, ItemDescriptor | None]]:
        return map(lambda item: (item, None), items)

    def get_property_descriptor(
            self,
            properties: Property | Iterable[Property],
            language: str | None = None,
            mask: Descriptor.TAttributeMask | None = None
    ) -> Iterator[tuple[Property, PropertyDescriptor | None]]:
        """Gets the descriptor of `properties`.

        Parameters:
           properties: Properties.
           language: Language tag.
           mask: Descriptor mask.

        Returns:
           An iterator of pairs "(property, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            properties, (Property, Iterable),
            self.get_property_descriptor, 'properties', 1)
        language = KIF_Object._check_optional_arg_str(
            language, self.context.options.language,
            self.get_property_descriptor, 'language', 2)
        assert language is not None
        mask = Descriptor.AttributeMask.check_optional(
            mask, Descriptor.ALL, self.get_property_descriptor, 'mask', 3)
        assert mask is not None
        if isinstance(properties, Property):
            return self._get_property_descriptor_tail(
                (properties,), language, mask)
        else:
            return self._get_property_descriptor_tail(map(
                lambda e: cast(Property, Property.check(
                    e, self.get_property_descriptor)),
                properties), language, mask)

    def _get_property_descriptor_tail(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, PropertyDescriptor | None]]:
        return self._chain_map_batched(
            lambda batch: self._get_property_descriptor(batch, language, mask),
            properties)

    def _get_property_descriptor(
            self,
            properties: Iterable[Property],
            language: str,
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Property, PropertyDescriptor | None]]:
        return map(lambda property: (property, None), properties)

    def get_lexeme_descriptor(
            self,
            lexemes: Lexeme | Iterable[Lexeme],
            mask: Descriptor.TAttributeMask | None = None
    ) -> Iterator[tuple[Lexeme, LexemeDescriptor | None]]:
        """Gets the descriptor of `lexemes`.

        Parameters:
           lexemes: Lexemes.

        Returns:
           An iterator of pairs "(lexeme, descriptor)".
        """
        KIF_Object._check_arg_isinstance(
            lexemes, (Lexeme, Iterable),
            self.get_lexeme_descriptor, 'lexemes', 1)
        mask = Descriptor.AttributeMask.check_optional(
            mask, Descriptor.ALL, self.get_lexeme_descriptor, 'mask', 3)
        assert mask is not None
        if isinstance(lexemes, Lexeme):
            return self._get_lexeme_descriptor_tail((lexemes,), mask)
        else:
            return self._get_lexeme_descriptor_tail(map(
                lambda e: cast(Lexeme, Lexeme.check(
                    e, self.get_lexeme_descriptor)), lexemes), mask)

    def _get_lexeme_descriptor_tail(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, LexemeDescriptor | None]]:
        return self._chain_map_batched(
            lambda batch: self._get_lexeme_descriptor(batch, mask), lexemes)

    def _get_lexeme_descriptor(
            self,
            lexemes: Iterable[Lexeme],
            mask: Descriptor.AttributeMask
    ) -> Iterator[tuple[Lexeme, LexemeDescriptor | None]]:
        return map(lambda lexeme: (lexeme, None), lexemes)
