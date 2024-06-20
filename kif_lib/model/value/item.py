# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...itertools import chain
from ...typing import ClassVar, Iterable, TypeAlias, Union
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .value import Datatype

ItemClass: TypeAlias = type['Item']
ItemDatatypeClass: TypeAlias = type['ItemDatatype']
ItemTemplateClass: TypeAlias = type['ItemTemplate']
ItemVariableClass: TypeAlias = type['ItemVariable']

TItem: TypeAlias = Union['Item', T_IRI]
VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']
VTItemContent: TypeAlias = Union[IRI_Template, Variable, 'TItem']


class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[ItemClass]  # pyright: ignore

    def __init__(self, iri: VTItemContent):
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[ItemClass]  # pyright: ignore


class ItemDatatype(Datatype):
    """Item datatype."""

    value_class: ClassVar[ItemClass]  # pyright: ignore


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

    datatype_class: ClassVar[ItemDatatypeClass]  # pyright: ignore
    datatype: ClassVar[ItemDatatype]             # pyright: ignore
    template_class: ClassVar[ItemTemplateClass]  # pyright: ignore
    variable_class: ClassVar[ItemVariableClass]  # pyright: ignore

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
