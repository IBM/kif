# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...rdflib import URIRef
from ...typing import cast, NoReturn, Optional, override, TypeAlias, Union
from ..kif_object import TCallable
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
VTStringContent: TypeAlias = Union['StringVariable', TString]
VStringContent: TypeAlias = Union['StringVariable', str]
VString: TypeAlias = Union['StringTemplate', 'StringVariable', 'String']


class ShallowDataValueTemplate(DataValueTemplate):
    """Abstract base class for shallow data value templates."""

    object_class: ShallowDataValueClass

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_string_variable(
                arg, i, self.__class__)
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

    object_class: ShallowDataValueClass


class ShallowDataValue(
        DataValue,
        template_class=ShallowDataValueTemplate,
        variable_class=ShallowDataValueVariable
):
    """Abstract base class for shallow data values."""

    template_class: ShallowDataValueTemplateClass
    variable_class: ShallowDataValueVariableClass

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
    """Base class for string templates.

    Parameters:
       content: String content or string variable.
    """

    object_class: StringClass

    def __init__(self, content: VTStringContent):
        super().__init__(content)


class StringVariable(ShallowDataValueVariable):
    """String variable.

    Parameters:
       name: Name.
    """

    object_class: StringClass

    @classmethod
    def _preprocess_arg_string_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['StringVariable', NoReturn]:
        return cast(StringVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class StringDatatype(Datatype):
    """String datatype."""

    value_class: StringClass

    _uri: URIRef = NS.WIKIBASE.String


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

    datatype_class: StringDatatypeClass
    datatype: StringDatatype
    template_class: StringTemplateClass
    variable_class: StringVariableClass

    @classmethod
    def _check_arg_string(
            cls,
            arg: TString,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['String', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, str), function, name, position))

    def __init__(self, content: VTStringContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_str(
                arg.args[0] if isinstance(arg, String) else arg, i)
        else:
            raise self._should_not_get_here()
