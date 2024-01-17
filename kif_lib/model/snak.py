# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag
from typing import NoReturn, Optional, Union

from .kif_object import KIF_Object, TCallable
from .value import Property, Value

at_property = property
TSnakMask = Union['SnakMask', int]


class SnakMask(Flag):
    """Mask representing concrete snak classes."""

    #: Mask representing ValueSnak's.
    VALUE_SNAK = auto()

    #: Mask representing SomeValueSnak's.
    SOME_VALUE_SNAK = auto()

    #: Mask representing NoValueSnak's.
    NO_VALUE_SNAK = auto()

    #: Mask representing all snak classes.
    ALL = (VALUE_SNAK | SOME_VALUE_SNAK | NO_VALUE_SNAK)


class Snak(KIF_Object):
    """Abstract base class for snaks."""

    #: Alias for :attr:`SnakMask.VALUE_SNAK`.
    VALUE_SNAK = SnakMask.VALUE_SNAK

    #: Alias for :attr:`SnakMask.SOME_VALUE_SNAK`.
    SOME_VALUE_SNAK = SnakMask.SOME_VALUE_SNAK

    #: Alias for :attr:`SnakMask.NO_VALUE_SNAK`.
    NO_VALUE_SNAK = SnakMask.NO_VALUE_SNAK

    #: Alias for :attr:`SnakMask.ALL`.
    ALL = SnakMask.ALL

    @classmethod
    def _check_arg_snak_mask(
            cls,
            arg: TSnakMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SnakMask, NoReturn]:
        return SnakMask(cls._check_arg_isinstance(
            arg, (SnakMask, int), function, name, position))

    @classmethod
    def _check_optional_arg_snak_mask(
            cls,
            arg: Optional[TSnakMask],
            default: Optional[SnakMask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[SnakMask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_snak_mask(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_snak_mask(
            cls,
            arg: TSnakMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[SnakMask, NoReturn]:
        return cls._check_arg_snak_mask(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_snak_mask(
            cls,
            arg,
            i: int,
            default: Optional[SnakMask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[SnakMask], NoReturn]:
        return cls._check_optional_arg_snak_mask(
            arg, default, function or cls, None, i)

    @property
    def property(self) -> Property:
        """Snak property."""
        return self.get_property()

    def get_property(self) -> Property:
        """Gets snak property.

        Returns:
           Snak property.
        """
        return self.args[0]

    _snak_mask = SnakMask.ALL

    @at_property
    def snak_mask(self) -> SnakMask:
        """The most specific snak mask for snak."""
        return self.get_snak_mask()

    def get_snak_mask(self) -> SnakMask:
        """Gets the most specific snak mask for snak.

        Returns:
           The most specific snak mask for snak.
        """
        return self._snak_mask


class ValueSnak(Snak):
    """Snak associating a property to a value.

    Parameters:
       arg1: Property.
       arg2: Value.
    """

    _snak_mask = SnakMask.VALUE_SNAK

    def __init__(self, arg1: Property, arg2: Value):
        return super().__init__(arg1, arg2)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        elif i == 2:
            return self._preprocess_arg_value(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def value(self) -> Value:
        """Snak value."""
        return self.get_value()

    def get_value(self) -> Value:
        """Gets snak value.

        Returns:
           Snak value.
        """
        return self.args[1]


class SomeValueSnak(Snak):
    """Snak associating a property to some unspecified value.

    Parameters:
       arg1: Property.
    """

    _snak_mask = SnakMask.SOME_VALUE_SNAK

    def __init__(self, arg1: Property):
        return super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        else:
            raise self._should_not_get_here()


class NoValueSnak(Snak):
    """Snak associating a property to no value.

    Parameters:
       arg1: Property.
    """

    _snak_mask = SnakMask.NO_VALUE_SNAK

    def __init__(self, arg1: Property):
        return super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        else:
            raise self._should_not_get_here()
