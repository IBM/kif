# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag
from typing import NoReturn, Optional, Union

from .kif_object import KIF_Object, TCallable
from .text_set import TextSet, TTextSet
from .value import Datatype, Item, Text, TText


class Descriptor(KIF_Object):
    """Abstract base class for entity descriptors."""


class PlainDescriptor(Descriptor):
    """Abstract base class for item or property descriptors."""

    class Mask(Flag):
        LABEL = auto()
        ALIASES = auto()
        DESCRIPTION = auto()
        ALL = LABEL | ALIASES | DESCRIPTION

    TMask = Union[Mask, int]

    #: Alias for :attr:`PlainDescriptor.Mask.LABEL`.
    LABEL = Mask.LABEL

    #: Alias for :attr:`PlainDescriptor.Mask.ALIASES`.
    ALIASES = Mask.ALIASES

    #: Alias for :attr:`PlainDescriptor.Mask.DESCRIPTION`.
    DESCRIPTION = Mask.DESCRIPTION

    #: Alias for :attr:`PlainDescriptor.Mask.ALL`.
    ALL = Mask.ALL

    @classmethod
    def _check_arg_plain_descriptor_mask(
            cls,
            arg: TMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Mask, NoReturn]:
        return cls.Mask(cls._check_arg_isinstance(
            arg, (cls.Mask, int), function, name, position))

    @classmethod
    def _check_optional_arg_plain_descriptor_mask(
            cls,
            arg: Optional[TMask],
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_plain_descriptor_mask(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_plain_descriptor_mask(
            cls,
            arg: TMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Mask, NoReturn]:
        return cls._check_arg_plain_descriptor_mask(
            arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_plain_descriptor_mask(
            cls,
            arg,
            i: int,
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[Mask], NoReturn]:
        return cls._check_optional_arg_plain_descriptor_mask(
            arg, default, function or cls, None, i)

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
        """Descriptor label."""
        return self.get_label()

    def get_label(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets descriptor label.

        If descriptor label is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Descriptor label.
        """
        label = self.args[0]
        return label if label is not None else default

    @property
    def aliases(self) -> TextSet:
        """Descriptor aliases."""
        return self.get_aliases()

    def get_aliases(self) -> TextSet:
        """Gets descriptor aliases.

        Returns:
           Descriptor aliases.
        """
        return self.args[1]

    @property
    def description(self) -> Optional[Text]:
        """Descriptor description."""
        return self.get_description()

    def get_description(
            self,
            default: Optional[Text] = None
    ) -> Optional[Text]:
        """Gets descriptor description.

        If descriptor description is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Descriptor description.
        """
        desc = self.args[2]
        return desc if desc is not None else default


class ItemDescriptor(PlainDescriptor):
    """Item descriptor.

    Parameters:
       arg1: Label.
       arg2: Aliases.
       arg3: Description.
    """

    def __init__(
            self,
            arg1: Optional[TText] = None,
            arg2: Optional[TTextSet] = None,
            arg3: Optional[TText] = None
    ):
        super().__init__(arg1, arg2, arg3)


class PropertyDescriptor(PlainDescriptor):
    """Property descriptor.

    Parameters:
        arg1: Label.
        arg2: Aliases.
        arg3: Description.
        arg4: Datatype.
    """

    def __init__(
            self,
            arg1: Optional[TText] = None,
            arg2: Optional[TTextSet] = None,
            arg3: Optional[TText] = None,
            arg4: Optional[Datatype] = None
    ):
        super().__init__(arg1, arg2, arg3, arg4)

    def _preprocess_arg(self, arg, i):
        if i == 4:
            return self._preprocess_optional_arg_datatype(arg, i)
        else:
            return super()._preprocess_arg(arg, i)

    @property
    def datatype(self) -> Optional[Datatype]:
        """Descriptor datatype."""
        return self.get_datatype()

    def get_datatype(
            self,
            default: Optional[Datatype] = None
    ) -> Optional[Datatype]:
        """Gets descriptor datatype.

        If descriptor datatype is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Descriptor datatype.
        """
        dt = self.args[3]
        return dt if dt is not None else default


class LexemeDescriptor(Descriptor):
    """Lexeme descriptor.

    Parameters:
        arg1: Lemma.
        arg2: Lexical category.
        arg3: Language.
    """

    def __init__(
            self,
            arg1: TText,
            arg2: Item,
            arg3: Item,
    ):
        super().__init__(arg1, arg2, arg3)

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
        """Lexeme lemma."""
        return self.get_lemma()

    def get_lemma(self) -> Text:
        """Gets lexeme lemma.

        Returns:
           Lemma.
        """
        return self.args[0]

    @property
    def category(self) -> Item:
        """Lexeme lexical category."""
        return self.get_category()

    def get_category(self) -> Item:
        """Gets lexeme lexical category.

        Returns:
           Lexical category.
        """
        return self.args[1]

    @property
    def language(self) -> Item:
        """Lexeme language."""
        return self.get_language()

    def get_language(self) -> Item:
        """Gets lexeme language.

        Returns:
           Language.
        """
        return self.args[2]
