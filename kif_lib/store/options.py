# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import sys

from ..context import Section
from ..model import ReferenceRecordSet, TQuantity, TReferenceRecordSet
from ..typing import Any, ClassVar
from .abc import Store


@dataclasses.dataclass
class StoreOptions(Section, name='store'):
    """Store options."""

    def __init__(self, **kwargs) -> None:
        self._init_extra_references(kwargs)
        self._init_flags(kwargs)
        self._init_max_limit(kwargs)
        self._init_limit(kwargs)
        self._init_max_page_size(kwargs)
        self._init_page_size(kwargs)
        self._init_max_timeout(kwargs)
        self._init_timeout(kwargs)

    # -- extra_references --

    _extra_references: ReferenceRecordSet

    def _init_extra_references(self, kwargs: dict[str, Any]) -> None:
        self.extra_references = kwargs.get(
            '_extra_references', ReferenceRecordSet())

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
        ('KIF_STORE_FLAGS', (
            Store.Flags.ALL & ~(Store.Flags.DEBUG | Store.Flags.ORDER)))

    _flags: Store.Flags

    def _init_flags(self, kwargs: dict[str, Any]) -> None:
        self.flags = kwargs.get(
            '_flags', int(self.getenv(
                self._v_flags[0], self._v_flags[1].value)))

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

    _v_max_limit: ClassVar[tuple[str, int]] =\
        ('KIF_STORE_MAX_LIMIT', sys.maxsize)

    _max_limit: int

    def _init_max_limit(self, kwargs: dict[str, Any]) -> None:
        self.max_limit = kwargs.get(
            '_max_limit', self.getenv(*self._v_max_limit))

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

    _v_limit: ClassVar[tuple[str, int | None]] = ('KIF_STORE_LIMIT', None)

    _limit: int | None

    def _init_limit(self, kwargs: dict[str, Any]) -> None:
        self.limit = kwargs.get('_limit', self.getenv(*self._v_limit))

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

    # -- max_page_size --

    _v_max_page_size: ClassVar[tuple[str, int]] =\
        ('KIF_STORE_MAX_PAGE_SIZE', sys.maxsize)

    _max_page_size: int

    def _init_max_page_size(self, kwargs: dict[str, Any]) -> None:
        self.max_page_size = kwargs.get(
            '_max_page_size', self.getenv(*self._v_max_page_size))

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

    _v_page_size: ClassVar[tuple[str, int]] =\
        ('KIF_STORE_PAGE_SIZE', 100)

    _page_size: int

    def _init_page_size(self, kwargs: dict[str, Any]) -> None:
        self.page_size = kwargs.get(
            '_page_size', self.getenv(*self._v_page_size))

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

    _v_max_timeout: ClassVar[tuple[str, float]] =\
        ('KIF_STORE_MAX_TIMEOUT', float(sys.maxsize))

    _max_timeout: float

    def _init_max_timeout(self, kwargs: dict[str, Any]) -> None:
        self.max_timeout = kwargs.get(
            '_max_timeout', self.getenv(*self._v_max_timeout))

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

    _v_timeout: ClassVar[tuple[str, float | None]] =\
        ('KIF_STORE_TIMEOUT', None)

    _timeout: float | None

    def _init_timeout(self, kwargs: dict[str, Any]) -> None:
        self.timeout = kwargs.get('_timeout', self.getenv(*self._v_timeout))

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
