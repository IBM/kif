# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import Any, ClassVar, override, TypeAlias, Union
from ..term import Variable
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .string import String, TString
from .value import Datatype

T_IRI: TypeAlias = Union['IRI', TString]
V_IRI: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'IRI']
VT_IRI: TypeAlias = Union[Variable, V_IRI, T_IRI]
VT_IRI_Content: TypeAlias = Union[Variable, T_IRI]


class IRI_Template(ShallowDataValueTemplate):
    """IRI template.

    Parameters:
       content: IRI content or string variable.
    """

    object_class: ClassVar[type[IRI]]  # pyright: ignore

    def __init__(self, content: VT_IRI_Content) -> None:
        super().__init__(content)


class IRI_Variable(ShallowDataValueVariable):
    """IRI variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[IRI]]  # pyright: ignore


class IRI_Datatype(Datatype):
    """IRI datatype."""

    value_class: ClassVar[type[IRI]]  # pyright: ignore


class IRI(
        ShallowDataValue,
        datatype_class=IRI_Datatype,
        template_class=IRI_Template,
        variable_class=IRI_Variable
):
    """IRI.

    Parameters:
       content: IRI content.
    """

    datatype_class: ClassVar[type[IRI_Datatype]]  # pyright: ignore
    datatype: ClassVar[IRI_Datatype]              # pyright: ignore
    template_class: ClassVar[type[IRI_Template]]  # pyright: ignore
    variable_class: ClassVar[type[IRI_Variable]]  # pyright: ignore

    def __init__(self, content: VT_IRI_Content) -> None:
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_: IRI, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, IRI):
                return arg.content
            else:
                return String.check(arg, type(self_), None, i).content
        else:
            raise self_._should_not_get_here()
