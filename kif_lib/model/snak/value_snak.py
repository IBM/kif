# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ...typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from ..term import Template, Variable
from ..value import (
    Datatype,
    Property,
    PropertyTemplate,
    TProperty,
    TValue,
    Value,
    ValueTemplate,
    ValueVariable,
    VTProperty,
    VTValue,
    VValue,
)
from .snak import Snak, SnakTemplate, SnakVariable

TValueSnak: TypeAlias = Union['ValueSnak', tuple[TProperty, TValue]]
VTValueSnak: TypeAlias = Union[Variable, 'VValueSnak', TValueSnak]
VValueSnak: TypeAlias =\
    Union['ValueSnakTemplate', 'ValueSnakVariable', 'ValueSnak']

if TYPE_CHECKING:                      # pragma: no cover
    from ..fingerprint import ConverseSnakFingerprint


class ValueSnakTemplate(SnakTemplate):
    """Value snak template.

    Parameters:
       property: Property, property template, or property variable.
       value: Value, value template, or value variable.
    """

    object_class: ClassVar[type[ValueSnak]]  # pyright: ignore

    def __init__(self, property: VTProperty, value: VTValue) -> None:
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

    @override
    def _set_args(self, args: tuple[Any, ...]) -> None:
        prop, value = args
        if isinstance(prop, Variable):  # nothing to do
            super()._set_args(args)
            return
        assert isinstance(prop, (Property, PropertyTemplate))
        if isinstance(prop.range, Variable):  # nothing to do
            super()._set_args(args)
            return
        assert isinstance(prop.range, (Datatype, type(None)))
        if prop.range is None:  # guess prop.range
            dt: Datatype | None = None
            if (isinstance(value, Variable)
                and hasattr(value, 'object_class')
                    and hasattr(value.object_class, 'datatype')):
                assert isinstance(value, ValueVariable)
                assert hasattr(value, 'object_class')
                assert hasattr(value.object_class, 'datatype')
                dt = value.object_class.datatype
            elif isinstance(value, Value):
                assert hasattr(value, 'datatype')
                dt = value.datatype
            elif isinstance(value, Template):
                assert isinstance(value, ValueTemplate)
                assert hasattr(value, 'object_class')
                assert hasattr(value.object_class, 'datatype')
                dt = value.object_class.datatype
            if dt is not None:
                prop = prop.replace(prop.iri, dt)
                super()._set_args((prop, value))
            else:
                super()._set_args(args)
            return
        assert prop.range is not None
        prop_dt: Datatype = prop.range
        if isinstance(value, Variable):  # coerce value into prop.range
            super()._set_args((
                prop,
                prop_dt.value_class.variable_class.check(
                    value, type(self), 'value', 2)))
            return
        assert isinstance(value, (Value, ValueTemplate))
        if isinstance(value, Value):
            assert hasattr(value, 'datatype')
            value_dt: Datatype = value.datatype
        elif isinstance(value, ValueTemplate):
            assert hasattr(value, 'object_class')
            assert hasattr(value.object_class, 'datatype')
            value_dt = value.object_class.datatype
        else:
            raise self._should_not_get_here()
        if prop_dt != value_dt:  # range-value mismatch
            src = prop_dt.value_class.__qualname__
            tgt = value_dt.value_class.__qualname__
            raise self._arg_error(
                f"cannot apply {src} property to {tgt}",
                type(self), 'value', 2, ValueError)
        super()._set_args((prop, value))

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

    object_class: ClassVar[type[ValueSnak]]  # pyright: ignore


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

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, tuple) and len(arg) >= 2:
            return cls(
                Property.check(arg[0], function or cls.check, name, position),
                Value.check(arg[1], function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self, property: VTProperty, value: VTValue) -> None:
        super().__init__(property, value)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Property.check(arg, type(self_), None, i)
        elif i == 2:
            return Value.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @override
    def _set_args(self, args: tuple[Any, ...]) -> None:
        prop, value = args
        assert isinstance(prop, Property)
        assert isinstance(value, Value)
        if prop.range is None:
            prop = prop.replace(prop.iri, value.datatype)
            super()._set_args((prop, value))
        elif prop.range != value.datatype:
            value = prop.range.value_class.check(
                value, type(self), 'value', 2)
            super()._set_args((prop, value))
        else:
            super()._set_args(args)

    def __neg__(self) -> ConverseSnakFingerprint:
        from ..fingerprint import ConverseSnakFingerprint
        return ConverseSnakFingerprint(self)

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
