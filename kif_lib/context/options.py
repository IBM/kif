# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from ..codec.options import CodecOptions
from ..compiler.options import CompilerOptions
from ..model.options import ModelOptions
from ..store.options import StoreOptions
from ..typing import Any, ClassVar, Iterable
from ..vocabulary.options import VocabularyOptions
from .section import Section

if TYPE_CHECKING:                     # pragma: no cover
    from ..model import TTextLanguage


@dataclasses.dataclass
class EntityRegistryOptions(Section, name='entities'):
    """Entity registry options."""

    def __init__(self, **kwargs) -> None:
        self._init_resolve(kwargs)

    # -- resolve --

    _v_resolve: ClassVar[tuple[Iterable[str], bool]] =\
        (('KIF_ENTITIES_RESOLVE', 'KIF_RESOLVE_ENTITIES'), False)

    _resolve: bool

    def _init_resolve(self, kwargs: dict[str, Any] = {}) -> None:
        self.resolve = bool(kwargs.get(
            '_resolve', self.getenv_bool(*self._v_resolve)))

    @property
    def resolve(self) -> bool:
        """Whether to resolve entity data automatically."""
        return self.get_resolve()

    @resolve.setter
    def resolve(self, resolve: bool) -> None:
        self.set_resolve(resolve)

    def get_resolve(self) -> bool:
        """Gets the value of the resolve flag.

        Returns:
           Resolve flag value.
        """
        return self._resolve

    def set_resolve(self, resolve: bool | None) -> None:
        """Sets the value of the resolve flag.

        Parameters:
           resolve: Resolve flag value or ``None``.
        """
        if resolve is None:
            self._init_resolve()
        else:
            self._resolve = bool(resolve)


@dataclasses.dataclass
class Options(Section, name='kif'):
    """KIF options."""

    #: Codec options.
    codec: CodecOptions = dataclasses.field(default_factory=CodecOptions)

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
