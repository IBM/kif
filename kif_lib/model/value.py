# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from enum import Enum
from itertools import chain
from typing import cast, Collection, Iterable, NoReturn, Optional, Union

from rdflib import Literal, URIRef

from .. import namespace as NS
from .kif_object import (
    Datetime,
    Decimal,
    KIF_Object,
    TCallable,
    TDatetime,
    TDecimal,
)

T_IRI = Union['IRI', NS.T_URI]
TString = Union['String', str]
TText = Union['Text', TString]
TTimePrecision = Union['Time.Precision', int]


class Value(KIF_Object):
    """Abstract base class for values."""

    @classmethod
    def _preprocess_arg_value(
            cls,
            arg: Union['Value', float, int, str],
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Value', NoReturn]:
        if isinstance(arg, (float, int)):
            return Quantity(arg)
        elif isinstance(arg, str):
            return String(arg)
        else:
            return cast(Value, Value.check(arg, function or cls, None, i))

    @property
    def value(self) -> str:
        """Value's simple value."""
        return self.get_value()

    @abstractmethod
    def get_value(self) -> str:
        """Gets value's simple value.

        Returns:
           Simple value.
        """
        raise self._must_be_implemented_in_subclass()

    def n3(self) -> str:
        """Gets value's simple value in N3 format.

        Returns:
           Simple value in N3 format.
        """
        node = self._to_rdflib()
        if isinstance(node, Literal):
            return cast(Literal, node).n3()
        elif isinstance(node, URIRef):
            return cast(URIRef, node).n3()
        else:
            self._should_not_get_here()

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
        from rdflib.term import _NUMERIC_LITERAL_TYPES
        cls._check_arg_isinstance(
            node, (Literal, URIRef), cls._from_rdflib, 'node', 1)
        res: Value
        if isinstance(node, URIRef):
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
                res = Text(str(literal), literal.language)
            else:
                res = String(str(literal))
        else:
            raise cls._should_not_get_here()
        return cast(Value, cls.check(res))

    def _to_rdflib(self) -> Union[Literal, URIRef]:
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


class Entity(Value):
    """Abstract base class for entities."""

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_iri(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return self.args[0].value

    @property
    def iri(self) -> 'IRI':
        """Entity IRI."""
        return self.get_iri()

    def get_iri(self) -> 'IRI':
        """Gets entity IRI.

        Returns:
           Entity IRI.
        """
        return self.args[0]


class Item(Entity):
    """Entity representing a thing.

    Parameters:
       arg1: IRI.
    """

    def __init__(self, arg1: T_IRI):
        super().__init__(arg1)


class Property(Entity):
    """Entity representing a relationship.

    Parameters:
       arg1: IRI.
    """

    def __init__(self, arg1: T_IRI):
        super().__init__(arg1)

    def __call__(self, arg1, arg2=None):
        if arg2 is not None:
            return self.Statement(arg1, self.ValueSnak(self, arg2))
        else:
            return self.ValueSnak(self, arg1)


class Lexeme(Entity):
    """Entity representing a word or phrase.

    Parameters:
       arg1: IRI.
    """

    def __init__(self, arg1: T_IRI):
        super().__init__(arg1)


def Items(arg1: T_IRI, *args: T_IRI) -> Iterable[Item]:
    """Constructs one or more items.

    Parameters:
       arg1: IRI.
       args: Remaining IRIs.

    Returns:
       The resulting items.
    """
    return map(Item, chain([arg1], args))


def Properties(arg1: T_IRI, *args: T_IRI) -> Iterable[Property]:
    """Constructs one or more properties.

    Parameters:
       arg1: IRI.
       args: Remaining IRIs.

    Returns:
       The resulting properties.
    """
    return map(Property, chain([arg1], args))


def Lexemes(arg1: T_IRI, *args: T_IRI) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       arg1: IRI.
       args: Remaining IRIs.

    Returns:
       The resulting lexemes.
    """
    return map(Lexeme, chain([arg1], args))


class DataValue(Value):
    """Abstract base class for data values."""

    def get_value(self) -> str:
        return self.args[0]


class IRI(DataValue):
    """IRI value.

    Parameters:
       arg1: IRI.
    """

    @classmethod
    def _check_arg_iri(
            cls,
            arg: T_IRI,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['IRI', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, URIRef, str), function, name, position))

    def __init__(self, arg1: T_IRI):
        super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, IRI):
                arg = arg.args[0]
            elif isinstance(arg, URIRef):
                arg = str(arg)
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return self.args[0]


class Text(DataValue):
    """Monolingual text value.

    Parameters:
       arg1: String.
       arg2: Language tag.
    """

    #: Default language tag.
    default_language = 'en'

    @classmethod
    def _check_arg_text(
            cls,
            arg: TText,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Text', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, str), function, name, position))

    def __init__(self, arg1: TText, arg2: Optional[TText] = None):
        if isinstance(arg1, Text) and arg2 is None:
            arg2 = arg1.language
        super().__init__(arg1, arg2)

    def _preprocess_arg(self, arg, i):
        if isinstance(arg, (String, Text)):
            arg = arg.args[0]
        if i == 1:
            return self._preprocess_arg_str(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_str(
                arg, i, self.default_language)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return self.args[0]

    @property
    def language(self) -> str:
        """Language tag."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets language tag.

        Returns:
           Language tag.
        """
        return self.args[1]


class String(DataValue):
    """String value.

    Parameters:
       arg1: String.
    """

    @classmethod
    def _check_arg_string(
            cls,
            arg: TString,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['String', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, str), function, name, position))

    def __init__(self, arg1: TString):
        super().__init__(arg1)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, String):
                arg = arg.args[0]
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


class DeepDataValue(DataValue):
    """Abstract base class for deep data values."""


class Quantity(DeepDataValue):
    """Deep data value representing a quantity.

    Parameters:
       arg1: Amount.
       arg2: Unit.
       arg3: Lower bound.
       arg4: Upper bound.
    """

    def __init__(
            self,
            arg1: TDecimal,
            arg2: Optional[Item] = None,
            arg3: Optional[TDecimal] = None,
            arg4: Optional[TDecimal] = None):
        super().__init__(arg1, arg2, arg3, arg4)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_decimal(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_item(arg, i)
        elif i == 3:
            return self._preprocess_optional_arg_decimal(arg, i)
        elif i == 4:
            return self._preprocess_optional_arg_decimal(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return str(self.args[0])

    @property
    def amount(self) -> Decimal:
        """Quantity amount."""
        return self.get_amount()

    def get_amount(self) -> Decimal:
        """Gets quantity amount.

        Returns:
           Amount.
        """
        return self.args[0]

    @property
    def unit(self) -> Optional[Item]:
        """Quantity unit."""
        return self.get_unit()

    def get_unit(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets quantity unit.

        If quantity unit is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Quantity unit or `default` (quantity has no unit).
        """
        unit = self.args[1]
        return unit if unit is not None else default

    @property
    def lower_bound(self) -> Optional[Decimal]:
        """Quantity lower bound."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets quantity lower bound.

        If quantity lower bound is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Lower bound or `default` (quantity has no lower bound).
        """
        lb = self.args[2]
        return lb if lb is not None else default

    @property
    def upper_bound(self) -> Optional[Decimal]:
        """Quantity upper bound."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets quantity upper bound.

        If quantity upper bound is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Lower bound or `default` (quantity has no upper bound).
        """
        ub = self.args[3]
        return ub if ub is not None else default


class Time(DeepDataValue):
    """Deep data value representing a timestamp.

    Parameters:
       arg1: Time.
       arg2: Precision.
       arg3: Time zone.
       arg4: Calendar model.
    """

    # See:
    # <https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Time>.
    # <https://www.mediawiki.org/wiki/Wikibase/DataModel#Dates_and_times>.

    class Precision(Enum):
        BILLION_YEARS = 0
        HUNDRED_MILLION_YEARS = 1
        TEN_MILLION_YEARS = 2
        MILLION_YEARS = 3
        HUNDRED_THOUSAND_YEARS = 4
        TEN_THOUSAND_YEARS = 5
        MILLENIA = 6
        CENTURY = 7
        DECADE = 8
        YEAR = 9
        MONTH = 10
        DAY = 11
        HOUR = 12
        MINUTE = 13
        SECOND = 14

    #: Alias for :attr:`Time.Precision.BILLION_YEARS`.
    BILLION_YEARS = Precision.BILLION_YEARS

    #: Alias for :attr:`Time.Precision.HUNDRED_MILLION_YEARS`.
    HUNDRED_MILLION_YEARS = Precision.HUNDRED_MILLION_YEARS

    #: Alias for :attr:`Time.Precision.TEN_MILLION_YEARS`.
    TEN_MILLION_YEARS = Precision.TEN_MILLION_YEARS

    #: Alias for :attr:`Time.Precision.MILLION_YEARS`.
    MILLION_YEARS = Precision.MILLION_YEARS

    #: Alias for :attr:`Time.Precision.HUNDRED_THOUSAND_YEARS`.
    HUNDRED_THOUSAND_YEARS = Precision.HUNDRED_THOUSAND_YEARS

    #: Alias for :attr:`Time.Precision.TEN_THOUSAND_YEARS`.
    TEN_THOUSAND_YEARS = Precision.TEN_THOUSAND_YEARS

    #: Alias for :attr:`Time.Precision.MILLENIA`.
    MILLENIA = Precision.MILLENIA

    #: Alias for :attr:`Time.Precision.CENTURY`.
    CENTURY = Precision.CENTURY

    #: Alias for :attr:`Time.Precision.DECADE`.
    DECADE = Precision.DECADE

    #: Alias for :attr:`Time.Precision.YEAR`.
    YEAR = Precision.YEAR

    #: Alias for :attr:`Time.Precision.MONTH`.
    MONTH = Precision.MONTH

    #: Alias for :attr:`Time.Precision.DAY`.
    DAY = Precision.DAY

    #: Alias for :attr:`Time.Precision.HOUR`.
    HOUR = Precision.HOUR

    #: Alias for :attr:`Time.Precision.MINUTE`.
    MINUTE = Precision.MINUTE

    #: Alias for :attr:`Time.Precision.SECOND`.
    SECOND = Precision.SECOND

    @classmethod
    def _check_arg_precision(
            cls,
            arg: TTimePrecision,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Time.Precision', NoReturn]:
        arg = cls._check_arg_isinstance(
            arg, (cls.Precision, int), function, name, position)
        try:
            return cls.Precision(arg)
        except ValueError:
            raise cls._arg_error(
                f'expected {cls.Precision.__qualname__}',
                function, name, position, ValueError)

    @classmethod
    def _check_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            default: Optional['Time.Precision'] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional['Time.Precision'], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_precision(
                arg, function, name, position)

    @classmethod
    def _preprocess_arg_precision(
            cls,
            arg: TTimePrecision,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Time.Precision', NoReturn]:
        return cls._check_arg_precision(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            i: int,
            default: Optional['Time.Precision'] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional['Time.Precision'], NoReturn]:
        return cls._check_optional_arg_precision(
            arg, default, function or cls, None, i)

    def __init__(
            self,
            arg1: TDatetime,
            arg2: Optional[TTimePrecision] = None,
            arg3: Optional[int] = None,
            arg4: Optional[Item] = None):
        super().__init__(arg1, arg2, arg3, arg4)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_datetime(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_precision(arg, i)
        elif i == 3:
            return self._preprocess_optional_arg_int(arg, i)
        elif i == 4:
            return self._preprocess_optional_arg_item(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return str(self.args[0].isoformat())

    @property
    def time(self) -> Datetime:
        """Time value."""
        return self.get_time()

    def get_time(self) -> Datetime:
        """Gets time value.

        Returns:
           Time value.
        """
        return self.args[0]

    @property
    def precision(self) -> Optional[Precision]:
        """Time precision."""
        return self.get_precision()

    def get_precision(
            self,
            default: Optional['Time.Precision'] = None
    ) -> Optional[Precision]:
        """Gets time precision.

        If time precision is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Precision or `default` (time has no precision).
        """
        prec = self.args[1]
        return prec if prec is not None else default

    @property
    def timezone(self) -> Optional[int]:
        """Timezone"""
        return self.get_timezone()

    def get_timezone(
            self,
            default: Optional[int] = None
    ) -> Optional[int]:
        """Gets timezone.

        If timezone is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Timezone or `default` (time has no timezone).
        """
        tz = self.args[2]
        return tz if tz is not None else default

    @property
    def calendar_model(self) -> Optional[Item]:
        """Time calendar model."""
        return self.get_calendar_model()

    def get_calendar_model(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets time calendar model.

        If time calendar model is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Calendar model or `default` (calendar model).
        """
        cal = self.args[3]
        return cal if cal is not None else default
