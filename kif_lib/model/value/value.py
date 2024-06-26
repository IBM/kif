# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc
import datetime
import decimal

import typing_extensions

from ... import namespace as NS
from ...rdflib import Literal, URIRef
from ...typing import (
    Any,
    cast,
    ClassVar,
    Collection,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from ..kif_object import KIF_Object, TLocation
from ..template import Template
from ..variable import Variable
from .datatype import Datatype, DatatypeClass

if typing_extensions.TYPE_CHECKING:  # pragma: no cover
    from .quantity import TDecimal  # noqa: F401
    from .time import TDatetime  # noqa: F401

ValueClass: TypeAlias = type['Value']
ValueTemplateClass: TypeAlias = type['ValueTemplate']
ValueVariableClass: TypeAlias = type['ValueVariable']

TValue: TypeAlias = Union['Value', 'TDatetime', 'TDecimal', str]
VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', 'Value']
VTValue: TypeAlias = Union[Variable, VValue, TValue]


class ValueTemplate(Template):
    """Abstract base class for value templates."""

    object_class: ClassVar[ValueClass]  # pyright: ignore


class ValueVariable(Variable):
    """Value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[ValueClass]  # pyright: ignore


class Value(
        KIF_Object,
        template_class=ValueTemplate,
        variable_class=ValueVariable
):
    """Abstract base class for values."""

    template_class: ClassVar[ValueTemplateClass]  # pyright: ignore
    variable_class: ClassVar[ValueVariableClass]  # pyright: ignore

    #: Datatype class associated with this value class.
    datatype_class: ClassVar[DatatypeClass]

    #: Datatype associated with this value class.
    datatype: ClassVar[Datatype]

    @classmethod
    def __init_subclass__(cls, **kwargs):
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
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        if isinstance(arg, str):
            arg = cls._String.check(arg, function, name, position)
        elif isinstance(arg, datetime.datetime):
            arg = cls._Time.check(arg, function, name, position)
        elif isinstance(arg, (decimal.Decimal, float, int)):
            arg = cls._Quantity.check(arg, function, name, position)
        return super().check(arg, function, name, position)

    @property
    def value(self) -> str:
        """The simple value of value."""
        return self.get_value()

    @abc.abstractmethod
    def get_value(self) -> str:
        """Gets the simple value of value.

        Returns:
           Simple value.
        """
        raise self._must_be_implemented_in_subclass()

    def n3(self) -> str:
        """Gets the simple value of value in N3 format.

        Returns:
           Simple value in N3 format.
        """
        node = self._to_rdflib()
        if isinstance(node, Literal):
            return cast(Literal, node).n3()
        elif isinstance(node, URIRef):
            return cast(URIRef, node).n3()
        else:
            raise self._should_not_get_here()

    @classmethod
    def _from_rdflib(
            cls,
            node: Union[Literal, URIRef],
            item_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_item_prefixes,
            property_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_property_prefixes,
            lexeme_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_lexeme_prefixes
    ) -> 'Value':
        from ...rdflib import _NUMERIC_LITERAL_TYPES
        assert isinstance(node, (Literal, URIRef))
        res: Value
        if isinstance(node, URIRef):
            uri = cast(URIRef, node)
            if NS.Wikidata.is_wd_item(uri, item_prefixes):
                if item_prefixes == NS.Wikidata.default_item_prefixes:
                    res = cls._Item(uri)
                else:
                    res = cls._Item(
                        NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_property(uri, property_prefixes):
                if property_prefixes == NS.Wikidata.default_property_prefixes:
                    res = cls._Property(uri)
                else:
                    res = cls._Property(
                        NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_lexeme(uri, lexeme_prefixes):
                if lexeme_prefixes == NS.Wikidata.default_lexeme_prefixes:
                    res = cls._Lexeme(uri)
                else:
                    res = cls._Lexeme(
                        NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            else:
                res = cls._IRI(uri)
        elif isinstance(node, Literal):
            literal = cast(Literal, node)
            if literal.datatype in _NUMERIC_LITERAL_TYPES:
                res = cls._Quantity(str(literal))
            elif (literal.datatype == NS.XSD.dateTime
                  or literal.datatype == NS.XSD.date):
                res = cls._Time(str(literal))
            elif literal.datatype is None and literal.language:
                res = cls._Text(literal, literal.language)
            else:
                if issubclass(cls, cls._ExternalId):
                    res = cls._ExternalId(literal)
                else:
                    res = cls._String(literal)
        else:
            raise cls._should_not_get_here()
        return cast(Value, cls.check(res))  # pyright: ignore

    def _to_rdflib(self) -> Union[Literal, URIRef]:
        from .entity import Entity
        from .iri import IRI
        from .quantity import Quantity
        from .string import String
        from .text import Text
        from .time import Time
        if isinstance(self, (Entity, IRI)):
            return URIRef(self.value)
        elif isinstance(self, Quantity):
            return Literal(self.value, datatype=NS.XSD.decimal)
        elif isinstance(self, Time):
            return Literal(self.value, datatype=NS.XSD.dateTime)
        elif isinstance(self, Text):
            return Literal(self.value, cast(Text, self).language)
        elif isinstance(self, String):
            return Literal(self.value)
        else:
            raise self._should_not_get_here()
