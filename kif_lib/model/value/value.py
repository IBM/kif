# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod

from ... import namespace as NS
from ...rdflib import Literal, URIRef
from ...typing import cast, Collection, NoReturn, Optional, TypeAlias, Union
from ..kif_object import Datetime, KIF_Object, TCallable, TDatetime, TDecimal
from ..template import Template
from ..variable import Variable
from .datatype import Datatype, DatatypeClass

ValueClass: TypeAlias = type['Value']
ValueTemplateClass: TypeAlias = type['ValueTemplate']
ValueVariableClass: TypeAlias = type['ValueVariable']

TValue: TypeAlias = Union['Value', NS.T_URI, TDatetime, TDecimal, str]
VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', 'Value']
VVValue: TypeAlias = Union['Variable', VValue]


class ValueTemplate(Template):
    """Abstract base class for value templates."""

    object_class: ValueClass


class ValueVariable(Variable):
    """Value variable.

    Parameters:
       name: Name.
    """

    object_class: ValueClass

    @classmethod
    def _preprocess_arg_value_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['ValueVariable', NoReturn]:
        return cast(ValueVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class Value(
        KIF_Object,
        template_class=ValueTemplate,
        variable_class=ValueVariable
):
    """Abstract base class for values."""

    template_class: ValueTemplateClass
    variable_class: ValueVariableClass

    #: Datatype class associated with this value class.
    datatype_class: DatatypeClass

    #: Datatype associated with this value class.
    datatype: Datatype

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'datatype_class' in kwargs:
            cls.datatype_class = kwargs['datatype_class']
            assert issubclass(cls.datatype_class, Datatype)
            cls.datatype = cls.datatype_class()
            cls.datatype_class.value_class = cls

    @classmethod
    def _check_arg_value(
            cls,
            arg: TValue,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Value', NoReturn]:
        arg = cls._check_arg_isinstance(
            arg, (cls, URIRef, Datetime, float, int, str),
            function, name, position)
        if isinstance(arg, URIRef):
            return cls._IRI(arg)
        elif isinstance(arg, Datetime):
            return cls._Time(arg)
        elif isinstance(arg, (float, int)):
            return cls._Quantity(arg)
        elif isinstance(arg, str):
            return cls._String(arg)
        else:
            assert isinstance(arg, Value)
            return arg

    @property
    def value(self) -> str:
        """The simple value of value."""
        return self.get_value()

    @abstractmethod
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
        cls._check_arg_isinstance(
            node, (Literal, URIRef), cls._from_rdflib, 'node', 1)
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
                res = cls._Text(str(literal), literal.language)
            else:
                res = cls._String(str(literal))
        else:
            raise cls._should_not_get_here()
        return cast(Value, cls.check(res))

    def _to_rdflib(self) -> Union[Literal, URIRef]:
        from .text import Text
        if self.is_entity() or self.is_iri():
            return URIRef(self.value)
        elif self.is_quantity():
            return Literal(self.value, datatype=NS.XSD.decimal)
        elif self.is_time():
            return Literal(self.value, datatype=NS.XSD.dateTime)
        elif self.is_text():
            return Literal(self.value, cast(Text, self).language)
        elif self.is_string():
            return Literal(self.value)
        else:
            raise self._should_not_get_here()
