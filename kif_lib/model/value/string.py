# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import (
    Any,
    cast,
    ClassVar,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..kif_object import TLocation
from ..variable import Variable
from .data_value import DataValue, DataValueTemplate, DataValueVariable
from .value import Datatype

ShallowDataValueClass: TypeAlias = type['ShallowDataValue']
ShallowDataValueTemplateClass: TypeAlias = type['ShallowDataValueTemplate']
ShallowDataValueVariableClass: TypeAlias = type['ShallowDataValueVariable']

StringClass: TypeAlias = type['String']
StringDatatypeClass: TypeAlias = type['StringDatatype']
StringTemplateClass: TypeAlias = type['StringTemplate']
StringVariableClass: TypeAlias = type['StringVariable']

TString: TypeAlias = Union['String', str]
VString: TypeAlias = Union['StringTemplate', 'StringVariable', 'String']
VStringContent: TypeAlias = Union['StringVariable', str]
VTStringContent: TypeAlias = Union[Variable, TString]


class ShallowDataValueTemplate(DataValueTemplate):
    """Abstract base class for shallow data value templates."""

    object_class: ClassVar[ShallowDataValueClass]  # pyright: ignore

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # content
            return StringVariable.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def content(self) -> VStringContent:
        """The content of shallow data value template."""
        return self.get_content()

    def get_content(self) -> VStringContent:
        """Gets the content of shallow data value.

        Returns:
           String variable.
        """
        return self.args[0]


class ShallowDataValueVariable(DataValueVariable):
    """Shallow data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[ShallowDataValueClass]  # pyright: ignore


class ShallowDataValue(
        DataValue,
        template_class=ShallowDataValueTemplate,
        variable_class=ShallowDataValueVariable
):
    """Abstract base class for shallow data values."""

    template_class: ClassVar[ShallowDataValueTemplateClass]  # pyright: ignore
    variable_class: ClassVar[ShallowDataValueVariableClass]  # pyright: ignore

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
        if cls is ShallowDataValue:
            if isinstance(arg, str):
                return cast(Self, String(arg))
        else:                   # concrete subclass?
            if isinstance(arg, String):
                return cls(arg.content)
            if isinstance(arg, str):
                return cls(str(arg))
        raise cls._check_error(arg, function, name, position)

    def get_value(self) -> str:
        return self.args[0]

    @property
    def content(self) -> str:
        """The content of shallow data value."""
        return self.get_content()

    def get_content(self) -> str:
        """Gets the content of shallow data value.

        Returns:
           String content.
        """
        return self.args[0]


class StringTemplate(ShallowDataValueTemplate):
    """String template.

    Parameters:
       content: String content or string variable.
    """

    object_class: ClassVar[StringClass]  # pyright: ignore

    def __init__(self, content: VTStringContent):
        super().__init__(content)


class StringVariable(ShallowDataValueVariable):
    """String variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[StringClass]  # pyright: ignore


class StringDatatype(Datatype):
    """String datatype."""

    value_class: ClassVar[StringClass]  # pyright: ignore


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

    datatype_class: ClassVar[StringDatatypeClass]  # pyright: ignore
    datatype: ClassVar[StringDatatype]             # pyright: ignore
    template_class: ClassVar[StringTemplateClass]  # pyright: ignore
    variable_class: ClassVar[StringVariableClass]  # pyright: ignore

    def __init__(self, content: VTStringContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, String):
                return arg.content
            else:
                return str(self_._check_arg_str(arg, type(self_), None, i))
        else:
            raise self_._should_not_get_here()
