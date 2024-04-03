# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import auto, Flag

from ..typing import Final, NoReturn, Optional, override, TypeAlias, Union
from .kif_object import KIF_Object, TCallable
from .pattern import Template, Variable
from .value import Property, Value, VProperty, VValue

VSnak: TypeAlias =\
    Union['SnakTemplate', 'SnakVariable', 'Snak']

VValueSnak: TypeAlias =\
    Union['ValueSnakTemplate', 'ValueSnakVariable', 'ValueSnak']

VSomeValueSnak: TypeAlias =\
    Union['SomeValueSnakTemplate', 'SomeValueSnakVariable', 'SomeValueSnak']

VNoValueSnak: TypeAlias =\
    Union['NoValueSnakTemplate', 'NoValueSnakVariable', 'NoValueSnak']


class SnakTemplate(Template):
    """Abstract base class for snak templates."""

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # property
            if Template.test(arg):
                return self._preprocess_arg_property_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_property_variable(arg, i)
            else:
                return Snak._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class SnakVariable(Variable):
    """Snak variable.

    Parameters:
       name: String
    """


class Snak(KIF_Object):
    """Abstract base class for snaks."""

    #: Concrete template class associated with this snak class (if any).
    template_class: type[Template]

    #: Variable class associated with this snak class.
    variable_class: type[Variable] = SnakVariable

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

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_property(arg, i)
        else:
            raise self._should_not_get_here()

    #: Mask of this snak class.
    mask: Mask = Mask.ALL

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
       property: Property.
       value: Value.
    """

    def __init__(self, property: VProperty, value: VValue):
        return super().__init__(property, value)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # property
            return super()._preprocess_arg(arg, i)
        elif i == 2:            # value
            if Template.test(arg):
                return self._preprocess_arg_value_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_value_variable(arg, i)
            else:
                return ValueSnak._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class ValueSnakVariable(SnakVariable):
    """Value snak variable.

    Parameters:
       name: String.
    """


class ValueSnak(Snak):
    """Value snak.

    Parameters:
       property: Property.
       value: Value.
    """

    template_class: type[Template] = ValueSnakTemplate

    variable_class: type[Variable] = ValueSnakVariable

    mask: Snak.Mask = Snak.VALUE_SNAK

    def __init__(self, property: VProperty, value: VValue):
        return super().__init__(property, value)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
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


# -- Some-value snak -------------------------------------------------------

class SomeValueSnakTemplate(SnakTemplate):
    """Some-value snak template.

    Parameters:
       property: Property.
    """

    def __init__(self, property: VProperty):
        return super().__init__(property)


class SomeValueSnakVariable(SnakVariable):
    """Some-value snak variable.

    Parameters:
       name: String
    """


class SomeValueSnak(Snak):
    """Some-value snak.

    Parameters:
       property: Property.
    """

    template_class: type[Template] = SomeValueSnakTemplate

    variable_class: type[Variable] = SomeValueSnakVariable

    mask: Snak.Mask = Snak.SOME_VALUE_SNAK

    def __init__(self, property: VProperty):
        return super().__init__(property)


# -- No-value snak ---------------------------------------------------------

class NoValueSnakTemplate(SnakTemplate):
    """No-value snak template.

    Parameters:
       parameters: Property.
    """

    def __init__(self, property: VProperty):
        return super().__init__(property)


class NoValueSnakVariable(SnakVariable):
    """No-value snak variable.

    Parameters:
       name: String.
    """


class NoValueSnak(Snak):
    """No-value snak.

    Parameters:
       property: Property.
    """

    template_class: type[Template] = NoValueSnakTemplate

    variable_class: type[Variable] = NoValueSnakVariable

    mask: Snak.Mask = Snak.NO_VALUE_SNAK

    def __init__(self, property: VProperty):
        return super().__init__(property)
