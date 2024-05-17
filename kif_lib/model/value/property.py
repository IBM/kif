# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...itertools import chain
from ...rdflib import URIRef
from ...typing import cast, Iterable, NoReturn, Optional, TypeAlias, Union
from ..kif_object import TCallable
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI, IRI_Template, IRI_Variable, T_IRI
from .string import String
from .value import Datatype

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
    """

    object_class: PropertyClass

    def __init__(self, iri: VTPropertyContent):
        super().__init__(iri)

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

    def __init__(self, iri: VTPropertyContent):
        super().__init__(iri)

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
