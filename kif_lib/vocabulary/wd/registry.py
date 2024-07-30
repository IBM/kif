# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import pathlib

from ...model import Datatype, Entity, Item, Lexeme, Property, TDatatype
from ...namespace import WD
from ...typing import Any, cast, ClassVar, Iterator, Optional, TypedDict, Union


class WikidataEntityRegistry:
    """Wikidata entity registry."""

    #: Path to wikidata_items.json.
    _wikidata_items_json: ClassVar[str] = 'wikidata_items.json'

    #: Path to wikidata_propertis.json
    _wikidata_properties_json: ClassVar[str] = 'wikidata_properties.json'

    #: Entry in Wikidata entity registry.
    class Entry(TypedDict):
        entity: Entity
        label: Optional[str]
        description: Optional[str]

    @classmethod
    def _load_wikidata_entities(cls) -> dict[str, Entry]:
        return dict(cls._iterate_wikidata_entities())

    @classmethod
    def _iterate_wikidata_entities(cls) -> Iterator[tuple[str, Entry]]:
        it = [(Item, cls._load_wikidata_items_json()),
              (Property, cls._load_wikidata_properties_json().items())]
        for cons, table in it:
            for _, entry_dict in table:
                entity = Entity.from_ast(entry_dict['object'])
                assert isinstance(entity, cons)
                yield entity.iri.content, cls.Entry({
                    'entity': entity,
                    'label': entry_dict.get('label'),
                    'description': entry_dict.get('description')
                })

    @classmethod
    def _load_wikidata_items_json(cls) -> dict[str, Any]:
        return cls._load_wikidata_json(cls._wikidata_items_json)

    @classmethod
    def _load_wikidata_properties_json(cls) -> dict[str, Any]:
        return cls._load_wikidata_json(cls._wikidata_properties_json)

    @classmethod
    def _load_wikidata_json(cls, name: str) -> dict[str, Any]:
        import json
        try:
            path = cls._get_wikidata_json_path(name)
            with open(path, encoding='utf-8') as fp:
                return json.load(fp)
        except FileNotFoundError:
            return {}

    @classmethod
    def _get_wikidata_json_path(cls, name: str) -> pathlib.Path:
        from importlib import util
        spec = util.find_spec(__name__)
        assert spec is not None
        assert spec.origin is not None
        return pathlib.Path(cast(str, spec.origin)).parent / name

    __slots__ = (
        '_registry',
    )

    #: Registry table.
    _registry: dict[str, Entry]

    def __init__(self):
        self._registry = self._load_wikidata_entities()

    def _add_or_update_entry(
            self,
            entity: Entity,
            label: Optional[str] = None,
            description: Optional[str] = None
    ) -> Entry:
        name = entity.iri.content
        if name not in self._registry:
            self._registry[name] = {
                'entity': entity,
                'label': None,
                'description': None,
            }
        entry = self._registry[name]
        if label is not None:
            entry['label'] = label
        if description is not None:
            entry['description'] = description
        return entry

    def get_entity_label(self, entity: Entity) -> Optional[str]:
        entry = self._registry.get(entity.iri.content)
        return entry.get('label') if entry is not None else None

    def get_entity_description(self, entity: Entity) -> Optional[str]:
        entry = self._registry.get(entity.iri.content)
        return entry.get('description') if entry is not None else None

    def P(
            self,
            name: Union[int, str],
            label: Optional[str] = None,
            description: Optional[str] = None,
            datatype: Optional[TDatatype] = None
    ) -> Property:
        if not isinstance(name, str) or name[0] != 'P':
            name = str(WD[f'P{name}'])
        if name in self._registry:
            entity = self._registry[name]['entity']
            assert isinstance(entity, Property)
            prop: Property = entity
        else:
            prop = Property(name, Datatype.check_optional(
                datatype, None, self.P, 'datatype', 4))
        self._add_or_update_entry(prop, label, description)
        return prop

    def Q(
            self,
            name: Union[int, str],
            label: Optional[str] = None,
            description: Optional[str] = None
    ) -> Item:
        if not isinstance(name, str) or name[0] != 'Q':
            name = str(WD[f'Q{name}'])
        if name in self._registry:
            entity = self._registry[name]['entity']
            assert isinstance(entity, Item)
            item: Item = entity
        else:
            item = Item(name)
        self._add_or_update_entry(item, label, description)
        return item

    def L(self, name: Union[int, str]) -> Lexeme:
        if not isinstance(name, str) or name[0] != 'L':
            name = str(WD[f'L{name}'])
        if name in self._registry:
            entity = self._registry[name]['entity']
            assert isinstance(entity, Lexeme)
            lexeme: Lexeme = entity
        else:
            lexeme = Lexeme(name)
        self._add_or_update_entry(lexeme)
        return lexeme
