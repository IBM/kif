# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import enum
import functools

from ..typing import Any, Callable, Final, Optional, override, TypeAlias, Union
from .fingerprint import (
    AndFingerprint,
    Fingerprint,
    SnakFingerprint,
    TFingerprint,
    ValueFingerprint,
)
from .kif_object import KIF_Object
from .set import SnakSet
from .snak import NoValueSnak, Snak, SomeValueSnak, TSnak, ValueSnak
from .statement import Statement, TStatement
from .value import (
    Datatype,
    DataValue,
    DeepDataValue,
    Entity,
    ExternalIdDatatype,
    IRI_Datatype,
    ItemDatatype,
    LexemeDatatype,
    PropertyDatatype,
    QuantityDatatype,
    ShallowDataValue,
    StringDatatype,
    TDatatype,
    TextDatatype,
    TimeDatatype,
    Value,
)

at_property = property


class Filter(KIF_Object):
    """Filter specification.

    Parameters:
       subject: Fingerprint.
       property: Fingerprint.
       value: Fingerprint.
       snak_mask: Snak mask.
       subject_mask: Datatype mask.
       property_mask: Datatype mask.
       value_mask: Datatype mask.
    """

    class DatatypeMask(enum.Flag):
        """Mask for concrete datatype classes."""

        #: Mask for :class:`ItemDatatype`.
        ITEM = enum.auto()

        #: Mask for :class:`PropertyDatatype`.
        PROPERTY = enum.auto()

        #: Mask for :class:`LexemeDatatype`.
        LEXEME = enum.auto()

        #: Mask for :class:`IRI_Datatype`.
        IRI = enum.auto()

        #: Mask for :class:`TextDatatype`.
        TEXT = enum.auto()

        #: Mask for :class:`StringDatatype`.
        STRING = enum.auto()

        #: Mask for :class:`ExternalIdDatatype`.
        EXTERNAL_ID = enum.auto()

        #: Mask for :class:`QuantityDatatype`.
        QUANTITY = enum.auto()

        #: Mask for :class:`TimeDatatype`.
        TIME = enum.auto()

        #: Mask for all datatype classes.
        VALUE = (
            ITEM
            | PROPERTY
            | LEXEME
            | IRI
            | TEXT
            | STRING
            | EXTERNAL_ID
            | QUANTITY
            | TIME)

        #: Mask for entity datatype classes.
        ENTITY = ITEM | PROPERTY | LEXEME

        #: Mask for data-value datatype classes.
        DATA_VALUE = VALUE & ~ENTITY

        #: Mask for shallow data-value datatype classes.
        SHALLOW_DATA_VALUE = IRI | TEXT | STRING | EXTERNAL_ID

        #: Mask for deep data-value datatype classes.
        DEEP_DATA_VALUE = DATA_VALUE & ~SHALLOW_DATA_VALUE

        #: Mask for all datatype classes.
        ALL = VALUE

        @classmethod
        def check(
                cls,
                arg: Any,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None,
        ) -> 'Filter.DatatypeMask':
            """Coerces `arg` to datatype mask.

            If `arg` cannot be coerced, raises an error.

            Parameters:
               arg: Value.
               function: Function or function name.
               name: Argument name.
               position: Argument position.

            Returns:
               Datatype mask.
            """
            if isinstance(arg, cls):
                return arg
            elif isinstance(arg, int):
                try:
                    return cls(arg)
                except ValueError as err:
                    raise Datatype._check_error(
                        arg, function or cls.check, name, position,
                        ValueError, to_=cls.__qualname__) from err
            else:
                if (isinstance(arg, type)
                        and issubclass(arg, (Datatype, Value))):
                    mask = cls._from_abstract_datatype_or_value_class(arg)
                    if mask is not None:
                        return mask
                return cls._from_datatype(Datatype.check(
                    arg, function or cls.check, name, position))

        @classmethod
        def check_optional(
                cls,
                arg: Optional[Any],
                default: Optional[Any] = None,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Optional['Filter.DatatypeMask']:
            """Coerces optional `arg` to datatype mask.

            If `arg` cannot be coerced, raises an error.

            If `arg` is ``None``, returns `default`.

            Parameters:
               arg: Value.
               default: Default value.
               function: Function or function name.
               name: Argument name.
               position: Argument position.

            Returns:
               Datatype mask or `default`.
            """
            if arg is None:
                arg = default
            if arg is None:
                return arg
            else:
                return cls.check(arg, function, name, position)

        @classmethod
        @functools.cache
        def _from_abstract_datatype_or_value_class(
                cls,
                arg: Union[type[Datatype], type[Value]]
        ) -> Optional['Filter.DatatypeMask']:
            if arg is Datatype:
                return cls.ALL
            elif arg is Value:
                return cls.VALUE
            elif arg is Entity:
                return cls.ENTITY
            elif arg is DataValue:
                return cls.DATA_VALUE
            elif arg is ShallowDataValue:
                return cls.SHALLOW_DATA_VALUE
            elif arg is DeepDataValue:
                return cls.DEEP_DATA_VALUE
            else:
                return None

        @classmethod
        @functools.cache
        def _from_datatype(cls, datatype: Datatype) -> 'Filter.DatatypeMask':
            if isinstance(datatype, ItemDatatype):
                return cls.ITEM
            elif isinstance(datatype, PropertyDatatype):
                return cls.PROPERTY
            elif isinstance(datatype, LexemeDatatype):
                return cls.LEXEME
            elif isinstance(datatype, IRI_Datatype):
                return cls.IRI
            elif isinstance(datatype, TextDatatype):
                return cls.TEXT
            elif isinstance(datatype, ExternalIdDatatype):
                return cls.EXTERNAL_ID
            elif isinstance(datatype, StringDatatype):
                return cls.STRING
            elif isinstance(datatype, QuantityDatatype):
                return cls.QUANTITY
            elif isinstance(datatype, TimeDatatype):
                return cls.TIME
            else:
                raise Filter._should_not_get_here()

        def match(self, datatype: TDatatype) -> bool:
            """Tests whether datatype mask matches `datatype`.

            Parameters:
               datatype: Datatype.

            Returns:
               ``True`` if successful; ``False`` otherwise.
            """
            return bool(self & self.check(datatype))

    #: Mask for value datatypes.
    VALUE: Final[DatatypeMask] = DatatypeMask.VALUE

    #: Mask for entity datatypes.
    ENTITY: Final[DatatypeMask] = DatatypeMask.ENTITY

    #: Mask for :class:`ItemDatatype`.
    ITEM: Final[DatatypeMask] = DatatypeMask.ITEM

    #: Mask for :class:`PropertyDatatype`.
    PROPERTY: Final[DatatypeMask] = DatatypeMask.PROPERTY

    #: Mask for :class:`LexemeDatatype`.
    LEXEME: Final[DatatypeMask] = DatatypeMask.LEXEME

    #: Mask for data-value datatypes.
    DATA_VALUE: Final[DatatypeMask] = DatatypeMask.DATA_VALUE

    #: Mask for shallow-data-value datatypes.
    SHALLOW_DATA_VALUE: Final[DatatypeMask] = DatatypeMask.SHALLOW_DATA_VALUE

    #: Mask for :class:`IRI_Datatype`.
    IRI: Final[DatatypeMask] = DatatypeMask.IRI

    #: Mask for :class:`TextDatatype`.
    TEXT: Final[DatatypeMask] = DatatypeMask.TEXT

    #: Mask for :class:`StringDatatype`.
    STRING: Final[DatatypeMask] = DatatypeMask.STRING

    #: Mask for :class:`ExternalIdDatatype`.
    EXTERNAL_ID: Final[DatatypeMask] = DatatypeMask.EXTERNAL_ID

    #: Mask for deep-data-value datatypes.
    DEEP_DATA_VALUE: Final[DatatypeMask] = DatatypeMask.DEEP_DATA_VALUE

    #: Mask for :class:`QuantityDatatype`.
    QUANTITY: Final[DatatypeMask] = DatatypeMask.QUANTITY

    #: Mask for :class:`TimeDatatype`.
    TIME: Final[DatatypeMask] = DatatypeMask.TIME

    #: Type alias for DatatypeMask.
    TDatatypeMask: TypeAlias = Union[DatatypeMask, TDatatype, int]

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
        ) -> 'Filter.SnakMask':
            """Coerces `arg` to snak mask.

            If `arg` cannot be coerced, raises an error.

            Parameters:
               arg: Value.
               function: Function or function name.
               name: Argument name.
               position: Argument position.

            Returns:
               Snak mask.
            """
            if isinstance(arg, cls):
                return arg
            elif isinstance(arg, int):
                try:
                    return cls(arg)
                except ValueError as err:
                    raise Snak._check_error(
                        arg, function or cls.check, name, position,
                        ValueError, to_=cls.__qualname__) from err
            elif isinstance(arg, type) and issubclass(arg, Snak):
                return cls._from_snak_class(arg)
            else:
                return cls._from_snak(Snak.check(
                    arg, function or cls.check, name, position))

        @classmethod
        def check_optional(
                cls,
                arg: Optional[Any],
                default: Optional[Any] = None,
                function: Optional[Union[Callable[..., Any], str]] = None,
                name: Optional[str] = None,
                position: Optional[int] = None
        ) -> Optional['Filter.SnakMask']:
            """Coerces optional `arg` to snak mask.

            If `arg` cannot be coerced, raises an error.

            If `arg` is ``None``, returns `default`.

            Parameters:
               arg: Value.
               default: Default value.
               function: Function or function name.
               name: Argument name.
               position: Argument position.

            Returns:
               Snak mask or `default`.
            """
            if arg is None:
                arg = default
            if arg is None:
                return arg
            else:
                return cls.check(arg, function, name, position)

        @classmethod
        @functools.cache
        def _from_snak_class(
                cls,
                snak_class: type[Snak]
        ) -> 'Filter.SnakMask':
            if snak_class is Snak:
                return Filter.SnakMask.ALL
            elif snak_class is ValueSnak:
                return cls.VALUE_SNAK
            elif snak_class is SomeValueSnak:
                return cls.SOME_VALUE_SNAK
            elif snak_class is NoValueSnak:
                return cls.NO_VALUE_SNAK
            else:
                raise Filter._should_not_get_here()

        @classmethod
        @functools.cache
        def _from_snak(cls, snak: Snak) -> 'Filter.SnakMask':
            if isinstance(snak, ValueSnak):
                return cls.VALUE_SNAK
            elif isinstance(snak, SomeValueSnak):
                return cls.SOME_VALUE_SNAK
            elif isinstance(snak, NoValueSnak):
                return cls.NO_VALUE_SNAK
            else:
                raise Filter._should_not_get_here()

        def match(self, snak: TSnak) -> bool:
            """Tests whether snak mask matches `snak`.

            Parameters:
               snak: Snak.

            Returns:
               ``True`` if successful; ``False`` otherwise.
            """
            return bool(self & self.check(snak))

    #: Mask for :class:`ValueSnak`.
    VALUE_SNAK: Final[SnakMask] = SnakMask.VALUE_SNAK

    #: Mask for :class:`SomeValueSnak`.
    SOME_VALUE_SNAK: Final[SnakMask] = SnakMask.SOME_VALUE_SNAK

    #: Mask for :class:`NoValueSnak`.
    NO_VALUE_SNAK: Final[SnakMask] = SnakMask.NO_VALUE_SNAK

    #: Type alias for SnakMask.
    TSnakMask: TypeAlias = Union[SnakMask, type['Snak'], TSnak, int]

    @classmethod
    def from_snak(
            cls,
            subject: Optional[TFingerprint] = None,
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
            subject: Optional[TFingerprint] = None,
            property: Optional[TFingerprint] = None,
            value: Optional[TFingerprint] = None,
            snak_mask: Optional[TSnakMask] = None,
            subject_mask: Optional[TDatatypeMask] = None,
            property_mask: Optional[TDatatypeMask] = None,
            value_mask: Optional[TDatatypeMask] = None
    ):
        super().__init__(
            subject, property, value, snak_mask,
            subject_mask, property_mask, value_mask)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if 1 <= i <= 3:         # subject, property, value
            return Fingerprint.check(arg, type(self), None, i)
        elif i == 4:            # snak mask
            return self.SnakMask.check_optional(
                arg, self.SnakMask.ALL, type(self), None, i)
        elif i == 5:            # subject mask
            return self.DatatypeMask.check_optional(
                arg, self.ENTITY, type(self), None, i)
        elif i == 6:            # property mask
            return self.DatatypeMask.check_optional(
                arg, self.PROPERTY, type(self), None, i)
        elif i == 7:            # value mask
            return self.DatatypeMask.check_optional(
                arg, self.VALUE, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @override
    def _set_args(self, args: tuple[Any, ...]):
        super()._set_args(args)

    @at_property
    def subject(self) -> Fingerprint:
        """The subject of filter."""
        return self.get_subject()

    def get_subject(self) -> Fingerprint:
        """Gets the subject of filter.

        Returns:
           Fingerprint.
        """
        return self.args[0]

    @at_property
    def property(self) -> Fingerprint:
        """The property of filter."""
        return self.get_property()

    def get_property(self) -> Fingerprint:
        """Gets the property of filter.

        Returns:
           Fingerprint.
        """
        return self.args[1]

    @at_property
    def value(self) -> Fingerprint:
        """Filter value."""
        return self.get_value()

    def get_value(self) -> Fingerprint:
        """Gets the value of filter.

        Returns:
           Fingerprint.
        """
        return self.args[2]

    @at_property
    def snak_mask(self) -> SnakMask:
        """The snak mask of filter."""
        return self.get_snak_mask()

    def get_snak_mask(self) -> SnakMask:
        """Gets the snak mask of filter.

        Returns:
           Snak mask.
        """
        return self.args[3]

    @at_property
    def subject_mask(self) -> DatatypeMask:
        """The subject datatype mask of filter."""
        return self.get_subject_mask()

    def get_subject_mask(self) -> DatatypeMask:
        """Gets the subject datatype mask of filter.

        Returns:
           Subject datatype mask.
        """
        return self.args[4] & self.ENTITY

    @at_property
    def property_mask(self) -> DatatypeMask:
        """The property datatype mask of filter."""
        return self.get_property_mask()

    def get_property_mask(self) -> DatatypeMask:
        """Gets the property datatype mask of filter.

        Returns:
           Property datatype mask.
        """
        return self.args[5] & self.PROPERTY

    @at_property
    def value_mask(self) -> DatatypeMask:
        """The value datatype mask of filter."""
        return self.get_value_mask()

    def get_value_mask(self) -> DatatypeMask:
        """Gets the value datatype mask of filter.

        Returns:
           Value datatype mask.
        """
        return self.args[6] & self.VALUE

    def is_full(self) -> bool:
        """Tests whether filter is full.

        A full filter matches anything.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        f = self.normalize()
        return (f.snak_mask == self.SnakMask.ALL
                and f.subject.is_full()
                and f.subject_mask == self.ENTITY
                and f.property.is_full()
                and f.property_mask == self.PROPERTY
                and f.value.is_full()
                and f.value_mask == self.VALUE)

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
        f = self.normalize()
        return (f.snak_mask.value == 0
                or f.subject_mask.value == 0
                or f.property_mask.value == 0)

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
        if not Fingerprint.check(self.subject).match(stmt.subject):
            return False        # subject mismatch
        if not Fingerprint.check(self.property).match(stmt.snak.property):
            return False        # property mismatch
        fp = Fingerprint.check(self.value)
        if isinstance(stmt.snak, ValueSnak):
            if fp.is_empty():
                return False    # snak mismatch
            if not fp.match(stmt.snak.value):
                return False    # value mismatch
        else:
            if not fp.is_empty() and not fp.is_full():
                return False    # snak mismatch
        return True

    def normalize(self) -> 'Filter':
        """Reduce filter to a normal form.

        Normalizes the fingerprint expressions in filter.

        Returns:
           Filter.
        """
        subject = self.subject.normalize(Filter.ENTITY)
        subject_mask = self.subject_mask & subject.datatype_mask
        property = self.property.normalize(Filter.PROPERTY)
        property_mask = self.property_mask & property.datatype_mask
        value = self.value.normalize(self.VALUE)
        value_mask = self.value_mask & value.datatype_mask
        snak_mask = self.snak_mask
        if 0 < value_mask.value < self.VALUE.value:
            snak_mask &= self.VALUE_SNAK
        return Filter(
            subject, property, value, snak_mask,
            subject_mask, property_mask, value_mask)

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
            f1.subject & f2.subject,
            f1.property & f2.property,
            f1.value & f2.value,
            f1.snak_mask & f2.snak_mask,
            f1.subject_mask & f2.subject_mask,
            f1.property_mask & f2.property_mask,
            f1.value_mask & f2.value_mask).normalize()

    def _unpack_legacy(
            self
    ) -> tuple[
        Optional[Union[Value, SnakSet]],
        Optional[Union[Value, SnakSet]],
        Optional[Union[Value, SnakSet]],
        'Filter.SnakMask'
    ]:
        filter = self.normalize()
        assert isinstance(filter.subject, Fingerprint)
        assert isinstance(filter.property, Fingerprint)
        assert isinstance(filter.value, Fingerprint)
        subject: Optional[Union[Value, SnakSet]]
        property: Optional[Union[Value, SnakSet]]
        value: Optional[Union[Value, SnakSet]]
        if filter.subject.is_full():
            subject = None
        elif isinstance(filter.subject, ValueFingerprint):
            subject = filter.subject.value
        elif isinstance(filter.subject, (SnakFingerprint, AndFingerprint)):
            subject = filter._unpack_legacy_fp_to_snak_set(filter.subject)
        else:
            raise filter._should_not_get_here()
        if filter.property.is_full():
            property = None
        elif isinstance(filter.property, ValueFingerprint):
            property = filter.property.value
        elif isinstance(filter.property, (SnakFingerprint, AndFingerprint)):
            property = filter._unpack_legacy_fp_to_snak_set(filter.property)
        else:
            raise filter._should_not_get_here()
        if filter.value.is_full():
            value = None
        elif isinstance(filter.value, ValueFingerprint):
            value = filter.value.value
        elif isinstance(filter.value, (SnakFingerprint, AndFingerprint)):
            value = filter._unpack_legacy_fp_to_snak_set(filter.value)
        else:
            raise filter._should_not_get_here()
        return subject, property, value, filter.snak_mask

    def _unpack_legacy_fp_to_snak_set(self, fp: Fingerprint) -> SnakSet:
        if isinstance(fp, SnakFingerprint):
            return SnakSet(fp.snak)
        elif isinstance(fp, AndFingerprint):
            return SnakSet().union(*map(
                self._unpack_legacy_fp_to_snak_set, fp.args))
        else:
            raise self._should_not_get_here()
