# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from enum import Enum

from ... import namespace as NS
from ...rdflib import URIRef
from ...typing import Any, cast, ClassVar, Optional, override, TypeAlias, Union
from ..kif_object import Datetime, Decimal, TDatetime, TLocation
from ..template import Template
from ..variable import Variable
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .item import Item, VItem, VTItemContent
from .quantity import Quantity, QuantityVariable, TQuantity, VTQuantityContent
from .value import Datatype

TimeClass: TypeAlias = type['Time']
TimeDatatypeClass: TypeAlias = type['TimeDatatype']
TimeTemplateClass: TypeAlias = type['TimeTemplate']
TimeVariableClass: TypeAlias = type['TimeVariable']

TTime: TypeAlias = Union['Time', TDatetime]
VTTimeContent: TypeAlias = Union[Variable, TTime]
VTimeContent: TypeAlias = Union['TimeVariable', Datetime]
VTime: TypeAlias = Union['TimeTemplate', 'TimeVariable', 'Time']

TTimePrecision: TypeAlias = Union['Time.Precision', TQuantity]
VTTimePrecisionContent: TypeAlias = Union[Variable, TTimePrecision]
VTimePrecisionContent: TypeAlias = Union[QuantityVariable, 'Time.Precision']

TTimeTimezone: TypeAlias = TQuantity
VTTimeTimezoneContent: TypeAlias = VTQuantityContent
VTimeTimezoneContent: TypeAlias = Union[QuantityVariable, int]


class TimeTemplate(DeepDataValueTemplate):
    """Time template.

    Parameters:
       time: Time or time variable.
       precision: Precision or quantity variable.
       timezone: Time zone or quantity variable.
       calendar: Calendar model, item template, or item variable.
    """

    object_class: ClassVar[TimeClass]  # pyright: ignore

    def __init__(
            self,
            time: VTTimeContent,
            precision: Optional[VTTimePrecisionContent] = None,
            timezone: Optional[VTTimeTimezoneContent] = None,
            calendar: Optional[VTItemContent] = None):
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # time
            if Variable.test(arg):
                return self._preprocess_arg_time_variable(
                    arg, i, self.__class__)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 2:            # precision
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(
                    arg, i, self.__class__)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 3:            # timezone
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(
                    arg, i, self.__class__)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 4:            # calendar
            if Template.test(arg):
                return self._preprocess_arg_item_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_item_variable(
                    arg, i, self.__class__)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def time(self) -> VTimeContent:
        """The date-time of time template."""
        return self.get_time()

    def get_time(self) -> VTimeContent:
        """Gets the date-time of time.

        Returns:
           Date-Time or time variable.
        """
        return self.args[0]

    @property
    def precision(self) -> Optional[VTimePrecisionContent]:
        """The precision of time template."""
        return self.get_precision()

    def get_precision(
            self,
            default: Optional[VTimePrecisionContent] = None
    ) -> Optional[VTimePrecisionContent]:
        """Gets the precision of time.

        If the precision is ``None``, returns `default`.

        Parameters:
           default: Default precision.

        Returns:
           Precision or quantity variable.
        """
        prec = self.args[1]
        return prec if prec is not None else default

    @property
    def timezone(self) -> Optional[VTimeTimezoneContent]:
        """The timezone of time template."""
        return self.get_timezone()

    def get_timezone(
            self,
            default: Optional[VTimeTimezoneContent] = None
    ) -> Optional[VTimeTimezoneContent]:
        """Gets the timezone of time template

        If the timezone is ``None``, returns `default`.

        Parameters:
           default: Default timezone.

        Returns:
           Timezone or quantity variable.
        """
        tz = self.args[2]
        return tz if tz is not None else default

    @property
    def calendar(self) -> Optional[VItem]:
        """The calendar model of time template."""
        return self.get_calendar()

    def get_calendar(
            self,
            default: Optional[VItem] = None
    ) -> Optional[VItem]:
        """Gets calendar model of time template.

        If the calendar model is ``None``, returns `default`.

        Parameters:
           default: Default calendar model.

        Returns:
           Calendar model, item template, or item variable.
        """
        cal = self.args[3]
        return cal if cal is not None else default


