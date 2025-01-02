# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
import enum

from ...typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from ..term import Template, Variable
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .item import Item, ItemTemplate, ItemVariable, VItem, VTItem
from .string import String, TString
from .value import Datatype

TDecimal: TypeAlias = Union[decimal.Decimal, float, int, enum.Enum, TString]
TQuantity: TypeAlias = Union['Quantity', TDecimal]
VQuantity: TypeAlias =\
    Union['QuantityTemplate', 'QuantityVariable', 'Quantity']
VQuantityContent: TypeAlias = Union['QuantityVariable', decimal.Decimal]
VTQuantityContent: TypeAlias = Union[Variable, TQuantity]


class QuantityTemplate(DeepDataValueTemplate):
    """Quantity template.

    Parameters:
       amount: Amount or quantity variable.
       unit: Unit, item template, or item variable.
       lower_bound: Lower bound or quantity variable.
       upper_bound: Upper bound or quantity variable.
    """

    object_class: ClassVar[type[Quantity]]  # pyright: ignore

    def __init__(
            self,
            amount: VTQuantityContent,
            unit: VTItem | None = None,
            lower_bound: VTQuantityContent | None = None,
            upper_bound: VTQuantityContent | None = None
    ) -> None:
        super().__init__(amount, unit, lower_bound, upper_bound)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # amount
            if isinstance(arg, Variable):
                return QuantityVariable.check(arg, type(self), None, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 2:            # unit
            if isinstance(arg, Template):
                return ItemTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return ItemVariable.check(arg, type(self), None, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 3:            # lower-bound
            if isinstance(arg, Variable):
                return QuantityVariable.check(arg, type(self), None, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 4:            # upper-bound
            if isinstance(arg, Variable):
                return QuantityVariable.check(arg, type(self), None, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def amount(self) -> VQuantityContent:
        """The amount of quantity template."""
        return self.get_amount()

    def get_amount(self) -> VQuantityContent:
        """Gets the amount of quantity template

        Returns:
           Amount or quantity variable.
        """
        return self.args[0]

    @property
    def unit(self) -> VItem | None:
        """The unit of quantity template."""
        return self.get_unit()

    def get_unit(self, default: VItem | None = None) -> VItem | None:
        """Gets the unit of quantity template

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit, item template, or item variable.
        """
        return self.get(1, default)

    @property
    def lower_bound(self) -> VQuantityContent | None:
        """The lower bound of quantity template."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: VQuantityContent | None = None
    ) -> VQuantityContent | None:
        """Gets the lower bound of quantity template

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound or quantity variable.
        """
        return self.get(2, default)

    @property
    def upper_bound(self) -> VQuantityContent | None:
        """The upper bound of quantity template."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: VQuantityContent | None = None
    ) -> VQuantityContent | None:
        """Gets the upper bound of quantity template.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound or quantity variable.
        """
        return self.get(3, default)


class QuantityVariable(DeepDataValueVariable):
    """Quantity variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Quantity]]  # pyright: ignore


class QuantityDatatype(Datatype):
    """Quantity datatype."""

    instance: ClassVar[QuantityDatatype]  # pyright: ignore
    value_class: ClassVar[type[Quantity]]  # pyright: ignore


class Quantity(
        DeepDataValue,
        datatype_class=QuantityDatatype,
        template_class=QuantityTemplate,
        variable_class=QuantityVariable
):
    """Quantity.

    Parameters:
       amount: Amount.
       unit: Unit.
       lower_bound: Lower bound.
       upper_bound: Upper bound.
    """

    datatype_class: ClassVar[type[QuantityDatatype]]  # pyright: ignore
    datatype: ClassVar[QuantityDatatype]              # pyright: ignore
    template_class: ClassVar[type[QuantityTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[QuantityVariable]]  # pyright: ignore

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
        elif isinstance(arg, (decimal.Decimal, float, int)):
            return cls(arg)
        elif isinstance(arg, enum.Enum):
            return cls(arg.value)
        elif isinstance(arg, str):
            try:
                return cls(arg)
            except ValueError as err:
                raise cls._check_error(
                    arg, function, name, position, ValueError) from err
        elif isinstance(arg, String):
            return cls.check(arg.content, function, name, position)
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            amount: VTQuantityContent,
            unit: VTItem | None = None,
            lower_bound: VTQuantityContent | None = None,
            upper_bound: VTQuantityContent | None = None):
        super().__init__(amount, unit, lower_bound, upper_bound)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1 or i == 3 or i == 4:  # amount, lower/upper_bound
            if arg is None and (i == 3 or i == 4):
                return None
            if isinstance(arg, Quantity):
                return arg.amount
            elif isinstance(arg, (decimal.Decimal, float, int, str)):
                try:
                    return decimal.Decimal(arg)
                except decimal.InvalidOperation as err:
                    raise Quantity._check_error(
                        arg, type(self_), None, i, ValueError) from err
            else:
                raise Quantity._check_error(arg, type(self_), None, i)
        elif i == 2:            # unit
            return Item.check_optional(arg, None, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @property
    def amount(self) -> decimal.Decimal:
        """The amount of quantity."""
        return self.get_amount()

    def get_amount(self) -> decimal.Decimal:
        """Gets the amount of quantity.

        Returns:
           Amount.
        """
        return self.args[0]

    @property
    def unit(self) -> Item | None:
        """The unit of quantity."""
        return self.get_unit()

    def get_unit(self, default: Item | None = None) -> Item | None:
        """Gets the unit of quantity.

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit.
        """
        return self.get(1, default)

    @property
    def lower_bound(self) -> decimal.Decimal | None:
        """The lower bound of quantity."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: decimal.Decimal | None = None
    ) -> decimal.Decimal | None:
        """Gets the lower bound of quantity.

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound.
        """
        return self.get(2, default)

    @property
    def upper_bound(self) -> decimal.Decimal | None:
        """The upper bound of quantity."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: decimal.Decimal | None = None
    ) -> decimal.Decimal | None:
        """Gets the upper bound of quantity.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound.
        """
        return self.get(3, default)
