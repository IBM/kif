# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import decimal

from ...typing import (
    Any,
    Callable,
    ClassVar,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..template import Template
from ..variable import Variable
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .item import Item, ItemTemplate, ItemVariable, VItem, VTItem
from .string import String, TString
from .value import Datatype

TDecimal: TypeAlias = Union[decimal.Decimal, float, int, TString]
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

    object_class: ClassVar[type['Quantity']]  # pyright: ignore

    def __init__(
            self,
            amount: VTQuantityContent,
            unit: Optional[VTItem] = None,
            lower_bound: Optional[VTQuantityContent] = None,
            upper_bound: Optional[VTQuantityContent] = None):
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
    def unit(self) -> Optional[VItem]:
        """The unit of quantity template."""
        return self.get_unit()

    def get_unit(self, default: Optional[VItem] = None) -> Optional[VItem]:
        """Gets the unit of quantity template

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit, item template, or item variable.
        """
        return self.get(1, default)

    @property
    def lower_bound(self) -> Optional[VQuantityContent]:
        """The lower bound of quantity template."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[VQuantityContent] = None
    ) -> Optional[VQuantityContent]:
        """Gets the lower bound of quantity template

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound or quantity variable.
        """
        return self.get(2, default)

    @property
    def upper_bound(self) -> Optional[VQuantityContent]:
        """The upper bound of quantity template."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[VQuantityContent] = None
    ) -> Optional[VQuantityContent]:
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

    object_class: ClassVar[type['Quantity']]  # pyright: ignore


class QuantityDatatype(Datatype):
    """Quantity datatype."""

    value_class: ClassVar[type['Quantity']]  # pyright: ignore


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
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, (decimal.Decimal, float, int)):
            return cls(arg)
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
            unit: Optional[VTItem] = None,
            lower_bound: Optional[VTQuantityContent] = None,
            upper_bound: Optional[VTQuantityContent] = None):
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

    @override
    def get_value(self) -> str:
        return str(self.amount)

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
    def unit(self) -> Optional[Item]:
        """The unit of quantity."""
        return self.get_unit()

    def get_unit(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets the unit of quantity.

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit.
        """
        return self.get(1, default)

    @property
    def lower_bound(self) -> Optional[decimal.Decimal]:
        """The lower bound of quantity."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[decimal.Decimal] = None
    ) -> Optional[decimal.Decimal]:
        """Gets the lower bound of quantity.

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound.
        """
        return self.get(2, default)

    @property
    def upper_bound(self) -> Optional[decimal.Decimal]:
        """The upper bound of quantity."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[decimal.Decimal] = None
    ) -> Optional[decimal.Decimal]:
        """Gets the upper bound of quantity.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound.
        """
        return self.get(3, default)
