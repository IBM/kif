# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from enum import auto, Enum, Flag
from functools import cache

from rdflib import Literal, URIRef

from .. import namespace as NS
from ..itertools import chain
from ..typing import (
    cast,
    Collection,
    Final,
    Iterable,
    NoReturn,
    Optional,
    override,
    Union,
)
from .kif_object import (
    Datetime,
    Decimal,
    KIF_Object,
    TCallable,
    TDatetime,
    TDecimal,
)

T_IRI = Union['IRI', NS.T_URI]
TDatatype = Union['Datatype', T_IRI]
TExternalId = Union['ExternalId', 'String', str]
TString = Union['String', str]
TText = Union['Text', TString]
TTimePrecision = Union['Time.Precision', int]


# == Value =================================================================

class Value(KIF_Object):
    """Abstract base class for values."""

    class Mask(Flag):
        """Mask for concrete value classes."""

        #: Mask for :class:`Item`.
        ITEM = auto()

        #: Mask for :class:`Property`.
        PROPERTY = auto()

        #: Mask for :class:`Lexeme`.
        LEXEME = auto()

        #: Mask for :class:`IRI`.
        IRI = auto()

        #: Mask for :class:`Text`.
        TEXT = auto()

        #: Mask for :class:`String`.
        STRING = auto()

        #: Mask for :class:`ExternalId`.
        EXTERNAL_ID = auto()

        #: Mask for :class:`Quantity`.
        QUANTITY = auto()

        #: Mask for :class:`Time`.
        TIME = auto()

        #: Mask for :class:`Entity`.
        ENTITY = ITEM | PROPERTY | LEXEME

        #: Mask for :class:`ShallowDataValue`.
        SHALLOW_DATA_VALUE = IRI | TEXT | STRING | EXTERNAL_ID

        #: Mask for :class:`DeepDataValue`.
        DEEP_DATA_VALUE = TIME | QUANTITY

        #: Mask for :class:`DataValue`.
        DATA_VALUE = SHALLOW_DATA_VALUE | DEEP_DATA_VALUE

        #: Mask for all value classes.
        ALL = ENTITY | SHALLOW_DATA_VALUE | DEEP_DATA_VALUE

    #: Mask for :class:`Item`.
    ITEM: Final[Mask] = Mask.ITEM

    #: Mask for :class:`Property`.
    PROPERTY: Final[Mask] = Mask.PROPERTY

    #: Mask for :class:`Lexeme`.
    LEXEME: Final[Mask] = Mask.LEXEME

    #: Mask for :class:`IRI`.
    IRI: Final[Mask] = Mask.IRI

    #: Mask for :class:`Text`.
    TEXT: Final[Mask] = Mask.TEXT

    #: Mask for :class:`String`.
    STRING: Final[Mask] = Mask.STRING

    #: Mask for :class:`ExternalId`.
    EXTERNAL_ID: Final[Mask] = Mask.EXTERNAL_ID

    #: Mask for :class:`Quantity`.
    QUANTITY: Final[Mask] = Mask.QUANTITY

    #: Mask for :class:`Time`.
    TIME: Final[Mask] = Mask.TIME

    #: Mask for :class:`Entity`.
    ENTITY: Final[Mask] = Mask.ENTITY

    #: Mask for :class:`ShallowDataValue`.
    SHALLOW_DATA_VALUE: Final[Mask] = Mask.SHALLOW_DATA_VALUE

    #: Mask for :class:`DeepDataValue`.
    DEEP_DATA_VALUE: Final[Mask] = Mask.DEEP_DATA_VALUE

    #: Mask for :class:`DataValue`.
    DATA_VALUE: Final[Mask] = Mask.DATA_VALUE

    #: Mask for all value classes.
    ALL: Final[Mask] = Mask.ALL

    TMask = Union[Mask, int]

    @classmethod
    def _check_arg_value_mask(
            cls,
            arg: TMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Mask, NoReturn]:
        return cls.Mask(cls._check_arg_isinstance(
            arg, (cls.Mask, int), function, name, position))

    @classmethod
    def _check_optional_arg_value_mask(
            cls,
            arg: Optional[TMask],
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_value_mask(arg, function, name, position)

    @classmethod
    def _preprocess_arg_value_mask(
            cls,
            arg: TMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Mask, NoReturn]:
        return cls._check_arg_value_mask(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_value_mask(
            cls,
            arg,
            i: int,
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_value_mask(arg, i, function)

    #: Mask of this value class.
    mask: Mask = Mask.ALL

    @classmethod
    def get_mask(cls) -> Mask:
        """Gets the mask of this value class.

        Returns:
           Mask.
        """
        return cls.mask

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


# == Entity ================================================================

class Entity(Value):
    """Abstract base class for entities."""

    mask: Value.Mask = Value.ENTITY

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_iri(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return self.args[0].value

    @property
    def iri(self) -> 'IRI':
        """The iri of entity."""
        return self.get_iri()

    def get_iri(self) -> 'IRI':
        """Gets the iri of entity.

        Returns:
           IRI.
        """
        return self.args[0]


# -- Item ------------------------------------------------------------------

class Item(Entity):
    """Person or thing.

    Parameters:
       iri: IRI.
    """

    mask: Value.Mask = Value.ITEM

    def __init__(self, iri: T_IRI):
        super().__init__(iri)


def Items(iri: T_IRI, *iris: T_IRI) -> Iterable[Item]:
    """Constructs one or more items.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting items.
    """
    return map(Item, chain([iri], iris))


# -- Property --------------------------------------------------------------

class Property(Entity):
    """Binary relationship.

    Parameters:
       iri: IRI.
    """

    mask: Value.Mask = Value.PROPERTY

    def __init__(self, iri: T_IRI):
        super().__init__(iri)

    def __call__(self, value1, value2=None):
        if value2 is not None:
            return self._Statement(value1, self._ValueSnak(self, value2))
        else:
            return self._ValueSnak(self, value1)


def Properties(iri: T_IRI, *iris: T_IRI) -> Iterable[Property]:
    """Constructs one or more properties.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting properties.
    """
    return map(Property, chain([iri], iris))


# -- Lexeme ----------------------------------------------------------------

class Lexeme(Entity):
    """Word or phrase.

    Parameters:
       iri: IRI.
    """

    mask: Value.Mask = Value.LEXEME

    def __init__(self, iri: T_IRI):
        super().__init__(iri)


def Lexemes(iri: T_IRI, *iris: T_IRI) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting lexemes.
    """
    return map(Lexeme, chain([iri], iris))


# == Data value ============================================================

class DataValue(Value):
    """Abstract base class for data values."""

    mask: Value.Mask = Value.DATA_VALUE


# == Shallow data value ====================================================

class ShallowDataValue(DataValue):
    """Abstract base class for shallow data values."""

    mask: Value.Mask = Value.SHALLOW_DATA_VALUE

    def get_value(self) -> str:
        return self.args[0]

    @property
    def content(self) -> str:
        """The content of shallow data value."""
        return self.get_content()

    def get_content(self) -> str:
        """Gets the content of shallow data value.

        Returns:
           Content.
        """
        return self.args[0]


# -- IRI -------------------------------------------------------------------

class IRI(ShallowDataValue):
    """IRI.

    Parameters:
       content: IRI content.
    """

    mask: Value.Mask = Value.IRI

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

    def __init__(self, content: T_IRI):
        super().__init__(content)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, IRI):
                arg = arg.args[0]
            elif isinstance(arg, URIRef):
                arg = str(arg)
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


# -- Text ------------------------------------------------------------------

class Text(ShallowDataValue):
    """Monolingual text.

    Parameters:
       content: Text content.
       language: Language tag.
    """

    mask: Value.Mask = Value.TEXT

    #: Default language tag.
    default_language: Final[str] = 'en'

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

    def __init__(self, content: TText, language: Optional[str] = None):
        if isinstance(content, Text) and language is None:
            language = content.language
        super().__init__(content, language)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, (String, Text)):
                arg = arg.args[0]
            return self._preprocess_arg_str(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_str(
                arg, i, self.default_language)
        else:
            raise self._should_not_get_here()

    @property
    def language(self) -> str:
        """The language tag of text."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets the language tag of text.

        Returns:
           Language tag.
        """
        return self.args[1]


# -- String ----------------------------------------------------------------

class String(ShallowDataValue):
    """String.

    Parameters:
       content: String.
    """

    mask: Value.Mask = Value.STRING

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

    def __init__(self, content: TString):
        super().__init__(content)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, String):
                arg = arg.args[0]
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


# -- External id -----------------------------------------------------------

class ExternalId(String):
    """External id.

    Parameters:
       content: External id.
    """

    mask: Value.Mask = Value.EXTERNAL_ID

    @classmethod
    def _check_arg_external_id(
            cls,
            arg: TExternalId,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['ExternalId', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, String, str), function, name, position))

    @classmethod
    @override
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
        res = Value._from_rdflib(
            node, item_prefixes, property_prefixes, lexeme_prefixes)
        if res.is_string():
            return cls(cast(String, res))
        else:
            return cast(Value, cls.check(res))

    def __init__(self, content: TExternalId):
        super().__init__(content)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, (ExternalId, String)):
                arg = arg.args[0]
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


# == Deep data value =======================================================

class DeepDataValue(DataValue):
    """Abstract base class for deep data values."""

    mask: Value.Mask = Value.DEEP_DATA_VALUE


# -- Quantity --------------------------------------------------------------

class Quantity(DeepDataValue):
    """Quantity.

    Parameters:
       amount: Amount.
       unit: Unit.
       lower_bound: Lower bound.
       upper_bound: Upper bound.
    """

    mask: Value.Mask = Value.QUANTITY

    def __init__(
            self,
            amount: TDecimal,
            unit: Optional[Item] = None,
            lower_bound: Optional[TDecimal] = None,
            upper_bound: Optional[TDecimal] = None):
        super().__init__(amount, unit, lower_bound, upper_bound)

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
        """The amount of quantity."""
        return self.get_amount()

    def get_amount(self) -> Decimal:
        """Gets the amount of quantity.

        Returns:
           Amount.
        """
        return self.args[0]

    @property
    def unit(self) -> Optional[Item]:
        """The unit of quantity."""
        return self.get_unit()

    def get_unit(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets the unit of quantity.

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit.
        """
        unit = self.args[1]
        return unit if unit is not None else default

    @property
    def lower_bound(self) -> Optional[Decimal]:
        """The lower bound of quantity."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the lower bound of quantity.

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound.
        """
        lb = self.args[2]
        return lb if lb is not None else default

    @property
    def upper_bound(self) -> Optional[Decimal]:
        """The upper bound of quantity."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the upper bound of quantity.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound.
        """
        ub = self.args[3]
        return ub if ub is not None else default


# -- Time ------------------------------------------------------------------

class Time(DeepDataValue):
    """Time.

    Parameters:
       time: Time.
       precision: Precision.
       timezone: Time zone.
       calendar: Calendar model.
    """

    mask: Value.Mask = Value.TIME

    # See:
    # <https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Time>.
    # <https://www.mediawiki.org/wiki/Wikibase/DataModel#Dates_and_times>.

    class Precision(Enum):
        """Time precision."""

        #: Billion years.
        BILLION_YEARS = 0

        #: Hundred million years.
        HUNDRED_MILLION_YEARS = 1

        #: Ten million years.
        TEN_MILLION_YEARS = 2

        #: Million years.
        MILLION_YEARS = 3

        #: Hundred thousand years.
        HUNDRED_THOUSAND_YEARS = 4

        #: Ten thousand years.
        TEN_THOUSAND_YEARS = 5

        #: Millennia.
        MILLENNIA = 6

        #: Century.
        CENTURY = 7

        #: Decade.
        DECADE = 8

        #: Year.
        YEAR = 9

        #: Month.
        MONTH = 10

        #: Day.
        DAY = 11

        #: Hour.
        HOUR = 12

        #: Minute.
        MINUTE = 13

        #: Second.
        SECOND = 14

    #: Billion years.
    BILLION_YEARS = Precision.BILLION_YEARS

    #: Hundred million years.
    HUNDRED_MILLION_YEARS = Precision.HUNDRED_MILLION_YEARS

    #: Ten million years.
    TEN_MILLION_YEARS = Precision.TEN_MILLION_YEARS

    #: Million years.
    MILLION_YEARS = Precision.MILLION_YEARS

    #: Hundred thousand years.
    HUNDRED_THOUSAND_YEARS = Precision.HUNDRED_THOUSAND_YEARS

    #: Ten thousand years.
    TEN_THOUSAND_YEARS = Precision.TEN_THOUSAND_YEARS

    #: Millennia.
    MILLENNIA = Precision.MILLENNIA

    #: Century.
    CENTURY = Precision.CENTURY

    #: Decade.
    DECADE = Precision.DECADE

    #: Year
    YEAR = Precision.YEAR

    #: Month.
    MONTH = Precision.MONTH

    #: Day.
    DAY = Precision.DAY

    #: Hour.
    HOUR = Precision.HOUR

    #: Minute.
    MINUTE = Precision.MINUTE

    #: Second.
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
            time: TDatetime,
            precision: Optional[TTimePrecision] = None,
            timezone: Optional[int] = None,
            calendar: Optional[Item] = None):
        super().__init__(time, precision, timezone, calendar)

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
        """The date-time of time."""
        return self.get_time()

    def get_time(self) -> Datetime:
        """Gets the date-time of time.

        Returns:
           Datetime.
        """
        return self.args[0]

    @property
    def precision(self) -> Optional[Precision]:
        """The precision of time."""
        return self.get_precision()

    def get_precision(
            self,
            default: Optional['Time.Precision'] = None
    ) -> Optional[Precision]:
        """Gets the precision of time.

        If the precision is ``None``, returns `default`.

        Parameters:
           default: Default precision.

        Returns:
           Precision.
        """
        prec = self.args[1]
        return prec if prec is not None else default

    @property
    def timezone(self) -> Optional[int]:
        """The timezone of time."""
        return self.get_timezone()

    def get_timezone(
            self,
            default: Optional[int] = None
    ) -> Optional[int]:
        """Gets the timezone of time.

        If the timezone is ``None``, returns `default`.

        Parameters:
           default: Default timezone.

        Returns:
           Timezone.
        """
        tz = self.args[2]
        return tz if tz is not None else default

    @property
    def calendar(self) -> Optional[Item]:
        """The calendar model of time."""
        return self.get_calendar()

    def get_calendar(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets calendar model of time.

        If the calendar model is ``None``, returns `default`.

        Parameters:
           default: Default calendar model.

        Returns:
           Calendar model.
        """
        cal = self.args[3]
        return cal if cal is not None else default


# == Datatype ==============================================================

class Datatype(KIF_Object):
    """Abstract base class for datatypes."""

    #: The datatype of :class:`Item`.
    item: 'ItemDatatype'

    #: The datatype of :class:`Property`.
    property: 'PropertyDatatype'

    #: The datatype of :class:`Lexeme`.
    lexeme: 'LexemeDatatype'

    #: The datatype of :class:`IRI`.
    iri: 'IRI_Datatype'

    #: The datatype of :class:`Text`.
    text: 'TextDatatype'

    #: The datatype of :class:`String`.
    string: 'StringDatatype'

    #: The datatype of :class:`ExternalId`.
    external_id: 'ExternalIdDatatype'

    #: The datatype of :class:`Quantity`.
    quantity: 'QuantityDatatype'

    #: The datatype of :class:`Time`.
    time: 'TimeDatatype'

    @classmethod
    def _preprocess_arg_datatype(
            cls,
            arg: TDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Datatype', NoReturn]:
        if isinstance(arg, (IRI, URIRef, str)):
            if isinstance(arg, IRI):
                uri: URIRef = URIRef(arg.value)
            elif isinstance(arg, URIRef):
                uri = arg
            elif isinstance(arg, str):
                uri = URIRef(arg)
            else:
                raise cls._should_not_get_here()
            try:
                return cls._from_rdflib(uri)
            except ValueError as err:
                return cast(Datatype, cls._check_arg(
                    arg, False, str(err), function or cls,
                    None, i, ValueError))
        else:
            return cast(Datatype, Datatype.check(
                arg, function or cls, None, i))

    _uri: URIRef

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == cls.item._uri:
            return cls.item
        elif uri == cls.property._uri:
            return cls.property
        elif uri == cls.lexeme._uri:
            return cls.lexeme
        elif uri == cls.iri._uri:
            return cls.iri
        elif uri == cls.text._uri:
            return cls.text
        elif uri == cls.string._uri:
            return cls.string
        elif uri == cls.external_id._uri:
            return cls.external_id
        elif uri == cls.quantity._uri:
            return cls.quantity
        elif uri == cls.time._uri:
            return cls.time
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        return cls._uri

    @classmethod
    @cache
    def from_value_class(cls, value_class: type[Value]) -> 'Datatype':
        """Gets the datatype of `value_class`.

        Parameters:
           value_class: Value class.

        Returns:
           Datatype.
        """
        if value_class is Item:
            return cls.item
        elif value_class is Property:
            return cls.property
        elif value_class is Lexeme:
            return cls.lexeme
        elif value_class is IRI:
            return cls.iri
        elif value_class is Text:
            return cls.text
        elif value_class is String:
            return cls.string
        elif value_class is ExternalId:
            return cls.external_id
        elif value_class is Quantity:
            return cls.quantity
        elif value_class is Time:
            return cls.time
        else:
            cls._check_arg_issubclass(
                value_class, Value, cls.from_value_class, 'value_class', 2)
            raise cls._arg_error(
                f'no datatype for {value_class.__qualname__}',
                cls.from_value_class, 'value_class', 2)

    @classmethod
    @abstractmethod
    def to_value_class(cls) -> type[Value]:
        """Gets the value class of datatype.

        Returns:
           Value class.
        """
        raise cls._must_be_implemented_in_subclass()

    def __init__(self):
        return super().__init__()


class ItemDatatype(Datatype):
    """Datatype of :class:`Item`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseItem

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Item


class PropertyDatatype(Datatype):
    """Datatype of :class:`Property`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseProperty

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Property


class LexemeDatatype(Datatype):
    """Datatype of :class:`Lexeme`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseLexeme

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Lexeme


class IRI_Datatype(Datatype):
    """Datatype of :class:`IRI`."""

    _uri: URIRef = NS.WIKIBASE.Url

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return IRI


class TextDatatype(Datatype):
    """Datatype of :class:`Text`."""

    _uri: URIRef = NS.WIKIBASE.Monolingualtext

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Text


class StringDatatype(Datatype):
    """Datatype of :class:`String`."""

    _uri: URIRef = NS.WIKIBASE.String

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return String


class ExternalIdDatatype(StringDatatype):
    """Datatype of :class:`ExternalId`."""

    _uri: URIRef = NS.WIKIBASE.ExternalId

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return ExternalId


class QuantityDatatype(Datatype):
    """Datatype of :class:`Quantity`."""

    _uri: URIRef = NS.WIKIBASE.Quantity

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Quantity


class TimeDatatype(Datatype):
    """Datatype of :class:`Time`."""

    _uri: URIRef = NS.WIKIBASE.Time

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Time


Datatype.item = ItemDatatype()
Datatype.property = PropertyDatatype()
Datatype.lexeme = LexemeDatatype()
Datatype.iri = IRI_Datatype()
Datatype.text = TextDatatype()
Datatype.string = StringDatatype()
Datatype.external_id = ExternalIdDatatype()
Datatype.quantity = QuantityDatatype()
Datatype.time = TimeDatatype()
