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
    TTextLanguage,
)
from ..rdflib import Graph, NamespaceManager
from ..store import Store
from ..typing import (
    Any,
    Callable,
    cast,
    Hashable,
    Iterable,
    Location,
    Mapping,
    Optional,
    override,
    Set,
    TypeAlias,
    TypeVar,
    Union,
)

E = TypeVar('E', bound=Entity)
T = TypeVar('T')
set_ = set

Prefix: TypeAlias = str
TextMap: TypeAlias = dict[str, Text]
TextSet: TypeAlias = set_[Text]
TextSetMap: TypeAlias = dict[str, set[Text]]


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
        if desc is None:
            return None
        elif isinstance(obj, Item):
            return cast(Item.Descriptor, desc)
        elif isinstance(obj, Property):
            return cast(Property.Descriptor, desc)
        elif isinstance(obj, Lexeme):
            return cast(Lexeme.Descriptor, desc)
        else:
            raise KIF_Object._should_not_get_here()

    def _describe(self, entity: Entity) -> dict[str, Any] | None:
        return self._cache.get(entity.iri.content)

    def get_label(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            function: Location | None = None
    ) -> Text | None:
        """Gets label of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Label or ``None``.
        """
        function = function or self.get_label
        t = self.describe(entity, function)
        if not t:
            return None
        lang = self._check_optional_language(entity, language, function)
        if 'labels' in t:
            return t['labels'].get(lang)
        else:
            return None

    def get_aliases(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            function: Location | None = None
    ) -> TextSet | None:
        """Gets aliases of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Aliases or ``None``.
        """
        function = function or self.get_aliases
        t = self.describe(entity, function)
        if not t:
            return None
        lang = self._check_optional_language(entity, language, function)
        if 'aliases' in t:
            return cast(TextSet | None, t['aliases'].get(lang))
        else:
            return None

    def get_description(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            function: Location | None = None
    ) -> Text | None:
        """Gets description of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Description or ``None``.
        """
        function = function or self.get_description
        t = self.describe(entity, function)
        if not t:
            return None
        lang = self._check_optional_language(entity, language, function)
        if 'descriptions' in t:
            return t['descriptions'].get(lang)
        else:
            return None

    def _check_optional_language(
            self,
            entity: Item | Property,
            language: TTextLanguage | None,
            function: Location | None
    ) -> str:
        language = String.check_optional(
            language, None, function, 'language')
        if language:
            return language.content
        else:
            return entity.context.options.language

    def get_range(
            self,
            entity: Property,
            function: Location | None = None
    ) -> Datatype | None:
        """Gets range of property.

        Parameters:
           entity: Property.
           function: Function or function name.

        Returns:
           Datatype or ``None``.
        """
        t = self.describe(entity, function or self.get_range)
        return t['range'] if t and 'range' in t else None

    def get_inverse(
            self,
            property: Property,
            function: Location | None = None
    ) -> Property | None:
        """Gets inverse of property.

        Parameters:
           entity: Property.
           function: Function or function name.

        Returns:
           Property or ``None``.
        """
        t = self.describe(property, function or self.get_inverse)
        return t['inverse'] if t and 'inverse' in t else None

    def get_lemma(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Text | None:
        """Gets lemma of lexeme.

        Parameters:
           entity: Lexeme.
           function: Function or function name.

        Returns:
           Lemma or ``None``.
        """
        t = self.describe(lexeme, function or self.get_lemma)
        return t['lemma'] if t and 'lemma' in t else None

    def get_category(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Item | None:
        """Gets lexical category of lexeme.

        Parameters:
           entity: Lexeme.
           function: Function or function name.

        Returns:
           Lexical category or ``None``.
        """
        t = self.describe(lexeme, function or self.get_category)
        return t['category'] if t and 'category' in t else None

    def get_language(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Item | None:
        """Gets language of lexeme.

        Parameters:
           entity: Lexeme.
           function: Function or function name.

        Returns:
           Language or ``None``.
        """
        t = self.describe(lexeme, function or self.get_language)
        return t['language'] if t and 'language' in t else None

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
           range: Range.
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
            labels: Iterable[TText] | None = None,
            alias: TText | None = None,
            aliases: Iterable[TText] | None = None,
            description: TText | None = None,
            descriptions: Iterable[TText] | None = None,
            range: TDatatype | None = None,
            inverse: TProperty | None = None,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None,
            function: Location | None = None,
            **kwargs: Any
    ) -> E:
        function = function or self.register
        labels = labels or ()
        aliases = aliases or ()
        descriptions = descriptions or ()
        return cast(E, self._do_register(
            entity=Entity.check(entity, function, 'entity'),
            labels=list(map(
                lambda t: Text.check(t, function, 'labels'),
                itertools.chain((label,), labels)
                if label is not None else labels)),
            aliases=list(map(
                lambda t: Text.check(t, function, 'aliases'),
                itertools.chain((alias,), aliases)
                if alias is not None else aliases)),
            descriptions=list(map(
                lambda t: Text.check(t, function, 'descriptions'),
                itertools.chain((description,), descriptions)
                if description is not None else descriptions)),
            range=Datatype.check_optional(range, None, function, 'range'),
            inverse=Property.check_optional(
                inverse, None, function, 'inverse'),
            lemma=Text.check_optional(lemma, None, function, 'lemma'),
            category=Item.check_optional(
                category, None, function, 'category'),
            language=Item.check_optional(
                language, None, function, 'language')))

    def _do_register(
            self,
            entity: E,
            labels: Iterable[Text],
            aliases: Iterable[Text],
            descriptions: Iterable[Text],
            range: Datatype | None,
            inverse: Property | None,
            lemma: Text | None,
            category: Item | None,
            language: Item | None
    ) -> E:
        ret: E = entity
        if isinstance(entity, (Item, Property)):
            for label in labels:
                self._add_label(entity, label)
            for alias in aliases:
                self._add_alias(entity, alias)
            for description in descriptions:
                self._add_description(entity, description)
            if isinstance(entity, Property):
                if range is not None:
                    ret = cast(E, entity.replace(  # update ret's range
                        entity.KEEP, self._add_range(entity, range)))
                elif entity.range is None:
                    t = self._describe(entity)
                    if t is not None and 'range' in t:
                        ret = cast(E, entity.replace(  # update ret's range
                            entity.KEEP, t['range']))
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
            label_language: TTextLanguage | None = None,
            alias_language: TTextLanguage | None = None,
            description_language: TTextLanguage | None = None,
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
            labels=list(map(
                lambda t: Text.check(t, function, 'labels'),
                itertools.chain((label,), labels)
                if label is not None else labels)),
            aliases=list(map(
                lambda t: Text.check(t, function, 'aliases'),
                itertools.chain((alias,), aliases)
                if alias is not None else aliases)),
            descriptions=list(map(
                lambda t: Text.check(t, function, 'descriptions'),
                itertools.chain((description,), descriptions)
                if description is not None else descriptions)),
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
    ) -> TextSetMap | TextSet | None:
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
    ) -> TextSetMap | TextSet | Text | None:
        if language is not None and language in t:  # remove by language
            assert text is None
            return cast(TextSet, t.pop(language))
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


