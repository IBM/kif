# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import enum
import functools

from ..typing import (
    Any,
    Callable,
    cast,
    Final,
    Optional,
    override,
    Self,
    TypeAlias,
    Union,
)
from .fingerprint import (
    EntityFingerprint,
    Fingerprint,
    PropertyFingerprint,
    TEntityFingerprint,
    TFingerprint,
    TPropertyFingerprint,
)
from .kif_object import KIF_Object
from .snak import NoValueSnak, Snak, SomeValueSnak, ValueSnak
from .statement import Statement, TStatement
from .value import DeepDataValue, Quantity, Time

at_property = property


class Filter(KIF_Object):
    """Filter specification.

    Parameters:
       subject: Entity fingerprint.
       property: Property fingerprint.
       value: Fingerprint.
       snak_mask: Snak mask.
    """

    class SnakMask(enum.Flag):
        """Mask for concrete snak classes."""

        #: Mask for :class:`ValueSnak`.
        VALUE_SNAK = enum.auto()

        #: Mask for :class:`SomeValueSnak`.
        SOME_VALUE_SNAK = enum.auto()

        #: Mask for :class:`NoValueSnak`.
        NO_VALUE_SNAK = enum.auto()

        #: Mask for all snak classes.
        ALL = (VALUE_SNAK | SOME_VALUE_SNAK | NO_VALUE_SNAK)

        @classmethod
        def check(
                cls,
                arg: Any,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Self:
            if isinstance(arg, cls):
                return arg
            elif isinstance(arg, int):
                try:
                    return cls(arg)
                except ValueError as err:
                    raise Snak._check_error(
                        arg, function or cls.check, name, position,
                        ValueError, to_=cls.__qualname__) from err
            elif isinstance(arg, ValueSnak):
                return cast(Self, cls.VALUE_SNAK)
            elif isinstance(arg, SomeValueSnak):
                return cast(Self, cls.SOME_VALUE_SNAK)
            elif isinstance(arg, NoValueSnak):
                return cast(Self, cls.NO_VALUE_SNAK)
            else:
                raise Snak._check_error(
                    arg, function or cls.check, name, position,
                    to_=cls.__qualname__)

        @classmethod
        def check_optional(
                cls,
                arg: Optional[Any],
                default: Optional[Any] = None,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Optional[Self]:
            if arg is None:
                arg = default
            if arg is None:
                return arg
            else:
                return cls.check(arg, function, name, position)

    #: Mask for :class:`ValueSnak`.
    VALUE_SNAK: Final[SnakMask] = SnakMask.VALUE_SNAK

    #: Mask for :class:`SomeValueSnak`.
    SOME_VALUE_SNAK: Final[SnakMask] = SnakMask.SOME_VALUE_SNAK

    #: Mask for :class:`NoValueSnak`.
    NO_VALUE_SNAK: Final[SnakMask] = SnakMask.NO_VALUE_SNAK

    #: Type alias for SnakMask.
    TSnakMask: TypeAlias = Union[SnakMask, Snak, int]

    @classmethod
    def from_snak(
            cls,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None
    ) -> 'Filter':
        """Creates filter from snak.

        Parameters:
           subject: Entity fingerprint.
           snak: Snak.

        Returns:
           Filter.
        """
        if snak is None:
            property = None
            value = None
            snak_mask = None
        else:
            property = snak.property
            if isinstance(snak, ValueSnak):
                value = snak.value
            else:
                value = None
            snak_mask = cls.SnakMask.check(snak)
        return cls(subject, property, value, snak_mask)

    @classmethod
    def from_statement(cls, stmt: Statement) -> 'Filter':
        """Creates filter from statement.

        Parameters:
           stmt: Statement.

        Returns:
           Filter.
        """
        return cls.from_snak(stmt.subject, stmt.snak)

    def __init__(
            self,
            subject: Optional[TEntityFingerprint] = None,
            property: Optional[TPropertyFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None
    ):
        super().__init__(subject, property, value, snak_mask)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            return EntityFingerprint.check_optional(
                arg, None, type(self), None, i)
        elif i == 2:
            return PropertyFingerprint.check_optional(
                arg, None, type(self), None, i)
        elif i == 3:
            return Fingerprint.check_optional(
                arg, None, type(self), None, i)
        elif i == 4:
            return self.SnakMask.check_optional(
                arg, self.SnakMask.ALL, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @at_property
    def subject(self) -> Optional[EntityFingerprint]:
        """The subject of filter."""
        return self.get_subject()

    def get_subject(
            self,
            default: Optional[EntityFingerprint] = None
    ) -> Optional[EntityFingerprint]:
        """Gets the subject of filter.

        If the subject is ``None``, returns `default`.

        Parameters:
           default: Default subject.

        Returns:
           Entity fingerprint.
        """
        subj = self.args[0]
        return subj if subj is not None else default

    @at_property
    def property(self) -> Optional[PropertyFingerprint]:
        """The property of filter."""
        return self.get_property()

    def get_property(
            self,
            default: Optional[PropertyFingerprint] = None
    ) -> Optional[PropertyFingerprint]:
        """Gets the property of filter.

        If the property is ``None``, returns `default`.

        Parameters:
           default: Default property.

        Returns:
           Property fingerprint.
        """
        prop = self.args[1]
        return prop if prop is not None else default

    @at_property
    def value(self) -> Optional[Fingerprint]:
        """Filter value."""
        return self.get_value()

    def get_value(
            self,
            default: Optional[Fingerprint] = None
    ) -> Optional[Fingerprint]:
        """Gets the value of filter.

        If the value is ``None``, returns `default`.

        Parameters:
           default: Default value.

        Returns:
           Fingerprint.
        """
        val = self.args[2]
        return val if val is not None else default

    @at_property
    def snak_mask(self) -> SnakMask:
        """The snak mask of filter."""
        return self.get_snak_mask()

    def get_snak_mask(self) -> SnakMask:
        """Gets the snak mask of filter.

        Returns:
           Snak mask.
        """
        return self.SnakMask(self.args[3])

    def is_full(self) -> bool:
        """Tests whether filter is full.

        A full filter matches anything.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return (
            self.subject is None
            and self.property is None
            and self.value is None
            and self.snak_mask is self.SnakMask.ALL)

    def is_nonfull(self) -> bool:
        """Tests whether filter is non-full.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return not self.is_full()

    def is_empty(self) -> bool:
        """Tests whether filter is empty.

        An empty filter matches nothing.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return (
            self.snak_mask.value == 0
            or (self.value is not None
                and not (self.snak_mask & self.VALUE_SNAK)))

    def is_nonempty(self) -> bool:
        """Tests whether filter is non-empty.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return not self.is_empty()

    def match(self, stmt: TStatement) -> bool:
        """Tests whether filter shallow-matches statement.

        Parameters:
           stmt: Statement.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        stmt = Statement.check(stmt, self.match, 'stmt', 1)
        # Snak mask mismatch.
        if not bool(self.snak_mask & self.SnakMask.check(stmt.snak)):
            return False
        # Subject mismatch.
        if (self.subject is not None
            and self.subject.entity is not None
                and self.subject.entity != stmt.subject):
            return False
        # Property mismatch.
        if (self.property is not None
            and self.property.property is not None
            and (self.property.property.iri != stmt.snak.property.iri
                 or (self.property.property.range is not None
                     and self.property.property.range
                     != stmt.snak.property.range))):
            return False
        # Value mismatch.
        if (self.value is not None and self.value.value is not None):
            if not isinstance(stmt.snak, ValueSnak):
                return False
            assert isinstance(stmt.snak, ValueSnak)
            value = stmt.snak.value
            if type(self.value.value) is not type(value):
                return False
            if not isinstance(value, DeepDataValue):
                if self.value.value != value:
                    return False
            elif isinstance(value, Quantity):
                fr_qt = cast(Quantity, self.value.value)
                qt = value
                if (fr_qt.amount != qt.amount
                    or (fr_qt.unit is not None
                        and fr_qt.unit != qt.unit)
                    or (fr_qt.lower_bound is not None
                        and fr_qt.lower_bound != qt.lower_bound)
                    or (fr_qt.upper_bound is not None
                        and fr_qt.upper_bound != qt.upper_bound)):
                    return False
            elif isinstance(value, Time):
                fr_tm, tm = cast(Time, self.value.value), value
                fr_tm_time, tm_time = fr_tm.time, tm.time
                if fr_tm_time.tzinfo is None:
                    tm_time = tm_time.replace(tzinfo=None)
                if (fr_tm_time != tm_time
                    or (fr_tm.precision is not None
                        and fr_tm.precision != tm.precision)
                    or (fr_tm.timezone is not None
                        and fr_tm.timezone != tm.timezone)
                    or (fr_tm.calendar is not None
                        and fr_tm.calendar != tm.calendar)):
                    return False
            else:
                raise self._should_not_get_here()
        # Success.
        return True

    def combine(self, *others: 'Filter') -> 'Filter':
        """Combines filter with `others`.

        Parameters:
           others: Filters.

        Returns:
           Filter.
        """
        return functools.reduce(self._combine, others, self)

    @classmethod
    def _combine(cls, pat1: 'Filter', pat2: 'Filter'):
        pat2 = cast(Filter, Filter.check(pat2, cls.combine))
        return pat1.__class__(
            pat1._combine_subject(pat2.subject),
            pat1._combine_property(pat2.property),
            pat1._combine_value(pat2.value),
            pat1.snak_mask & pat2.snak_mask)

    def _combine_subject(
            self,
            other: Optional[EntityFingerprint]
    ) -> Optional[EntityFingerprint]:
        if self.subject is None:
            return other
        if other is None:
            return self.subject
        assert self.subject is not None
        assert other is not None
        if (self.subject.snak_set is not None
                and other.snak_set is not None):
            return EntityFingerprint(
                self.subject.snak_set.union(other.snak_set))
        raise ValueError('subjects cannot be combined')

    def _combine_property(
            self,
            other: Optional[PropertyFingerprint]
    ) -> Optional[PropertyFingerprint]:
        if self.property is None:
            return other
        if other is None:
            return self.property
        assert self.property is not None
        assert other is not None
        if (self.property.snak_set is not None
                and other.snak_set is not None):
            return PropertyFingerprint(
                self.property.snak_set.union(other.snak_set))
        raise ValueError('properties cannot be combined')

    def _combine_value(
            self,
            other: Optional[Fingerprint]
    ) -> Optional[Fingerprint]:
        if self.value is None:
            return other
        if other is None:
            return self.value
        assert self.value is not None
        assert other is not None
        if (self.value.snak_set is not None
                and other.snak_set is not None):
            return Fingerprint(
                self.value.snak_set.union(other.snak_set))
        raise ValueError('values cannot be combined')
