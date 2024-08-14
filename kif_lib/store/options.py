# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ..context import Section
from ..typing import Union
from .abc import Store


@dataclasses.dataclass
class StoreOptions(Section):
    """Value options."""

    _default_flags: Store.Flags

    def __init__(self, **kwargs):
        self.default_flags = kwargs.get(
            '_default_flags',
            int(self.getenv(
                'KIF_STORE_DEFAULT_FLAGS',
                (Store.Flags.ALL
                 & ~(Store.Flags.DEBUG | Store.Flags.ORDER)).value)))

    @property
    def default_flags(self) -> Store.Flags:
        """The default store flags."""
        return self._default_flags

    @default_flags.setter
    def default_flags(self, flags: Union[int, Store.Flags]):
        self._default_flags = Store.Flags(flags)
