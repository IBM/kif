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
    from .value import Value

TDatatype: TypeAlias = Union['Datatype', type['Datatype'], type['Value']]
VDatatype: TypeAlias = Union['DatatypeVariable', 'Datatype']
VTDatatype: TypeAlias = Union[Variable, TDatatype]


class DatatypeVariable(Variable):
    """Datatype variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type['Datatype']]  # pyright: ignore


class Datatype(KIF_Object, variable_class=DatatypeVariable):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    variable_class: ClassVar[type[DatatypeVariable]]  # pyright: ignore

    #: Value class associated with this datatype class.
    value_class: ClassVar[type['Value']]

    def __new__(
            cls,
            datatype_class: Optional[TDatatype] = None
    ):
        if datatype_class is None:
            if cls is Datatype:
                raise cls._check_error(
                    datatype_class, cls, 'datatype_class', 1)
            datatype_class = cls
        elif isinstance(datatype_class, Datatype):
            datatype_class = type(datatype_class)
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
            res: Datatype = Item.datatype
        elif uri == WIKIBASE.WikibaseProperty:
            res = Property.datatype
        elif uri == WIKIBASE.WikibaseLexeme:
            res = Lexeme.datatype
        elif uri == WIKIBASE.Url:
            res = IRI.datatype
        elif uri == WIKIBASE.Monolingualtext:
            res = Text.datatype
        elif uri == WIKIBASE.String:
            res = String.datatype
        elif uri == WIKIBASE.ExternalId:
            res = ExternalId.datatype
        elif uri == WIKIBASE.Quantity:
            res = Quantity.datatype
        elif uri == WIKIBASE.Time:
            res = Time.datatype
        else:
            raise cls._check_error(uri, cls._from_rdflib, 'uri', 1)
        return cls.check(res, cls._from_rdflib, 'uri', 1)

    def _to_rdflib(self) -> URIRef:
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
        if isinstance(self, ItemDatatype):
            return WIKIBASE.WikibaseItem
        elif isinstance(self, PropertyDatatype):
            return WIKIBASE.WikibaseProperty
        elif isinstance(self, LexemeDatatype):
            return WIKIBASE.WikibaseLexeme
        elif isinstance(self, IRI_Datatype):
            return WIKIBASE.Url
        elif isinstance(self, TextDatatype):
            return WIKIBASE.Monolingualtext
        elif isinstance(self, ExternalIdDatatype):
            return WIKIBASE.ExternalId
        elif isinstance(self, StringDatatype):
            return WIKIBASE.String
        elif isinstance(self, QuantityDatatype):
            return WIKIBASE.Quantity
        elif isinstance(self, TimeDatatype):
            return WIKIBASE.Time
        else:
            raise self._should_not_get_here()

    def __init__(
            self,
            datatype_class: Optional[TDatatype] = None
    ):
        assert not (type(self) is Datatype and datatype_class is None)
        super().__init__()
