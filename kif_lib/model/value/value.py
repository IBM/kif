# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from functools import cache

from ... import namespace as NS
from ...rdflib import Literal, URIRef
from ...typing import cast, Collection, NoReturn, Optional, TypeAlias, Union
from ..kif_object import (
    Datetime,
    KIF_Object,
    KIF_ObjectClass,
    TCallable,
    TDatetime,
    TDecimal,
)
from ..template import Template
from ..variable import Variable

DatatypeClass: TypeAlias = type['Datatype']
TDatatypeClass: TypeAlias = Union[DatatypeClass, KIF_ObjectClass]

ValueClass: TypeAlias = type['Value']
ValueTemplateClass: TypeAlias = type['ValueTemplate']
ValueVariableClass: TypeAlias = type['ValueVariable']

TValue: TypeAlias = Union['Value', NS.T_URI, TDatetime, TDecimal, str]
VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', 'Value']
VVValue: TypeAlias = Union['Variable', VValue]


class Datatype(KIF_Object):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    #: Value class associated with this datatype class.
    value_class: ValueClass

    def __new__(
            cls,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        datatype_cls = cls._check_optional_arg_datatype_class(
            datatype_class, cls, cls, 'datatype_class', 1)
        assert datatype_cls is not None
        return super().__new__(datatype_cls)

    @classmethod
    def _check_arg_datatype_class(
            cls,
            arg: TDatatypeClass,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DatatypeClass, NoReturn]:
        if isinstance(arg, type) and issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'datatype_class'),
                f'no datatype class for {arg.__qualname__}',
                function, name, position), 'datatype_class')

    _uri: URIRef

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == cls._ItemDatatype._uri:
            return cls._ItemDatatype()
        elif uri == cls._PropertyDatatype._uri:
            return cls._PropertyDatatype()
        elif uri == cls._LexemeDatatype._uri:
            return cls._LexemeDatatype()
        elif uri == cls._IRI_Datatype._uri:
            return cls._IRI_Datatype()
        elif uri == cls._TextDatatype._uri:
            return cls._TextDatatype()
        elif uri == cls._StringDatatype._uri:
            return cls._StringDatatype()
        elif uri == cls._ExternalIdDatatype._uri:
            return cls._ExternalIdDatatype()
        elif uri == cls._QuantityDatatype._uri:
            return cls._QuantityDatatype()
        elif uri == cls._TimeDatatype._uri:
            return cls._TimeDatatype()
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        return cls._uri

    @classmethod
    def from_value_template_class(
            cls,
            value_template_class: ValueTemplateClass
    ) -> 'Datatype':
        """Gets the datatype of `value_template_class`.

        Parameters:
           value_template_class: Value template class.

        Returns:
           Datatype.
        """
        cls._check_arg_issubclass(
            value_template_class, ValueTemplate,
            cls.from_value_template_class, 'value_template_class', 1)
        obj_class = value_template_class.object_class
        assert issubclass(obj_class, Value)
        if hasattr(obj_class, 'datatype'):
            return obj_class.datatype
        else:
            raise cls._arg_error(
                f'no datatype for {value_template_class.__qualname__}',
                cls.from_value_template_class, 'value_template_class', 1)

    @classmethod
    def to_value_template_class(cls) -> ValueTemplateClass:
        """Gets the value template class of datatype.

        Returns:
           Value template class.
        """
        return cls.value_class.template_class

    @classmethod
    def from_value_variable_class(
            cls,
            value_variable_class: ValueVariableClass
    ) -> 'Datatype':
        """Gets the datatype of `value_variable_class`.

        Parameters:
           value_variable_class: Value variable class.

        Returns:
           Datatype.
        """
        cls._check_arg_issubclass(
            value_variable_class, ValueVariable,
            cls.from_value_variable_class, 'value_variable_class', 1)
        obj_class = value_variable_class.object_class
        assert issubclass(obj_class, Value)
        if hasattr(obj_class, 'datatype_class'):
            return obj_class.datatype
        else:
            raise cls._arg_error(
                f'no datatype for {value_variable_class.__qualname__}',
                cls.from_value_variable_class, 'value_variable_class', 1)

    @classmethod
    def to_value_variable_class(cls) -> ValueVariableClass:
        """Gets the value variable class of datatype.

        Returns:
           Value variable class.
        """
        return cls.value_class.variable_class

    @classmethod
    def from_value_class(cls, value_class: ValueClass) -> 'Datatype':
        """Gets the datatype of `value_class`.

        Parameters:
           value_class: Value class.

        Returns:
           Datatype.
        """
        cls._check_arg_issubclass(
            value_class, Value, cls.from_value_class, 'value_class', 2)
        if hasattr(value_class, 'datatype'):
            return value_class.datatype
        else:
            raise cls._arg_error(
                f'no datatype for {value_class.__qualname__}',
                cls.from_value_class, 'value_class', 1)

    def __init__(
            self,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        if self.__class__ == Datatype:
            self._check_arg_not_none(
                datatype_class, self.__class__, 'datatype_class', 1)
            assert datatype_class is not None
            self._check_arg(
                datatype_class, datatype_class is not Datatype,
                f'expected proper subclass of {self.__class__.__qualname__}',
                self.__class__, 'datatype_class', 1)
        super().__init__()


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
