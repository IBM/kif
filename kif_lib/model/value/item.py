# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import overload

from ...typing import ClassVar, Iterable, TypeAlias, Union
from ..term import Template, Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .string import TString
from .text import Text
from .value import Datatype

if TYPE_CHECKING:               # pragma: no cover
    from .quantity import (  # noqa: F401
        Quantity,
        QuantityTemplate,
        QuantityVariable,
        TQuantity,
        VQuantity,
    )

TItem: TypeAlias = Union['Item', T_IRI]
VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']
VTItem: TypeAlias = Union[Variable, VItem, TItem]
VTItemContent: TypeAlias = Union[Variable, IRI_Template, TItem]


class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[type[Item]]  # pyright: ignore

    def __init__(self, iri: VTItemContent):
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Item]]  # pyright: ignore


class ItemDatatype(Datatype):
    """Item datatype."""

    instance: ClassVar[ItemDatatype]  # pyright: ignore
    value_class: ClassVar[type[Item]]  # pyright: ignore


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

    def __init__(self, iri: VTItemContent) -> None:
        super().__init__(iri)

    @overload
    def __rmatmul__(self, other: QuantityTemplate) -> QuantityTemplate:
        ...                     # pragma: no cover

    @overload
    def __rmatmul__(self, other: TQuantity) -> Quantity:
        ...                     # pragma: no cover

    def __rmatmul__(
            self,
            other: QuantityTemplate | TQuantity
    ) -> QuantityTemplate | Quantity:
        from .quantity import Quantity, QuantityTemplate
        if isinstance(other, Template):
            return QuantityTemplate.check(other).replace(
                self.KEEP, self, self.KEEP, self.KEEP)
        else:
            return Quantity.check(other).replace(
                self.KEEP, self, self.KEEP, self.KEEP)

    @property
    def label(self) -> Text | None:
        """The label of item in KIF context."""
        return self.get_label()

    def get_label(self, language: TString | None = None) -> Text | None:
        """Gets the label of item in KIF context.

        Parameters:
           language: Language.

        Returns:
           Label or ``None`` (no label for item in KIF context).
        """
        return self.context.registry.get_label(self, language)


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
