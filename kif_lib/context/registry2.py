# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..cache import Cache
from ..model import Datatype, Entity, Item, KIF_Object, Lexeme, Property, Text
from ..typing import Any, Callable, cast, Optional, TypeAlias, TypeVar, Union
from .context import Context

S = TypeVar('S')
T = TypeVar('T')
TextMap: TypeAlias = dict[str, Text]
TextSetMap: TypeAlias = dict[str, set[Text]]


class EntityRegistry(Cache):
    """KIF entity registry.

    Parameters:
       context: Context.
    """

    __slots__ = (
        '_context',
    )

    def __init__(self, context: Context) -> None:
        self._context = context
        super().__init__()

    def _describe(
            self, entity: Entity
    ) -> Item.Descriptor | Property.Descriptor | Lexeme.Descriptor | None:
        return cast(Optional[Union[
            Item.Descriptor, Property.Descriptor, Lexeme.Descriptor]],
            self._cache.get(entity.iri.content))

    def _add_label(self, entity: Entity, label: Text) -> Text:
        return self._do_add_into_text_map(
            'labels', entity, label, self._do_add_into_text_map_tail)

    def _remove_label(
            self,
            entity: Entity,
            label: Text | None = None,
            language: str | None = None
    ) -> TextMap | Text | None:
        return self._do_remove_from_text_map(
            'labels', entity, label, language,
            self._do_remove_from_text_map_tail)

    def _add_alias(self, entity: Entity, alias: Text) -> Text:
        return self._do_add_into_text_map(
            'aliases', entity, alias, self._do_add_into_text_set_map_tail)

    def _remove_alias(
            self,
            entity: Entity,
            alias: Text | None = None,
            language: str | None = None
    ) -> TextSetMap | set[Text] | None:
        return self._do_remove_from_text_map(
            'aliases', entity, alias, language,
            self._do_remove_from_text_set_map_tail)

    def _add_description(self, entity: Entity, description: Text) -> Text:
        return self._do_add_into_text_map(
            'descriptions', entity, description,
            self._do_add_into_text_map_tail)

    def _remove_description(
            self,
            entity: Entity,
            description: Text | None = None,
            language: str | None = None
    ) -> TextMap | Text | None:
        return self._do_remove_from_text_map(
            'descriptions', entity, description, language,
            self._do_remove_from_text_map_tail)

    def _do_add_into_text_map(
            self,
            field: str,
            entity: Entity,
            text: Text,
            tail: Callable[[T, Text], Text]
    ) -> Text:
        k = entity.iri.content
        t = cast(T, self.get(k, field) or self.set(k, field, {}))
        return tail(t, text)

    @staticmethod
    def _do_add_into_text_map_tail(t: TextMap, text: Text) -> Text:
        t[text.language] = text
        return text

    @staticmethod
    def _do_add_into_text_set_map_tail(t: TextSetMap, text: Text) -> Text:
        if text.language not in t:
            t[text.language] = set()
        t[text.language].add(text)
        return text

    def _do_remove_from_text_map(
            self,
            field: str,
            entity: Entity,
            text: Text | None,
            language: str | None,
            tail: Callable[[T, Text | None, str | None], S]
    ) -> Any:
        assert text is None or language is None
        k = entity.iri.content
        t = cast(T | None, self.get(k, field))
        if t is None:                           # nothing to do
            return None
        elif text is None and language is None:  # remove all
            return cast(T, self.unset(k, field))
        else:
            ret = tail(t, text, language)
            if not t:
                self.unset(k, field)
            return ret

    @staticmethod
    def _do_remove_from_text_map_tail(
            t: TextMap,
            text: Text | None,
            language: str | None
    ) -> Text | None:
        if language is not None:  # remove by language
            assert text is None
            return cast(Text, t.pop(language))
        elif text is not None:  # remove by content and language
            assert language is None
            if text == t[text.language]:
                return cast(Text, t.pop(text.language))
            else:
                return None
        else:
            raise KIF_Object._should_not_get_here()

    @staticmethod
    def _do_remove_from_text_set_map_tail(
            t: TextSetMap,
            text: Text | None,
            language: str | None
    ) -> TextSetMap | set[Text] | Text | None:
        if language is not None:  # remove by language
            assert text is None
            return cast(set[Text], t.pop(language))
        elif text is not None:  # remove by content and language
            assert language is None
            if text.language in t:
                ts = t[text.language]
                if text in ts:
                    ts.remove(text)
                    if not ts:
                        del t[text.language]
                    return text
                else:
                    return None
            else:
                return None
        else:
            raise KIF_Object._should_not_get_here()

    def _add_range(self, property: Property, range: Datatype) -> Datatype:
        return self.set(property.iri.content, 'range', range)

    def _remove_range(self, property: Property) -> Datatype | None:
        return self.unset(property.iri.content, 'range')

    def _add_inverse(
            self,
            property: Property,
            inverse: Property
    ) -> Property:
        return self.set(property.iri.content, 'inverse', inverse)

    def _remove_inverse(
            self,
            property: Property,
            inverse: Property
    ) -> Property | None:
        return self.unset(property.iri.content, 'inverse')

    def _add_lemma(self, lexeme: Lexeme, lemma: Text) -> Text:
        return self.set(lexeme.iri.content, 'lemma', lemma)

    def _remove_lemma(self, lexeme: Lexeme) -> Text | None:
        return self.unset(lexeme.iri.content, 'lemma')

    def _add_category(self, lexeme: Lexeme, category: Item) -> Item | None:
        return self.set(lexeme, 'category', category)

    def _remove_category(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme.iri.content, 'category')

    def _add_language(self, lexeme: Lexeme, language: Item) -> Item | None:
        return self.set(lexeme, 'language', language)

    def _remove_language(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme.iri.content, 'language')
