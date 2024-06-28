# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, TypeAlias, Union
from ..value import VTProperty
from ..variable import Variable
from .snak import Snak, SnakTemplate, SnakVariable

VNoValueSnak: TypeAlias =\
    Union['NoValueSnakTemplate', 'NoValueSnakVariable', 'NoValueSnak']

VVNoValueSnak: TypeAlias = Union[Variable, VNoValueSnak]


class NoValueSnakTemplate(SnakTemplate):
    """No-value snak template.

    Parameters:
       parameters: Property, property template, or property variable.
    """

    object_class: ClassVar[type['NoValueSnak']]  # pyright: ignore

    def __init__(self, property: VTProperty):
        super().__init__(property)


class NoValueSnakVariable(SnakVariable):
    """No-value snak variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type['NoValueSnak']]  # pyright: ignore


class NoValueSnak(
        Snak,
        template_class=NoValueSnakTemplate,
        variable_class=NoValueSnakVariable
):
    """No-value snak.

    Parameters:
       property: Property.
    """

    template_class: ClassVar[type[NoValueSnakTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[NoValueSnakVariable]]  # pyright: ignore

    mask: ClassVar[Snak.Mask] = Snak.NO_VALUE_SNAK

    def __init__(self, property: VTProperty):
        super().__init__(property)
