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
from .fingerprint.expression import Fp
from .kif_object import KIF_Object
from .snak import NoValueSnak, Snak, SomeValueSnak, ValueSnak
from .statement import Statement, TStatement

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
            if isinstance(arg, Fp):
                return arg
            else:
                return EntityFingerprint.check_optional(
                    arg, None, type(self), None, i)
        elif i == 2:
            if isinstance(arg, Fp):
                return arg
            else:
                return PropertyFingerprint.check_optional(
                    arg, None, type(self), None, i)
        elif i == 3:
            if isinstance(arg, Fp):
                return arg
            else:
                return Fingerprint.check_optional(
                    arg, None, type(self), None, i)
        elif i == 4:
            return self.SnakMask.check_optional(
                arg, self.SnakMask.ALL, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @override
    def _set_args(self, args: tuple[Any, ...]):
        super()._set_args(args)

    @at_property
    def subject(self) -> Optional[Union[EntityFingerprint, Fp]]:
        """The subject of filter."""
        return self.get_subject()

    def get_subject(
            self,
            default: Optional[Union[EntityFingerprint, Fp]] = None
    ) -> Optional[Union[EntityFingerprint, Fp]]:
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
    def property(self) -> Optional[Union[PropertyFingerprint, Fp]]:
        """The property of filter."""
        return self.get_property()

    def get_property(
            self,
            default: Optional[Union[PropertyFingerprint, Fp]] = None
    ) -> Optional[Union[PropertyFingerprint, Fp]]:
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
    def value(self) -> Optional[Union[Fingerprint, Fp]]:
        """Filter value."""
        return self.get_value()

    def get_value(
            self,
            default: Optional[Union[Fingerprint, Fp]] = None
    ) -> Optional[Union[Fingerprint, Fp]]:
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
        if not bool(self.snak_mask & self.SnakMask.check(stmt.snak)):
            return False        # snak mask mismatch
        if not Fp.check(self.subject).match(stmt.subject):
            return False        # subject mismatch
        if not Fp.check(self.property).match(stmt.snak.property):
            return False        # property mismatch
        fp = Fp.check(self.value)
        if isinstance(stmt.snak, ValueSnak):
            if fp.is_empty():
                return False    # snak mismatch
            if not fp.match(stmt.snak.value):
                return False    # value mismatch
        else:
            if not fp.is_empty() and not fp.is_full():
                return False    # snak mismatch
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
    def _combine(cls, f1: 'Filter', f2: 'Filter'):
        f2 = Filter.check(f2, cls.combine)
        return f1.__class__(
            f1._combine_subject(f2.subject),
            f1._combine_property(f2.property),
            f1._combine_value(f2.value),
            f1.snak_mask & f2.snak_mask)

    def _combine_subject(
            self,
            other: Optional[Union[EntityFingerprint, Fp]]
    ) -> Optional[Union[EntityFingerprint, Fp]]:
        if isinstance(self.subject, Fp) or isinstance(other, Fp):
            return Fp.check(self.subject) & Fp.check(other)
        else:
            return self._combine_subject_legacy(other)

    def _combine_subject_legacy(
            self, other: Optional[EntityFingerprint]
    ) -> Optional[EntityFingerprint]:
        assert isinstance(self.subject, (EntityFingerprint, type(None)))
        assert isinstance(other, (EntityFingerprint, type(None)))
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
            other: Optional[Union[PropertyFingerprint, Fp]]
    ) -> Optional[Union[PropertyFingerprint, Fp]]:
        if isinstance(self.property, Fp) or isinstance(other, Fp):
            return Fp.check(self.property) & Fp.check(other)
        else:
            return self._combine_property_legacy(other)

    def _combine_property_legacy(
            self,
            other: Optional[PropertyFingerprint]
    ) -> Optional[PropertyFingerprint]:
        assert isinstance(self.property, (PropertyFingerprint, type(None)))
        assert isinstance(other, (PropertyFingerprint, type(None)))
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
            other: Optional[Union[Fingerprint, Fp]]
    ) -> Optional[Union[Fingerprint, Fp]]:
        if isinstance(self.value, Fp) or isinstance(other, Fp):
            return Fp.check(self.value) & Fp.check(other)
        else:
            return self._combine_value_legacy(other)

    def _combine_value_legacy(
            self,
            other: Optional[Fingerprint]
    ) -> Optional[Fingerprint]:
        assert isinstance(self.value, (Fingerprint, type(None)))
        assert isinstance(other, (Fingerprint, type(None)))
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
