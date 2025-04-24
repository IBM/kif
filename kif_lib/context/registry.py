# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from typing_extensions import overload

from .. import itertools
from .. import namespace as NS
from ..cache import Cache
from ..model import (
    AliasProperty,
    Datatype,
    DescriptionProperty,
    Entity,
    Filter,
    IRI,
    Item,
    KIF_Object,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
    OrFingerprint,
    Property,
    String,
    T_IRI,
    TDatatype,
    TEntity,
    Text,
    TItem,
    TProperty,
    TString,
    TText,
    TTextLanguage,
    ValueSnak,
)
from ..rdflib import Graph, NamespaceManager, split_uri
from ..store import Store
from ..typing import (
    Any,
    Callable,
    cast,
    Hashable,
    Iterable,
    Iterator,
    Location,
    Mapping,
    Optional,
    override,
    Set,
    TypeAlias,
    TypeVar,
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
        """Gets the label of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Label or ``None``.
        """
        function = function or self.get_label
        t = self.describe(entity, function)
        lang = self._check_optional_language(entity, language, function)
        if t and 'labels' in t:
            return t['labels'].get(lang)
        else:
            return None

    def get_aliases(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            function: Location | None = None
    ) -> Set[Text] | None:
        """Gets the aliases of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Aliases or ``None``.
        """
        function = function or self.get_aliases
        t = self.describe(entity, function)
        lang = self._check_optional_language(entity, language, function)
        if t and 'aliases' in t:
            return cast(Optional[Set[Text]], t['aliases'].get(lang))
        else:
            return None

    def get_description(
            self,
            entity: Item | Property,
            language: TTextLanguage | None = None,
            function: Location | None = None
    ) -> Text | None:
        """Gets the description of item or property.

        Parameters:
           entity: Item or property.
           language: Language.
           function: Function or function name.

        Returns:
           Description or ``None``.
        """
        function = function or self.get_description
        t = self.describe(entity, function)
        lang = self._check_optional_language(entity, language, function)
        if t and 'descriptions' in t:
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
            property: Property,
            function: Location | None = None
    ) -> Datatype | None:
        """Gets the range of property.

        Parameters:
           property: Property.
           function: Function or function name.

        Returns:
           Datatype or ``None``.
        """
        property = Property.check(
            property, function or self.get_range, 'property')
        return self.get(property, 'range')

    def get_inverse(
            self,
            property: Property,
            function: Location | None = None
    ) -> Property | None:
        """Gets the inverse of property.

        Parameters:
           property: Property.
           function: Function or function name.

        Returns:
           Property or ``None``.
        """
        property = Property.check(
            property, function or self.get_inverse, 'property')
        return self.get(property, 'inverse')

    def get_lemma(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Text | None:
        """Gets the lemma of lexeme.

        Parameters:
           lexeme: Lexeme.
           function: Function or function name.

        Returns:
           Lemma or ``None``.
        """
        lexeme = Lexeme.check(lexeme, function or self.get_lemma, 'lexeme')
        return self.get(lexeme, 'lemma')

    def get_category(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Item | None:
        """Gets the lexical category of lexeme.

        Parameters:
           lexeme: Lexeme.
           function: Function or function name.

        Returns:
           Lexical category or ``None``.
        """
        lexeme = Lexeme.check(lexeme, function or self.get_category, 'lexeme')
        return self.get(lexeme, 'category')

    def get_language(
            self,
            lexeme: Lexeme,
            function: Location | None = None
    ) -> Item | None:
        """Gets the language of lexeme.

        Parameters:
           lexeme: Lexeme.
           function: Function or function name.

        Returns:
           Language or ``None``.
        """
        lexeme = Lexeme.check(lexeme, function or self.get_language, 'lexeme')
        return self.get(lexeme, 'language')

    @overload
    def register(self, entity: Item, **kwargs: Any) -> Item:
        """Adds or updates item data.

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
        """Adds or updates property data.

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
        """Adds or updates lexeme data.

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
        return cast(E, self._register(
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

    def _register(
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
            labels: Iterable[TText] | None = None,
            alias: TText | None = None,
            aliases: Iterable[TText] | None = None,
            description: TText | None = None,
            descriptions: Iterable[TText] | None = None,
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
        labels = labels or ()
        aliases = aliases or ()
        descriptions = descriptions or ()
        return self._unregister(
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

    def _unregister(
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
                    status |= self._remove_range(entity) is not None
                if inverse:
                    status |= self._remove_inverse(entity) is not None
        elif isinstance(entity, Lexeme):
            if lemma:
                status |= self._remove_lemma(entity) is not None
            if category:
                status |= self._remove_category(entity) is not None
            if language:
                status |= self._remove_language(entity) is not None
        if all:
            status |= self.unset(entity) is not None
        return status

    def _add_label(self, entity: Entity, label: Text) -> Text:
        return self._add_into_text_map(
            'labels', entity, label, self._add_into_text_map_tail)

    def _remove_label(
            self,
            entity: Entity,
            label: Text | None = None,
            language: str | None = None
    ) -> TextMap | Text | None:
        return self._remove_from_text_map(
            'labels', entity, label, language,
            self._remove_from_text_map_tail)

    def _remove_all_labels(self, entity: Entity) -> TextMap | None:
        return self.unset(entity, 'labels')

    def _add_alias(self, entity: Entity, alias: Text) -> Text:
        return self._add_into_text_map(
            'aliases', entity, alias, self._add_into_text_set_map_tail)

    def _remove_alias(
            self,
            entity: Entity,
            alias: Text | None = None,
            language: str | None = None
    ) -> TextSetMap | TextSet | None:
        return self._remove_from_text_map(
            'aliases', entity, alias, language,
            self._remove_from_text_set_map_tail)

    def _remove_all_aliases(self, entity: Entity) -> TextSetMap | None:
        return self.unset(entity, 'aliases')

    def _add_description(self, entity: Entity, description: Text) -> Text:
        return self._add_into_text_map(
            'descriptions', entity, description,
            self._add_into_text_map_tail)

    def _remove_description(
            self,
            entity: Entity,
            description: Text | None = None,
            language: str | None = None
    ) -> TextMap | Text | None:
        return self._remove_from_text_map(
            'descriptions', entity, description, language,
            self._remove_from_text_map_tail)

    def _remove_all_descriptions(self, entity: Entity) -> TextMap | None:
        return self.unset(entity, 'descriptions')

    def _add_into_text_map(
            self,
            field: str,
            entity: Entity,
            text: Text,
            tail: Callable[[T, Text], Text]
    ) -> Text:
        t = cast(T, self.get(entity, field) or self.set(entity, field, {}))
        return tail(t, text)

    @staticmethod
    def _add_into_text_map_tail(t: TextMap, text: Text) -> Text:
        t[text.language] = text
        return text

    @staticmethod
    def _add_into_text_set_map_tail(t: TextSetMap, text: Text) -> Text:
        if text.language not in t:
            t[text.language] = set()
        t[text.language].add(text)
        return text

    def _remove_from_text_map(
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
        ret = tail(t, text, language)
        if not t:
            self.unset(entity, field)
        return ret

    @staticmethod
    def _remove_from_text_map_tail(
            t: TextMap,
            text: Text | None,
            language: str | None
    ) -> Text | None:
        if language is not None:  # remove by language
            assert text is None
            if language in t:
                return cast(Text, t.pop(language))
            else:
                return None
        elif text is not None:  # remove by content and language
            assert language is None
            if text.language in t and text == t[text.language]:
                return cast(Text, t.pop(text.language))
            else:
                return None
        else:
            raise KIF_Object._should_not_get_here()

    @staticmethod
    def _remove_from_text_set_map_tail(
            t: TextSetMap,
            text: Text | None,
            language: str | None
    ) -> TextSetMap | TextSet | Text | None:
        if language is not None and language in t:  # remove by language
            assert text is None
            return cast(TextSet, t.pop(language))
        elif text is not None and text.language in t:  # remove by content
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

    def resolve(
            self,
            entities: Iterable[tuple[TEntity, Store]],
            label: bool = False,
            aliases: bool = False,
            description: bool = False,
            language: TTextLanguage | None = None,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            lexeme_language: bool = False,
            all: bool = False,
            force: bool = False,
            function: Location | None = None
    ) -> bool:
        """Resolves entity data using the given stores.

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in `language`.

        If `force` is given, forces resolution.

        Parameters:
           entities: Entity-store pairs.
           label: Whether to resolve labels.
           aliases: Whether to resolve aliases.
           description: Whether to resolve descriptions.
           language: Language.
           range: Whether to resolve ranges.
           inverse: Whether to resolve inverses.
           lemma: Whether to resolve lemmas.
           category: Whether to resolve lexical categories.
           lexeme_language: Whether to resolve lexeme languages.
           all: Whether to resolve all data.
           force: Whether to force resolve.
           function: Function or function name.

        Returns:
           ``True`` if any entity data was resolved; ``False`` otherwise.
        """
        function = function or self.resolve
        return self._resolve(
            entities=map(lambda t: (
                Entity.check(t[0], function, 'entities'), t[1]), entities),
            label=label, aliases=aliases, description=description,
            language=(
                String.check(language, function, 'language').content
                if language is not None else None),
            range=range, inverse=inverse,
            lemma=lemma, category=category, lexeme_language=lexeme_language,
            all=all, force=force)

    def _resolve(
            self,
            entities: Iterable[tuple[Entity, Store]],
            label: bool = False,
            aliases: bool = False,
            description: bool = False,
            language: str | None = None,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            lexeme_language: bool = False,
            all: bool = False,
            force: bool = False,
            _wd_label: Property = LabelProperty(),
            _wd_alias: Property = AliasProperty(),
            _wd_description: Property = DescriptionProperty(),
            _wd_inverse: Property = Property(NS.WD['P1696'], Property),
            _wd_lemma: Property = LemmaProperty(),
            _wd_lexical_category: Property = LexicalCategoryProperty(),
            _wd_language: Property = LanguageProperty(),
    ) -> bool:
        status = False
        if all:
            label = True
            aliases = True
            description = True
            range = True
            inverse = True
            lemma = True
            category = True
            lexeme_language = True
        if not (label or aliases or description
                or range or inverse
                or lemma or category or lexeme_language):
            return status       # nothing to do
        key: Callable[[tuple[Entity, Store]], int] = lambda t: id(t[1])
        pairs = list(self._resolve_preprocess_entities(
            entities, label, aliases, description, language,
            range, inverse, lemma, category, lexeme_language, force))
        id_map = {key(t): t[1] for t in pairs}
        for id_, group in itertools.groupby(sorted(pairs, key=key), key=key):
            store = id_map[id_]
            subject_fp = OrFingerprint(*map(lambda t: t[0], group))
            property_fp = OrFingerprint(
                _wd_label if label else False,
                _wd_alias if aliases else False,
                _wd_description if description else False,
                _wd_inverse if inverse else False,
                _wd_lemma if lemma else False,
                _wd_lexical_category if category else False,
                _wd_language if lexeme_language else False)
            f = Filter(
                subject=subject_fp,
                property=property_fp,
                language=language,
                snak_mask=Filter.VALUE_SNAK)
            for stmt in store.filter(filter=f):
                ###
                # Parse the resulting statements, ignoring inconsistencies.
                ###
                if not isinstance(stmt.snak, ValueSnak):
                    continue
                s, p, v = stmt.subject, stmt.snak.property, stmt.snak.value
                if isinstance(s, (Item, Property)):
                    if p == _wd_label and isinstance(v, Text):
                        status |= bool(self._add_label(s, v))
                    elif p == _wd_alias and isinstance(v, Text):
                        status |= bool(self._add_alias(s, v))
                    elif p == _wd_description and isinstance(v, Text):
                        status |= bool(self._add_description(s, v))
                    if isinstance(s, Property):
                        ###
                        # FIXME: Currently, we always resolve range.
                        ###
                        if s.range is not None:
                            status |= bool(self._add_range(s, s.range))
                        if p == _wd_inverse and isinstance(v, Property):
                            status |= bool(self._add_inverse(s, v))
                elif isinstance(s, Lexeme):
                    if p == _wd_lemma and isinstance(v, Text):
                        status |= bool(self._add_lemma(s, v))
                    elif p == _wd_lexical_category and isinstance(v, Item):
                        status |= bool(self._add_category(s, v))
                    elif p == _wd_language and isinstance(v, Item):
                        status |= bool(self._add_language(s, v))
                else:
                    raise KIF_Object._should_not_get_here()
        return status

    def _resolve_preprocess_entities(
            self,
            entities: Iterable[tuple[Entity, Store]],
            label: bool = False,
            aliases: bool = False,
            description: bool = False,
            language: str | None = None,
            range: bool = False,
            inverse: bool = False,
            lemma: bool = False,
            category: bool = False,
            lexeme_language: bool = False,
            force: bool = False
    ) -> Iterator[tuple[Entity, Store]]:
        for t in entities:
            if force:
                yield t
                continue
            entity, _ = t
            desc = self._describe(entity)
            if not desc:
                yield t
                continue
            if isinstance(entity, (Item, Property)):
                if not language:
                    yield t
                    continue
                if ((label and ('labels' not in desc
                     or language not in desc['labels']))
                    or (aliases and ('aliases' not in desc
                        or language not in desc['aliases']))
                    or (description and ('descriptions' not in desc
                        or language not in desc['descriptions']))):
                    yield t
                    continue
                if isinstance(entity, Property):
                    if (range and 'range' not in desc
                            or inverse and 'inverse' not in desc):
                        yield t
            elif isinstance(entity, Lexeme):
                if ((lemma and 'lemma' not in desc)
                    or (category and 'category' not in desc)
                        or (lexeme_language and 'language' not in desc)):
                    yield t
                    continue
            else:
                raise KIF_Object._should_not_get_here()


class IRI_Registry(Registry):
    """IRI registry.

    Parameters:
       prefixes: Initial prefixes.
    """

    __slots__ = (
        '_nsm',
    )

    #: Namespace manager.
    _nsm: NamespaceManager

    def __init__(self, prefixes: Mapping[Prefix, str] | None = None) -> None:
        prefixes = cast(
            Mapping[Prefix, str], KIF_Object._check_optional_arg_isinstance(
                prefixes, Mapping, {}, type(self), 'prefixes', 1))
        assert prefixes is not None
        super().__init__()
        self._init_nsm()
        for k, v in prefixes.items():
            prefix = String.check(k, type(self), 'prefixes', 1)
            iri = IRI.check(v, type(self), 'prefixes', 1)
            self._add_prefix(iri, prefix.content)

    def _init_nsm(self) -> None:
        self._nsm = NamespaceManager(Graph(), bind_namespaces='none')

    def _reset_nsm(self) -> None:
        self._init_nsm()
        for iri_content, t in self._cache.items():
            if 'prefix' in t:
                self._nsm.bind(t['prefix'], iri_content)

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
        function = function or self.lookup_resolver
        if isinstance(iri, Entity):
            iri = iri.iri
        else:
            iri = IRI.check(iri, function, 'iri')
        resolver = self.get_resolver(iri, function)
        if resolver is not None:
            return resolver
        try:
            ns, _ = split_uri(iri.content)
        except ValueError:
            return None
        else:
            return self.get_resolver(ns, function)

    def lookup_schema(
            self,
            iri: T_IRI | Property,
            function: Location | None = None
    ) -> Property.Schema | None:
        """Searches for property schema for IRI.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Property schema or ``None``.
        """
        function = function or self.lookup_schema
        if isinstance(iri, Property):
            iri = iri.iri
        else:
            iri = IRI.check(iri, function, 'iri')
        schema = self.get_schema(iri, function)
        if schema is not None:
            return schema
        try:
            ns, _ = split_uri(iri.content)
        except ValueError:
            return None
        else:
            return self.get_schema(ns, function)

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
        return cast(Optional[IRI.Descriptor], self._cache.get(iri.content))

    def get_prefix(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> Prefix | None:
        """Gets the IRI prefix.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Prefix or ``None.
        """
        iri = IRI.check(iri, function or self.get_prefix, 'iri')
        return self.get(iri, 'prefix')

    def get_resolver(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> Store | None:
        """Gets the IRI entity resolver.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Store or ``None``.
        """
        iri = IRI.check(iri, function or self.get_resolver, 'iri')
        return self.get(iri, 'resolver')

    def get_schema(
            self,
            iri: T_IRI,
            function: Location | None = None
    ) -> Property.Schema | None:
        """Gets the IRI property schema.

        Parameters:
           iri: IRI.
           function: Function or function name.

        Returns:
           Property schema or ``None``.
        """
        iri = IRI.check(iri, function or self.get_schema, 'iri')
        return self.get(iri, 'schema')

    def register(
            self,
            iri: T_IRI,
            prefix: TString | None = None,
            resolver: Store | None = None,
            schema: Property.TSchema | None = None,
            function: Location | None = None
    ) -> IRI:
        """Adds or updates IRI data.

        Parameters:
           iri: IRI.
           prefix: Prefix.
           resolver: Resolver store.
           schema: Property schema.
           function: Function or function name.

        Returns:
           IRI.
        """
        function = function or self.register
        return self._register(
            iri=IRI.check(iri, function, 'iri'),
            prefix=(String.check(prefix, function, 'prefix').content
                    if prefix is not None else None),
            resolver=KIF_Object._check_optional_arg_isinstance(
                resolver, Store, None, function, 'resolver'),
            schema=cast(Property.Schema, {
                k: IRI.check(v, function, 'schema')
                for k, v in schema.items()}) if schema else None)

    def _register(
            self,
            iri: IRI,
            prefix: Prefix | None,
            resolver: Store | None,
            schema: Property.Schema | None
    ) -> IRI:
        if prefix is not None:
            self._add_prefix(iri, prefix)
        if resolver is not None:
            self._add_resolver(iri, resolver)
        if schema is not None:
            self._add_schema(iri, schema)
        return iri

    def unregister(
            self,
            iri: T_IRI,
            prefix: bool = False,
            resolver: bool = False,
            schema: bool = False,
            all: bool = False,
            function: Location | None = None
    ) -> bool:
        """Remove IRI data.

        Parameters:
           iri: IRI.
           prefix: Whether to remove prefix.
           resolver: Whether to remove resolver.
           schema: Whether to remove property schema.
           all: Whether to remove all data.
           function: Function or function name.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        function = function or self.unregister
        return self._unregister(
            iri=IRI.check(iri, function, 'iri'),
            prefix=bool(prefix),
            resolver=bool(resolver),
            schema=bool(schema),
            all=bool(all))

    def _unregister(
            self,
            iri: IRI,
            prefix: bool = False,
            resolver: bool = False,
            schema: bool = False,
            all: bool = False
    ) -> bool:
        status: bool = False
        if prefix:
            status |= self._remove_prefix(iri) is not None
        if resolver:
            status |= self._remove_resolver(iri) is not None
        if schema:
            status |= self._remove_schema(iri) is not None
        if all:
            status |= self.unset(iri) is not None
        if status:
            self._reset_nsm()
        return status

    def _add_prefix(self, iri: IRI, prefix: Prefix) -> Prefix:
        self._nsm.bind(prefix, iri.content, replace=True)
        return self.set(iri, 'prefix', prefix)

    def _remove_prefix(self, iri: IRI) -> Prefix | None:
        return self.unset(iri, 'prefix')

    def _add_resolver(self, iri: IRI, resolver: Store) -> Store:
        return self.set(iri, 'resolver', resolver)

    def _remove_resolver(self, iri: IRI) -> Store | None:
        return self.unset(iri, 'resolver')

    def _add_schema(
            self,
            iri: IRI,
            schema: Property.Schema
    ) -> Property.Schema:
        return self.set(iri, 'schema', schema)

    def _remove_schema(self, iri: IRI) -> Property.Schema | None:
        return self.unset(iri, 'schema')
