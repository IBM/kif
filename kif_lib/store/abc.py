# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..cache import Cache
from ..context import Context
from ..error import Error as KIF_Error
from ..error import ShouldNotGetHere
from ..model import (
    AnnotatedStatement,
    Entity,
    Filter,
    Fingerprint,
    KIF_Object,
    Quantity,
    ReferenceRecordSet,
    Snak,
    Statement,
    String,
    TFingerprint,
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
    TypeAlias,
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
            flags: TFlags | None = None,
            limit: int | None = None,
            page_size: int | None = None,
            timeout: float | None = None,
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

    #: Type alias for store flags.
    TFlags: TypeAlias = Flags | int

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

    def _init_flags(self, flags: TFlags | None = None) -> None:
        flags = self.Flags.check_optional(
            flags, self.default_flags, type(self), 'flags')
        assert flags is not None
        self._flags = flags

    @property
    def flags(self) -> Flags:
        """The store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: TFlags) -> None:
        flags = self.Flags.check(flags, self.set_flags, 'flags', 1)
        if flags != self._flags and self._do_set_flags(self._flags, flags):
            self._flags = flags

    def _do_set_flags(self, old: Flags, new: Flags) -> bool:
        self._cache.clear()
        return True

    def get_flags(self) -> Flags:
        """Gets the store flags.

        Returns:
           Store flags.
        """
        return self._flags

    def has_flags(self, flags: TFlags) -> bool:
        """Tests whether `flags` are set in store.

        Parameters:
           flags: Store flags.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        flags = self.Flags.check(flags, self.has_flags, 'flags', 1)
        return bool(self.flags & flags)

    def set_flags(self, flags: TFlags) -> None:
        """Sets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        flags = self.Flags.check(flags, self.set_flags, 'flags', 1)
        self.flags |= flags

    def unset_flags(self, flags: TFlags) -> None:
        """Unsets `flags` in store.

        Parameters:
           flags: Store flags.
        """
        flags = self.Flags.check(flags, self.unset_flags, 'flags', 1)
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
    def _do_check_optional(
            cls,
            check: Callable[
                [Any, Location | None, str | None, int | None], T],
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> T | None:
        if arg is None:
            arg = default
        if arg is None:
            return default
        else:
            return check(arg, function, name, position)

    @classmethod
    def _check_optional_limit(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int | None:
        return cls._do_check_optional(
            cls._check_limit, arg, default, function, name, position)

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

        If `limit` is ``None``, assumes :attr:`Store.default_limit`.

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
        return cls._do_check_optional(
            cls._check_page_size, arg, default, function, name, position)

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

        If `page_size` is ``None``, assumes :attr:`Store.default_page_size`.

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
        return cls._do_check_optional(
            cls._check_timeout,
            arg, default, function, name, position)

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

# -- Set interface ---------------------------------------------------------

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Store):
            ###
            # Prevent __eq__ from triggering content equality.
            ###
            return id(self) == id(other)
        else:
            return NotImplemented

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
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None
    ) -> int:
        """Counts statements matching filter.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter.

        Returns:
           The number of statements matching filter.
        """
        return self._count_tail(self._check_filter(
            subject=subject,
            property=property,
            value=value,
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
            language=language,
            annotated=annotated,
            snak=snak,
            filter=filter,
            function=self.count))

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
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            function: Location | None = None
    ) -> Filter:
        subject = Fingerprint.check_optional(
            subject, None, function, 'subject', 1)
        property = Fingerprint.check_optional(
            property, None, function, 'property', 2)
        value = Fingerprint.check_optional(
            value, None, function, 'value', 3)
        snak_mask = Filter.SnakMask.check_optional(
            snak_mask, Filter.SnakMask.ALL, function, 'snak_mask', 4)
        subject_mask = Filter.DatatypeMask.check_optional(
            subject_mask, Filter.ENTITY, function, 'subject_mask', 5)
        property_mask = Filter.DatatypeMask.check_optional(
            property_mask, Filter.PROPERTY, function, 'property_mask', 6)
        value_mask = Filter.DatatypeMask.check_optional(
            value_mask, Filter.VALUE, function, 'value_mask', 7)
        rank_mask = Filter.RankMask.check_optional(
            rank_mask, Filter.RankMask.ALL, function, 'rank_mask', 8)
        language = String.check(
            language, function, 'language', 9).content\
            if language is not None else None
        annotated = bool(annotated)
        if filter is None:
            filter = Filter(
                subject=subject,
                property=property,
                value=value,
                snak_mask=snak_mask,
                subject_mask=subject_mask,
                property_mask=property_mask,
                value_mask=value_mask,
                rank_mask=rank_mask,
                language=language,
                annotated=annotated)
        else:
            filter = Filter.check(
                filter, function, 'filter', 12).combine(Filter(
                    subject=subject,
                    property=property,
                    value=value,
                    snak_mask=snak_mask,
                    subject_mask=subject_mask,
                    property_mask=property_mask,
                    value_mask=value_mask,
                    rank_mask=rank_mask,
                    language=language,
                    annotated=annotated))
        if snak is not None:
            filter = filter.combine(Filter.from_snak(None, Snak.check(
                snak, function, 'snak', 11)))
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
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
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
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           language: Language.
           annotated: Annotated flag.
           snak: Snak.
           filter: Filter filter.
           limit: Limit (maximum number) of statements to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of statements matching filter.
        """
        filter = self._check_filter(
            subject=subject,
            property=property,
            value=value,
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
            language=language,
            annotated=annotated,
            snak=snak,
            filter=filter,
            function=self.filter)
        limit = self._as_limit(limit, self.filter, 'limit', 13)
        distinct = self._as_distinct(distinct, self.filter, 'distinct', 14)
        return self._filter_with_hooks(filter, limit, distinct)

    def _as_limit(
            self,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> int:
        current_limit = self.limit
        if current_limit is None:
            current_limit = self.default_limit
        if current_limit is None:
            current_limit = self.max_limit
        limit = self._check_optional_limit(
            arg, current_limit, function, name, position)
        assert limit is not None
        return limit

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

    def filter_annotated(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: Filter.TSnakMask | None = None,
            subject_mask: Filter.TDatatypeMask | None = None,
            property_mask: Filter.TDatatypeMask | None = None,
            value_mask: Filter.TDatatypeMask | None = None,
            rank_mask: Filter.TRankMask | None = None,
            language: str | None = None,
            annotated: bool | None = None,
            snak: Snak | None = None,
            filter: Filter | None = None,
            limit: int | None = None,
            distinct: bool | None = None
    ) -> Iterator[AnnotatedStatement]:
        """:meth:`Store.filter` with annotations.

        Parameters:
           subject: Entity.
           property: Property.
           value: Value.
           snak_mask: Snak mask.
           subject_mask: Datatype mask.
           property_mask: Datatype mask.
           value_mask: Datatype mask.
           language: Language.
           annotated: Annotated flag (ignored).
           snak: Snak.
           filter: Filter.
           limit: Limit (maximum number) of statements to return.
           distinct: Whether to skip duplicated matches.

        Returns:
           An iterator of annotated statements matching filter.
        """
        return cast(Iterator[AnnotatedStatement], self.filter(
            subject=subject,
            property=property,
            value=value,
            snak_mask=snak_mask,
            subject_mask=subject_mask,
            property_mask=property_mask,
            value_mask=value_mask,
            rank_mask=rank_mask,
            language=language,
            annotated=True,     # force
            snak=snak,
            filter=filter,
            limit=limit,
            distinct=distinct))
