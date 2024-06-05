# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...itertools import chain
from ...rdflib import URIRef
from ...typing import cast, Iterable, NoReturn, Optional, TypeAlias, Union
from ..kif_object import TCallable
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI, IRI_Template, T_IRI
from .string import String
from .value import Datatype

ItemClass: TypeAlias = type['Item']
ItemDatatypeClass: TypeAlias = type['ItemDatatype']
ItemTemplateClass: TypeAlias = type['ItemTemplate']
ItemVariableClass: TypeAlias = type['ItemVariable']

TItem: TypeAlias = Union['Item', T_IRI]
VTItemContent: TypeAlias = Union[IRI_Template, Variable, 'TItem']
VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']


class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ItemClass

    def __init__(self, iri: VTItemContent):
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
       name: Name.
    """

    object_class: ItemClass

    @classmethod
    def _preprocess_arg_item_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['ItemVariable', NoReturn]:
        return cast(ItemVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class ItemDatatype(Datatype):
    """Item datatype."""

    value_class: ItemClass

    _uri: URIRef = NS.WIKIBASE.WikibaseItem


class Item(
        Entity,
        datatype_class=ItemDatatype,
        template_class=ItemTemplate,
        variable_class=ItemVariable
):
    """Person or thing.

    Parameters:
       iri: IRI.
    """

    datatype_class: ItemDatatypeClass
    datatype: ItemDatatype
    template_class: ItemTemplateClass
    variable_class: ItemVariableClass

    @classmethod
    def _check_arg_item(
            cls,
            arg: TItem,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Item', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, IRI, URIRef, String, str), function, name, position))

    def __init__(self, iri: VTItemContent):
        super().__init__(iri)


def Items(iri: VTItemContent, *iris: VTItemContent) -> Iterable[Item]:
    """Constructs one or more items.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting items.
    """
    return map(Item, chain([iri], iris))