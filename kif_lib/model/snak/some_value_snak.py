# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from ..term import Variable
from ..value import Property, VTProperty
from .snak import Snak, SnakTemplate, SnakVariable

VSomeValueSnak: TypeAlias =\
    Union['SomeValueSnakTemplate', 'SomeValueSnakVariable', 'SomeValueSnak']

VVSomeValueSnak: TypeAlias = Union[Variable, VSomeValueSnak]


class SomeValueSnakTemplate(SnakTemplate):
    """Some-value snak template.

    Parameters:
       property: Property, property template, or property variable.
    """

    object_class: ClassVar[type[SomeValueSnak]]  # pyright: ignore

    def __init__(self, property: VTProperty) -> None:
        super().__init__(property)


class SomeValueSnakVariable(SnakVariable):
    """Some-value snak variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[SomeValueSnak]]  # pyright: ignore


class SomeValueSnak(
        Snak,
        template_class=SomeValueSnakTemplate,
        variable_class=SomeValueSnakVariable
):
    """Some-value snak.

    Parameters:
       property: Property.
    """

    template_class: ClassVar[type[SomeValueSnakTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[SomeValueSnakVariable]]  # pyright: ignore

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
        else:
            return cls(Property.check(
                arg, function or cls.check, name, position))

    def __init__(self, property: VTProperty) -> None:
        super().__init__(property)
