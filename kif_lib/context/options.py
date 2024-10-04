# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..compiler.options import CompilerOptions
from ..model.options import ModelOptions
from ..store.options import StoreOptions
from .section import Section


@dataclasses.dataclass
class Options(Section, name='kif'):
    """KIF options."""

    #: Compiler options.
    compiler: CompilerOptions = dataclasses.field(
        default_factory=CompilerOptions)

    #: Model options.
    model: ModelOptions = dataclasses.field(default_factory=ModelOptions)

    #: Store options.
    store: StoreOptions = dataclasses.field(default_factory=StoreOptions)

    @property
    def language(self) -> str:
        """The default language tag."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets the default language tag.

        Returns:
           Language tag.
        """
        return self.model.value.text.language
