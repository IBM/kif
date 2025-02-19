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
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    String,
    T_IRI,
    TDatatype,
    Text,
    TItem,
    TProperty,
    TString,
    TText,
)
from ..rdflib import Graph, NamespaceManager
from ..typing import (
    Any,
    Callable,
    cast,
    Hashable,
    Iterable,
    Location,
    Optional,
    override,
    TypeAlias,
    TypeVar,
    Union,
)

E = TypeVar('E', bound=Union[Item, Property, Lexeme])
T = TypeVar('T')
TKey: TypeAlias = str
TextMap: TypeAlias = dict[str, Text]
TextSetMap: TypeAlias = dict[str, set[Text]]
set_ = set


class Registry(Cache):
    """Abstract base class for registries."""

    @abc.abstractmethod
    def __init__(self) -> None:
        super().__init__()


class EntityRegistry(Registry):
    """Entity registry."""

    def __init__(self) -> None:
        super().__init__()

    @override
    def get(self, obj: Hashable, key: str) -> Any:
        assert isinstance(obj, Entity)
        return super().get(obj.iri.content, key)

    @override
    def set(self, obj: Hashable, key: str, value: T) -> T:
        assert isinstance(obj, Entity)
        return super().set(obj.iri.content, key, value)

    @override
    def unset(self, obj: Hashable, key: str | None = None) -> Any:
        assert isinstance(obj, Entity)
        return super().unset(obj.iri.content, key)

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
            entity: Item | Property | Lexeme,
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
        """Add or update entity data.

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
        """Add or update property data.

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
        """Add or update lexeme data.

        Parameters:
           entity: Lexeme.
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

    @overload
    def unregister(self, entity: Item, **kwargs: Any) -> bool:
        """Remove item data.

        Parameters:
           entity: Item.
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           label_language: Language.
           alias_language: Language.
           description_language: Language.
           all_labels: Whether to remove all labels.
           all_aliases: Whether to remove all aliases.
           all_descriptions: Whether to remove all descriptions.
           all: Whether to remove all data.
           function: Function or function name.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        ...                     # pragma: no cover

    @overload
    def unregister(self, entity: Property, **kwargs: Any) -> bool:
        """Remove property data.

        Parameters:
           entity: Property.
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           label_language: Language.
           alias_language: Language.
           description_language: Language.
           all_labels: Whether to remove all labels.
           all_aliases: Whether to remove all aliases.
           all_descriptions: Whether to remove all descriptions.
           range: Whether to remove range.
           inverse: Whether to remove inverse.
           all: Whether to remove all data.
           function: Function or function name.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        ...                     # pragma: no cover

    @overload
    def unregister(self, entity: Lexeme, **kwargs: Any) -> bool:
        """Remove lexeme data.

        Parameters:
           entity: Lexeme.
           lemma: Whether to remove lemma.
           category: Whether to remove category.
           language: Whether to remove language.
           all: Whether to remove all data.
           function: Function or function name.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        ...                     # pragma: no cover

    def unregister(
            self,
            entity: Item | Property | Lexeme,
            label: TText | None = None,
            labels: Iterable[TText] = (),
            alias: TText | None = None,
            aliases: Iterable[TText] = (),
            description: TText | None = None,
            descriptions: Iterable[TText] = (),
            label_language: TString | None = None,
            alias_language: TString | None = None,
            description_language: TString | None = None,
            all_labels: bool = False,
            all_aliases: bool = False,
            all_descriptions: bool = False,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            language: bool = False,
            all: bool = False,
            function: Location | None = None,
            **kwargs: Any
    ) -> bool:
        function = function or self.unregister
        return self._do_unregister(
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
            label_language=String.check_optional(
                label_language, None, function, 'label_language'),
            alias_language=String.check_optional(
                alias_language, None, function, 'alias_language'),
            description_language=String.check_optional(
                description_language, None, function, 'description_language'),
            all_labels=bool(all_labels),
            all_aliases=bool(all_aliases),
            all_descriptions=bool(all_descriptions),
            range=bool(range),
            inverse=bool(inverse),
            lemma=bool(lemma),
            category=bool(category),
            language=bool(language),
            all=bool(all))

    def _do_unregister(
            self,
            entity: Entity,
            labels: Iterable[Text],
            aliases: Iterable[Text],
            descriptions: Iterable[Text],
            label_language: String | None = None,
            alias_language: String | None = None,
            description_language: String | None = None,
            all_labels: bool = False,
            all_aliases: bool = False,
            all_descriptions: bool = False,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            language: bool = False,
            all: bool = False
    ) -> bool:
        status: bool = False
        if isinstance(entity, (Item, Property)):
            for label in labels:
                status |= bool(self._remove_label(entity, label))
            for alias in aliases:
                status |= bool(self._remove_alias(entity, alias))
            for description in descriptions:
                status |= bool(self._remove_description(entity, description))
            if label_language:
                status |= bool(self._remove_label(
                    entity, language=label_language.content))
            if alias_language:
                status |= bool(self._remove_alias(
                    entity, language=alias_language.content))
            if description_language:
                status |= bool(self._remove_description(
                    entity, language=description_language.content))
            if all_labels:
                status |= bool(self._remove_all_labels(entity))
            if all_aliases:
                status |= bool(self._remove_all_aliases(entity))
            if all_descriptions:
                status |= bool(self._remove_all_descriptions(entity))
            if isinstance(entity, Property):
                if range:
                    status |= bool(self._remove_range(entity))
                if inverse:
                    status |= bool(self._remove_inverse(entity))
        elif isinstance(entity, Lexeme):
            if lemma:
                status |= bool(self._remove_lemma(entity))
            if category:
                status |= bool(self._remove_category(entity))
            if language:
                status |= bool(self._remove_language(entity))
        if all:
            status |= bool(self.unset(entity))
        return status

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

    def _remove_all_labels(self, entity: Entity) -> TextMap | None:
        return self.unset(entity, 'labels')

    def _add_alias(self, entity: Entity, alias: Text) -> Text:
        return self._do_add_into_text_map(
            'aliases', entity, alias, self._do_add_into_text_set_map_tail)

    def _remove_alias(
            self,
            entity: Entity,
            alias: Text | None = None,
            language: str | None = None
    ) -> TextSetMap | set_[Text] | None:
        return self._do_remove_from_text_map(
            'aliases', entity, alias, language,
            self._do_remove_from_text_set_map_tail)

    def _remove_all_aliases(self, entity: Entity) -> TextSetMap | None:
        return self.unset(entity, 'aliases')

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

    def _remove_all_descriptions(self, entity: Entity) -> TextMap | None:
        return self.unset(entity, 'labels')

    def _do_add_into_text_map(
            self,
            field: str,
            entity: Entity,
            text: Text,
            tail: Callable[[T, Text], Text]
    ) -> Text:
        t = cast(T, self.get(entity, field) or self.set(entity, field, {}))
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
        t = cast(Optional[T], self.get(entity, field))
        if t is None:                           # nothing to do
            return None
        elif text is None and language is None:  # remove all
            return cast(T, self.unset(entity, field))
        else:
            ret = tail(t, text, language)
            if not t:
                self.unset(entity, field)
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
    ) -> TextSetMap | set_[Text] | Text | None:
        if language is not None and language in t:  # remove by language
            assert text is None
            return cast(set_[Text], t.pop(language))
        elif text is not None and text.language in t:  # remove by text
            assert language is None
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

    def _add_range(self, property: Property, range: Datatype) -> Datatype:
        return self.set(property, 'range', range)

    def _remove_range(self, property: Property) -> Datatype | None:
        return self.unset(property, 'range')

    def _add_inverse(self, property: Property, inverse: Property) -> Property:
        return self.set(property, 'inverse', inverse)

    def _remove_inverse(self, property: Property) -> Property | None:
        return self.unset(property, 'inverse')

    def _add_lemma(self, lexeme: Lexeme, lemma: Text) -> Text:
        return self.set(lexeme, 'lemma', lemma)

    def _remove_lemma(self, lexeme: Lexeme) -> Text | None:
        return self.unset(lexeme, 'lemma')

    def _add_category(self, lexeme: Lexeme, category: Item) -> Item | None:
        return self.set(lexeme, 'category', category)

    def _remove_category(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme, 'category')

    def _add_language(self, lexeme: Lexeme, language: Item) -> Item | None:
        return self.set(lexeme, 'language', language)

    def _remove_language(self, lexeme: Lexeme) -> Item | None:
        return self.unset(lexeme, 'language')


