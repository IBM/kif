# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ...typing import (
    cast,
    ClassVar,
    Iterable,
    override,
    Self,
    TypeAlias,
    TypedDict,
    Union,
)
from ..term import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .item import Item, TItem
from .string import TString
from .text import Text, TText
from .value import Datatype

if TYPE_CHECKING:               # pragma: no cover
    from ...store import Store
    from ..snak import ValueSnak

TLexeme: TypeAlias = Union['Lexeme', T_IRI]
VLexeme: TypeAlias = Union['LexemeTemplate', 'LexemeVariable', 'Lexeme']
VTLexeme: TypeAlias = Union[Variable, VLexeme, TLexeme]
VTLexemeContent: TypeAlias = Union[Variable, IRI_Template, TLexeme]


class LexemeTemplate(EntityTemplate):
    """Lexeme template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[type[Lexeme]]  # pyright: ignore

    def __init__(self, iri: VTLexemeContent) -> None:
        super().__init__(iri)


class LexemeVariable(EntityVariable):
    """Lexeme variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Lexeme]]  # pyright: ignore


class LexemeDatatype(Datatype):
    """Lexeme datatype."""

    instance: ClassVar[LexemeDatatype]  # pyright: ignore
    value_class: ClassVar[type[Lexeme]]  # pyright: ignore


class Lexeme(
        Entity,
        datatype_class=LexemeDatatype,
        template_class=LexemeTemplate,
        variable_class=LexemeVariable
):
    """Word or phrase.

    Parameters:
       iri: IRI.
    """

    datatype_class: ClassVar[type[LexemeDatatype]]  # pyright: ignore
    datatype: ClassVar[LexemeDatatype]              # pyright: ignore
    template_class: ClassVar[type[LexemeTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[LexemeVariable]]  # pyright: ignore

    class Descriptor(TypedDict, total=False):
        """Lexeme descriptor."""

        #: Lemma.
        lemma: Text

        #: Lexical category.
        category: Item

        #: Language.
        language: Item

    @classmethod
    def descriptor_to_snaks(
            cls,
            descriptor: Descriptor,
    ) -> Iterable[ValueSnak]:
        """Converts lexeme descriptor to (value) snaks.

        Parameters:
           descriptor: Lexeme descriptor.

        Returns:
           (Value) snaks.
        """
        if 'lemma' in descriptor:
            from .pseudo_property import LemmaProperty
            yield LemmaProperty()(descriptor['lemma'])
        if 'category' in descriptor:
            from .pseudo_property import LexicalCategoryProperty
            yield LexicalCategoryProperty()(descriptor['category'])
        if 'language' in descriptor:
            from .pseudo_property import LanguageProperty
            yield LanguageProperty()(descriptor['language'])

    def __init__(self, iri: VTLexemeContent) -> None:
        super().__init__(iri)

    @override
    def display(self, language: TString | None = None) -> str:
        return super().display(language)  # fallback

    def describe(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Lexeme.Descriptor | None:
        """Gets the descriptor of lexeme in KIF context.

        If `resolve` is ``True``, resolves property data.

        If `resolver` is given, uses it to resolve lexeme data.
        Otherwise, uses the resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Lexeme descriptor or ``None``.
        """
        return self.context.describe(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.describe)

    @property
    def lemma(self) -> Text | None:
        """The lemma of lexeme in KIF context."""
        return self.get_lemma()

    def get_lemma(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Text | None:
        """Gets the lemma of lexeme in KIF context.

        Parameters:
           resolve: Whether to resolve lemma.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Lemma or ``None``.
        """
        return self.context.get_lemma(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.get_lemma)

    @property
    def category(self) -> Item | None:
        """The category of lexeme in KIF context."""
        return self.get_category()

    def get_category(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Item | None:
        """Gets the lexical category of lexeme in KIF context.

        Parameters:
           resolve: Whether to resolve lexical category.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Lexical category or ``None``.
        """
        return self.context.get_category(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.get_category)

    @property
    def language(self) -> Item | None:
        """The language of lexeme in KIF context."""
        return self.get_language()

    def get_language(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Item | None:
        """Gets the language of lexeme in KIF context.

        Parameters:
           resolve: Whether to resolve language.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Language or ``None``.
        """
        return self.context.get_language(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.get_language)

    def register(
            self,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None,
    ) -> Self:
        """Adds or updates lexeme data in KIF context.

        Parameters:
           lemma: Lemma.
           category: Lexical category.
           language: Language.

        Returns:
           Lexeme.
        """
        return cast(Self, self.context.entities.register(
            self, lemma=lemma, category=category, language=language,
            function=self.register))

    def unregister(
            self,
            lemma: bool = False,
            category: bool = False,
            language: bool = False
    ) -> bool:
        """Removes lexeme data from KIF context.

        If called with no arguments, removes all lexeme data.

        Parameters:
           lemma: Whether to remove lemma.
           category: Whether to remove category.
           language: Whether to remove language.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        if lemma is False and category is False and language is False:
            return self.context.entities.unregister(
                self, all=True, function=self.unregister)
        else:
            return self.context.entities.unregister(
                self, lemma=lemma, category=category, language=language,
                function=self.unregister)


def Lexemes(iri: VTLexemeContent, *iris: VTLexemeContent) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting lexemes.
    """
    from ... import itertools
    return map(Lexeme, itertools.chain([iri], iris))
