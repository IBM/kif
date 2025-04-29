# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import enum
import sys

from ...typing import Any, ClassVar, Location, override, Self, TypeAlias, Union
from ..term import Template, Variable
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .item import Item, ItemTemplate, ItemVariable, VItem, VTItem
from .quantity import Quantity, QuantityVariable, TQuantity, VTQuantityContent
from .string import String
from .value import Datatype

TDatetime: TypeAlias = Union[datetime.datetime, datetime.date, str]
TTime: TypeAlias = Union['Time', TDatetime]
VTime: TypeAlias = Union['TimeTemplate', 'TimeVariable', 'Time']
VTimeContent: TypeAlias = Union['TimeVariable', datetime.datetime]
VTTimeContent: TypeAlias = Union[Variable, TTime]

TTimePrecision: TypeAlias = Union['Time.Precision', TQuantity]
VTimePrecisionContent: TypeAlias = Union[QuantityVariable, 'Time.Precision']
VTTimePrecisionContent: TypeAlias = Union[Variable, TTimePrecision]

TTimeTimezone: TypeAlias = TQuantity
VTimeTimezoneContent: TypeAlias = Union[QuantityVariable, int]
VTTimeTimezoneContent: TypeAlias = VTQuantityContent


class TimeTemplate(DeepDataValueTemplate):
    """Time template.

    Parameters:
       time: Time or time variable.
       precision: Precision or quantity variable.
       timezone: Time zone or quantity variable.
       calendar: Calendar model, item template, or item variable.
    """

    object_class: ClassVar[type[Time]]  # pyright: ignore

    def __init__(
            self,
            time: VTTimeContent,
            precision: VTTimePrecisionContent | None = None,
            timezone: VTTimeTimezoneContent | None = None,
            calendar: VTItem | None = None
    ) -> None:
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # time
            if isinstance(arg, Variable):
                return TimeVariable.check(arg, type(self), None, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 2:            # precision
            if isinstance(arg, Variable):
                return QuantityVariable.check(arg, type(self), None, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 3:            # timezone
            if isinstance(arg, Variable):
                return QuantityVariable.check(arg, type(self), None, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 4:            # calendar
            if isinstance(arg, Template):
                return ItemTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return ItemVariable.check(arg, type(self), None, i)
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
    def precision(self) -> VTimePrecisionContent | None:
        """The precision of time template."""
        return self.get_precision()

    def get_precision(
            self,
            default: VTimePrecisionContent | None = None
    ) -> VTimePrecisionContent | None:
        """Gets the precision of time.

        If the precision is ``None``, returns `default`.

        Parameters:
           default: Default precision.

        Returns:
           Precision or quantity variable.
        """
        return self.get(1, default)

    @property
    def timezone(self) -> VTimeTimezoneContent | None:
        """The timezone of time template."""
        return self.get_timezone()

    def get_timezone(
            self,
            default: VTimeTimezoneContent | None = None
    ) -> VTimeTimezoneContent | None:
        """Gets the timezone of time template

        If the timezone is ``None``, returns `default`.

        Parameters:
           default: Default timezone.

        Returns:
           Timezone or quantity variable.
        """
        return self.get(2, default)

    @property
    def calendar(self) -> VItem | None:
        """The calendar model of time template."""
        return self.get_calendar()

    def get_calendar(
            self,
            default: VItem | None = None
    ) -> VItem | None:
        """Gets calendar model of time template.

        If the calendar model is ``None``, returns `default`.

        Parameters:
           default: Default calendar model.

        Returns:
           Calendar model, item template, or item variable.
        """
        return self.get(3, default)


class TimeVariable(DeepDataValueVariable):
    """Time variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Time]]  # pyright: ignore


class TimeDatatype(Datatype):
    """Time datatype."""

    instance: ClassVar[TimeDatatype]  # pyright: ignore
    value_class: ClassVar[type[Time]]  # pyright: ignore


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

    datatype_class: ClassVar[type[TimeDatatype]]  # pyright: ignore
    datatype: ClassVar[TimeDatatype]              # pyright: ignore
    template_class: ClassVar[type[TimeTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[TimeVariable]]  # pyright: ignore

    # See:
    # <https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Time>.
    # <https://www.mediawiki.org/wiki/Wikibase/DataModel#Dates_and_times>.

    class Precision(enum.Enum):
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
        elif isinstance(arg, String):
            return cls(arg.content)
        elif isinstance(arg, (datetime.datetime, datetime.date, str)):
            return cls(arg)
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            time: VTTimeContent,
            precision: VTTimePrecisionContent | None = None,
            timezone: VTTimeTimezoneContent | None = None,
            calendar: VTItem | None = None
    ) -> None:
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if arg is None and 2 <= i <= 4:
            return None
        if i == 1:              # time
            if isinstance(arg, Time):
                return arg.time
            elif isinstance(arg, str):
                ###
                # FIXME: Python's fromisoformat() does not support the +/-
                # sign used by Wikidata at the start of date-time literals.
                ###
                arg = arg[1:] if arg[0] == '+' or arg[0] == '-' else arg
                if arg[-1] == 'Z' and sys.version_info < (3, 11):
                    ###
                    # FIXME: Python < 3.11's fromisoformat() does not
                    # support the trailing "Z".  Move this hack to a
                    # separate module.
                    ###
                    arg = arg[:-1]
                try:
                    dt = datetime.datetime.fromisoformat(arg)
                except ValueError as err:
                    raise Time._check_error(
                        arg, type(self_), None, i, ValueError) from err
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=datetime.timezone.utc)
                else:
                    return dt
            elif isinstance(arg, datetime.datetime):
                return arg
            elif isinstance(arg, datetime.date):
                return datetime.datetime.combine(
                    arg, datetime.time(), tzinfo=datetime.timezone.utc)
            else:
                raise Time._check_error(arg, type(self_), None, i)
        elif i == 2:            # precision
            if isinstance(arg, Time.Precision):
                return arg
            else:
                try:
                    return Time.Precision(
                        Quantity.check(arg, type(self_), None, i).amount)
                except ValueError as err:
                    raise Time._check_error(
                        arg, type(self_), None, i,
                        to_=Time.Precision.__qualname__) from err
        elif i == 3:            # timezone
            if isinstance(arg, int):
                return arg
            else:
                return int(Quantity.check(arg, type(self_), None, i).amount)
        elif i == 4:            # calendar
            return Item.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @property
    def time(self) -> datetime.datetime:
        """The date-time of time."""
        return self.get_time()

    def get_time(self) -> datetime.datetime:
        """Gets the date-time of time.

        Returns:
           Datetime.
        """
        return self.args[0]

    @property
    def precision(self) -> Precision | None:
        """The precision of time."""
        return self.get_precision()

    def get_precision(
            self,
            default: Time.Precision | None = None
    ) -> Precision | None:
        """Gets the precision of time.

        If the precision is ``None``, returns `default`.

        Parameters:
           default: Default precision.

        Returns:
           Precision.
        """
        return self.get(1, default)

    @property
    def timezone(self) -> int | None:
        """The timezone of time."""
        return self.get_timezone()

    def get_timezone(self, default: int | None = None) -> int | None:
        """Gets the timezone of time.

        If the timezone is ``None``, returns `default`.

        Parameters:
           default: Default timezone.

        Returns:
           Timezone.
        """
        return self.get(2, default)

    @property
    def calendar(self) -> Item | None:
        """The calendar model of time."""
        return self.get_calendar()

    def get_calendar(self, default: Item | None = None) -> Item | None:
        """Gets the calendar model of time.

        If the calendar model is ``None``, returns `default`.

        Parameters:
           default: Default calendar model.

        Returns:
           Calendar model.
        """
        return self.get(3, default)
