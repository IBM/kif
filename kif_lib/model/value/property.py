# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...itertools import chain
from ...rdflib import URIRef
from ...typing import (
    cast,
    Iterable,
    NoReturn,
    Optional,
    override,
    TypeAlias,
    Union,
)
from ..kif_object import TCallable
from ..template import Template
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI, IRI_Template, IRI_Variable, T_IRI
from .string import String
from .value import Datatype, VTDatatypeContent

PropertyClass: TypeAlias = type['Property']
PropertyDatatypeClass: TypeAlias = type['PropertyDatatype']
PropertyTemplateClass: TypeAlias = type['PropertyTemplate']
PropertyVariableClass: TypeAlias = type['PropertyVariable']

TProperty: TypeAlias = Union['Property', T_IRI]
VTPropertyContent: TypeAlias = Union[IRI_Template, IRI_Variable, 'TProperty']
VProperty: TypeAlias =\
    Union['PropertyTemplate', 'PropertyVariable', 'Property']
VVProperty: TypeAlias = Union[Variable, VProperty]


class PropertyTemplate(EntityTemplate):
    """Property template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
       range: Datatype or datatype variable.
    """

    object_class: PropertyClass

    def __init__(
            self,
            iri: VTPropertyContent,
            range: Optional[VTDatatypeContent] = None
    ):
        super().__init__(iri, range)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # iri
            if isinstance(arg, (Template, Variable)):
                return super()._preprocess_arg(arg, i)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        elif i == 2:            # range
            if Variable.test(arg):
                return self._preprocess_arg_datatype_variable(
                    arg, i, self.__class__)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    def __call__(self, value1, value2=None):
        if value2 is not None:
            return self._Statement(value1, self._ValueSnak(self, value2))
        else:
            return self._ValueSnak(self, value1)


class PropertyVariable(EntityVariable):
    """Property variable.

    Parameters:
       name: Name.
    """

    object_class: PropertyClass

    @classmethod
    def _preprocess_arg_property_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['PropertyVariable', NoReturn]:
        return cast(PropertyVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))

    def __call__(self, value1, value2=None):
        if value2 is not None:
            return self._Statement(value1, self._ValueSnak(self, value2))
        else:
            return self._ValueSnak(self, value1)


class PropertyDatatype(Datatype):
    """Property datatype."""

    value_class: PropertyClass

    _uri: URIRef = NS.WIKIBASE.WikibaseProperty


class Property(
        Entity,
        datatype_class=PropertyDatatype,
        template_class=PropertyTemplate,
        variable_class=PropertyVariable
):
    """Binary relationship.

    Parameters:
       iri: IRI.
       range: Datatype.
    """

    datatype_class: PropertyDatatypeClass
    datatype: PropertyDatatype
    template_class: PropertyTemplateClass
    variable_class: PropertyVariableClass

    @classmethod
    def _check_arg_property(
            cls,
            arg: TProperty,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Property', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, IRI, URIRef, String, str), function, name, position))

    def __init__(
            self,
            iri: VTPropertyContent,
            range: Optional[VTDatatypeContent] = None
    ):
        super().__init__(iri, range)

    @override
    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # iri
            return Entity._static_preprocess_arg(self, arg, i)
        elif i == 2:            # range
            return self._preprocess_optional_arg_datatype(arg, i)
        else:
            raise self._should_not_get_here()

    def __call__(self, value1, value2=None):
        if value2 is not None:
            return self._Statement(value1, self._ValueSnak(self, value2))
        else:
            return self._ValueSnak(self, value1)


def Properties(
        iri: VTPropertyContent,
        *iris: VTPropertyContent
) -> Iterable[Property]:
    """Constructs one or more properties.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting properties.
    """
    return map(Property, chain([iri], iris))
