# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import Any, Final, override, TypeAlias, Union
from .flags import Flags
from .kif_object import KIF_Object
from .set import TextSet, TTextSet
from .value import Datatype, Item, TDatatype, Text, TItem, TText


class Descriptor(KIF_Object):
    """Abstract base class for descriptors."""

    class AttributeMask(Flags):
        """Mask for descriptor attributes."""

        #: Mask for the label attribute of descriptor.
        LABEL = Flags.auto()

        #: Mask for the aliases attribute of descriptor.
        ALIASES = Flags.auto()

        #: Mask for the description attribute of descriptor.
        DESCRIPTION = Flags.auto()

        #: Mask for the datatype attribute of descriptor.
        DATATYPE = Flags.auto()

        #: Mask for the lemma attribute of descriptor.
        LEMMA = Flags.auto()

        #: Mask for the lexical category attribute of descriptor.
        CATEGORY = Flags.auto()

        #: Mask for the language attribute of descriptor.
        LANGUAGE = Flags.auto()

        #: Mask for all attributes of item descriptor.
        ITEM_DESCRIPTOR_ATTRIBUTES = LABEL | ALIASES | DESCRIPTION

        #: Mask for all attributes of property descriptor.
        PROPERTY_DESCRIPTOR_ATTRIBUTES = ITEM_DESCRIPTOR_ATTRIBUTES | DATATYPE

        #: Mask for all attributes of lexeme descriptor.
        LEXEME_DESCRIPTOR_ATTRIBUTES = LEMMA | CATEGORY | LANGUAGE

        #: Mask for all attributes of descriptor.
        ALL = (
            ITEM_DESCRIPTOR_ATTRIBUTES
            | PROPERTY_DESCRIPTOR_ATTRIBUTES
            | LEXEME_DESCRIPTOR_ATTRIBUTES)

    #: Mask for the label attribute of descriptor.
    LABEL: Final[AttributeMask] = AttributeMask.LABEL

    #: Mask for the aliases attribute of descriptor.
    ALIASES: Final[AttributeMask] = AttributeMask.ALIASES

    #: Mask for the description attribute of descriptor.
    DESCRIPTION: Final[AttributeMask] = AttributeMask.DESCRIPTION

    #: Mask for the datatype attribute of descriptor.
    DATATYPE: Final[AttributeMask] = AttributeMask.DATATYPE

    #: Mask for the lemma attribute of descriptor.
    LEMMA: Final[AttributeMask] = AttributeMask.LEMMA

    #: Mask for the lexical category attribute of descriptor.
    CATEGORY: Final[AttributeMask] = AttributeMask.CATEGORY

    #: Mask for the language attribute of descriptor.
    LANGUAGE: Final[AttributeMask] = AttributeMask.LANGUAGE

    #: Mask for all attributes of item descriptor.
    ITEM_DESCRIPTOR_ATTRIBUTES: Final[AttributeMask] =\
        AttributeMask.ITEM_DESCRIPTOR_ATTRIBUTES

    #: Mask for all attributes of property descriptor.
    PROPERTY_DESCRIPTOR_ATTRIBUTES: Final[AttributeMask] =\
        AttributeMask.PROPERTY_DESCRIPTOR_ATTRIBUTES

    #: Mask for all attributes of lexeme descriptor.
    LEXEME_DESCRIPTOR_ATTRIBUTES: Final[AttributeMask] =\
        AttributeMask.LEXEME_DESCRIPTOR_ATTRIBUTES

    #: Mask for all attributes of descriptor.
    ALL: Final[AttributeMask] = AttributeMask.ALL

    TAttributeMask: TypeAlias = Union[AttributeMask, int]


