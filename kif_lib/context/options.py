# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from ..compiler.options import CompilerOptions
from ..model.options import ModelOptions
from ..store.options import StoreOptions
from ..typing import Any, ClassVar
from ..vocabulary.options import VocabularyOptions
from .section import Section

if TYPE_CHECKING:                     # pragma: no cover
    from ..model import TTextLanguage  # noqa: F401


@dataclasses.dataclass
class EntityRegistryOptions(Section, name='entities'):
    """Entity registry options."""

    def __init__(self, **kwargs) -> None:
        self._init_resolve(kwargs)

    # -- resolve --

    _v_resolve: ClassVar[tuple[str, bool | None]] =\
        ('KIF_ENTITIES_RESOLVE', None)

    _resolve: bool | None

    def _init_resolve(self, kwargs: dict[str, Any]) -> None:
        self.resolve = kwargs.get('_resolve', self.getenv(*self._v_resolve))

    @property
    def resolve(self) -> bool:
        """Whether to resolve entity data automatically."""
        return self.get_resolve()

    @resolve.setter
    def resolve(self, resolve: bool | None) -> None:
        self.set_resolve(resolve)

    def get_resolve(self) -> bool:
        """Gets the value of the resolve flag.

        Returns:
           Resolve flag value.
        """
        return bool(self._resolve)

    def set_resolve(self, resolve: bool | None) -> None:
        """Sets the value of the resolve flag.

        Parameters:
           resolve: Resolve flag value or ``None``.
        """
        self._resolve = bool(resolve)


@dataclasses.dataclass
class Options(Section, name='kif'):
    """KIF options."""

    #: Compiler options.
    compiler: CompilerOptions = dataclasses.field(
        default_factory=CompilerOptions)

    #: Entity registry options.
    entities: EntityRegistryOptions = dataclasses.field(
        default_factory=EntityRegistryOptions)

    #: Model options.
    model: ModelOptions = dataclasses.field(default_factory=ModelOptions)

    #: Store options.
    store: StoreOptions = dataclasses.field(default_factory=StoreOptions)

    #: Vocabulary options.
    vocabulary: VocabularyOptions = dataclasses.field(
        default_factory=VocabularyOptions)

    # -- language --

    @property
    def language(self) -> str:
        """The default language."""
        return self.get_language()

    @language.setter
    def language(self, language: TTextLanguage) -> None:
        self.set_language(language)

    def get_language(self) -> str:
        """Gets the default language.

        Returns:
           Language.
        """
        return self.model.value.text.language

    def set_language(self, language: TTextLanguage) -> None:
        """Sets the default language.

        Parameters:
           language: Language.
        """
        self.model.value.text.language = language  # type: ignore
