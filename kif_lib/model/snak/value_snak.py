# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import Any, ClassVar, override, TypeAlias, Union
from ..template import Template
from ..value import (
    Property,
    Value,
    ValueTemplate,
    ValueVariable,
    VTProperty,
    VTValue,
    VValue,
)
from ..variable import Variable
from .snak import Snak, SnakTemplate, SnakVariable

VValueSnak: TypeAlias =\
    Union['ValueSnakTemplate', 'ValueSnakVariable', 'ValueSnak']

VVValueSnak: TypeAlias = Union[Variable, VValueSnak]


class ValueSnakTemplate(SnakTemplate):
    """Value snak template.

    Parameters:
       property: Property, property template, or property variable.
       value: Value, value template, or value variable.
    """

    object_class: ClassVar[type['ValueSnak']]  # pyright: ignore

    def __init__(self, property: VTProperty, value: VTValue):
        super().__init__(property, value)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # property
            return super()._preprocess_arg(arg, i)
        elif i == 2:            # value
            if isinstance(arg, Template):
                return ValueTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
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

    object_class: ClassVar[type['ValueSnak']]  # pyright: ignore


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

    template_class: ClassVar[type[ValueSnakTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ValueSnakVariable]]  # pyright: ignore

    mask: ClassVar[Snak.Mask] = Snak.VALUE_SNAK

    # class DatatypeError(ValueError):
    #     """Bad property application attempt."""

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
