# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing_extensions import TYPE_CHECKING

from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
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

if TYPE_CHECKING:                      # pragma: no cover
    from ..fingerprint import Fp, TFp
    from .value_snak import TValueSnak  # noqa: F401

at_property = property

TSnak: TypeAlias = Union['Snak', 'TValueSnak']
VSnak: TypeAlias = Union['SnakTemplate', 'SnakVariable', 'Snak']
VTSnak: TypeAlias = Union[Variable, VSnak, TSnak]


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

    def __and__(self, other: 'TFp') -> 'Fp':
        from ..fingerprint import AndFp
        return AndFp(self, other)

    def __rand__(self, other: 'TFp') -> 'Fp':
        from ..fingerprint import AndFp
        return AndFp(other, self)

    def __or__(self, other: 'TFp') -> 'Fp':
        from ..fingerprint import OrFp
        return OrFp(self, other)

    def __ror__(self, other: 'TFp') -> 'Fp':
        from ..fingerprint import OrFp
        return OrFp(self, other)

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
