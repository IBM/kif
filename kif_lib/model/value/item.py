# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import overload

from ...typing import (
    cast,
    ClassVar,
    Iterable,
    Mapping,
    override,
    Self,
    Set,
    TypeAlias,
    TypedDict,
    Union,
)
from ..term import Template, Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .text import Text, TText, TTextLanguage, TTextSet
from .value import Datatype

if TYPE_CHECKING:               # pragma: no cover
    from ...store import Store
    from ..snak import ValueSnak
    from .quantity import Quantity, QuantityTemplate, TQuantity

TItem: TypeAlias = Union['Item', T_IRI]
VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']
VTItem: TypeAlias = Union[Variable, VItem, TItem]
VTItemContent: TypeAlias = Union[Variable, IRI_Template, TItem]


class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[type[Item]]  # pyright: ignore

    def __init__(self, iri: VTItemContent) -> None:
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Item]]  # pyright: ignore


class ItemDatatype(Datatype):
    """Item datatype."""

    instance: ClassVar[ItemDatatype]  # pyright: ignore
    value_class: ClassVar[type[Item]]  # pyright: ignore


class Item(
        Entity,
        datatype_class=ItemDatatype,
        template_class=ItemTemplate,
        variable_class=ItemVariable
):
    """Person or thing.

    Parameters:
       iri: IRI.
    """

    datatype_class: ClassVar[type[ItemDatatype]]  # pyright: ignore
    datatype: ClassVar[ItemDatatype]              # pyright: ignore
    template_class: ClassVar[type[ItemTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ItemVariable]]  # pyright: ignore

    class Descriptor(TypedDict, total=False):
        """Item descriptor in KIF context."""

        #: Label indexed by language.
        labels: Mapping[str, Text]

        #: Aliases indexed by language.
        aliases: Mapping[str, Set[Text]]

        #: Description indexed by language.
        descriptions: Mapping[str, Text]

    @classmethod
    def descriptor_to_snaks(
            cls,
            descriptor: Descriptor
    ) -> Iterable[ValueSnak]:
        """Converts item descriptor to (value) snaks.

        Parameters:
           descriptor: Item descriptor.

        Returns:
           (Value) snaks.
        """
        if 'labels' in descriptor:
            from .pseudo_property import LabelProperty
            for label in descriptor['labels'].values():
                yield LabelProperty()(label)
        if 'aliases' in descriptor:
            from .pseudo_property import AliasProperty
            for aliases in descriptor['aliases'].values():
                yield from map(AliasProperty(), aliases)
        if 'description' in descriptor:
            from .pseudo_property import DescriptionProperty
            for description in descriptor['descriptions'].values():
                yield DescriptionProperty()(description)

    def __init__(self, iri: VTItemContent) -> None:
        super().__init__(iri)

    @overload
    def __rmatmul__(self, other: QuantityTemplate) -> QuantityTemplate:
        """Constructs quantity template using item as the unit.

        Parameters:
           other: Quantity template.

        Returns:
           Quantity template.
        """
        ...                     # pragma: no cover

    @overload
    def __rmatmul__(self, other: TQuantity) -> Quantity:
        """Constructs quantity using item as the unit.

        Parameters:
           other: Quantity.

        Returns:
           Quantity template.
        """
        ...                     # pragma: no cover

    def __rmatmul__(
            self,
            other: QuantityTemplate | TQuantity
    ) -> QuantityTemplate | Quantity:
        from .quantity import Quantity, QuantityTemplate
        if isinstance(other, Template):
            return QuantityTemplate.check(other).replace(
                self.KEEP, self, self.KEEP, self.KEEP)
        else:
            return Quantity.check(other).replace(
                self.KEEP, self, self.KEEP, self.KEEP)

    @override
    def display(self, language: TTextLanguage | None = None) -> str:
        label = self.get_label(language)
        if label:
            return label.content
        else:
            return super().display(language)  # fallback

    def describe(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Item.Descriptor | None:
        """Gets the descriptor of item in KIF context.

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in all languages.

        If `resolve` is ``True``, resolves item data.

        If `resolver` is given, uses it to resolve item data.
        Otherwise, uses the resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Item descriptor or ``None``.
        """
        return self.context.describe(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.describe)

    @property
    def label(self) -> Text | None:
        """The label of item in KIF context."""
        return self.get_label()

    def get_label(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Text | None:
        """Gets the label of item in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve label.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Label or ``None``.
        """
        return self.context.get_label(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_label)

    @property
    def aliases(self) -> Set[Text] | None:
        """The aliases of item in KIF context."""
        return self.get_aliases()

    def get_aliases(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Set[Text] | None:
        """Gets the aliases of item in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve aliases.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Aliases or ``None``.
        """
        return self.context.get_aliases(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_aliases)

    @property
    def description(self) -> Text | None:
        """The description of item in KIF context."""
        return self.get_description()

    def get_description(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Text | None:
        """Gets the description of item in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve description.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Description or ``None``.
        """
        return self.context.get_description(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_description)

    def register(
            self,
            label: TText | None = None,
            labels: TTextSet | None = None,
            alias: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None,
            descriptions: TTextSet | None = None
    ) -> Self:
        """Adds or updates item data in KIF context.

        Parameters:
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.

        Returns:
           Item.
        """
        return cast(Self, self.context.entities.register(
            self, label=label, labels=labels, alias=alias, aliases=aliases,
            description=description, descriptions=descriptions,
            function=self.register))

    def unregister(
            self,
            label: TText | None = None,
            labels: TTextSet | None = None,
            alias: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None,
            descriptions: TTextSet | None = None,
            label_language: TTextLanguage | None = None,
            alias_language: TTextLanguage | None = None,
            description_language: TTextLanguage | None = None,
            all_labels: bool = False,
            all_aliases: bool = False,
            all_descriptions: bool = False
    ) -> bool:
        """Removes item data from KIF context.

        If called with no arguments, removes all item data.

        Parameters:
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

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        if (label is None and labels is None
                and alias is None and aliases is None
                and description is None and descriptions is None
                and label_language is None
                and alias_language is None
                and description_language is None
                and all_labels is False
                and all_aliases is False
                and all_descriptions is False):
            return self.context.entities.unregister(
                self, all=True, function=self.unregister)
        else:
            return self.context.entities.unregister(
                self, label=label, labels=labels,
                alias=alias, aliases=aliases,
                description=description, descriptions=descriptions,
                label_language=label_language, alias_language=alias_language,
                description_language=description_language,
                all_labels=all_labels, all_aliases=all_aliases,
                all_descriptions=all_descriptions, function=self.unregister)


def Items(iri: VTItemContent, *iris: VTItemContent) -> Iterable[Item]:
    """Constructs one or more items.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting items.
    """
    from ... import itertools
    return map(Item, itertools.chain((iri,), iris))
