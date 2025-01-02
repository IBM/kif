# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import decimal
import enum
from typing import TYPE_CHECKING

from ... import namespace as NS
from ...rdflib import Literal, URIRef
from ...typing import (
    Any,
    cast,
    ClassVar,
    Collection,
    Location,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..term import ClosedTerm, Template, Variable
from .datatype import Datatype

if TYPE_CHECKING:  # pragma: no cover
    from ..fingerprint import AndFingerprint, OrFingerprint, TFingerprint
    from .quantity import TDecimal  # noqa: F401
    from .time import TDatetime  # noqa: F401

TValue: TypeAlias = Union['Value', 'TDatetime', 'TDecimal', str]
VTValue: TypeAlias = Union[Variable, 'VValue', TValue]
VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', 'Value']


class ValueTemplate(Template):
    """Abstract base class for value templates."""

    object_class: ClassVar[type[Value]]  # pyright: ignore


class ValueVariable(Variable):
    """Value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Value]]  # pyright: ignore


class Value(
        ClosedTerm,
        template_class=ValueTemplate,
        variable_class=ValueVariable
):
    """Abstract base class for values."""

    template_class: ClassVar[type[ValueTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ValueVariable]]  # pyright: ignore

    #: Datatype class associated with this value class.
    datatype_class: ClassVar[type[Datatype]]

    #: Datatype associated with this value class.
    datatype: ClassVar[Datatype]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if 'datatype_class' in kwargs:
            cls.datatype_class = kwargs['datatype_class']
            assert issubclass(cls.datatype_class, Datatype)
            cls.datatype = cls.datatype_class()
            cls.datatype_class.value_class = cls

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        if isinstance(arg, str):
            from .string import String
            arg = String.check(arg, function, name, position)
        elif isinstance(arg, datetime.datetime):
            from .time import Time
            arg = Time.check(arg, function, name, position)
        elif isinstance(arg, (decimal.Decimal, float, int, enum.Enum)):
            from .quantity import Quantity
            arg = Quantity.check(arg, function, name, position)
        return super().check(arg, function, name, position)

    def __and__(self, other: TFingerprint) -> AndFingerprint:
        from ..fingerprint import AndFingerprint
        return AndFingerprint(self, other)

    def __rand__(self, other: TFingerprint) -> AndFingerprint:
        from ..fingerprint import AndFingerprint
        return AndFingerprint(other, self)

    def __or__(self, other: TFingerprint) -> OrFingerprint:
        from ..fingerprint import OrFingerprint
        return OrFingerprint(self, other)

    def __ror__(self, other: TFingerprint) -> OrFingerprint:
        from ..fingerprint import OrFingerprint
        return OrFingerprint(self, other)

    def n3(self) -> str:
        """Gets the simple value of value in N3 format.

        Returns:
           Simple value in N3 format.
        """
        return self._to_rdflib().n3()

    @classmethod
    def _from_rdflib(
            cls,
            node: Literal | URIRef | str,
            item_prefixes: Collection[NS.T_NS] | None = None,
            property_prefixes: Collection[NS.T_NS] | None = None,
            lexeme_prefixes: Collection[NS.T_NS] | None = None
    ) -> Self:
        from ...rdflib import _NUMERIC_LITERAL_TYPES
        from .external_id import ExternalId
        from .iri import IRI
        from .item import Item
        from .lexeme import Lexeme
        from .property import Property
        from .quantity import Quantity
        from .string import String
        from .text import Text
        from .time import Time
        assert isinstance(node, (Literal, URIRef))
        res: Value
        if isinstance(node, URIRef):
            if not item_prefixes:
                item_prefixes = NS.Wikidata.default_item_prefixes
            if not property_prefixes:
                property_prefixes = NS.Wikidata.default_property_prefixes
            if not lexeme_prefixes:
                lexeme_prefixes = NS.Wikidata.default_lexeme_prefixes
            uri = cast(URIRef, node)
            if NS.Wikidata.is_wd_item(uri, item_prefixes):
                if item_prefixes == NS.Wikidata.default_item_prefixes:
                    res = Item(uri)
                else:
                    res = Item(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_property(uri, property_prefixes):
                if property_prefixes == NS.Wikidata.default_property_prefixes:
                    res = Property(uri)
                else:
                    res = Property(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_lexeme(uri, lexeme_prefixes):
                if lexeme_prefixes == NS.Wikidata.default_lexeme_prefixes:
                    res = Lexeme(uri)
                else:
                    res = Lexeme(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            else:
                res = IRI(uri)
        elif isinstance(node, Literal):
            literal = cast(Literal, node)
            if literal.datatype in _NUMERIC_LITERAL_TYPES:
                res = Quantity(str(literal))
            elif (literal.datatype == NS.XSD.dateTime
                  or literal.datatype == NS.XSD.date):
                res = Time(str(literal))
            elif literal.datatype is None and literal.language:
                res = Text(literal, literal.language)
            else:
                if issubclass(cls, ExternalId):
                    res = ExternalId(literal)
                else:
                    res = String(literal)
        else:
            raise cls._should_not_get_here()
        return cls.check(res, cls._from_rdflib, 'node', 1)

    def _to_rdflib(self) -> Literal | URIRef:
        from .entity import Entity
        from .iri import IRI
        from .quantity import Quantity
        from .string import String
        from .text import Text
        from .time import Time
        if isinstance(self, Entity):
            return URIRef(self.iri.content)
        elif isinstance(self, IRI):
            return URIRef(self.content)
        elif isinstance(self, Quantity):
            return Literal(str(self.amount), datatype=NS.XSD.decimal)
        elif isinstance(self, Time):
            return Literal(self.time.isoformat(), datatype=NS.XSD.dateTime)
        elif isinstance(self, Text):
            return Literal(self.content, self.language)
        elif isinstance(self, String):
            return Literal(self.content)
        else:
            raise self._should_not_get_here()
