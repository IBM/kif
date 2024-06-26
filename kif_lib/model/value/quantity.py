# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import decimal

from ... import namespace as NS
from ...rdflib import URIRef
from ...typing import Any, ClassVar, Optional, override, Self, TypeAlias, Union
from ..kif_object import Decimal, TDecimal, TLocation
from ..template import Template
from ..variable import Variable
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .item import Item, ItemTemplate, ItemVariable, VItem, VTItem
from .string import String
from .value import Datatype

QuantityClass: TypeAlias = type['Quantity']
QuantityDatatypeClass: TypeAlias = type['QuantityDatatype']
QuantityTemplateClass: TypeAlias = type['QuantityTemplate']
QuantityVariableClass: TypeAlias = type['QuantityVariable']

TQuantity: TypeAlias = Union['Quantity', TDecimal]
VQuantity: TypeAlias =\
    Union['QuantityTemplate', 'QuantityVariable', 'Quantity']
VQuantityContent: TypeAlias = Union['QuantityVariable', Decimal]
VTQuantityContent: TypeAlias = Union[Variable, TQuantity]


class QuantityTemplate(DeepDataValueTemplate):
    """Quantity template.

    Parameters:
       amount: Amount or quantity variable.
       unit: Unit, item template, or item variable.
       lower_bound: Lower bound or quantity variable.
       upper_bound: Upper bound or quantity variable.
    """

    object_class: ClassVar[QuantityClass]  # pyright: ignore

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
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(
                    arg, i, self.__class__)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 2:            # unit
            if Template.test(arg):
                return ItemTemplate.check(arg, type(self), None, i)
            elif Variable.test(arg):
                return ItemVariable.check(arg, type(self), None, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 3:            # lower-bound
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(
                    arg, i, self.__class__)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 4:            # upper-bound
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(
                    arg, i, self.__class__)
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
        unit = self.args[1]
        return unit if unit is not None else default

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
        lb = self.args[2]
        return lb if lb is not None else default

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
        ub = self.args[3]
        return ub if ub is not None else default


class QuantityVariable(DeepDataValueVariable):
    """Quantity variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[QuantityClass]  # pyright: ignore


class QuantityDatatype(Datatype):
    """Quantity datatype."""

    value_class: ClassVar[QuantityClass]  # pyright: ignore

    _uri: ClassVar[URIRef] = NS.WIKIBASE.Quantity


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

    datatype_class: ClassVar[QuantityDatatypeClass]  # pyright: ignore
    datatype: ClassVar[QuantityDatatype]             # pyright: ignore
    template_class: ClassVar[QuantityTemplateClass]  # pyright: ignore
    variable_class: ClassVar[QuantityVariableClass]  # pyright: ignore

    @classmethod
    def _check_arg_quantity(
            cls,
            arg: TQuantity,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Quantity':
        if isinstance(arg, Quantity):
            return arg
        else:
            return cls(cls._check_arg_decimal(arg, function, name, position))

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, (Decimal, float, int, str)):
            return cls(arg)
        elif isinstance(arg, String):
            return cls(arg.content)
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
            elif isinstance(arg, (Decimal, float, int, str)):
                try:
                    return Decimal(arg)
                except decimal.InvalidOperation as err:
                    raise Quantity._check_error(
                        arg, type(self_), None, i, ValueError) from err
            else:
                raise Quantity._check_error(arg, type(self_), None, i)
        elif i == 2:            # unit
            return Item.check_optional(arg, None, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    def get_value(self) -> str:
        return str(self.args[0])

    @property
    def amount(self) -> Decimal:
        """The amount of quantity."""
        return self.get_amount()

    def get_amount(self) -> Decimal:
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
        unit = self.args[1]
        return unit if unit is not None else default

    @property
    def lower_bound(self) -> Optional[Decimal]:
        """The lower bound of quantity."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the lower bound of quantity.

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound.
        """
        lb = self.args[2]
        return lb if lb is not None else default

    @property
    def upper_bound(self) -> Optional[Decimal]:
        """The upper bound of quantity."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the upper bound of quantity.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound.
        """
        ub = self.args[3]
        return ub if ub is not None else default
