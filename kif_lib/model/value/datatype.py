# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import functools

import typing_extensions

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
    def _from_rdflib(cls, uri: URIRef) -> Self:
        from ...namespace import WIKIBASE
        datatype_class: DatatypeClass
        if uri == WIKIBASE.WikibaseItem:
            datatype_class = cls._ItemDatatype
        elif uri == WIKIBASE.WikibaseProperty:
            datatype_class = cls._PropertyDatatype
        elif uri == WIKIBASE.WikibaseLexeme:
            datatype_class = cls._LexemeDatatype
        elif uri == WIKIBASE.Url:
            datatype_class = cls._IRI_Datatype
        elif uri == WIKIBASE.Monolingualtext:
            datatype_class = cls._TextDatatype
        elif uri == WIKIBASE.String:
            datatype_class = cls._StringDatatype
        elif uri == WIKIBASE.ExternalId:
            datatype_class = cls._ExternalIdDatatype
        elif uri == WIKIBASE.Quantity:
            datatype_class = cls._QuantityDatatype
        elif uri == WIKIBASE.Time:
            datatype_class = cls._TimeDatatype
        else:
            raise cls._check_error(uri, cls._from_rdflib, 'uri', 1)
        return cls.check(datatype_class, cls._from_rdflib, 'uri', 1)

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        from ...namespace import WIKIBASE
        if cls is cls._ItemDatatype:
            return WIKIBASE.WikibaseItem
        elif cls is cls._PropertyDatatype:
            return WIKIBASE.WikibaseProperty
        elif cls is cls._LexemeDatatype:
            return WIKIBASE.WikibaseLexeme
        elif cls is cls._IRI_Datatype:
            return WIKIBASE.Url
        elif cls is cls._TextDatatype:
            return WIKIBASE.Monolingualtext
        elif cls is cls._StringDatatype:
            return WIKIBASE.String
        elif cls is cls._ExternalIdDatatype:
            return WIKIBASE.ExternalId
        elif cls is cls._QuantityDatatype:
            return WIKIBASE.Quantity
        elif cls is cls._TimeDatatype:
            return WIKIBASE.Time
        else:
            raise cls._check_error(cls, cls._to_rdflib)

    def __init__(
            self,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        assert not (type(self) is Datatype and datatype_class is None)
        super().__init__()
