# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import functools

import typing_extensions

from ... import namespace as NS
from ...rdflib import URIRef
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
from ..kif_object import KIF_Object, TLocation
from ..variable import Variable

if typing_extensions.TYPE_CHECKING:  # pragma: no cover
    from .value import ValueClass

DatatypeClass: TypeAlias = type['Datatype']
TDatatypeClass: TypeAlias = Union[DatatypeClass, 'ValueClass']
DatatypeVariableClass: TypeAlias = type['DatatypeVariable']

TDatatype: TypeAlias = Union['Datatype', TDatatypeClass]
VTDatatype: TypeAlias = Union[Variable, TDatatype]

VTDatatypeContent: TypeAlias = Union[Variable, TDatatype]
VDatatype: TypeAlias = Union['DatatypeVariable', 'Datatype']
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
            function: Optional[TLocation] = None,
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
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == NS.WIKIBASE.WikibaseItem:
            return cls._ItemDatatype()
        elif uri == NS.WIKIBASE.WikibaseProperty:
            return cls._PropertyDatatype()
        elif uri == NS.WIKIBASE.WikibaseLexeme:
            return cls._LexemeDatatype()
        elif uri == NS.WIKIBASE.Url:
            return cls._IRI_Datatype()
        elif uri == NS.WIKIBASE.Monolingualtext:
            return cls._TextDatatype()
        elif uri == NS.WIKIBASE.String:
            return cls._StringDatatype()
        elif uri == NS.WIKIBASE.ExternalId:
            return cls._ExternalIdDatatype()
        elif uri == NS.WIKIBASE.Quantity:
            return cls._QuantityDatatype()
        elif uri == NS.WIKIBASE.Time:
            return cls._TimeDatatype()
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        if cls is cls._ItemDatatype:
            return NS.WIKIBASE.WikibaseItem
        elif cls is cls._PropertyDatatype:
            return NS.WIKIBASE.WikibaseProperty
        elif cls is cls._LexemeDatatype:
            return NS.WIKIBASE.WikibaseLexeme
        elif cls is cls._IRI_Datatype:
            return NS.WIKIBASE.Url
        elif cls is cls._TextDatatype:
            return NS.WIKIBASE.Monolingualtext
        elif cls is cls._StringDatatype:
            return NS.WIKIBASE.String
        elif cls is cls._ExternalIdDatatype:
            return NS.WIKIBASE.ExternalId
        elif cls is cls._QuantityDatatype:
            return NS.WIKIBASE.Quantity
        elif cls is cls._TimeDatatype:
            return NS.WIKIBASE.Time
        else:
            raise cls._should_not_get_here()

    def __init__(
            self,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        assert not (type(self) is Datatype and datatype_class is None)
        super().__init__()
