# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Final, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable
from .text_set import TextSet, TTextSet
from .value import Datatype, Item, Text, TText


class Descriptor(KIF_Object):
    """Abstract base class for descriptors."""


class PlainDescriptor(Descriptor):
    """Abstract base class for plain descriptors."""

    class FieldMask(Flag):
        """Mask for plain descriptor fields."""

        #: Mask for the label field.
        LABEL = auto()

        #: Mask for the aliases field.
        ALIASES = auto()

        #: Mask for the description field.
        DESCRIPTION = auto()

        #: Mask for all fields.
        ALL = LABEL | ALIASES | DESCRIPTION

    #: Mask for the label field of plain descriptor.
    LABEL: Final[FieldMask] = FieldMask.LABEL

    #: Mask for the aliases field of plain descriptor.
    ALIASES: Final[FieldMask] = FieldMask.ALIASES

    #: Mask for the description field of plain descriptor.
    DESCRIPTION: Final[FieldMask] = FieldMask.DESCRIPTION

    #: Mask for all fields of plain descriptor.
    ALL: Final[FieldMask] = FieldMask.ALL

    TFieldMask = Union[FieldMask, int]

    @classmethod
    def _check_arg_plain_descriptor_field_mask(
            cls,
            arg: TFieldMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[FieldMask, NoReturn]:
        return cls.FieldMask(cls._check_arg_isinstance(
            arg, (cls.FieldMask, int), function, name, position))

    @classmethod
    def _check_optional_arg_plain_descriptor_field_mask(
            cls,
            arg: Optional[TFieldMask],
            default: Optional[FieldMask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[FieldMask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_plain_descriptor_field_mask(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_plain_descriptor_field_mask(
            cls,
            arg: TFieldMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[FieldMask, NoReturn]:
        return cls._check_arg_plain_descriptor_field_mask(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_plain_descriptor_field_mask(
            cls,
            arg,
            i: int,
            default: Optional[FieldMask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[FieldMask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_plain_descriptor_field_mask(
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
        """The label field of plain descriptor."""
        return self.get_label()

    def get_label(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets the label field of plain descriptor.

        If the label field is ``None``, returns `default`.

        Parameters:
           default: Default label.

        Returns:
           Label.
        """
        label = self.args[0]
        return label if label is not None else default

    @property
    def aliases(self) -> TextSet:
        """The aliases field of plain descriptor."""
        return self.get_aliases()

    def get_aliases(self) -> TextSet:
        """Gets the aliases field of plain descriptor.

        Returns:
           Aliases.
        """
        return self.args[1]

    @property
    def description(self) -> Optional[Text]:
        """The description field of plain descriptor."""
        return self.get_description()

    def get_description(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets the description field of plain descriptor.

        If the description field is ``None``, returns `default`.

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
        """The datatype field of property descriptor."""
        return self.get_datatype()

    def get_datatype(
            self,
            default: Optional[Datatype] = None
    ) -> Optional[Datatype]:
        """Gets the datatype field of property descriptor.

        If the datatype field is ``None``, returns `default`.

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
        """The lemma field of lexeme descriptor."""
        return self.get_lemma()

    def get_lemma(self) -> Text:
        """Gets the lemma field of lexeme descriptor.

        Returns:
           Lemma.
        """
        return self.args[0]

    @property
    def category(self) -> Item:
        """The lexical category field of lexeme descriptor."""
        return self.get_category()

    def get_category(self) -> Item:
        """Gets the lexical category field of lexeme descriptor.

        Returns:
           Lexical category.
        """
        return self.args[1]

    @property
    def language(self) -> Item:
        """The language field of lexeme descriptor."""
        return self.get_language()

    def get_language(self) -> Item:
        """Gets the language field of lexeme descriptor.

        Returns:
           Language.
        """
        return self.args[2]