class PrefixRegistry(Registry):
    """Prefix registry."""

    __slots__ = (
        '_nsm',
    )

    #: Namespace manager.
    _nsm: NamespaceManager

    def __init__(self) -> None:
        super().__init__()
        self._reset_nsm()

    def _reset_nsm(self) -> None:
        self._nsm = NamespaceManager(Graph(), bind_namespaces='none')
        for iri_content, prefixes in self._cache.items():
            for prefix in prefixes:
                self._nsm.bind(prefix, iri_content)

    @override
    def get(self, obj: Hashable, key: str) -> Any:
        assert isinstance(obj, IRI)
        return super().get(obj.content, key)

    @override
    def set(self, obj: Hashable, key: str, value: T) -> T:
        assert isinstance(obj, IRI)
        return super().set(obj.content, key, value)

    @override
    def unset(self, obj: Hashable, key: str | None = None) -> Any:
        assert isinstance(obj, IRI)
        return super().unset(obj.content, key)

    def curie(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> str | None:
        """Generates CURIE from IRI.

        See <https://en.wikipedia.org/wiki/CURIE>.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           CURIE (compact IRI) string or ``None``.
        """
        iri = IRI.check(iri, function or self.curie, 'iri')
        try:
            return self._nsm.curie(iri.content, False)
        except BaseException:
            return None

    def decurie(
            self,
            curie: TString,
            function: Location | None = None
    ) -> IRI | None:
        """Expands CURIE into IRI.

        Parameters:
           curie: String.

        Returns:
           IRI or ``None``.
        """
        curie = String.check(curie, function or self.decurie, 'curie')
        try:
            return IRI.check(self._nsm.expand_curie(curie.content))
        except BaseException:
            return None

    def describe(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> IRI.Descriptor | None:
        """Describes IRI.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           IRI descriptor or ``None`` (no descriptor for IRI).
        """
        function = function or self.describe
        iri = IRI.check(iri, function, 'iri')
        return cast(IRI.Descriptor | None, self._cache.get(iri.content))

    def _describe(self, entity: Entity) -> dict[str, Any] | None:
        return self._cache.get(entity.iri.content)

    def register(
            self,
            iri: T_IRI,
            prefix: TString | None = None,
            prefixes: Iterable[TString] = (),
            function: Location | None = None
    ) -> IRI:
        """Add or update IRI prefixes.

        Parameters:
           iri: IRI.
           prefix: Prefix.
           prefixes: Prefixes.
           function: Function or function name.

        Returns:
           IRI.
        """
        function = function or self.register
        return self._do_register(
            iri=IRI.check(iri, function, 'iri'),
            prefixes=map(
                lambda t: String.check(t, function, 'prefixes').content,
                itertools.chain((prefix,), prefixes) if prefix else prefixes))

    def unregister(
            self,
            iri: T_IRI,
            prefix: T_IRI | None = None,
            prefixes: Iterable[TString] = (),
            all: bool = False,
            function: Location | None = None
    ) -> bool:
        """Remove IRI prefixes.

        Parameters:
           iri: IRI.
           prefix: Prefixes.
           prefixes: Prefixes.
           all: Whether to remove all prefixes.
           function: Function or function name.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        function = function or self.unregister
        return self._do_unregister(
            iri=IRI.check(iri, function, 'iri'),
            prefixes=map(
                lambda t: String.check(t, function, 'prefixes').content,
                itertools.chain((prefix,), prefixes) if prefix else prefixes),
            all=bool(all))

    def _do_register(self, iri: IRI, prefixes: Iterable[str]) -> IRI:
        for prefix in prefixes:
            self._add_prefix(iri, prefix)
        return iri

    def _do_unregister(
            self,
            iri: IRI,
            prefixes: Iterable[str],
            all: bool = False
    ) -> bool:
        status: bool = False
        for prefix in prefixes:
            status |= bool(self._remove_prefix(iri, prefix))
        if all:
            status |= bool(self.unset(iri))
        if status:
            self._reset_nsm()
        return status

    def _add_prefix(self, iri: IRI, prefix: str) -> str:
        prefixes: set_[str] = (
            self.get(iri, 'prefixes') or self.set(iri, 'prefixes', set()))
        prefixes.add(prefix)
        self._nsm.bind(prefix, iri.content, replace=True)
        return prefix

    def _remove_prefix(self, iri: IRI, prefix: str) -> str | None:
        prefixes: Union[set_[str], None] = self.get(iri, 'prefixes')
        if prefixes is None or prefix not in prefixes:
            return None
        prefixes.remove(prefix)
        if not prefixes:
            self.unset(iri, 'prefixes')
        return prefix
