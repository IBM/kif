# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import sys

from ..context import Section
from ..model import Filter, ReferenceRecordSet, TQuantity, TReferenceRecordSet
from ..typing import Any, ClassVar, Final, Iterable, Optional, override
from .abc import Store

DEFAULT_BASE_FILTER: Final[Filter] = Filter()
DEFAULT_DISTINCT: Final[bool] = True
DEFAULT_EXTRA_REFERENCES: Final[ReferenceRecordSet] = ReferenceRecordSet()
DEFAULT_MAX_LIMIT: Final[int] = sys.maxsize
DEFAULT_LIMIT: Final[Optional[int]] = None
DEFAULT_LOOKAHEAD: Final[int] = 2
DEFAULT_MAX_PAGE_SIZE: Final[int] = sys.maxsize
DEFAULT_PAGE_SIZE: Final[int] = 100
DEFAULT_MAX_TIMEOUT: Final[float] = float(sys.maxsize)
DEFAULT_TIMEOUT: Final[Optional[int]] = None


@dataclasses.dataclass
class _StoreOptions(Section):
    """Common store options."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._init_base_filter(kwargs)
        self._init_distinct(kwargs)
        self._init_extra_references(kwargs)
        self._init_flags(kwargs)
        self._init_max_limit(kwargs)
        self._init_limit(kwargs)
        self._init_lookahead(kwargs)
        self._init_max_page_size(kwargs)
        self._init_page_size(kwargs)
        self._init_max_timeout(kwargs)
        self._init_timeout(kwargs)

    # -- base_filter  --

    _base_filter: Filter | None

    def _init_base_filter(self, kwargs: dict[str, Any]) -> None:
        self.base_filter = kwargs.get('_base_filter', DEFAULT_BASE_FILTER)

    @property
    def base_filter(self) -> Filter:
        """The base filter option."""
        return self.get_base_filter()

    @base_filter.setter
    def base_filter(self, base_filter: Filter) -> None:
        self.set_base_filter(base_filter)

    def get_base_filter(self) -> Filter:
        """Gets the base filter option.

        Returns:
           Filter.
        """
        assert self._base_filter is not None
        return self._base_filter

    def set_base_filter(
            self,
            base_filter: Filter
    ) -> None:
        """Sets the base filter option.

        Parameters:
           base_filter: Filter.
        """
        self._base_filter = Filter.check(
            base_filter, self.set_base_filter, 'base_filter', 1)

    # -- distinct --

    _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_STORE_DISTINCT',), DEFAULT_DISTINCT)

    _distinct: bool | None

    def _init_distinct(self, kwargs: dict[str, Any]) -> None:
        self.distinct = kwargs.get(
            '_distinct', self.getenv_optional_bool(*self._v_distinct))

    @property
    def distinct(self) -> bool:
        """The distinct flag."""
        return self.get_distinct()

    @distinct.setter
    def distinct(self, distinct: bool) -> None:
        self.set_distinct(distinct)

    def get_distinct(self) -> bool:
        """Gets the distinct flag.

        Returns:
           Distinct flag.
        """
        assert self._distinct is not None
        return self._distinct

    def set_distinct(self, distinct: bool) -> None:
        """Sets the distinct flag.

        Parameters:
           distinct: Distinct flag.
        """
        self._distinct = bool(distinct)

    # -- extra_references --

    _extra_references: ReferenceRecordSet | None

    def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
        self.extra_references = kwargs.get(
            '_extra_references', DEFAULT_EXTRA_REFERENCES)

    @property
    def extra_references(self) -> ReferenceRecordSet:
        """The extra-references option."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(self, extra_references: TReferenceRecordSet) -> None:
        self.set_extra_references(extra_references)

    def get_extra_references(self) -> ReferenceRecordSet:
        """Gets the extra-references option.

        Returns:
           Reference record set.
        """
        assert self._extra_references is not None
        return self._extra_references

    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet
    ) -> None:
        """Sets the extra-references option.

        Parameters:
           extra_references: Reference record set.
        """
        self._extra_references = ReferenceRecordSet.check(
            extra_references, self.set_extra_references,
            'extra_references', 1)

    # -- flags --

    _v_flags: ClassVar[tuple[str, Store.Flags]] =\
        ('KIF_STORE_FLAGS', (Store.Flags.ALL & ~(Store.Flags.DEBUG)))

    _flags: Store.Flags

    def _init_flags(self, kwargs: dict[str, Any]) -> None:
        self.flags = kwargs.get(
            '_flags', self.getenv_int(
                self._v_flags[0], self._v_flags[1].value))

    @property
    def flags(self) -> Store.Flags:
        """The store-flags option."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Store.Flags | int) -> None:
        self.set_flags(flags)

    def get_flags(self) -> Store.Flags:
        """Gets the store-flags option.

        Returns:
           Store flags.
        """
        return self._flags

    def set_flags(self, flags: Store.Flags | int) -> None:
        """Sets the store-flags option.

        Parameters:
           flags: Store flags.
        """
        self._flags = Store.Flags.check(flags, self.set_flags, 'flags', 1)

    # -- max_limit --

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_MAX_LIMIT',), DEFAULT_MAX_LIMIT)

    _max_limit: int | None

    def _init_max_limit(self, kwargs: dict[str, Any]) -> None:
        self.max_limit = kwargs.get(
            '_max_limit', self.getenv_optional_int(*self._v_max_limit))

    @property
    def max_limit(self) -> int:
        """The maximum limit option."""
        return self.get_max_limit()

    @max_limit.setter
    def max_limit(self, max_limit: TQuantity) -> None:
        self.set_max_limit(max_limit)

    def get_max_limit(self) -> int:
        """Gets the maximum limit option.

        Returns:
           Limit.
        """
        assert self._max_limit is not None
        return self._max_limit

    def set_max_limit(self, max_limit: TQuantity) -> None:
        """Sets the maximum limit option.

        If `max_limit` is negative, assumes zero.

        Parameters:
           max_limit: Integer quantity.
        """
        self._max_limit = Store._check_limit(
            max_limit, self.set_max_limit, 'max_limit', 1)

    # -- limit --

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_LIMIT',), DEFAULT_LIMIT)

    _limit: int | None

    def _init_limit(self, kwargs: dict[str, Any]) -> None:
        self.limit = kwargs.get(
            '_limit', self.getenv_optional_int(*self._v_limit))

    @property
    def limit(self) -> int | None:
        """The limit option."""
        return self.get_limit()

    @limit.setter
    def limit(self, limit: TQuantity | None) -> None:
        self.set_limit(limit)

    def get_limit(self) -> int | None:
        """Gets the limit option.

        Returns:
           Limit or ``None``.
        """
        return self._limit

    def set_limit(self, limit: TQuantity | None) -> None:
        """Sets the limit option.

        If `limit` is negative, assumes zero.

        Parameters:
           limit: Integer quantity or ``None``.
        """
        self._limit = Store._check_optional_limit(
            limit, None, self.set_limit, 'limit', 1)

    # -- lookahead --

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_LOOKAHEAD',), 2)

    _lookahead: int | None

    def _init_lookahead(self, kwargs: dict[str, Any]) -> None:
        self.lookahead = kwargs.get(
            '_lookahead', self.getenv_optional_int(*self._v_lookahead))

    @property
    def lookahead(self) -> int:
        """The lookahead option."""
        return self.get_lookahead()

    @lookahead.setter
    def lookahead(self, lookahead: TQuantity) -> None:
        self.set_lookahead(lookahead)

    def get_lookahead(self) -> int:
        """Gets the lookahead option.

        Returns:
           Lookahead.
        """
        assert self._lookahead is not None
        return self._lookahead

    def set_lookahead(self, lookahead: TQuantity) -> None:
        """Sets the lookahead option.

        If `lookahead` is zero or negative, assumes 1.

        Parameters:
           lookahead: Integer quantity.
        """
        self._lookahead = Store._check_lookahead(
            lookahead, self.set_lookahead, 'lookahead', 1)

    # -- max_page_size --

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_MAX_PAGE_SIZE',), DEFAULT_MAX_PAGE_SIZE)

    _max_page_size: int | None

    def _init_max_page_size(self, kwargs: dict[str, Any]) -> None:
        self.max_page_size = kwargs.get(
            '_max_page_size', self.getenv_optional_int(
                *self._v_max_page_size))

    @property
    def max_page_size(self) -> int:
        """The maximum page size option."""
        return self.get_max_page_size()

    @max_page_size.setter
    def max_page_size(self, max_page_size: TQuantity) -> None:
        self.set_max_page_size(max_page_size)

    def get_max_page_size(self) -> int:
        """Gets the maximum page size option.

        Returns:
           Page size.
        """
        assert self._max_page_size is not None
        return self._max_page_size

    def set_max_page_size(self, max_page_size: TQuantity) -> None:
        """Sets the maximum page size option.

        If `max_page_size` is negative, assumes zero.

        Parameters:
           max_page_size: Integer quantity.
        """
        self._max_page_size = Store._check_page_size(
            max_page_size, self.set_max_page_size, 'max_page_size', 1)

    # -- page_size --

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_STORE_PAGE_SIZE',), DEFAULT_PAGE_SIZE)

    _page_size: int | None

    def _init_page_size(self, kwargs: dict[str, Any]) -> None:
        self.page_size = kwargs.get(
            '_page_size', self.getenv_optional_int(*self._v_page_size))

    @property
    def page_size(self) -> int:
        """The page size option."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: TQuantity) -> None:
        self.set_page_size(page_size)

    def get_page_size(self) -> int:
        """Gets the page size option.

        Returns:
           Page size.
        """
        assert self._page_size is not None
        return self._page_size

    def set_page_size(self, page_size: TQuantity) -> None:
        """Sets the page size option.

        If `page_size` is negative, assumes zero.

        Parameters:
           page_size: Integer quantity.
        """
        self._page_size = Store._check_page_size(
            page_size, self.set_page_size, 'page_size', 1)

    # -- max_timeout --

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_STORE_MAX_TIMEOUT',), DEFAULT_MAX_TIMEOUT)

    _max_timeout: float | None

    def _init_max_timeout(self, kwargs: dict[str, Any]) -> None:
        self.max_timeout = kwargs.get(
            '_max_timeout', self.getenv_optional_float(*self._v_max_timeout))

    @property
    def max_timeout(self) -> float:
        """The maximum timeout option (in seconds)."""
        return self.get_max_timeout()

    @max_timeout.setter
    def max_timeout(self, max_timeout: TQuantity) -> None:
        self.set_max_timeout(max_timeout)

    def get_max_timeout(self) -> float:
        """Gets the maximum timeout option (in seconds).

        Returns:
           Timeout.
        """
        assert self._max_timeout is not None
        return self._max_timeout

    def set_max_timeout(self, max_timeout: TQuantity) -> None:
        """Sets the maximum timeout option (in seconds).

        If `max_timeout` is negative, assumes zero.

        Parameters:
           max_timeout: Quantity.
        """
        self._max_timeout = Store._check_timeout(
            max_timeout, self.set_max_timeout, 'max_timeout', 1)

    # -- timeout --

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_STORE_TIMEOUT',), None)

    _timeout: float | None

    def _init_timeout(self, kwargs: dict[str, Any]) -> None:
        self.timeout = kwargs.get(
            '_timeout', self.getenv_optional_float(*self._v_timeout))

    @property
    def timeout(self) -> float | None:
        """The timeout option (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: TQuantity | None) -> None:
        self.set_timeout(timeout)

    def get_timeout(self) -> float | None:
        """Gets the timeout option (in seconds).

        Returns:
           Timeout or ``None``.
        """
        return self._timeout

    def set_timeout(self, timeout: TQuantity | None) -> None:
        """Sets the timeout option.

        If `timeout` is negative, assumes zero.

        Parameters:
           timeout: Quantity or ``None``.
        """
        self._timeout = Store._check_optional_timeout(
            timeout, None, self.set_timeout, 'timeout', 1)


class _StoreOptionsOverride(_StoreOptions):

    # -- base_filter --

    def _init_base_filter(self, kwargs: dict[str, Any]) -> None:
        self.base_filter = kwargs.get('_base_filter', None)  # pyright: ignore

    @override
    def get_base_filter(self) -> Filter:
        if self._base_filter is None:
            return self.get_context().options.store.base_filter
        else:
            return super().get_base_filter()

    @override
    def set_base_filter(self, base_filter: Filter | None) -> None:
        if base_filter is None:
            self._base_filter = None
        else:
            super().set_base_filter(base_filter)

    # -- distinct --

    @override
    def get_distinct(self) -> bool:
        if self._distinct is None:
            return self.get_context().options.store.distinct
        else:
            return super().get_distinct()

    @override
    def set_distinct(self, distinct: bool | None) -> None:
        if distinct is None:
            self._distinct = None
        else:
            super().set_distinct(distinct)

    # -- extra_references --

    @override
    def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
        self.extra_references = kwargs.get(
            '_extra_references', None)  # pyright: ignore

    @override
    def get_extra_references(self) -> ReferenceRecordSet:
        if self._extra_references is None:
            return self.get_context().options.store.extra_references
        else:
            return super().get_extra_references()

    @override
    def set_extra_references(
            self,
            extra_references: TReferenceRecordSet | None
    ) -> None:
        if extra_references is None:
            self._extra_references = None
        else:
            super().set_extra_references(extra_references)

    # -- max_limit --

    @override
    def get_max_limit(self) -> int:
        if self._max_limit is None:
            return self.get_context().options.store.max_limit
        else:
            return super().get_max_limit()

    @override
    def set_max_limit(self, max_limit: TQuantity | None) -> None:
        if max_limit is None:
            self._max_limit = None
        else:
            super().set_max_limit(max_limit)

    # -- limit --

    @override
    def get_limit(self) -> int | None:
        if self._limit is None:
            return self.get_context().options.store.limit
        else:
            return super().get_limit()

    # -- lookahead -

    @override
    def get_lookahead(self) -> int:
        if self._lookahead is None:
            return self.get_context().options.store.lookahead
        else:
            return super().get_lookahead()

    @override
    def set_lookahead(self, lookahead: TQuantity | None) -> None:
        if lookahead is None:
            self._lookahead = None
        else:
            super().set_lookahead(lookahead)

    # -- max_page_size --

    @override
    def get_max_page_size(self) -> int:
        if self._max_page_size is None:
            return self.get_context().options.store.max_page_size
        else:
            return super().get_max_page_size()

    @override
    def set_max_page_size(self, max_page_size: TQuantity | None) -> None:
        if max_page_size is None:
            self._max_page_size = None
        else:
            super().set_max_page_size(max_page_size)

    # -- page_size --

    @override
    def get_page_size(self) -> int:
        if self._page_size is None:
            return self.get_context().options.store.page_size
        else:
            return super().get_page_size()

    @override
    def set_page_size(self, page_size: TQuantity | None) -> None:
        if page_size is None:
            self._page_size = None
        else:
            super().set_page_size(page_size)

    # -- max_timeout --

    @override
    def get_max_timeout(self) -> float:
        if self._max_timeout is None:
            return self.get_context().options.store.max_timeout
        else:
            return super().get_max_timeout()

    @override
    def set_max_timeout(self, max_timeout: TQuantity | None) -> None:
        if max_timeout is None:
            self._max_timeout = None
        else:
            super().set_max_timeout(max_timeout)

    # -- timeout --

    @override
    def get_timeout(self) -> float | None:
        if self._timeout is None:
            return self.get_context().options.store.timeout
        else:
            return super().get_timeout()


class EmptyStoreOptions(_StoreOptionsOverride, name='empty'):
    """Empty store options."""

    _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_EMPTY_STORE_DISTINCT',), None)

    _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_MAX_LIMIT',), None)

    _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_LIMIT',), None)

    _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_LOOKAHEAD',), None)

    _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_MAX_PAGE_SIZE',), None)

    _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
        (('KIF_EMPTY_STORE_PAGE_SIZE',), None)

    _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_STORE_MAX_TIMEOUT',), None)

    _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
        (('KIF_EMPTY_STORE_TIMEOUT',), None)


@dataclasses.dataclass
class StoreOptions(_StoreOptions, name='store'):
    """Common store options."""

    empty: EmptyStoreOptions = dataclasses.field(
        default_factory=EmptyStoreOptions)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.empty = EmptyStoreOptions()
