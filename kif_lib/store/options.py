# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import sys

from ..context import Section
from ..model import ReferenceRecordSet, TQuantity, TReferenceRecordSet
from ..typing import Any, ClassVar, Optional, Union
from .abc import Store


@dataclasses.dataclass
class StoreOptions(Section, name='store'):
    """Store options."""

    def __init__(self, **kwargs) -> None:
        self._init_extra_references(kwargs)
        self._init_flags(kwargs)
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
        """The set of extra references."""
        return self.get_extra_references()

    @extra_references.setter
    def extra_references(self, extra_references: TReferenceRecordSet):
        self.set_extra_references(extra_references)

    def get_extra_references(self) -> ReferenceRecordSet:
        """Gets the set of extra references.

        Returns:
           Reference record set.
        """
        return self._extra_references

    def set_extra_references(self, extra_references: TReferenceRecordSet):
        """Sets the set of extra reference.

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
        """The store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Union[Store.Flags, int]):
        self.set_flags(flags)

    def get_flags(self) -> Store.Flags:
        """Gets the store flags.

        Returns:
           Store flags.
        """
        return self._flags

    def set_flags(self, flags: Union[Store.Flags, int]):
        """Sets the store flags.

        Parameters:
           flags: Store flags.
        """
        self._flags = Store.Flags.check(flags, self.set_flags, 'flags', 1)

    # -- max_page_size --

    _v_max_page_size: ClassVar[tuple[str, int]] =\
        ('KIF_STORE_MAX_PAGE_SIZE', sys.maxsize)

    _max_page_size: int

    def _init_max_page_size(self, kwargs: dict[str, Any]) -> None:
        self.max_page_size = kwargs.get(
            '_max_page_size', self.getenv(*self._v_max_page_size))

    @property
    def max_page_size(self) -> int:
        """The maximum page size."""
        return self.get_max_page_size()

    @max_page_size.setter
    def max_page_size(self, max_page_size: TQuantity):
        self.set_max_page_size(max_page_size)

    def get_max_page_size(self) -> int:
        """Gets the maximum page size.

        Returns:
           Page size.
        """
        return self._max_page_size

    def set_max_page_size(self, max_page_size: TQuantity):
        """Sets the maximum page size.

        If `max_page_size` is negative, assumes zero.

        Parameters:
           max_page_size: Quantity.
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
        """The page size."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: TQuantity):
        self.set_page_size(page_size)

    def get_page_size(self) -> int:
        """Gets the page size.

        Returns:
           Page size.
        """
        return self._page_size

    def set_page_size(self, page_size: TQuantity):
        """Sets the page size.

        If `page_size` is negative, assumes zero.

        Parameters:
           page_size: Quantity.
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
        """The maximum timeout."""
        return self.get_max_timeout()

    @max_timeout.setter
    def max_timeout(self, max_timeout: TQuantity):
        self.set_max_timeout(max_timeout)

    def get_max_timeout(self) -> float:
        """Gets the maximum timeout (in seconds).

        Returns:
           Timeout.
        """
        return self._max_timeout

    def set_max_timeout(self, max_timeout: TQuantity):
        """Sets the maximum timeout (in seconds).

        If `max_timeout` is negative, assumes zero.

        Parameters:
           max_timeout: Quantity.
        """
        self._max_timeout = Store._check_timeout(
            max_timeout, self.set_max_timeout, 'max_timeout', 1)

    # -- timeout --

    _v_timeout: ClassVar[tuple[str, Optional[float]]] =\
        ('KIF_STORE_TIMEOUT', None)

    _timeout: Optional[float]

    def _init_timeout(self, kwargs: dict[str, Any]) -> None:
        self.timeout = kwargs.get('_timeout', self.getenv(*self._v_timeout))

    @property
    def timeout(self) -> Optional[float]:
        """The timeout (in seconds)."""
        return self.get_timeout()

    @timeout.setter
    def timeout(self, timeout: Optional[TQuantity]):
        self.set_timeout(timeout)

    def get_timeout(self) -> Optional[float]:
        """Gets the timeout (in seconds).

        Returns:
           Timeout.
        """
        return self._timeout

    def set_timeout(self, timeout: Optional[TQuantity]):
        """Sets the timeout.

        If `timeout` is negative, assumes zero.

        Parameters:
           timeout: Quantity.
        """
        self._timeout = Store._check_optional_timeout(
            timeout, None, self.set_timeout, 'timeout', 1)
