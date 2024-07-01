# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import enum

from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..kif_object import KIF_Object
from ..template import Template
from ..value import Property, PropertyTemplate, PropertyVariable, VProperty
from ..variable import Variable

at_property = property

VSnak: TypeAlias = Union['SnakTemplate', 'SnakVariable', 'Snak']
VVSnak: TypeAlias = Union[Variable, VSnak]


class SnakTemplate(Template):
    """Abstract base class for snak templates."""

    object_class: ClassVar[type['Snak']]  # pyright: ignore

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # property
            if isinstance(arg, Template):
                return PropertyTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return PropertyVariable.check(arg, type(self), None, i)
            else:
                return Snak._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def property(self) -> VProperty:
        """The property of snak template."""
        return self.get_property()

    def get_property(self) -> VProperty:
        """Gets the property of snak template.

        Returns:
           Property, property template, or property variable.
        """
        return self.args[0]


class SnakVariable(Variable):
    """Snak variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type['Snak']]  # pyright: ignore


class Snak(
        KIF_Object,
        template_class=SnakTemplate,
        variable_class=SnakVariable
):
    """Abstract base class for snaks."""

    template_class: ClassVar[type[SnakTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[SnakVariable]]  # pyright: ignore

    class Mask(enum.Flag):
        """Mask for concrete snak classes."""

        #: Mask for :class:`ValueSnak`.
        VALUE_SNAK = enum.auto()

        #: Mask for :class:`SomeValueSnak`.
        SOME_VALUE_SNAK = enum.auto()

        #: Mask for :class:`NoValueSnak`.
        NO_VALUE_SNAK = enum.auto()

        #: Mask for all snak classes.
        ALL = (VALUE_SNAK | SOME_VALUE_SNAK | NO_VALUE_SNAK)

        @classmethod
        def check(
                cls,
                arg: Any,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Self:
            if isinstance(arg, cls):
                return arg
            elif isinstance(arg, int):
                try:
                    return cls(arg)
                except ValueError as err:
                    raise Snak._check_error(
                        arg, function or cls.check, name, position,
                        ValueError, to_=cls.__qualname__) from err
            else:
                raise Snak._check_error(
                    arg, function or cls.check, name, position,
                    to_=cls.__qualname__)

        @classmethod
        def check_optional(
                cls,
                arg: Optional[Any],
                default: Optional[Any] = None,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Optional[Self]:
            if arg is None:
                arg = default
            if arg is None:
                return arg
            else:
                return cls.check(arg, function, name, position)

    #: Mask for :class:`ValueSnak`.
    VALUE_SNAK: Final[Mask] = Mask.VALUE_SNAK

    #: Mask for :class:`SomeValueSnak`.
    SOME_VALUE_SNAK: Final[Mask] = Mask.SOME_VALUE_SNAK

    #: Mask for :class:`NoValueSnak`.
    NO_VALUE_SNAK: Final[Mask] = Mask.NO_VALUE_SNAK

    #: Mask for all snak classes.
    ALL: Final[Mask] = Mask.ALL

    TMask: TypeAlias = Union[Mask, int]

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, tuple):
            from .value_snak import ValueSnak
            return cast(Self, ValueSnak.check(
                arg, function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Property.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    #: Mask of this snak class.
    mask: ClassVar[Mask] = Mask.ALL

    @classmethod
    def get_mask(cls) -> Mask:
        """Gets the mask of this snak class.

        Returns:
           Mask.
        """
        return cls.mask

    @at_property
    def property(self) -> Property:
        """The property of snak."""
        return self.get_property()

    def get_property(self) -> Property:
        """Gets the property of snak.

        Returns:
           Property.
        """
        return self.args[0]
