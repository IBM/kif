# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ..compiler.options import CompilerOptions
from ..model.options import ModelOptions
from ..store.options import StoreOptions
from ..vocabulary.options import VocabularyOptions
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

    #: Vocabulary options.
    vocabulary: VocabularyOptions = dataclasses.field(
        default_factory=VocabularyOptions)

    @property
    def language(self) -> str:
        """The default language."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets the default language.

        Returns:
           Language.
        """
        return self.model.value.text.language
