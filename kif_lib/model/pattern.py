# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from functools import reduce

from ..typing import cast, Optional
from .fingerprint import (
    EntityFingerprint,
    Fingerprint,
    PropertyFingerprint,
    TEntityFingerprint,
    TFingerprint,
    TPropertyFingerprint,
)
from .kif_object import KIF_Object
from .snak import Snak, ValueSnak
from .statement import Statement


class Pattern(KIF_Object):
    """Abstract base class for patterns."""


at_property = property


class FilterPattern(Pattern):
    """Filter pattern.

    Parameters:
       arg1: Entity fingerprint.
       arg2: Property fingerprint.
       arg3: Fingerprint.
       arg4: Snak mask.
    """

    @classmethod
    def from_snak(
            cls,
            subject: Optional[TEntityFingerprint] = None,
            snak: Optional[Snak] = None
    ) -> 'FilterPattern':
        """Creates filter pattern from snak.

        Parameters:
           subject: Entity fingerprint.
           snak: Snak.

        Returns:
           The resulting filter pattern.
        """
        if snak is None:
            property = None
            value = None
            snak_mask = None
        else:
            property = snak.property
            if snak.is_value_snak():
                value = cast(ValueSnak, snak).value
            else:
                value = None
            snak_mask = snak.mask
        return cls(subject, property, value, snak_mask)

    @classmethod
    def from_statement(cls, stmt: Statement) -> 'FilterPattern':
        """Creates filter pattern from statement.

        Parameters:
           stmt: Statement.

        Returns:
           The resulting filter pattern.
        """
        return cls.from_snak(stmt.subject, stmt.snak)

    def __init__(
            self,
            arg1: Optional[TEntityFingerprint] = None,
            arg2: Optional[TPropertyFingerprint] = None,
            arg3: Optional[TFingerprint] = None,
            arg4: Optional[Snak.TMask] = None
    ):
        super().__init__(arg1, arg2, arg3, arg4)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_optional_arg_entity_fingerprint(arg, i)
        elif i == 2:
            return self._preprocess_optional_arg_property_fingerprint(arg, i)
        elif i == 3:
            return self._preprocess_optional_arg_fingerprint(arg, i)
        elif i == 4:
            return Snak._preprocess_optional_arg_snak_mask(
                arg, i, Snak.ALL).value
        else:
            self._should_not_get_here()

    @at_property
    def subject(self) -> Optional[EntityFingerprint]:
        """Filter pattern subject."""
        return self.get_subject()

    def get_subject(
            self,
            default: Optional[EntityFingerprint] = None
    ) -> Optional[EntityFingerprint]:
        """Gets filter pattern subject.

        If filter pattern subject is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Filter pattern subject or `default` (pattern has no subject).
        """
        subj = self.args[0]
        return subj if subj is not None else default

    @at_property
    def property(self) -> Optional[PropertyFingerprint]:
        """Filter pattern property."""
        return self.get_property()

    def get_property(
            self,
            default: Optional[PropertyFingerprint] = None
    ) -> Optional[PropertyFingerprint]:
        """Gets filter pattern property.

        If filter pattern property is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Filter pattern property or `default` (pattern has no property).
        """
        prop = self.args[1]
        return prop if prop is not None else default

    @at_property
    def value(self) -> Optional[Fingerprint]:
        """Filter pattern value."""
        return self.get_value()

    def get_value(
            self,
            default: Optional[Fingerprint] = None
    ) -> Optional[Fingerprint]:
        """Gets filter pattern value.

        If filter pattern value is ``None``, returns `default`.

        Parameters:
           default: Default.

        Returns:
           Filter pattern value or `default` (pattern has no value).
        """
        val = self.args[2]
        return val if val is not None else default

    @at_property
    def snak_mask(self) -> Snak.Mask:
        """Filter pattern snak mask."""
        return self.get_snak_mask()

    def get_snak_mask(self) -> Snak.Mask:
        """Gets filter pattern snak mask.

        Returns:
           Filter pattern snak mask.
        """
        return Snak.Mask(self.args[3])

    def is_full(self) -> bool:
        """Tests whether filter pattern is full.

        A full pattern matches anything.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return (
            self.subject is None and self.property is None
            and self.value is None and self.snak_mask is Snak.ALL)

    def is_nonfull(self) -> bool:
        """Tests whether filter pattern is non-full.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return not self.is_full()

    def is_empty(self) -> bool:
        """Tests whether filter pattern is empty.

        An empty pattern matches nothing.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return (
            self.snak_mask.value == 0
            or (self.value is not None
                and not (self.snak_mask & Snak.VALUE_SNAK)))

    def is_nonempty(self) -> bool:
        """Tests whether filter pattern is non-empty.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return not self.is_empty()

    def combine(self, *others: 'FilterPattern') -> 'FilterPattern':
        """Combines filter pattern with `others`.

        Parameters:
           others: Filter patterns.

        Returns:
           The resulting filter pattern.

        Raises:
           ValueError: Patterns cannot be combined.
        """
        return reduce(self._combine, others, self)

    @classmethod
    def _combine(cls, pat1: 'FilterPattern', pat2: 'FilterPattern'):
        pat2 = cast(FilterPattern, FilterPattern.check(pat2, cls.combine))
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
