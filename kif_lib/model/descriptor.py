# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Final, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable
from .value import Datatype, Item, Text, TText
from .value_set import TextSet, TTextSet


class Descriptor(KIF_Object):
    """Abstract base class for descriptors."""


class PlainDescriptor(Descriptor):
    """Abstract base class for plain descriptors."""

    class AttributeMask(Flag):
        """Mask for plain descriptor attributes."""

        #: Mask for the label of plain descriptor.
        LABEL = auto()

        #: Mask for the aliases of plain descriptor.
        ALIASES = auto()

        #: Mask for the description of plain descriptor.
        DESCRIPTION = auto()

        #: Mask for all attributes of plain descriptor.
        ALL = LABEL | ALIASES | DESCRIPTION

    #: Mask for the label of plain descriptor.
    LABEL: Final[AttributeMask] = AttributeMask.LABEL

    #: Mask for the aliases of plain descriptor.
    ALIASES: Final[AttributeMask] = AttributeMask.ALIASES

    #: Mask for the description of plain descriptor.
    DESCRIPTION: Final[AttributeMask] = AttributeMask.DESCRIPTION

    #: Mask for all attributes of plain descriptor.
    ALL: Final[AttributeMask] = AttributeMask.ALL

    TAttributeMask = Union[AttributeMask, int]

    @classmethod
    def _check_arg_plain_descriptor_attribute_mask(
            cls,
            arg: TAttributeMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[AttributeMask, NoReturn]:
        return cls.AttributeMask(cls._check_arg_isinstance(
            arg, (cls.AttributeMask, int), function, name, position))

    @classmethod
    def _check_optional_arg_plain_descriptor_attribute_mask(
            cls,
            arg: Optional[TAttributeMask],
            default: Optional[AttributeMask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[AttributeMask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_plain_descriptor_attribute_mask(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_plain_descriptor_attribute_mask(
            cls,
            arg: TAttributeMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[AttributeMask, NoReturn]:
        return cls._check_arg_plain_descriptor_attribute_mask(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_plain_descriptor_attribute_mask(
            cls,
            arg,
            i: int,
            default: Optional[AttributeMask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[AttributeMask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_plain_descriptor_attribute_mask(
                arg, i, function)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_optional_arg_text(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_text_set(arg, i, TextSet())
        elif i == 3:
            return self._preprocess_optional_arg_text(arg, i)
        else:
            return self._should_not_get_here()

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

    def _preprocess_arg(self, arg, i):
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

    def __init__(self, lemma: TText, category: Item, language: Item):
        super().__init__(lemma, category, language)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_text(arg, i)
        elif i == 2:
            return self._preprocess_arg_item(arg, i)
        elif i == 3:
            return self._preprocess_arg_item(arg, i)
        else:
            return self._should_not_get_here()

    @property
    def lemma(self) -> Text:
        """The lemma of lexeme descriptor."""
        return self.get_lemma()

    def get_lemma(self) -> Text:
        """Gets the lemma of lexeme descriptor.

        Returns:
           Lemma.
        """
        return self.args[0]

    @property
    def category(self) -> Item:
        """The lexical category of lexeme descriptor."""
        return self.get_category()

    def get_category(self) -> Item:
        """Gets the lexical category of lexeme descriptor.

        Returns:
           Lexical category.
        """
        return self.args[1]

    @property
    def language(self) -> Item:
        """The language of lexeme descriptor."""
        return self.get_language()

    def get_language(self) -> Item:
        """Gets the language of lexeme descriptor.

        Returns:
           Language.
        """
        return self.args[2]
