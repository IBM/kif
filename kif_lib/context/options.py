# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ..model.options import ModelOptions
from ..store.options import StoreOptions
from .section import Section


@dataclasses.dataclass
class Options(Section):
    """KIF options."""

    #: Model options.
    model: 'ModelOptions' = dataclasses.field(default_factory=ModelOptions)

    #: Store options.
    store: 'StoreOptions' = dataclasses.field(default_factory=StoreOptions)

    @property
    def default_language(self) -> str:
        """The default language tag."""
        return self.get_default_language()

    def get_default_language(self) -> str:
        """Gets the default language tag.

        Returns:
           Language tag.
        """
        return self.model.value.text.default_language
