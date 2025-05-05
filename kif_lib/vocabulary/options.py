# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import dataclasses
import pathlib
from typing import TYPE_CHECKING

from ..context import Section
from ..model import String, TString
from ..typing import Any, ClassVar, Iterable

if TYPE_CHECKING:               # pragma: no cover
    from ..model import IRI, T_IRI


@dataclasses.dataclass
class _VocabularyOptions(Section):
    """Common vocabulary options."""

    _v_resolver: ClassVar[tuple[Iterable[str], str | None]]

    _resolver: IRI | None

    @abc.abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        self._init_resolver(kwargs)

    def _init_resolver(self, kwargs: dict[str, Any]) -> None:
        self.resolver = kwargs.get(
            '_resolver', self.getenv_optional_str(*self._v_resolver))

    @property
    def resolver(self) -> IRI | None:
        """The IRI of entity resolver."""
        return self.get_resolver()

    @resolver.setter
    def resolver(self, iri: T_IRI | None) -> None:
        self.set_resolver(iri)

    def get_resolver(self) -> IRI | None:
        """Gets the IRI of entity resolver.

        Returns:
           IRI or ``None``.
        """
        return self._resolver

    def set_resolver(self, iri: T_IRI | None) -> None:
        """Sets the IRI of entity resolver.

        Parameters:
           iri: IRI.
        """
        from ..model import IRI
        self._resolver = IRI.check_optional(
            iri, None, self.set_resolver, 'iri', 1)


@dataclasses.dataclass
class DBpediaOptions(_VocabularyOptions, name='db'):
    """PubChem vocabulary options."""

    _v_resolver: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_VOCABULARY_DB_RESOLVER', 'DBPEDIA'),
         'https://dbpedia.org/sparql')

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


@dataclasses.dataclass
class PubChemOptions(_VocabularyOptions, name='pc'):
    """PubChem vocabulary options."""

    _v_resolver: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_VOCABULARY_PC_RESOLVER', 'PUBCHEM'),
         'https://qlever.cs.uni-freiburg.de/api/pubchem')

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


@dataclasses.dataclass
class WikidataOptions(_VocabularyOptions, name='wd'):
    """Wikidata vocabulary options."""

    _v_resolver: ClassVar[tuple[Iterable[str], str | None]] =\
        (('KIF_VOCABULARY_WD_RESOLVER', 'WIKIDATA'),
         'https://query.wikidata.org/sparql')

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._init_item_cache(kwargs)
        self._init_property_cache(kwargs)

    # -- item_cache --

    _v_item_cache: ClassVar[tuple[str, pathlib.Path]] =\
        ('KIF_VOCABULARY_WD_ITEM_CACHE',
         pathlib.Path('wikidata_items.tsv'))

    _item_cache: pathlib.Path | None

    def _init_item_cache(self, kwargs: dict[str, Any]) -> None:
        self.item_cache = kwargs.get(
            '_item_cache', self.getenv_optional_path(*self._v_item_cache))

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
            '_property_cache',
            self.getenv_optional_path(*self._v_property_cache))

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

    db: DBpediaOptions = dataclasses.field(default_factory=DBpediaOptions)
    pc: PubChemOptions = dataclasses.field(default_factory=PubChemOptions)
    wd: WikidataOptions = dataclasses.field(default_factory=WikidataOptions)
