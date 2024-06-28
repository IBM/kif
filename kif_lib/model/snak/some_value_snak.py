# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, TypeAlias, Union
from ..value import VTProperty
from ..variable import Variable
from .snak import Snak, SnakTemplate, SnakVariable

VSomeValueSnak: TypeAlias =\
    Union['SomeValueSnakTemplate', 'SomeValueSnakVariable', 'SomeValueSnak']

VVSomeValueSnak: TypeAlias = Union[Variable, VSomeValueSnak]


class SomeValueSnakTemplate(SnakTemplate):
    """Some-value snak template.

    Parameters:
       property: Property, property template, or property variable.
    """

    object_class: ClassVar[type['SomeValueSnak']]  # pyright: ignore

    def __init__(self, property: VTProperty):
        super().__init__(property)


class SomeValueSnakVariable(SnakVariable):
    """Some-value snak variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type['SomeValueSnak']]  # pyright: ignore


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

    mask: ClassVar[Snak.Mask] = Snak.SOME_VALUE_SNAK

    def __init__(self, property: VTProperty):
        super().__init__(property)
