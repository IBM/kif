# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from functools import cache

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
from ..kif_object import (
    Datetime,
    Decimal,
    KIF_Object,
    TDatetime,
    TDecimal,
    TLocation,
)
from ..template import Template
from ..variable import Variable

ValueClass: TypeAlias = type['Value']
ValueTemplateClass: TypeAlias = type['ValueTemplate']
ValueVariableClass: TypeAlias = type['ValueVariable']

TValue: TypeAlias = Union['Value', NS.T_URI, TDatetime, TDecimal, str]
VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', 'Value']
VVValue: TypeAlias = Union[Variable, VValue]
VVTValue: TypeAlias = Union[VVValue, TValue]

DatatypeClass: TypeAlias = type['Datatype']
TDatatypeClass: TypeAlias = Union[DatatypeClass, ValueClass]
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

    @classmethod
    def _preprocess_arg_datatype_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[TLocation] = None
    ) -> 'DatatypeVariable':
        return cast(DatatypeVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class Datatype(KIF_Object, variable_class=DatatypeVariable):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    variable_class: ClassVar[DatatypeVariableClass]  # pyright: ignore

    #: Value class associated with this datatype class.
    value_class: ClassVar[ValueClass]

    def __new__(
            cls,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        datatype_cls = cls._check_optional_arg_datatype_class(
            datatype_class, cls, cls, 'datatype_class', 1)
        assert datatype_cls is not None
        return super().__new__(datatype_cls)  # pyright: ignore

    @classmethod
    def _check_arg_datatype_class(
            cls,
            arg: TDatatypeClass,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DatatypeClass:
        if isinstance(arg, type) and issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_value_class(
                cast(ValueClass, arg), function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'datatype_class'),
                f'no datatype class for {arg.__qualname__}',
                function, name, position), 'datatype_class')

    @classmethod
    def _check_arg_datatype(
            cls,
            arg: TDatatype,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Datatype':
        if isinstance(arg, type):
            return cls._check_arg_datatype_class(
                cast(DatatypeClass, arg), function, name, position)()
        else:
            return cls._check_arg_isinstance(
                arg, cls, function, name, position)

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
        elif isinstance(arg, type) and issubclass(arg, cls.value_class):
            return cast(Self, arg.datatype)
        else:
            raise cls._check_error(arg, function, name, position)

    _uri: ClassVar[URIRef]

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == cls._ItemDatatype._uri:
            return cls._ItemDatatype()
        elif uri == cls._PropertyDatatype._uri:
            return cls._PropertyDatatype()
        elif uri == cls._LexemeDatatype._uri:
            return cls._LexemeDatatype()
        elif uri == NS.WIKIBASE.Url:
            return cls._IRI_Datatype()
        elif uri == NS.WIKIBASE.Monolingualtext:
            return cls._TextDatatype()
        elif uri == NS.WIKIBASE.String:
            return cls._StringDatatype()
        elif uri == NS.WIKIBASE.ExternalId:
            return cls._ExternalIdDatatype()
        elif uri == cls._QuantityDatatype._uri:
            return cls._QuantityDatatype()
        elif uri == cls._TimeDatatype._uri:
            return cls._TimeDatatype()
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        if cls is cls._IRI_Datatype:
            return NS.WIKIBASE.Url
        if cls is cls._TextDatatype:
            return NS.WIKIBASE.Monolingualtext
        elif cls is cls._StringDatatype:
            return NS.WIKIBASE.String
        elif cls is cls._ExternalIdDatatype:
            return NS.WIKIBASE.ExternalId
        else:
            return cls._uri

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

    object_class: ClassVar[ValueClass]  # pyright: ignore


class ValueVariable(Variable):
    """Value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[ValueClass]  # pyright: ignore

    @classmethod
    def _preprocess_arg_value_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[TLocation] = None
    ) -> 'ValueVariable':
        return cast(ValueVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


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
    def _check_arg_value(
            cls,
            arg: TValue,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Value':
        if isinstance(arg, URIRef):
            return cls._IRI.check(arg, function, name, position)
        elif isinstance(arg, Datetime):
            return cls._check_arg_time(arg)
        elif isinstance(arg, (Decimal, float, int)):
            return cls._check_arg_quantity(arg)
        elif isinstance(arg, str):
            return cls._String.check(arg, function, name, position)
        else:
            return cls._check_arg_isinstance(
                arg, Value, function, name, position)

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
