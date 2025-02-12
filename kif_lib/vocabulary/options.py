# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import pathlib

from ..context import Section
from ..model import String, TString
from ..typing import Any, ClassVar


@dataclasses.dataclass
class WD_Options(Section, name='wd'):
    """Wikidata vocabulary options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_property_cache(kwargs)

    # -- item_cache --

    _v_item_cache: ClassVar[tuple[str, pathlib.Path | None]] =\
        ('KIF_VOCABULARY_WD_ITEM_CACHE',
         pathlib.Path('wikidata_properties.tsv'))

    _item_cache: pathlib.Path | None

    def _init_item_cache(self, kwargs: dict[str, Any]) -> None:
        self.item_cache = kwargs.get(
            '_item_cache', self.getenv(*self._v_item_cache))

    @property
    def item_cache(self) -> pathlib.Path | None:
        """Wikidata item cache filename."""
        return self.get_item_cache()

    @item_cache.setter
    def item_cache(self, path: pathlib.Path | TString | None) -> None:
        self.set_item_cache(path)

    def get_item_cache(self) -> pathlib.Path | None:
        """Gets path to Wikidata item cache.

        Returns:
           Path or ``None``.
        """
        return self._item_cache

    def set_item_cache(self, path: pathlib.Path | TString | None) -> None:
        """Sets path to Wikidata item cache.

        Parameters:
           path: Path or ``None``.
        """
        if path is None or isinstance(path, pathlib.Path):
            self._item_cache = path
        else:
            self._item_cache = pathlib.Path(String.check(
                path, self.set_item_cache, 'path', 1).content)

    # -- property_cache --

    _v_property_cache: ClassVar[tuple[str, pathlib.Path | None]] =\
        ('KIF_VOCABULARY_WD_PROPERTY_CACHE',
         pathlib.Path('wikidata_properties.tsv'))

    _property_cache: pathlib.Path | None

    def _init_property_cache(self, kwargs: dict[str, Any]) -> None:
        self.property_cache = kwargs.get(
            '_property_cache', self.getenv(*self._v_property_cache))

    @property
    def property_cache(self) -> pathlib.Path | None:
        """Wikidata property cache filename."""
        return self.get_property_cache()

    @property_cache.setter
    def property_cache(self, path: pathlib.Path | TString | None) -> None:
        self.set_property_cache(path)

    def get_property_cache(self) -> pathlib.Path | None:
        """Gets path to Wikidata property cache.

        Returns:
           Path or ``None``.
        """
        return self._property_cache

    def set_property_cache(self, path: pathlib.Path | TString | None) -> None:
        """Sets path to Wikidata property cache.

        Parameters:
           path: Path or ``None``.
        """
        if path is None or isinstance(path, pathlib.Path):
            self._property_cache = path
        else:
            self._property_cache = pathlib.Path(String.check(
                path, self.set_property_cache, 'path', 1).content)


@dataclasses.dataclass
class VocabularyOptions(Section, name='vocabulary'):
    """Vocabulary options."""

    wd: WD_Options = dataclasses.field(default_factory=WD_Options)