class TimeVariable(DeepDataValueVariable):
    """Time variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[TimeClass]  # pyright: ignore

    @classmethod
    def _preprocess_arg_time_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[TLocation] = None
    ) -> 'TimeVariable':
        return cast(TimeVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class TimeDatatype(Datatype):
    """Time datatype."""

    value_class: ClassVar[TimeClass]  # pyright: ignore

    _uri: ClassVar[URIRef] = NS.WIKIBASE.Time


class Time(
        DeepDataValue,
        datatype_class=TimeDatatype,
        template_class=TimeTemplate,
        variable_class=TimeVariable
):
    """Time.

    Parameters:
       time: Time.
       precision: Precision.
       timezone: Time zone.
       calendar: Calendar model.
    """

    datatype_class: ClassVar[TimeDatatypeClass]  # pyright: ignore
    datatype: ClassVar[TimeDatatype]             # pyright: ignore
    template_class: ClassVar[TimeTemplateClass]  # pyright: ignore
    variable_class: ClassVar[TimeVariableClass]  # pyright: ignore

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

    #: Year.
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
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Time.Precision':
        arg = cls._check_arg_isinstance(
            arg, (cls.Precision, Quantity, Decimal, float, int, str),
            function, name, position)
        try:
            if isinstance(arg, Quantity):
                arg = int(arg.args[0])
            if not isinstance(arg, (int, cls.Precision)):
                arg = int(arg)
            return cls.Precision(arg)
        except ValueError as err:
            raise cls._arg_error(
                f'expected {cls.Precision.__qualname__}',
                function, name, position, ValueError) from err

    @classmethod
    def _check_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            default: Optional['Time.Precision'] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional['Time.Precision']:
        if arg is None:
            return default
        else:
            return cls._check_arg_precision(arg, function, name, position)

    @classmethod
    def _preprocess_arg_precision(
            cls,
            arg: TTimePrecision,
            i: int,
            function: Optional[TLocation] = None
    ) -> 'Time.Precision':
        return cls._check_arg_precision(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            i: int,
            default: Optional['Time.Precision'] = None,
            function: Optional[TLocation] = None
    ) -> Optional['Time.Precision']:
        return cls._check_optional_arg_precision(
            arg, default, function or cls, None, i)

    @classmethod
    def _check_arg_timezone(
            cls,
            arg: TTimeTimezone,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> int:
        arg = cls._check_arg_isinstance(
            arg, (Quantity, Decimal, float, int, str),
            function, name, position)
        try:
            if isinstance(arg, Quantity):
                return int(arg.args[0])
            else:
                return int(arg)
        except ValueError as err:
            raise cls._arg_error(
                'expected timezone',
                function, name, position, ValueError) from err

    @classmethod
    def _check_optional_arg_timezone(
            cls,
            arg: Optional[TTimeTimezone],
            default: Optional[int] = None,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Optional[int]:
        if arg is None:
            return default
        else:
            return cls._check_arg_timezone(arg, function, name, position)

    @classmethod
    def _preprocess_arg_timezone(
            cls,
            arg: TTimeTimezone,
            i: int,
            function: Optional[TLocation] = None
    ) -> int:
        return cls._check_arg_timezone(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_timezone(
            cls,
            arg: Optional[TTimeTimezone],
            i: int,
            default: Optional[int] = None,
            function: Optional[TLocation] = None
    ) -> Optional[int]:
        return cls._check_optional_arg_timezone(
            arg, default, function or cls, None, i)

    @classmethod
    def _check_arg_time(
            cls,
            arg: TTime,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'Time':
        if isinstance(arg, Time):
            return arg
        else:
            return cls(cls._check_arg_datetime(arg, function, name, position))

    def __init__(
            self,
            time: VTTimeContent,
            precision: Optional[VTTimePrecisionContent] = None,
            timezone: Optional[VTTimeTimezoneContent] = None,
            calendar: Optional[VTItemContent] = None):
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # time
            return self_._preprocess_arg_datetime(
                arg.args[0] if isinstance(arg, Time) else arg, i)
        elif i == 2:            # precision
            return Time._preprocess_optional_arg_precision(
                arg, i, None, self_.__class__)
        elif i == 3:            # timezone
            return Time._preprocess_optional_arg_timezone(
                arg, i, None, self_.__class__)
        elif i == 4:            # calendar
            return self_._preprocess_optional_arg_item(arg, i)
        else:
            raise self_._should_not_get_here()

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
