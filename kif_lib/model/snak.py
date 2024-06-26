# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Any, ClassVar, Final, Optional, override, TypeAlias, Union
from .kif_object import KIF_Object, TLocation
from .template import Template
from .value import (
    Property,
    PropertyTemplate,
    PropertyVariable,
    Value,
    ValueTemplate,
    ValueVariable,
    VProperty,
    VTProperty,
    VTValue,
    VValue,
)
from .variable import Variable

VSnak: TypeAlias = Union['SnakTemplate', 'SnakVariable', 'Snak']
VVSnak: TypeAlias = Union[Variable, VSnak]

VValueSnak: TypeAlias =\
    Union['ValueSnakTemplate', 'ValueSnakVariable', 'ValueSnak']

VVValueSnak: TypeAlias = Union[Variable, VValueSnak]

VSomeValueSnak: TypeAlias =\
    Union['SomeValueSnakTemplate', 'SomeValueSnakVariable', 'SomeValueSnak']

VVSomeValueSnak: TypeAlias = Union[Variable, VSomeValueSnak]

VNoValueSnak: TypeAlias =\
    Union['NoValueSnakTemplate', 'NoValueSnakVariable', 'NoValueSnak']

VVNoValueSnak: TypeAlias = Union[Variable, VNoValueSnak]


class SnakTemplate(Template):
    """Abstract base class for snak templates."""

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # property
            if Template.test(arg):
                return PropertyTemplate.check(arg, type(self), None, i)
            elif Variable.test(arg):
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


class Snak(
        KIF_Object,
        template_class=SnakTemplate,
        variable_class=SnakVariable
):
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
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Mask:
        return cls.Mask(cls._check_arg_isinstance(
            arg, (cls.Mask, int), function, name, position))

    @classmethod
    def _check_optional_arg_snak_mask(
            cls,
            arg: Optional[TMask],
            default: Optional[Mask] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[Mask]:
        if arg is None:
            return default
        else:
            return cls._check_arg_snak_mask(arg, function, name, position)

    @classmethod
    def _preprocess_arg_snak_mask(
            cls,
            arg: TMask,
            i: int,
            function: Optional[TLocation] = None
    ) -> Mask:
        return cls._check_arg_snak_mask(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_snak_mask(
            cls,
            arg,
            i: int,
            default: Optional[Mask] = None,
            function: Optional[TLocation] = None
    ) -> Optional[Mask]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_snak_mask(arg, i, function)

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


# -- Value snak ------------------------------------------------------------

class ValueSnakTemplate(SnakTemplate):
    """Value snak template.

    Parameters:
       property: Property, property template, or property variable.
       value: Value, value template, or value variable.
    """

    def __init__(self, property: VTProperty, value: VTValue):
        super().__init__(property, value)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # property
            return super()._preprocess_arg(arg, i)
        elif i == 2:            # value
            if Template.test(arg):
                return ValueTemplate.check(arg, type(self), None, i)
            elif Variable.test(arg):
                return ValueVariable.check(arg, type(self), None, i)
            else:
                return ValueSnak._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def value(self) -> VValue:
        """The value of value snak template."""
        return self.get_value()

    def get_value(self) -> VValue:
        """Gets the value of value snak template.

        Returns:
           Value or value template or value variable.
        """
        return self.args[1]


class ValueSnakVariable(SnakVariable):
    """Value snak variable.

    Parameters:
       name: Name.
    """


class ValueSnak(
        Snak,
        template_class=ValueSnakTemplate,
        variable_class=ValueSnakVariable
):
    """Value snak.

    Parameters:
       property: Property.
       value: Value.
    """

    mask: ClassVar[Snak.Mask] = Snak.VALUE_SNAK

    class DatatypeError(ValueError):
        """Bad property application attempt."""

    def __init__(self, property: VTProperty, value: VTValue):
        super().__init__(property, value)

    # @override
    # def _set_args(self, args: TArgs):
    #     prop, value = args
    #     assert isinstance(prop, Property)
    #     assert isinstance(value, Value)
    #     if prop.range is None:
    #         prop = prop.replace(prop.iri, value.datatype)
    #         self._args = (prop, value)
    #     else:
    #         if prop.range != value.datatype:
    #             exp = prop.range.value_class.__qualname__
    #             got = value.datatype.value_class.__qualname__
    #             raise self._arg_error(
    #                 f"property expected {exp}, got {got}",
    #                 self.__class__, 'value', None, self.DatatypeError)
    #         else:
    #             self._args = args

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Property.check(arg, type(self_), None, i)
        elif i == 2:
            return Value.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

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


# -- Some-value snak -------------------------------------------------------

class SomeValueSnakTemplate(SnakTemplate):
    """Some-value snak template.

    Parameters:
       property: Property, property template, or property variable.
    """

    def __init__(self, property: VTProperty):
        super().__init__(property)


class SomeValueSnakVariable(SnakVariable):
    """Some-value snak variable.

    Parameters:
       name: Name.
    """


class SomeValueSnak(
        Snak,
        template_class=SomeValueSnakTemplate,
        variable_class=SomeValueSnakVariable
):
    """Some-value snak.

    Parameters:
       property: Property.
    """

    mask: ClassVar[Snak.Mask] = Snak.SOME_VALUE_SNAK

    def __init__(self, property: VTProperty):
        super().__init__(property)


# -- No-value snak ---------------------------------------------------------

class NoValueSnakTemplate(SnakTemplate):
    """No-value snak template.

    Parameters:
       parameters: Property, property template, or property variable.
    """

    def __init__(self, property: VTProperty):
        super().__init__(property)


class NoValueSnakVariable(SnakVariable):
    """No-value snak variable.

    Parameters:
       name: Name.
    """


class NoValueSnak(
        Snak,
        template_class=NoValueSnakTemplate,
        variable_class=NoValueSnakVariable
):
    """No-value snak.

    Parameters:
       property: Property.
    """

    mask: ClassVar[Snak.Mask] = Snak.NO_VALUE_SNAK

    def __init__(self, property: VTProperty):
        super().__init__(property)
