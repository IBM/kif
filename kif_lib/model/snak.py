# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Final, NoReturn, Optional, Union
from .kif_object import KIF_Object, TCallable
from .value import Property, Value

at_property = property


class Snak(KIF_Object):
    """Abstract base class for snaks."""

    class Mask(Flag):
        """Mask for concrete snak classes."""

        #: Mask for :class:`ValueSnak`.
        VALUE_SNAK = auto()

        #: Mask for :class:`SomeValueSnak`.
        SOME_VALUE_SNAK = auto()

        #: Mask for :class:`NoValueSnak`.
        NO_VALUE_SNAK = auto()

        #: Mask for all snak classes.
        ALL = (VALUE_SNAK | SOME_VALUE_SNAK | NO_VALUE_SNAK)

    #: Mask for :class:`ValueSnak`.
    VALUE_SNAK: Final[Mask] = Mask.VALUE_SNAK

    #: Mask for :class:`SomeValueSnak`.
    SOME_VALUE_SNAK: Final[Mask] = Mask.SOME_VALUE_SNAK

    #: Mask for :class:`NoValueSnak`.
    NO_VALUE_SNAK: Final[Mask] = Mask.NO_VALUE_SNAK

    #: Mask for all snak classes.
    ALL: Final[Mask] = Mask.ALL

    TMask = Union[Mask, int]

    @classmethod
    def _check_arg_snak_mask(
            cls,
            arg: TMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Mask, NoReturn]:
        return cls.Mask(cls._check_arg_isinstance(
            arg, (cls.Mask, int), function, name, position))

    @classmethod
    def _check_optional_arg_snak_mask(
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
            return cls._check_arg_snak_mask(arg, function, name, position)

    @classmethod
    def _preprocess_arg_snak_mask(
            cls,
            arg: TMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Mask, NoReturn]:
        return cls._check_arg_snak_mask(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_snak_mask(
            cls,
            arg,
            i: int,
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_snak_mask(arg, i, function)

    #: Mask of this snak class.
    mask: Mask = Mask.ALL

    @classmethod
    def get_mask(cls) -> Mask:
        """Gets the mask of this snak class.

        Returns:
           Mask
        """
        return cls.mask

    @property
    def property(self) -> Property:
        """The property of snak."""
        return self.get_property()

    def get_property(self) -> Property:
        """Gets the property of snak.

        Returns:
           Property.
        """
        return self.args[0]


class ValueSnak(Snak):
    """Property-value snak.

    Parameters:
       property: Property.
       value: Value.
    """

    mask: Snak.Mask = Snak.VALUE_SNAK

    def __init__(self, property: Property, value: Value):
        return super().__init__(property, value)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        elif i == 2:
            return self._preprocess_arg_value(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def value(self) -> Value:
        """The value of value snak."""
        return self.get_value()

    def get_value(self) -> Value:
        """Gets the value of value snak.

        Returns:
           Value.
        """
        return self.args[1]


class SomeValueSnak(Snak):
    """Property-"some value" snak.

    Parameters:
       property: Property.
    """

    mask: Snak.Mask = Snak.SOME_VALUE_SNAK

    def __init__(self, property: Property):
        return super().__init__(property)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        else:
            raise self._should_not_get_here()


class NoValueSnak(Snak):
    """Property-"no value" snak.

    Parameters:
       property: Property.
    """

    mask: Snak.Mask = Snak.NO_VALUE_SNAK

    def __init__(self, property: Property):
        return super().__init__(property)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        else:
            raise self._should_not_get_here()
