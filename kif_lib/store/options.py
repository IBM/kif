# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ..context import Section
from ..model import Quantity, TQuantity
from ..typing import Any, ClassVar, Optional, Union
from .abc import Store


@dataclasses.dataclass
class StoreOptions(Section, name='store'):
    """Store options."""

    def __init__(self, **kwargs) -> None:
        self._init_flags(kwargs)
        self._init_page_size(kwargs)
        self._init_timeout(kwargs)

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
        """The default store flags."""
        return self.get_flags()

    @flags.setter
    def flags(self, flags: Union[Store.Flags, int]):
        self.set_flags(flags)

    def get_flags(self):
        """Gets the default store flags.

        Returns:
           Store flags.
        """
        return self._flags

    def set_flags(self, flags: Union[Store.Flags, int]):
        """Sets the default store flags.

        Parameters:
           flags: Store flags.
        """
        self._flags = Store.Flags.check(flags, self.set_flags, 'flags', 1)

    # -- page size --

    _v_page_size: ClassVar[tuple[str, int]] =\
        ('KIF_STORE_PAGE_SIZE', 100)

    _page_size: int

    def _init_page_size(self, kwargs: dict[str, Any]) -> None:
        self.page_size = kwargs.get(
            '_page_size', self.getenv(*self._v_page_size))

    @property
    def page_size(self) -> int:
        """The default page size."""
        return self.get_page_size()

    @page_size.setter
    def page_size(self, page_size: TQuantity):
        self.set_page_size(page_size)

    def get_page_size(self) -> int:
        """Gets the default page size.

        Returns:
           Page size.
        """
        return self._page_size

    def set_page_size(self, page_size: TQuantity):
        """Sets the default page size.

        If `page_size` is less than zero, assumes zero.

        Parameters:
           page_size: Quantity.
        """
        self._page_size = max(int(Quantity.check(
            page_size, self.set_page_size, 'page_size', 1).amount), 0)

    # -- timeout --

    _v_timeout: ClassVar[tuple[str, Optional[int]]] =\
        ('KIF_STORE_TIMEOUT', None)

    _timeout: Optional[int]

    def _init_timeout(self, kwargs: dict[str, Any]) -> None:
        self.timeout = kwargs.get('_timeout', self.getenv(*self._v_timeout))

    @property
    def timeout(self) -> Optional[int]:
        """The default timeout."""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: Optional[TQuantity]):
        if timeout is None:
            self._timeout = None
        else:
            self._timeout = int(Quantity.check(
                timeout, 'timeout', 'timeout', 1).amount)
