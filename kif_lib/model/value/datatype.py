# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import functools

import typing_extensions

from ...rdflib import URIRef
from ...typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..kif_object import KIF_Object
from ..variable import Variable

if typing_extensions.TYPE_CHECKING:  # pragma: no cover
    from .value import ValueClass

DatatypeClass: TypeAlias = type['Datatype']
DatatypeVariableClass: TypeAlias = type['DatatypeVariable']
TDatatypeClass: TypeAlias = Union[DatatypeClass, 'ValueClass']

TDatatype: TypeAlias = Union['Datatype', TDatatypeClass]
VTDatatype: TypeAlias = Union[Variable, TDatatype]

VDatatype: TypeAlias = Union['DatatypeVariable', 'Datatype']
VTDatatypeContent: TypeAlias = Union[Variable, TDatatype]
VVDatatype: TypeAlias = Union[Variable, VDatatype]


class DatatypeVariable(Variable):
    """Datatype variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[DatatypeClass]  # pyright: ignore


class Datatype(KIF_Object, variable_class=DatatypeVariable):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    variable_class: ClassVar[DatatypeVariableClass]  # pyright: ignore

    #: Value class associated with this datatype class.
    value_class: ClassVar['ValueClass']

    def __new__(
            cls,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        if datatype_class is None:
            if cls is Datatype:
                raise cls._check_error(
                    datatype_class, cls, 'datatype_class', 1)
            datatype_class = cls
        if (isinstance(datatype_class, type)
                and issubclass(datatype_class, KIF_Object)
                and not issubclass(datatype_class, cls)
                and hasattr(datatype_class, 'datatype_class')):
            datatype_class = getattr(datatype_class, 'datatype_class')
        if (isinstance(datatype_class, type)
                and issubclass(datatype_class, cls)
                and datatype_class is not Datatype):
            return super().__new__(datatype_class)
        else:
            raise cls._check_error(datatype_class, cls, 'datatype_class', 1)

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Optional[Union[Callable[..., Any], str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, type) and issubclass(arg, cls):
            return cast(Self, arg.value_class.datatype)
        elif isinstance(arg, type) and hasattr(arg, 'datatype'):
            return cls.check(arg.datatype, function, name, position)
        else:
            raise cls._check_error(arg, function, name, position)

    @classmethod
    @functools.cache
    def _from_rdflib(cls, uri: URIRef) -> Self:
        from ...namespace import WIKIBASE
        from .external_id import ExternalId
        from .iri import IRI
        from .item import Item
        from .lexeme import Lexeme
        from .property import Property
        from .quantity import Quantity
        from .string import String
        from .text import Text
        from .time import Time
        if uri == WIKIBASE.WikibaseItem:
            return cast(Self, Item.datatype)
        elif uri == WIKIBASE.WikibaseProperty:
            return cast(Self, Property.datatype)
        elif uri == WIKIBASE.WikibaseLexeme:
            return cast(Self, Lexeme.datatype)
        elif uri == WIKIBASE.Url:
            return cast(Self, IRI.datatype)
        elif uri == WIKIBASE.Monolingualtext:
            return cast(Self, Text.datatype)
        elif uri == WIKIBASE.String:
            return cast(Self, String.datatype)
        elif uri == WIKIBASE.ExternalId:
            return cast(Self, ExternalId.datatype)
        elif uri == WIKIBASE.Quantity:
            return cast(Self, Quantity.datatype)
        elif uri == WIKIBASE.Time:
            return cast(Self, Time.datatype)
        else:
            raise cls._check_error(uri, cls._from_rdflib, 'uri', 1)

    @classmethod
    @functools.cache
    def _to_rdflib(cls) -> URIRef:
        from ...namespace import WIKIBASE
        from .external_id import ExternalIdDatatype
        from .iri import IRI_Datatype
        from .item import ItemDatatype
        from .lexeme import LexemeDatatype
        from .property import PropertyDatatype
        from .quantity import QuantityDatatype
        from .string import StringDatatype
        from .text import TextDatatype
        from .time import TimeDatatype
        if cls is ItemDatatype:
            return WIKIBASE.WikibaseItem
        elif cls is PropertyDatatype:
            return WIKIBASE.WikibaseProperty
        elif cls is LexemeDatatype:
            return WIKIBASE.WikibaseLexeme
        elif cls is IRI_Datatype:
            return WIKIBASE.Url
        elif cls is TextDatatype:
            return WIKIBASE.Monolingualtext
        elif cls is StringDatatype:
            return WIKIBASE.String
        elif cls is ExternalIdDatatype:
            return WIKIBASE.ExternalId
        elif cls is QuantityDatatype:
            return WIKIBASE.Quantity
        elif cls is TimeDatatype:
            return WIKIBASE.Time
        else:
            raise cls._check_error(cls, cls._to_rdflib)

    def __init__(
            self,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        assert not (type(self) is Datatype and datatype_class is None)
        super().__init__()
