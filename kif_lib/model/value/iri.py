# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...rdflib import URIRef
from ...typing import Any, cast, ClassVar, Optional, override, TypeAlias, Union
from ..kif_object import TLocation
from ..variable import Variable
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .string import String
from .value import Datatype

IRI_Class: TypeAlias = type['IRI']
IRI_DatatypeClass: TypeAlias = type['IRI_Datatype']
IRI_TemplateClass: TypeAlias = type['IRI_Template']
IRI_VariableClass: TypeAlias = type['IRI_Variable']

T_IRI: TypeAlias = Union['IRI', String, NS.T_URI]
VT_IRI_Content: TypeAlias = Union[Variable, T_IRI]
V_IRI: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'IRI']


class IRI_Template(ShallowDataValueTemplate):
    """IRI template.

    Parameters:
       content: IRI content or string variable.
    """

    object_class: ClassVar[IRI_Class]  # pyright: ignore

    def __init__(self, content: VT_IRI_Content):
        super().__init__(content)


class IRI_Variable(ShallowDataValueVariable):
    """IRI variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[IRI_Class]  # pyright: ignore

    @classmethod
    def _preprocess_arg_iri_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[TLocation] = None
    ) -> 'IRI_Variable':
        return cast(IRI_Variable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class IRI_Datatype(Datatype):
    """IRI datatype."""

    value_class: ClassVar[IRI_Class]  # pyright: ignore

    _uri: ClassVar[URIRef] = NS.WIKIBASE.Url


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

    datatype_class: ClassVar[IRI_DatatypeClass]  # pyright: ignore
    datatype: ClassVar[IRI_Datatype]             # pyright: ignore
    template_class: ClassVar[IRI_TemplateClass]  # pyright: ignore
    variable_class: ClassVar[IRI_VariableClass]  # pyright: ignore

    @classmethod
    def _check_arg_iri(
            cls,
            arg: T_IRI,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'IRI':
        return cls(cls._check_arg_isinstance(
            arg, (cls, URIRef, String, str), function, name, position))

    def __init__(self, content: VT_IRI_Content):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, (IRI, String)):
                arg = arg.args[0]
            elif isinstance(arg, URIRef):
                arg = str(arg)
            return self_._preprocess_arg_str(arg, i)
        else:
            raise self_._should_not_get_here()
