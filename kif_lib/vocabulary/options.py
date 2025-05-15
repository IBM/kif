# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import dataclasses
import pathlib
from typing import TYPE_CHECKING

from ..context import Section
from ..model import TString
from ..typing import Any, ClassVar, Iterable, Location

if TYPE_CHECKING:               # pragma: no cover
    from ..model import IRI, T_IRI


@dataclasses.dataclass
class _VocabularyOptions(Section):
    """Common vocabulary options."""

    #: The default value for the resolver option.
    DEFAULT_RESOLVER: ClassVar[str | None] = None

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

    def set_resolver(
            self,
            iri: T_IRI | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the IRI of entity resolver.

        Parameters:
           iri: IRI.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._resolver = self._check_optional_iri(
            iri, None, function, name, position)


@dataclasses.dataclass
class DBpediaOptions(_VocabularyOptions, name='db'):
    """DBpedia vocabulary options."""

    DEFAULT_RESOLVER = 'https://dbpedia.org/sparql'

    _v_resolver =\
        (('KIF_VOCABULARY_DB_RESOLVER', 'DBPEDIA'), DEFAULT_RESOLVER)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


@dataclasses.dataclass
class PubChemOptions(_VocabularyOptions, name='pc'):
    """PubChem vocabulary options."""

    DEFAULT_RESOLVER = 'https://qlever.cs.uni-freiburg.de/api/pubchem'

    _v_resolver =\
        (('KIF_VOCABULARY_PC_RESOLVER', 'PUBCHEM'), DEFAULT_RESOLVER)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


@dataclasses.dataclass
class WikidataOptions(_VocabularyOptions, name='wd'):
    """Wikidata vocabulary options."""

    DEFAULT_RESOLVER = 'https://query.wikidata.org/sparql'

    _v_resolver =\
        (('KIF_VOCABULARY_WD_RESOLVER', 'WIKIDATA'), DEFAULT_RESOLVER)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._init_item_cache(kwargs)
        self._init_property_cache(kwargs)

    # -- item_cache --

    #: The default value for the item cache option.
    DEFAULT_ITEM_CACHE: ClassVar[pathlib.Path] =\
        pathlib.Path('wikidata_items.tsv')

    _v_item_cache: ClassVar[tuple[str, pathlib.Path]] =\
        ('KIF_VOCABULARY_WD_ITEM_CACHE', DEFAULT_ITEM_CACHE)

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

    def set_item_cache(
            self,
            path: pathlib.Path | TString | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets path to Wikidata item cache.

        Parameters:
           path: Path.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._item_cache = self._check_optional_path(
            path, None, function, name, position)

    # -- property_cache --

    DEFAULT_PROPERTY_CACHE: ClassVar[pathlib.Path] =\
        pathlib.Path('wikidata_properties.tsv')

    _v_property_cache: ClassVar[tuple[str, pathlib.Path | None]] =\
        ('KIF_VOCABULARY_WD_PROPERTY_CACHE', DEFAULT_PROPERTY_CACHE)

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

    def set_property_cache(
            self,
            path: pathlib.Path | TString | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets path to Wikidata property cache.

        Parameters:
           path: Path.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._property_cache = self._check_optional_path(
            path, None, function, name, position)


@dataclasses.dataclass
class VocabularyOptions(Section, name='vocabulary'):
    """Vocabulary options."""

    db: DBpediaOptions = dataclasses.field(default_factory=DBpediaOptions)
    pc: PubChemOptions = dataclasses.field(default_factory=PubChemOptions)
    wd: WikidataOptions = dataclasses.field(default_factory=WikidataOptions)
