# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, Iterable, TypeAlias, Union
from ..term import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .value import Datatype

TItem: TypeAlias = Union['Item', T_IRI]
VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']
VTItem: TypeAlias = Union[Variable, VItem, TItem]
VTItemContent: TypeAlias = Union[Variable, IRI_Template, TItem]


class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[type['Item']]  # pyright: ignore

    def __init__(self, iri: VTItemContent):
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type['Item']]  # pyright: ignore


class ItemDatatype(Datatype):
    """Item datatype."""

    value_class: ClassVar[type['Item']]  # pyright: ignore


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

    datatype_class: ClassVar[type[ItemDatatype]]  # pyright: ignore
    datatype: ClassVar[ItemDatatype]              # pyright: ignore
    template_class: ClassVar[type[ItemTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ItemVariable]]  # pyright: ignore

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
    from ... import itertools
    return map(Item, itertools.chain((iri,), iris))
