# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..cache import Cache
from ..model import Entity, IRI, Item, Lexeme, Property
from ..namespace import WD
from ..typing import Any, cast, Optional, Union


class WikidataEntityRegistry(Cache):

    _wikidata_items_json = 'wikidata_items.json'
    _wikidata_properties_json = 'wikidata_properties.json'

    @classmethod
    def _load_wikidata_items_json(cls) -> dict[str, dict[str, str]]:
        return cls._load_wikidata_json(cls._wikidata_items_json)

    @classmethod
    def _load_wikidata_properties_json(cls) -> dict[str, dict[str, str]]:
        return cls._load_wikidata_json(cls._wikidata_properties_json)

    @classmethod
    def _load_wikidata_json(cls, name: str) -> dict[str, dict[str, str]]:
        from importlib import util as importlib_util
        from json import load
        from pathlib import Path

        spec = importlib_util.find_spec(__name__)
        assert spec is not None
        assert spec.origin is not None
        dir = Path(cast(str, spec.origin)).parent
        try:
            with open(dir / name) as fp:
                return load(fp)
        except FileNotFoundError:
            return dict()

    def __init__(self):
        super().__init__()
        it = [(Item, self._load_wikidata_items_json()),
              (Property, self._load_wikidata_properties_json().items())]
        for cons, table in it:
            for name, entry in table:
                entity = cons(IRI(name))
                for key, value in entry.items():
                    self.set(entity, key, value)

    def Q(
            self,
            name: Union[int, str],
            label: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Item:
        if not isinstance(name, str) or name[0] != 'Q':
            name = f'Q{name}'
        return cast(Item, self._get_entity(
            Item(WD[name]), label=label, description=description))

    def P(
            self,
            name: Union[int, str],
            label: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Property:
        if not isinstance(name, str) or name[0] != 'P':
            name = f'P{name}'
        return cast(Property, self._get_entity(
            Property(WD[name]), label=label, description=description))

    def L(self, name: Union[int, str]) -> Lexeme:
        if not isinstance(name, str) or name[0] != 'L':
            name = f'L{name}'
        return cast(Lexeme, self._get_entity(Lexeme(WD[name])))

    def _get_entity(
            self,
            entity: Entity,
            **kwargs: Any,
    ) -> Entity:
        for k, v in kwargs.items():
            if v is not None:
                self.set(entity, k, v)
        return entity