class IRI_Registry(Registry):
    """IRI registry."""

    __slots__ = (
        '_nsm',
    )

    #: Namespace manager.
    _nsm: NamespaceManager

    def __init__(self, prefixes: Mapping[Prefix, Any] | None = None) -> None:
        super().__init__()
        self._init_nsm()
        for k, v in (prefixes or {}).items():
            prefix = String.check(k, type(self), 'prefixes', 1)
            iri = IRI.check(v, type(self), 'prefixes', 1)
            self._add_prefix(iri, prefix.content)

    def _init_nsm(self) -> None:
        self._nsm = NamespaceManager(Graph(), bind_namespaces='none')

    def _reset_nsm(self) -> None:
        self._init_nsm()
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
        """Contracts IRI into CURIE string.

        See <https://en.wikipedia.org/wiki/CURIE>.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           CURIE string or ``None``.
        """
        iri = IRI.check(iri, function or self.curie, 'iri')
        try:
            return self._nsm.curie(iri.content, False)
        except BaseException:
            return None

    def uncurie(
            self,
            curie: TString,
            function: Location | None = None
    ) -> IRI | None:
        """Expands CURIE string into IRI.

        Parameters:
           curie: String.

        Returns:
           IRI or ``None``.
        """
        curie = String.check(curie, function or self.uncurie, 'curie')
        try:
            return IRI.check(self._nsm.expand_curie(curie.content))
        except BaseException:
            return None

    def lookup_resolver(
            self,
            iri: T_IRI | Entity,
            function: Location | None = None
    ) -> Store | None:
        """Searches for resolver for IRI.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Store or ``None``.
        """
        if isinstance(iri, Entity):
            iri = iri.iri
        else:
            iri = IRI.check(iri, function, 'iri')
        resolver = self.get_resolver(iri)
        if resolver is None:
            from ..rdflib import split_uri
            try:
                ns, _ = split_uri(iri.content)
                resolver = self.get_resolver(ns)
            except BaseException:
                pass
        return resolver

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

    def get_prefixes(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> Set[Prefix] | None:
        """Gets IRI prefixes.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Prefix set or ``None``.
        """
        t = self.describe(iri, function or self.get_prefixes)
        return t['prefixes'] if t and 'prefixes' in t else None

    def get_resolver(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> Store | None:
        """Gets IRI entity resolver.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Store or ``None``.
        """
        t = self.describe(iri, function or self.get_resolver)
        return t['resolver'] if t and 'resolver' in t else None

    def register(
            self,
            iri: T_IRI,
            prefix: TString | None = None,
            prefixes: Iterable[TString] | None = None,
            resolver: Store | None = None,
            function: Location | None = None
    ) -> IRI:
        """Add or update IRI data.

        Parameters:
           iri: IRI.
           prefix: Prefix.
           prefixes: Prefixes.
           resolver: Store.
           function: Function or function name.

        Returns:
           IRI.
        """
        function = function or self.register
        prefixes = prefixes or ()
        return self._do_register(
            iri=IRI.check(iri, function, 'iri'),
            prefixes=map(
                lambda t: String.check(t, function, 'prefixes').content,
                itertools.chain((prefix,), prefixes) if prefix else prefixes),
            resolver=KIF_Object._check_optional_arg_isinstance(
                resolver, Store, None, function, 'resolver'))

    def unregister(
            self,
            iri: T_IRI,
            prefix: TString | None = None,
            prefixes: Iterable[TString] = (),
            all_prefixes: bool = False,
            resolver: bool = False,
            all: bool = False,
            function: Location | None = None
    ) -> bool:
        """Remove IRI data.

        Parameters:
           iri: IRI.
           prefix: Prefix.
           prefixes: Prefixes.
           all_prefixes: Whether to remove all prefixes.
           resolver: Whether to remove resolver.
           all: Whether to remove all data.
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
            all_prefixes=bool(all_prefixes),
            resolver=bool(resolver),
            all=bool(all))

    def _do_register(
            self,
            iri: IRI,
            prefixes: Iterable[Prefix],
            resolver: Store | None
    ) -> IRI:
        for prefix in prefixes:
            self._add_prefix(iri, prefix)
        if resolver is not None:
            self._add_resolver(iri, resolver)
        return iri

    def _do_unregister(
            self,
            iri: IRI,
            prefixes: Iterable[Prefix],
            all_prefixes: bool = False,
            resolver: bool = False,
            all: bool = False
    ) -> bool:
        status: bool = False
        for prefix in prefixes:
            status |= bool(self._remove_prefix(iri, prefix))
        if all_prefixes:
            status |= bool(self._remove_all_prefixes(iri))
        if resolver:
            status |= bool(self._remove_resolver(iri))
        if all:
            status |= bool(self.unset(iri))
        if status:
            self._reset_nsm()
        return status

    def _add_prefix(self, iri: IRI, prefix: Prefix) -> Prefix:
        prefixes: set_[Prefix] = (
            self.get(iri, 'prefixes') or self.set(iri, 'prefixes', set()))
        prefixes.add(prefix)
        self._nsm.bind(prefix, iri.content, replace=True)
        return prefix

    def _remove_prefix(self, iri: IRI, prefix: Prefix) -> Prefix | None:
        prefixes: Union[set_[Prefix], None] = self.get(iri, 'prefixes')
        if prefixes is None or prefix not in prefixes:
            return None
        prefixes.remove(prefix)
        if not prefixes:
            self.unset(iri, 'prefixes')
        return prefix

    def _remove_all_prefixes(self, iri: IRI) -> set_[Prefix] | None:
        return self.unset(iri, 'labels')

    def _add_resolver(self, iri: IRI, resolver: Store) -> Store:
        return self.set(iri, 'resolver', resolver)

    def _remove_resolver(self, iri: IRI) -> Store | None:
        return self.unset(iri, 'resolver')
