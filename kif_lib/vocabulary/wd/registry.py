# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib

from ... import namespace as NS
from ...model import Datatype, Entity, Item, Lexeme, Property, TDatatype
from ...typing import cast, Final, TypedDict


class WikidataEntityRegistry:
    """Wikidata entity registry."""

    class ItemEntry(TypedDict):
        """Entry in item registry."""
        item: Item | None
        label: str | None

    class PropertyEntry(TypedDict):
        """Entry in property registry."""
        property: Property | None
        datatype_uri: str | None
        label: str | None
        inverse_uri: str | None

    class LexemeEntry(TypedDict):
        """Entry in lexeme registry."""
        lexeme: Lexeme | None
        lemma: str | None
        category: str | None
        language: str | None

    #: Name of Wikidata items cache file.
    WIKIDATA_ITEMS_TSV: Final[str] = 'wikidata_items.tsv'

    #: Name of Wikidata properties cache file.
    WIKIDATA_PROPERTIES_TSV: Final[str] = 'wikidata_properties.tsv'

    #: Name of Wikidata lexemes cache file.
    WIKIDATA_LEXEMES_TSV: Final[str] = 'wikidata_lexemes.tsv'

    @classmethod
    def _get_registry_dir(cls) -> pathlib.Path:
        from importlib import util
        spec = util.find_spec(__name__)
        assert spec is not None
        assert spec.origin is not None
        return pathlib.Path(cast(str, spec.origin)).parent

    __slots__ = (
        '_registry_dir',
        '_item_registry',
        '_property_registry',
        '_lexeme_registry',
    )

    #: Directory where the this file is installed.
    _registry_dir: pathlib.Path

    #: Item registry.
    _registry: dict[str, ItemEntry]

    #: Property registry.
    _property_registry: dict[str, PropertyEntry]

    #: Lexeme registry.
    _lexeme_registry: dict[str, LexemeEntry]

    def __init__(self) -> None:
        self._registry_dir = self._get_registry_dir()
        self._item_registry = self._load_items_tsv()
        self._property_registry = self._load_properties_tsv()
        self._lexeme_registry = {}

    @property
    def _items_tsv(self) -> pathlib.Path:
        return self._registry_dir / self.WIKIDATA_ITEMS_TSV

    @property
    def _properties_tsv(self) -> pathlib.Path:
        return self._registry_dir / self.WIKIDATA_PROPERTIES_TSV

    @property
    def _lexemes_tsv(self) -> pathlib.Path:
        return self._registry_dir / self.WIKIDATA_LEXEMES_TSV

    # def load(self) -> None:
    #     if not (self._registry_dir / self._items_tsv).exists():
    #         self._download_items_tsv()
    #     self._item_registry.update(self._load_items_tsv())

    # def _download_items_tsv(self) -> None:
    #     import gzip
    #     import httpx
    #     res = httpx.get('http://example.org', follow_redirects=True)
    #     res.raise_for_status()
    #     with open(self._registry_dir / self.WIKIDATA_ITEMS_TSV, 'wb') as fp:
    #         fp.write(gzip.decompress(res.content))

    def _load_items_tsv(self) -> dict[str, ItemEntry]:
        try:
            with open(self._items_tsv, encoding='utf-8') as fp:
                return dict(map(self._load_items_tsv_helper, fp.readlines()))
        except FileNotFoundError:
            return {}

    def _load_items_tsv_helper(
            self,
            line: str
    ) -> tuple[str, ItemEntry]:
        _, uri, label = line[:-1].split('\t')
        return uri, {
            'item': None,
            'label': label,
        }

    def _load_properties_tsv(self) -> dict[str, PropertyEntry]:
        try:
            with open(self._properties_tsv, encoding='utf-8') as fp:
                return dict(map(
                    self._load_properties_tsv_helper, fp.readlines()))
        except FileNotFoundError:
            return {}

    def _load_properties_tsv_helper(
            self,
            line: str
    ) -> tuple[str, PropertyEntry]:
        _, uri, datatype_uri, label, inverse_uri = line[:-1].split('\t')
        return uri, {
            'property': None,
            'datatype_uri': datatype_uri,
            'label': label,
            'inverse_uri': inverse_uri,
        }

    def _load_lexemes_tsv(self) -> dict[str, LexemeEntry]:
        raise NotImplementedError

    def get_label(
            self,
            entity: Entity,
            default: str | None = None
    ) -> str | None:
        """Gets the registered label of `entity`.

        If entity has no label registered, returns `default`.

        Parameters:
           default: Default label.

        Returns:
           Label.
        """
        uri = entity.iri.content
        if isinstance(entity, Item) and uri in self._item_registry:
            return self._item_registry[uri].get('label', default)
        elif isinstance(entity, Property) and uri in self._property_registry:
            return self._property_registry[uri].get('label', default)
        else:
            return default

    def get_inverse(
            self,
            property: Property,
            default: Property | None = None
    ) -> Property | None:
        """Gets the registered inverse property of `property`.

        If entity has no inverse property registered, returns `default`.

        Parameters:
           default: Default inverse property.

        Returns:
           Property.
        """
        uri = property.iri.content
        if uri in self._property_registry:
            inverse_uri = self._property_registry[uri].get('inverse_uri')
            if inverse_uri in self._property_registry:
                inverse = self._property_registry[inverse_uri].get('property')
                assert inverse is not None
                return inverse
        return default

    def P(
            self,
            name: int | str,
            label: str | None = None,
            datatype: TDatatype | None = None,
    ) -> Property:
        if isinstance(name, str) and name[0] == 'P':
            name = str(NS.WD[name])
        else:
            name = str(NS.WD[f'P{name}'])
        if name not in self._property_registry:  # add
            prop = Property(name, Datatype.check_optional(datatype))
            if label is not None or datatype is not None:
                self._property_registry[name] = {
                    'property': prop,
                    'datatype_uri': str(prop.datatype._to_rdflib()),
                    'label': label,
                    'inverse_uri': None,
                }
            return prop
        else:                   # update
            entry = self._property_registry[name]
            if datatype is not None:
                entry['datatype_uri'] = str(Datatype.check(
                    datatype)._to_rdflib())
            if label is not None:
                entry['label'] = label
            if entry['property'] is None:
                entry['property'] = Property(
                    name, Datatype.check_optional(entry.get('datatype_uri')))
            assert entry['property'] is not None
            return entry['property']

    def Q(
            self,
            name: int | str,
            label: str | None = None
    ) -> Item:
        if isinstance(name, str) and name[0] == 'Q':
            name = str(NS.WD[name])
        else:
            name = str(NS.WD[f'Q{name}'])
        if name not in self._item_registry:
            item = Item(name)
            if label is not None:
                self._item_registry[name] = {
                    'item': item,
                    'label': label,
                }
            return item
        else:
            entry = self._item_registry[name]
            if label is not None:
                entry['label'] = label
            if entry['item'] is None:
                entry['item'] = Item(name)
            assert entry['item'] is not None
            return entry['item']

    def L(self, name: int | str) -> Lexeme:
        if isinstance(name, str) and name[0] == 'L':
            name = str(NS.WD[name])
        else:
            name = str(NS.WD[f'L{name}'])
        return Lexeme(name)
