# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import pathlib

from ... import itertools
from ... import namespace as NS
from ...model import Datatype, Entity, Item, Lexeme, Property, TDatatype
from ...typing import (
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    TypedDict,
    Union,
)


class WikidataEntityRegistry:
    """Wikidata entity registry."""

    #: Entry in Wikidata entity registry.
    class Entry(TypedDict):
        entity: Entity
        label: Optional[str]
        description: Optional[str]

    WIKIDATA_ITEMS_TSV: Final[str] = 'wikidata_items.tsv'
    WIKIDATA_PROPERTIES_TSV: Final[str] = 'wikidata_properties.tsv'

    #: Names of the TSVs to load.
    _entity_tsvs: ClassVar[Sequence[str]] = (
        # WIKIDATA_ITEMS_TSV,
        WIKIDATA_PROPERTIES_TSV,
    )

    @classmethod
    def _get_registry_dir(cls) -> pathlib.Path:
        from importlib import util
        spec = util.find_spec(__name__)
        assert spec is not None
        assert spec.origin is not None
        return pathlib.Path(cast(str, spec.origin)).parent

    @classmethod
    def _load_tsvs(cls, paths: Iterable[pathlib.Path]) -> dict[str, Entry]:
        return dict(itertools.chain(*map(cls._iterate_tsv, paths)))

    @classmethod
    def _iterate_tsv(cls, path: pathlib.Path) -> Iterator[tuple[str, Entry]]:
        try:
            with open(path, encoding='utf-8') as fp:
                for line in fp:
                    _, label, entity_repr = line.split('\t')
                    entity = Entity.from_repr(entity_repr)
                    yield entity.iri.content, {
                        'entity': entity,
                        'label': label,
                        'description': None,
                    }
        except FileNotFoundError:
            pass

    __slots__ = (
        '_registry',
        '_registry_dir',
    )

    #: Registry table.
    _registry: dict[str, Entry]

    #: Directory where the this file is installed.
    _registry_dir: pathlib.Path

    def __init__(self):
        self._registry_dir = self._get_registry_dir()
        self._registry = self._load_tsvs(map(
            lambda p: self._registry_dir / p, self._entity_tsvs))

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
            name = str(NS.WD[f'P{name}'])
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
            name = str(NS.WD[f'Q{name}'])
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
            name = str(NS.WD[f'L{name}'])
        if name in self._registry:
            entity = self._registry[name]['entity']
            assert isinstance(entity, Lexeme)
            lexeme: Lexeme = entity
        else:
            lexeme = Lexeme(name)
        self._add_or_update_entry(lexeme)
        return lexeme
