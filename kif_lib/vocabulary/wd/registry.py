# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import pathlib

from ... import namespace as NS
from ...model import Datatype, Entity, Item, Lexeme, Property, TDatatype
from ...typing import cast, Final, Optional, TypedDict, Union


class WikidataEntityRegistry:
    """Wikidata entity registry."""

    #: Entry in item registry.
    class ItemEntry(TypedDict):
        item: Optional[Item]
        label: Optional[str]

    #: Entry in property registry.
    class PropertyEntry(TypedDict):
        property: Optional[Property]
        datatype_uri: Optional[str]
        label: Optional[str]

    #: Entry in lexeme registry.
    class LexemeEntry(TypedDict):
        lexeme: Optional[Lexeme]
        lemma: Optional[str]
        category: Optional[str]
        language: Optional[str]

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

    def __init__(self):
        self._registry_dir = self._get_registry_dir()
        self._item_registry = {}
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

    def _load_items_tsv(self) -> dict[str, ItemEntry]:
        try:
            with open(self._items_tsv, 'rt', encoding='utf-8') as fp:
                return dict(map(self._load_items_tsv_helper, fp.readlines()))
        except FileNotFoundError:
            return {}

    def _load_items_tsv_helper(
            self,
            line: str
    ) -> tuple[str, ItemEntry]:
        uri, label = line[:-1].split('\t')
        return uri, {
            'item': None,
            'label': label,
        }

    def _load_properties_tsv(self) -> dict[str, PropertyEntry]:
        try:
            with open(self._properties_tsv, 'rt', encoding='utf-8') as fp:
                return dict(map(
                    self._load_properties_tsv_helper, fp.readlines()))
        except FileNotFoundError:
            return {}

    def _load_properties_tsv_helper(
            self,
            line: str
    ) -> tuple[str, PropertyEntry]:
        uri, datatype_uri, label = line[:-1].split('\t')
        return uri, {
            'property': None,
            'datatype_uri': datatype_uri,
            'label': label,
        }

    def _load_lexemes_tsv(self) -> dict[str, LexemeEntry]:
        raise NotImplementedError

    def get_entity_label(self, entity: Entity) -> Optional[str]:
        uri = entity.iri.content
        if isinstance(entity, Item) and uri in self._item_registry:
            return self._item_registry[uri].get('label')
        elif isinstance(entity, Property) and uri in self._property_registry:
            return self._property_registry[uri].get('label')
        else:
            return None

    def P(
            self,
            name: Union[int, str],
            label: Optional[str] = None,
            datatype: Optional[TDatatype] = None
    ) -> Property:
        if isinstance(name, str) and name[0] == 'P':
            name = str(NS.WD[name])
        else:
            name = str(NS.WD[f'P{name}'])
        if name not in self._property_registry:
            prop = Property(name, Datatype.check_optional(datatype))
            if label is not None or datatype is not None:
                self._property_registry[name] = {
                    'property': prop,
                    'datatype_uri': str(prop.datatype._to_rdflib()),
                    'label': label,
                }
            return prop
        else:
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
            name: Union[int, str],
            label: Optional[str] = None
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

    def L(self, name: Union[int, str]) -> Lexeme:
        if isinstance(name, str) and name[0] == 'L':
            name = str(NS.WD[name])
        else:
            name = str(NS.WD[f'L{name}'])
        return Lexeme(name)
