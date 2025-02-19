# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing_extensions import overload

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
    TLexeme,
    TProperty,
    TString,
    TText,
)
from ..rdflib import Graph, NamespaceManager
from ..typing import Any, cast, Mapping, TypeAlias, TypedDict
from .context import Context

NilType: TypeAlias = KIF_Object.NilType
Nil = KIF_Object.Nil


class Registry:
    """KIF registry."""

    class ItemEntry(TypedDict):
        """Item entry in registry."""
        labels: Mapping[str, Text]  # indexed by language

    class PropertyEntry(TypedDict):
        """Property entry in registry."""
        datatype: Datatype
        inverse: Property | None
        labels: Mapping[str, Text]  # indexed by language

    class LexemeEntry(TypedDict):
        """Lexeme entry in registry."""
        lemma: Text
        category: Item
        language: Item

    __slots__ = (
        '_context',
        '_entity_cache',
        '_ns_manager',
        '_ns_prefix_table',
    )

    #: Parent context.
    _context: Context

    #: Entity cache.
    _entity_cache: Cache

    #: Namespace manager.
    _ns_manager: NamespaceManager

    #: Namespace prefix table.
    _ns_prefix_table: dict[str, IRI]

    def __init__(
            self,
            context: Context,
            prefixes: Mapping[str, Any] | None = None
    ) -> None:
        self._context = context
        self._entity_cache = Cache()
        self._ns_prefix_table = {
            str(k): IRI.check(str(v), type(self), 'prefixes', 2)
            for k, v in (prefixes or {}).items()
        }
        self._reset_ns_manager()

    def _reset_ns_manager(self) -> None:
        self._ns_manager = NamespaceManager(Graph(), bind_namespaces='none')
        for prefix, iri in self._ns_prefix_table.items():
            self._ns_manager.bind(prefix, iri.content)

    @property
    def context(self) -> Context:
        """The parent context."""
        return self.get_context()

    def get_context(self) -> Context:
        """Gets the parent context.

        Returns:
           Context.
        """
        return self._context

    def display(
            self,
            entity: Entity,
            default: TString | NilType | None = Nil
    ) -> str | None:
        """Gets a human-readable name for `entity`.

        Parameters:
           entity: Entity.
           default: Default human-readable name.

        Returns:
           Human-readable name.
        """
        entity = Entity.check(entity, self.display, 'entity', 1)
        name = None
        if isinstance(entity, (Item, Property)):
            label = self.get_label(entity)
            if label:
                name = label.content
        if name:
            return name
        else:
            try:
                return self._ns_manager.curie(entity.iri.content, False)
            except BaseException:
                if default is Nil:
                    return entity.iri.content
                elif default is None:
                    return None
                else:
                    return String.check(
                        default, self.display, 'default', 2).content

    def get_prefix(self, prefix: str) -> IRI | None:
        """Gets the namespace of `prefix` in registry.

        Parameters:
           prefix: Prefix.

        Returns:
           Namespace or ``None`` (no namespace for prefix).
        """
        return self._ns_prefix_table.get(prefix)

    def set_prefix(self, prefix: str, namespace: T_IRI) -> IRI:
        """Sets the namespace of `prefix` in registry.

        Parameters:
           prefix: Prefix.
           namespace: IRI.

        Returns:
           Namespace.
        """
        iri = IRI.check(namespace, self.set_prefix, 'namespace', 2)
        self._ns_prefix_table[prefix] = iri
        self._ns_manager.bind(prefix, iri.content, replace=True)
        return iri

    def unset_prefix(self, prefix: str) -> IRI | None:
        """Unsets the namespace of `prefix` in registry.

        Parameters:
           prefix: Prefix.

        Returns:
           Namespace or ``None`` (no namespace for prefix).
        """
        iri = self._ns_prefix_table.pop(prefix)
        if iri is not None:
            self._reset_ns_manager()
        return iri

    @overload
    def describe(self, entity: Item) -> ItemEntry | None:
        """Describes item.

        Parameters:
           entity: Item.

        Returns:
           Item entry in registry or ``None`` (no entry for item).
        """
        ...                     # pragma: no cover

    @overload
    def describe(self, entity: Property) -> PropertyEntry | None:
        """Describes property.

        Parameters:
           entity: Property.

        Returns:
           Property entry in registry or ``None`` (no entry for property).
        """
        ...                     # pragma: no cover

    @overload
    def describe(self, entity: Lexeme) -> LexemeEntry | None:
        """Describes lexeme.

        Parameters:
           entity: Lexeme.

        Returns:
           Lexeme entry in registry or ``None`` (no entry for lexeme).
        """
        ...                     # pragma: no cover

    def describe(
            self,
            entity: Item | Property | Lexeme
    ) -> ItemEntry | PropertyEntry | LexemeEntry | None:
        entry = self._entity_cache._cache.get(entity.iri.content, None)
        if entry is not None:
            if isinstance(entity, Item):
                return cast(Registry.ItemEntry, entry)
            elif isinstance(entity, Property):
                return cast(Registry.PropertyEntry, entry)
            elif isinstance(entity, Lexeme):
                return cast(Registry.LexemeEntry, entry)
            else:
                raise KIF_Object._should_not_get_here()
        else:
            return None

    def get_label(
            self,
            entity: Item | Property,
            language: TString | None = None
    ) -> Text | None:
        """Gets the label of `entity` in registry.

        Parameters:
           entity: Item or property.
           language: Language.

        Returns:
           Label or ``None`` (no label for language).
        """
        if isinstance(entity, (Item, Property)):
            key = entity.iri.content
        else:
            key = IRI.check(entity, self.get_label, 'entity', 1).content
        language = String.check_optional(
            language, self.context.options.language,
            self.get_label, 'language', 2)
        assert language is not None
        language = language.content
        labels = self._entity_cache.get(key, 'labels')
        if labels and language in labels:
            return labels[language]
        else:
            return None

    def set_label(self, entity: Item | Property, label: TText) -> Text:
        """Sets the label of `entity` in registry.

        Parameters:
           entity: Item or property.
           label: Label.

        Returns:
           Label.
        """
        if isinstance(entity, (Item, Property)):
            key = entity.iri.content
        else:
            key = IRI.check(entity, self.set_label, 'entity', 1).content
        label = Text.check(label, self.set_label, 'label', 2)
        labels: dict[str, Text] = (
            self._entity_cache.get(key, 'labels')
            or self._entity_cache.set(key, 'labels', {}))
        labels[label.language] = label
        return label

    def unset_label(
            self,
            entity: Item | Property,
            language: TString | None = None
    ) -> Text | None:
        """Unsets the label of `entity` in registry.

        Parameters:
           language: Language.

        Returns:
           The unset label or ``None`` (no label for language).
        """
        if isinstance(entity, (Item, Property)):
            key = entity.iri.content
        else:
            key = IRI.check(entity, self.set_label, 'entity', 1).content
        language = String.check_optional(
            language, self.context.options.language,
            self.get_label, 'language', 2)
        assert language is not None
        language = language.content
        labels = self._entity_cache.get(key, 'labels')
        if labels:
            if language in labels:
                return labels.pop(language)
            elif language is None:
                self._entity_cache.unset(key, 'labels')
        return None

    def get_datatype(self, property: TProperty) -> Datatype | None:
        """Gets the datatype of `property` in registry.

        Parameters:
           property: Property.

        Returns:
           Datatype or ``None`` (no datatype for property).
        """
        prop = Property.check(property, self.get_datatype, 'property', 1)
        return self._entity_cache.get(prop.iri.content, 'datatype')

    def set_datatype(
            self,
            property: TProperty,
            datatype: TDatatype
    ) -> Datatype:
        """Sets the datatype of `property` in registry.

        Parameters:
           property: Property.
           datatype: Datatype.

        Returns:
           Datatype.
        """
        prop = Property.check(property, self.set_datatype, 'property', 1)
        dt = Datatype.check(datatype, self.set_datatype, 'datatype', 2)
        return self._entity_cache.set(prop.iri.content, 'datatype', dt)

    def unset_datatype(self, property: TProperty) -> Datatype | None:
        """Unsets the datatype of `property` in registry.

        Parameters:
           property: Property.

        Returns:
           The unset datatype or ``None`` (no datatype for property).
        """
        prop = Property.check(property, self.unset_datatype, 'property', 1)
        return self._entity_cache.unset(prop.iri.content, 'datatype')

    def get_inverse(self, property: TProperty) -> Property | None:
        """Gets the inverse of `property` in registry.

        Parameters:
           property: Property.

        Returns:
           Inverse property or ``None`` (no inverse for property).
        """
        prop = Property.check(property, self.get_inverse, 'property', 1)
        return self._entity_cache.get(prop.iri.content, 'inverse')

    def set_inverse(self, property: Property, inverse: TProperty) -> Property:
        """Sets the inverse of `property` in registry.

        Parameters:
           property: Property.
           inverse: Property.

        Returns:
           Inverse property.
        """
        prop = Property.check(property, self.set_inverse, 'property', 1)
        iprop = Property.check(inverse, self.set_inverse, 'inverse', 2)
        return self._entity_cache.set(prop.iri.content, 'inverse', iprop)

    def unset_inverse(self, property: Property) -> Property | None:
        """Unsets the inverse of `property` in registry.

        Parameters:
           property: Property.

        Returns:
           The unset property or ``None`` (no inverse for property).
        """
        prop = Property.check(property, self.unset_inverse, 'property', 1)
        return self._entity_cache.unset(prop.iri.content, 'inverse')

    def get_lemma(self, lexeme: TLexeme) -> Text | None:
        """Gets the lemma of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           Lemma or ``None`` (no lemma for language).
        """
        lex = Lexeme.check(lexeme, self.get_lemma, 'lexeme', 1)
        return self._entity_cache.get(lex.iri.content, 'lemma')

    def set_lemma(self, lexeme: TLexeme, lemma: TText) -> Text:
        """Sets the lemma of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.
           lemma: Lemma.

        Returns:
           Lemma.
        """
        lex = Lexeme.check(lexeme, self.set_lemma, 'lexeme', 1)
        lemma = Text.check(lemma, self.set_lemma, 'lemma', 2)
        return self._entity_cache.set(lex.iri.content, 'lemma', lemma)

    def unset_lemma(self, lexeme: TLexeme) -> Text | None:
        """Unsets the lemma of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           The unset lemma or ``None`` (no lemma for lexeme).
        """
        lex = Lexeme.check(lexeme, self.unset_lemma, 'lexeme', 1)
        return self._entity_cache.unset(lex.iri.content, 'lemma')

    def get_category(self, lexeme: TLexeme) -> Item | None:
        """Gets the lexical category of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           Lexical category or ``None`` (no category for lexeme).
        """
        lex = Lexeme.check(lexeme, self.get_category, 'lexeme', 1)
        return self._entity_cache.get(lex.iri.content, 'category')

    def set_category(self, lexeme: TLexeme, category: TItem) -> Item:
        """Sets the category of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.
           category: Lexical category.

        Returns:
           Lexical category.
        """
        lex = Lexeme.check(lexeme, self.set_category, 'lexeme', 1)
        cat = Item.check(category, self.set_category, 'category', 2)
        return self._entity_cache.set(lex.iri.content, 'category', cat)

    def unset_category(self, lexeme: TLexeme) -> Item | None:
        """Unsets the lexical category of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           The unset lexical category or ``None`` (no category for lexeme).
        """
        lex = Lexeme.check(lexeme, self.unset_category, 'lexeme', 1)
        return self._entity_cache.unset(lex.iri.content, 'category')

    def get_language(self, lexeme: TLexeme) -> Item | None:
        """Gets the language of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           Language or ``None`` (no language for lexeme).
        """
        lex = Lexeme.check(lexeme, self.get_language, 'lexeme', 1)
        return self._entity_cache.get(lex.iri.content, 'language')

    def set_language(self, lexeme: TLexeme, language: TItem) -> Item:
        """Sets the language of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.
           language: Language.

        Returns:
           Language.
        """
        lex = Lexeme.check(lexeme, self.set_language, 'lexeme', 1)
        lang = Item.check(language, self.set_language, 'language', 2)
        return self._entity_cache.set(lex.iri.content, 'language', lang)

    def unset_language(self, lexeme: TLexeme) -> Item | None:
        """Unsets the language of `lexeme` in registry.

        Parameters:
           lexeme: Lexeme.

        Returns:
           The unset language or ``None`` (no language for lexeme).
        """
        lex = Lexeme.check(lexeme, self.unset_category, 'lexeme', 1)
        return self._entity_cache.unset(lex.iri.content, 'language')

    def make_item(self, item: TItem, label: TText | None = None) -> Item:
        """Creates item and update its entry in registry.

        If `label` is given, update item's label in registry.

        Parameters:
           item: Item.
           label: Label.

        Returns:
           The resulting item.
        """
        item = Item.check(item, self.make_item, 'item', 1)
        if label:
            self.set_label(item, label)
        return item

    def make_property(
            self,
            property: TProperty,
            label: TText | None = None,
            datatype: TDatatype | None = None,
            inverse: TProperty | None = None
    ) -> Property:
        """Creates property and updates its entry in registry.

        If `label` is given, updates property's label in registry.
        If `datatype` is given, updates property's datatype in registry.
        If `inverse` is given, updates property's inverse in registry.

        Parameters:
           property: Property.
           label: Label.
           datatype: Datatype.
           inverse: Inverse property.

        Returns:
           The resulting property.
        """
        prop = Property.check(property, self.make_property, 'property', 1)
        if label:
            self.set_label(prop, label)
        if datatype:
            prop = Property(prop.iri, self.set_datatype(prop, datatype))
        else:
            if prop.range is not None:
                self.set_datatype(prop, prop.range)
            else:
                prop = Property(prop.iri, self.get_datatype(prop))
        if inverse:
            self.set_inverse(prop, inverse)
        return prop

    def make_lexeme(
            self,
            lexeme: TLexeme,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None
    ) -> Lexeme:
        """Creates lexeme and updates its entry in registry.

        If `lemma` is given, updates lexeme's lemma in registry.
        If `category` is given, updates lexeme's category in registry.
        If `language` is given, updates lexeme's language in registry.

        Parameters:
           lexeme: Lexeme.
           lemma: Lemma.
           category: Lexical category.
           language: Language.

        Returns:
           The resulting lexeme.
        """
        lexeme = Lexeme.check(lexeme, self.make_lexeme, 'lexeme', 1)
        if lemma:
            self.set_lemma(lexeme, lemma)
        if category:
            self.set_category(lexeme, category)
        if language:
            self.set_language(lexeme, language)
        return lexeme
