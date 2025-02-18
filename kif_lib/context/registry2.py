# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from typing_extensions import overload

from .. import itertools
from ..cache import Cache
from ..model import (
    Datatype,
    Entity,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    TDatatype,
    Text,
    TItem,
    TProperty,
    TText,
)
from ..typing import (
    Any,
    Callable,
    cast,
    Iterable,
    Location,
    TypeAlias,
    TypeVar,
    Union,
)
from .context import Context

T = TypeVar('T')
E = TypeVar('E', bound=Union[Item, Property, Lexeme])
TextMap: TypeAlias = dict[str, Text]
TextSetMap: TypeAlias = dict[str, set[Text]]


class Registry(Cache):
    """Abstract base class for registries.

    Parameters:
       context: Context.
    """

    __slots__ = (
        '_context',
    )

    #: Parent context.
    _context: Context

    @abc.abstractmethod
    def __init__(self, context: Context) -> None:
        super().__init__()
        self._context = context


class EntityRegistry(Registry):
    """Entity registry.

    Parameters:
       context: Context.
    """

    def __init__(self, context: Context) -> None:
        super().__init__(context)

    @overload
    def describe(
            self,
            entity: Item,
            function: Location | None = None
    ) -> Item.Descriptor | None:
        """Describes item.

        Parameters:
           entity: Item.
           function: Function or function name.

        Returns:
           Item descriptor or ``None`` (no descriptor for item).
        """
        ...                     # pragma: no cover

    @overload
    def describe(
            self,
            entity: Property,
            function: Location | None = None
    ) -> Property.Descriptor | None:
        """Describes property.

        Parameters:
           entity: property.
           function: Function or function name.

        Returns:
           Property descriptor or ``None`` (no descriptor for property).
        """
        ...                     # pragma: no cover

    @overload
    def describe(
            self,
            entity: Lexeme,
            function: Location | None = None
    ) -> Lexeme.Descriptor | None:
        """Describes lexeme.

        Parameters:
           entity: lexeme.
           function: Function or function name.

        Returns:
           Lexeme descriptor or ``None`` (no descriptor for lexeme).
        """
        ...                     # pragma: no cover

    def describe(
            self,
            entity: E,
            function: Location | None = None
    ) -> Item.Descriptor | Property.Descriptor | Lexeme.Descriptor | None:
        function = function or self.describe
        obj = Entity.check(entity, function, 'entity')
        desc = self._describe(entity)
        if obj is not None:
            if isinstance(obj, Item):
                return cast(Item.Descriptor, desc)
            elif isinstance(obj, Property):
                return cast(Property.Descriptor, desc)
            elif isinstance(obj, Lexeme):
                return cast(Lexeme.Descriptor, desc)
            else:
                raise KIF_Object._should_not_get_here()
        else:
            return None

    def _describe(self, entity: Entity) -> dict[str, Any] | None:
        return self._cache.get(entity.iri.content)

    @overload
    def register(self, entity: Item, **kwargs: Any) -> Item:
        """Add or update item descriptor.

        Parameters:
           entity: Item.
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           function: Function or function name.

        Returns:
           Item.
        """
        ...                     # pragma: no cover

    @overload
    def register(self, entity: Property, **kwargs: Any) -> Property:
        """Add or update property descriptor.

        Parameters:
           entity: Property.
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           range: Range datatype.
           inverse: Inverse property.
           function: Function or function name.

        Returns:
           Property.
        """
        ...                     # pragma: no cover

    @overload
    def register(self, entity: Lexeme, **kwargs: Any) -> Lexeme:
        """Add or update lemma descriptor.

        Parameters:
           entity: Property.
           lemma: Lemma.
           category: Lexical category.
           language: Language.

        Returns:
           Lemma.
        """
        ...                     # pragma: no cover

    def register(
            self,
            entity: E,
            label: TText | None = None,
            labels: Iterable[TText] = (),
            alias: TText | None = None,
            aliases: Iterable[TText] = (),
            description: TText | None = None,
            descriptions: Iterable[TText] = (),
            range: TDatatype | None = None,
            inverse: TProperty | None = None,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None,
            function: Location | None = None,
            **kwargs: Any
    ) -> E:
        function = function or self.register
        return self._do_register(
            entity,
            labels=map(
                lambda t: Text.check(t, function, 'labels'),
                itertools.chain((label,), labels) if label else labels),
            aliases=map(
                lambda t: Text.check(t, function, 'aliases'),
                itertools.chain((alias,), aliases) if alias else aliases),
            descriptions=map(
                lambda t: Text.check(t, function, 'descriptions'),
                itertools.chain((description,), descriptions)
                if description else descriptions),
            range=Datatype.check_optional(range, None, function, 'range'),
            inverse=Property.check_optional(
                inverse, None, function, 'inverse'),
            lemma=Text.check_optional(lemma, None, function, 'lemma'),
            category=Item.check_optional(
                category, None, function, 'category'),
            language=Item.check_optional(
                language, None, function, 'language'))

    def _do_register(
            self,
            entity: T,
            labels: Iterable[Text],
            aliases: Iterable[Text],
            descriptions: Iterable[Text],
            range: Datatype | None,
            inverse: Property | None,
            lemma: Text | None = None,
            category: Item | None = None,
            language: Item | None = None
    ) -> T:
        ret: T = entity
        if isinstance(entity, (Item, Property)):
            for label in labels:
                self._add_label(entity, label)
            for alias in aliases:
                self._add_alias(entity, alias)
            for description in descriptions:
                self._add_description(entity, description)
            if isinstance(entity, Property):
                if range is not None:
                    ret = cast(T, entity.replace(  # update ret's range
                        entity.KEEP, self._add_range(entity, range)))
                if inverse is not None:
                    self._add_inverse(entity, inverse)
        elif isinstance(entity, Lexeme):
            if lemma is not None:
                self._add_lemma(entity, lemma)
            if category is not None:
                self._add_category(entity, category)
            if language is not None:
                self._add_language(entity, language)
        else:
            raise KIF_Object._should_not_get_here()
        return ret

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
            tail: Callable[[T, Text | None, str | None], Any]
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
        return self.set(lexeme.iri.content, 'category', category)

    def _remove_category(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme.iri.content, 'category')

    def _add_language(self, lexeme: Lexeme, language: Item) -> Item | None:
        return self.set(lexeme.iri.content, 'language', language)

    def _remove_language(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme.iri.content, 'language')
