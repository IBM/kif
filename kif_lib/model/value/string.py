# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import Any, ClassVar, override, TypeAlias, Union
from ..term import Variable
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .value import Datatype

TString: TypeAlias = Union['String', str]
VString: TypeAlias = Union['StringTemplate', 'StringVariable', 'String']
VStringContent: TypeAlias = Union['StringVariable', str]
VTStringContent: TypeAlias = Union[Variable, TString]


class StringTemplate(ShallowDataValueTemplate):
    """String template.

    Parameters:
       content: String content or string variable.
    """

    object_class: ClassVar[type[String]]  # pyright: ignore

    def __init__(self, content: VTStringContent) -> None:
        super().__init__(content)


class StringVariable(ShallowDataValueVariable):
    """String variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[String]]  # pyright: ignore


class StringDatatype(Datatype):
    """String datatype."""

    instance: ClassVar[StringDatatype]  # pyright: ignore
    value_class: ClassVar[type[String]]  # pyright: ignore


class String(
        ShallowDataValue,
        datatype_class=StringDatatype,
        template_class=StringTemplate,
        variable_class=StringVariable
):
    """String.

    Parameters:
       content: String content.
    """

    datatype_class: ClassVar[type[StringDatatype]]  # pyright: ignore
    datatype: ClassVar[StringDatatype]              # pyright: ignore
    template_class: ClassVar[type[StringTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[StringVariable]]  # pyright: ignore

    def __init__(self, content: VTStringContent) -> None:
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, String):
                return arg.content
            elif isinstance(arg, str):
                return str(arg)
            else:
                raise String._check_error(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()
