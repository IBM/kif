# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Any, Final, Optional, override, Union
from .kif_object import KIF_Object, TLocation
from .set import TextSet, TTextSet
from .value import Datatype, Item, Text, TText


class Descriptor(KIF_Object):
    """Abstract base class for descriptors."""

    class AttributeMask(Flag):
        """Mask for descriptor attributes."""

        #: Mask for the label attribute of descriptor.
        LABEL = auto()

        #: Mask for the aliases attribute of descriptor.
        ALIASES = auto()

        #: Mask for the description attribute of descriptor.
        DESCRIPTION = auto()

        #: Mask for the datatype attribute of descriptor.
        DATATYPE = auto()

        #: Mask for the lemma attribute of descriptor.
        LEMMA = auto()

        #: Mask for the lexical category attribute of descriptor.
        CATEGORY = auto()

        #: Mask for the language attribute of descriptor.
        LANGUAGE = auto()

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

    TAttributeMask = Union[AttributeMask, int]

    @classmethod
    def _check_arg_descriptor_attribute_mask(
            cls,
            arg: TAttributeMask,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> AttributeMask:
        return cls.AttributeMask(cls._check_arg_isinstance(
            arg, (cls.AttributeMask, int), function, name, position))

    @classmethod
    def _check_optional_arg_descriptor_attribute_mask(
            cls,
            arg: Optional[TAttributeMask],
            default: Optional[AttributeMask] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[AttributeMask]:
        if arg is None:
            return default
        else:
            return cls._check_arg_descriptor_attribute_mask(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_descriptor_attribute_mask(
            cls,
            arg: TAttributeMask,
            i: int,
            function: Optional[TLocation] = None
    ) -> AttributeMask:
        return cls._check_arg_descriptor_attribute_mask(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_descriptor_attribute_mask(
            cls,
            arg,
            i: int,
            default: Optional[AttributeMask] = None,
            function: Optional[TLocation] = None
    ) -> Optional[AttributeMask]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_descriptor_attribute_mask(
                arg, i, function)


class PlainDescriptor(Descriptor):
    """Abstract base class for plain descriptors."""

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            return self._preprocess_optional_arg_text(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_text_set(arg, i, TextSet())
        elif i == 3:
            return self._preprocess_optional_arg_text(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def label(self) -> Optional[Text]:
        """The label of plain descriptor."""
        return self.get_label()

    def get_label(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets the label of plain descriptor.

        If the label is ``None``, returns `default`.

        Parameters:
           default: Default label.

        Returns:
           Label.
        """
        label = self.args[0]
        return label if label is not None else default

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
    def description(self) -> Optional[Text]:
        """The description of plain descriptor."""
        return self.get_description()

    def get_description(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets the description of plain descriptor.

        If the description is ``None``, returns `default`.

        Parameters:
           default: Default description.

        Returns:
           Description.
        """
        description = self.args[2]
        return description if description is not None else default


class ItemDescriptor(PlainDescriptor):
    """Item descriptor.

    Parameters:
       label: Label.
       aliases: Aliases.
       description: Description.
    """

    def __init__(
            self,
            label: Optional[TText] = None,
            aliases: Optional[TTextSet] = None,
            description: Optional[TText] = None
    ):
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
            label: Optional[TText] = None,
            aliases: Optional[TTextSet] = None,
            description: Optional[TText] = None,
            datatype: Optional[Datatype] = None
    ):
        super().__init__(label, aliases, description, datatype)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 4:
            return self._preprocess_optional_arg_datatype(arg, i)
        else:
            return super()._preprocess_arg(arg, i)

    @property
    def datatype(self) -> Optional[Datatype]:
        """The datatype of property descriptor."""
        return self.get_datatype()

    def get_datatype(
            self,
            default: Optional[Datatype] = None
    ) -> Optional[Datatype]:
        """Gets the datatype of property descriptor.

        If the datatype is ``None``, returns `default`.

        Parameters:
           default: Default datatype.

        Returns:
           Datatype.
        """
        datatype = self.args[3]
        return datatype if datatype is not None else default


class LexemeDescriptor(Descriptor):
    """Lexeme descriptor.

    Parameters:
       lemma: Lemma.
       category: Lexical category.
       language: Language.
    """

    def __init__(
            self,
            lemma: Optional[TText] = None,
            category: Optional[Item] = None,
            language: Optional[Item] = None
    ):
        super().__init__(lemma, category, language)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            return self._preprocess_optional_arg_text(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_item(arg, i)
        elif i == 3:
            return self._preprocess_optional_arg_item(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def lemma(self) -> Optional[Text]:
        """The lemma of lexeme descriptor."""
        return self.get_lemma()

    def get_lemma(self, default: Optional[Text] = None) -> Optional[Text]:
        """Gets the lemma of lexeme descriptor.

        If the lemma is ``None``, returns `default`.

        Parameters:
           default: Default lemma.

        Returns:
           Lemma.
        """
        lemma = self.args[0]
        return lemma if lemma is not None else default

    @property
    def category(self) -> Optional[Item]:
        """The lexical category of lexeme descriptor."""
        return self.get_category()

    def get_category(self, default: Optional[Item] = None) -> Optional[Item]:
        """Gets the lexical category of lexeme descriptor.

        If the lexical category is ``None``, returns `default`.

        Parameters:
           default: Default lexical category.

        Returns:
           Lexical category.
        """
        category = self.args[1]
        return category if category is not None else default

    @property
    def language(self) -> Optional[Item]:
        """The language of lexeme descriptor."""
        return self.get_language()

    def get_language(self, default: Optional[Item] = None) -> Optional[Item]:
        """Gets the language of lexeme descriptor.

        If the language is ``None``, returns `default`.

        Parameters:
           default: Default language.

        Returns:
           Language.
        """
        language = self.args[2]
        return language if language is not None else default