class PlainDescriptor(Descriptor):
    """Abstract base class for plain descriptors."""

    #: Default aliases.
    default_aliases: Final[TextSet] = TextSet()

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # label
            return Text.check_optional(arg, None, type(self), None, i)
        elif i == 2:            # aliases
            return TextSet.check_optional(
                arg, self.default_aliases, type(self), None, i)
        elif i == 3:            # description
            return Text.check_optional(arg, None, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def label(self) -> Text | None:
        """The label of plain descriptor."""
        return self.get_label()

    def get_label(self, default: Text | None = None) -> Text | None:
        """Gets the label of plain descriptor.

        If the label is ``None``, returns `default`.

        Parameters:
           default: Default label.

        Returns:
           Label.
        """
        return self.get(0, default)

    @property
    def aliases(self) -> TextSet:
        """The aliases of plain descriptor."""
        return self.get_aliases()

    def get_aliases(self) -> TextSet:
        """Gets the aliases of plain descriptor.

        Returns:
           Aliases.
        """
        return self.args[1]

    @property
    def description(self) -> Text | None:
        """The description of plain descriptor."""
        return self.get_description()

    def get_description(self, default: Text | None = None) -> Text | None:
        """Gets the description of plain descriptor.

        If the description is ``None``, returns `default`.

        Parameters:
           default: Default description.

        Returns:
           Description.
        """
        return self.get(2, default)


class ItemDescriptor(PlainDescriptor):
    """Item descriptor.

    Parameters:
       label: Label.
       aliases: Aliases.
       description: Description.
    """

    def __init__(
            self,
            label: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None
    ) -> None:
        super().__init__(label, aliases, description)


class PropertyDescriptor(PlainDescriptor):
    """Property descriptor.

    Parameters:
       label: Label.
       aliases: Aliases.
       description: Description.
       datatype: Datatype.
    """

    def __init__(
            self,
            label: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None,
            datatype: TDatatype | None = None
    ) -> None:
        super().__init__(label, aliases, description, datatype)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 4:              # datatype
            return Datatype.check_optional(arg, None, type(self), None, i)
        else:
            return super()._preprocess_arg(arg, i)

    @property
    def datatype(self) -> Datatype | None:
        """The datatype of property descriptor."""
        return self.get_datatype()

    def get_datatype(self, default: Datatype | None = None) -> Datatype | None:
        """Gets the datatype of property descriptor.

        If the datatype is ``None``, returns `default`.

        Parameters:
           default: Default datatype.

        Returns:
           Datatype.
        """
        return self.get(3, default)


class LexemeDescriptor(Descriptor):
    """Lexeme descriptor.

    Parameters:
       lemma: Lemma.
       category: Lexical category.
       language: Language.
    """

    def __init__(
            self,
            lemma: TText | None = None,
            category: TItem | None = None,
            language: TItem | None = None
    ) -> None:
        super().__init__(lemma, category, language)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # lemma
            return Text.check_optional(arg, None, type(self), None, i)
        elif i == 2:            # category
            return Item.check_optional(arg, None, type(self), None, i)
        elif i == 3:            # language
            return Item.check_optional(arg, None, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def lemma(self) -> Text | None:
        """The lemma of lexeme descriptor."""
        return self.get_lemma()

    def get_lemma(self, default: Text | None = None) -> Text | None:
        """Gets the lemma of lexeme descriptor.

        If the lemma is ``None``, returns `default`.

        Parameters:
           default: Default lemma.

        Returns:
           Lemma.
        """
        return self.get(0, default)

    @property
    def category(self) -> Item | None:
        """The lexical category of lexeme descriptor."""
        return self.get_category()

    def get_category(self, default: Item | None = None) -> Item | None:
        """Gets the lexical category of lexeme descriptor.

        If the lexical category is ``None``, returns `default`.

        Parameters:
           default: Default lexical category.

        Returns:
           Lexical category.
        """
        return self.get(1, default)

    @property
    def language(self) -> Item | None:
        """The language of lexeme descriptor."""
        return self.get_language()

    def get_language(self, default: Item | None = None) -> Item | None:
        """Gets the language of lexeme descriptor.

        If the language is ``None``, returns `default`.

        Parameters:
           default: Default language.

        Returns:
           Language.
        """
        return self.get(2, default)
