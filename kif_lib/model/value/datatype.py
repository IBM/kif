# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
from typing import TYPE_CHECKING

from ...rdflib import URIRef
from ...typing import (
    Any,
    cast,
    ClassVar,
    Location,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..term import ClosedTerm, Term, Theta, Variable

if TYPE_CHECKING:               # pragma: no cover
    from .value import Value

TDatatype: TypeAlias = Union['Datatype', type['Datatype'], type['Value']]
VDatatype: TypeAlias = Union['DatatypeVariable', 'Datatype']
VTDatatype: TypeAlias = Union[Variable, TDatatype]


class DatatypeVariable(Variable):
    """Datatype variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Datatype]]  # pyright: ignore

    @override
    def _instantiate_tail(
            self,
            theta: Theta,
            coerce: bool,
            strict: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Term | None:
        from .iri import IRI
        from .string import String
        obj = theta[self]
        if not strict and isinstance(obj, (IRI, String, str)):
            ###
            # IMPORTANT: We need to be able to use Wikidata datatype IRIs to
            # instantiate datatype variables.
            ###
            return Datatype.check(obj, function, name, position)
        else:
            return super()._instantiate_tail(
                theta, coerce, strict, function, name, position)


class Datatype(ClosedTerm, variable_class=DatatypeVariable):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    variable_class: ClassVar[type[DatatypeVariable]]  # pyright: ignore

    #: Singleton instance of this datatype class.
    instance: ClassVar[Datatype]

    #: Value class associated with this datatype class.
    value_class: ClassVar[type[Value]]

    def __new__(cls, datatype_class: TDatatype | None = None):
        if datatype_class is None:
            if cls is Datatype:
                raise cls._check_error(
                    datatype_class, cls, 'datatype_class', 1)
            datatype_class = cls
        elif isinstance(datatype_class, Datatype):
            datatype_class = type(datatype_class)
        if (isinstance(datatype_class, type)
                and issubclass(datatype_class, ClosedTerm)  # pyright: ignore
                and not issubclass(datatype_class, cls)
                and hasattr(datatype_class, 'datatype_class')):
            datatype_class = getattr(datatype_class, 'datatype_class')
        if (isinstance(datatype_class, type)
                and issubclass(datatype_class, cls)  # pyright: ignore
                and datatype_class is not Datatype):
            if (hasattr(datatype_class, 'instance')
                    and type(datatype_class.instance) is datatype_class):
                return cast(Self, datatype_class.instance)
            else:
                return super().__new__(datatype_class)
        else:
            raise cls._check_error(datatype_class, cls, 'datatype_class', 1)

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.instance = cls()

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        from .iri import IRI
        from .string import String
        if isinstance(arg, cls):
            return arg
        elif (isinstance(arg, type)
              and issubclass(arg, cls)
              and arg is not Datatype):
            return cast(Self, arg.instance)
        elif isinstance(arg, type) and hasattr(arg, 'datatype'):
            return cls.check(
                arg.datatype, function, name, position)  # pyright: ignore
        elif isinstance(arg, (IRI, String, str)):
            iri = IRI.check(arg, function, name, position)
            try:
                return cls._from_rdflib(iri.content)
            except TypeError as err:
                raise cls._check_error(
                    arg, function, name, position) from err
        else:
            raise cls._check_error(arg, function, name, position)

    @classmethod
    @functools.cache
    def _from_rdflib(cls, uri: URIRef | str) -> Self:
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
        uri = str(uri)
        if uri == str(WIKIBASE.WikibaseItem):
            res: Datatype = Item.datatype
        elif uri == str(WIKIBASE.WikibaseProperty):
            res = Property.datatype
        elif uri == str(WIKIBASE.WikibaseLexeme):
            res = Lexeme.datatype
        elif uri == str(WIKIBASE.Url):
            res = IRI.datatype
        elif uri == str(WIKIBASE.Monolingualtext):
            res = Text.datatype
        elif uri == str(WIKIBASE.String):
            res = String.datatype
        elif uri == str(WIKIBASE.ExternalId):
            res = ExternalId.datatype
        elif uri == str(WIKIBASE.Quantity):
            res = Quantity.datatype
        elif uri == str(WIKIBASE.Time):
            res = Time.datatype
        else:                   # fallback
            res = String.datatype
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

    def __init__(self, datatype_class: TDatatype | None = None) -> None:
        assert not (type(self) is Datatype and datatype_class is None)
        super().__init__()
