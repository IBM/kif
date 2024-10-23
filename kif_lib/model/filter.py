# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools

from ..typing import (
    Any,
    cast,
    Final,
    Location,
    Optional,
    override,
    TypeAlias,
    Union,
)
from .fingerprint import (
    AndFingerprint,
    Fingerprint,
    SnakFingerprint,
    TFingerprint,
    ValueFingerprint,
)
from .flags import Flags
from .kif_object import KIF_Object
from .set import SnakSet
from .snak import NoValueSnak, Snak, SomeValueSnak, TSnak, ValueSnak
from .statement import Statement, TStatement
from .value import (
    Datatype,
    DataValue,
    DeepDataValue,
    Entity,
    ExternalId,
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    Lexeme,
    LexemeDatatype,
    Property,
    PropertyDatatype,
    Quantity,
    QuantityDatatype,
    ShallowDataValue,
    String,
    StringDatatype,
    TDatatype,
    Text,
    TextDatatype,
    Time,
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
       language: Language tag.
    """

    class DatatypeMask(Flags):
        """Mask for concrete datatype classes."""

        #: Mask for :class:`ItemDatatype`.
        ITEM = Flags.auto()

        #: Mask for :class:`PropertyDatatype`.
        PROPERTY = Flags.auto()

        #: Mask for :class:`LexemeDatatype`.
        LEXEME = Flags.auto()

        #: Mask for :class:`IRI_Datatype`.
        IRI = Flags.auto()

        #: Mask for :class:`TextDatatype`.
        TEXT = Flags.auto()

        #: Mask for :class:`StringDatatype`.
        STRING = Flags.auto()

        #: Mask for :class:`ExternalIdDatatype`.
        EXTERNAL_ID = Flags.auto()

        #: Mask for :class:`QuantityDatatype`.
        QUANTITY = Flags.auto()

        #: Mask for :class:`TimeDatatype`.
        TIME = Flags.auto()

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
        @override
        def check(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None,
        ) -> Filter.DatatypeMask:
            if isinstance(arg, (cls, int)):
                return super().check(arg, function, name, position)
            else:
                if (isinstance(arg, type)
                        and issubclass(arg, (Datatype, Value))):
                    mask = cls._from_abstract_datatype_or_value_class(arg)
                    if mask is not None:
                        return mask
                return cls._from_datatype(Datatype.check(
                    arg, function or cls.check, name, position))

        @classmethod
        def _from_abstract_datatype_or_value_class(
                cls,
                arg: type[Datatype] | type[Value],
                _cache: dict[
                    type[Datatype] | type[Value], Filter.DatatypeMask] = {}
        ) -> Filter.DatatypeMask | None:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[Datatype] = cls.ALL
                _cache[Value] = cls.VALUE
                _cache[Entity] = cls.ENTITY
                _cache[DataValue] = cls.DATA_VALUE
                _cache[ShallowDataValue] = cls.SHALLOW_DATA_VALUE
                _cache[DeepDataValue] = cls.DEEP_DATA_VALUE
            return _cache.get(arg)

        @classmethod
        def _from_datatype(
                cls,
                datatype: Datatype,
                _cache: dict[Datatype, Filter.DatatypeMask] = {}
        ) -> Filter.DatatypeMask:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[ItemDatatype()] = cls.ITEM
                _cache[PropertyDatatype()] = cls.PROPERTY
                _cache[LexemeDatatype()] = cls.LEXEME
                _cache[IRI_Datatype()] = cls.IRI
                _cache[TextDatatype()] = cls.TEXT
                _cache[StringDatatype()] = cls.STRING
                _cache[ExternalIdDatatype()] = cls.EXTERNAL_ID
                _cache[QuantityDatatype()] = cls.QUANTITY
                _cache[TimeDatatype()] = cls.TIME
            return _cache[datatype]

        def _to_datatype(
                self,
                _cache: dict[Filter.DatatypeMask, Datatype] = {}
        ) -> Datatype | None:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[Filter.ITEM] = ItemDatatype()
                _cache[Filter.PROPERTY] = PropertyDatatype()
                _cache[Filter.LEXEME] = LexemeDatatype()
                _cache[Filter.IRI] = IRI_Datatype()
                _cache[Filter.TEXT] = TextDatatype()
                _cache[Filter.STRING] = StringDatatype()
                _cache[Filter.EXTERNAL_ID] = ExternalIdDatatype()
                _cache[Filter.QUANTITY] = QuantityDatatype()
                _cache[Filter.TIME] = TimeDatatype()
            return _cache.get(self)

        def _to_value_class(
                self,
                _cache: dict[Filter.DatatypeMask, Any] = {}
        ) -> type[Value]:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[Filter.VALUE] = Value
                _cache[Filter.ENTITY] = Entity
                _cache[Filter.ITEM] = Item
                _cache[Filter.PROPERTY] = Property
                _cache[Filter.LEXEME] = Lexeme
                _cache[Filter.DATA_VALUE] = DataValue
                _cache[Filter.SHALLOW_DATA_VALUE] = ShallowDataValue
                _cache[Filter.IRI] = IRI
                _cache[Filter.TEXT] = Text
                _cache[Filter.STRING] = String
                _cache[Filter.EXTERNAL_ID] = ExternalId
                _cache[Filter.DEEP_DATA_VALUE] = ShallowDataValue
                _cache[Filter.QUANTITY] = Quantity
                _cache[Filter.TIME] = Time
            return cast(type[Value], _cache[self])

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

    class SnakMask(Flags):
        """Mask for concrete snak classes."""

        #: Mask for :class:`ValueSnak`.
        VALUE_SNAK = Flags.auto()

        #: Mask for :class:`SomeValueSnak`.
        SOME_VALUE_SNAK = Flags.auto()

        #: Mask for :class:`NoValueSnak`.
        NO_VALUE_SNAK = Flags.auto()

        #: Mask for all snak classes.
        ALL = (VALUE_SNAK | SOME_VALUE_SNAK | NO_VALUE_SNAK)

        @classmethod
        @override
        def check(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> Filter.SnakMask:
            if isinstance(arg, (cls, int)):
                return super().check(arg, function, name, position)
            elif isinstance(arg, type) and issubclass(arg, Snak):
                return cls._from_snak_class(arg)
            else:
                return cls._from_snak(Snak.check(
                    arg, function or cls.check, name, position))

        @classmethod
        def _from_snak_class(
                cls,
                snak_class: type[Snak],
                _cache: dict[type[Snak], Filter.SnakMask] = {}
        ) -> Filter.SnakMask:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[Snak] = Filter.SnakMask.ALL  # type: ignore
                _cache[ValueSnak] = cls.VALUE_SNAK
                _cache[SomeValueSnak] = cls.SOME_VALUE_SNAK
                _cache[NoValueSnak] = cls.NO_VALUE_SNAK
            return _cache[snak_class]

        @classmethod
        def _from_snak(cls, snak: Snak) -> Filter.SnakMask:
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
            subject: TFingerprint | None = None,
            snak: Snak | None = None
    ) -> Filter:
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
    def from_statement(cls, stmt: Statement) -> Filter:
        """Creates filter from statement.

        Parameters:
           stmt: Statement.

        Returns:
           Filter.
        """
        return cls.from_snak(stmt.subject, stmt.snak)

    def __init__(
            self,
            subject: TFingerprint | None = None,
            property: TFingerprint | None = None,
            value: TFingerprint | None = None,
            snak_mask: TSnakMask | None = None,
            subject_mask: TDatatypeMask | None = None,
            property_mask: TDatatypeMask | None = None,
            value_mask: TDatatypeMask | None = None,
            language: str | None = None
    ) -> None:
        super().__init__(
            subject, property, value, snak_mask,
            subject_mask, property_mask, value_mask, language)

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
        elif i == 8:
            arg = String.check_optional(
                arg, None, type(self), None, i)
            return arg.content if arg is not None else arg
        else:
            raise self._should_not_get_here()

    @override
    def _set_args(self, args: tuple[Any, ...]) -> None:
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

    @at_property
    def language(self) -> str | None:
        """The language tag of filter."""
        return self.get_language()

    def get_language(self) -> str | None:
        """Gets the language tag of filter.

        Returns:
           Language tag or ``None``.
        """
        return self.args[7]

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

    def combine(self, *others: Filter) -> Filter:
        """Combines filter with `others`.

        Parameters:
           others: Filters.

        Returns:
           Filter.
        """
        return functools.reduce(self._combine, others, self)

    @classmethod
    def _combine(cls, f1: Filter, f2: Filter) -> Filter:
        f2 = Filter.check(f2, cls.combine)
        if f1.language is None:
            language: Optional[str] = f2.language
        elif f2.language is None:
            language = f1.language
        elif f1.language != f2.language:
            language = None
        else:
            language = f1.language
        return f1.__class__(
            f1.subject & f2.subject,
            f1.property & f2.property,
            f1.value & f2.value,
            f1.snak_mask & f2.snak_mask,
            f1.subject_mask & f2.subject_mask,
            f1.property_mask & f2.property_mask,
            f1.value_mask & f2.value_mask,
            language
        ).normalize()

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
        if not self.subject.match(stmt.subject):
            return False        # subject mismatch
        if not self.property.match(stmt.snak.property):
            return False        # property mismatch
        if isinstance(stmt.snak, ValueSnak):
            if self.value.is_empty():
                return False    # snak mismatch
            if not self.value.match(stmt.snak.value):
                return False    # value mismatch
        else:
            if not self.value.is_empty() and not self.value.is_full():
                return False    # snak mismatch
        return True

    def normalize(self) -> Filter:
        """Reduce filter to a normal form.

        Normalizes the fingerprint expressions in filter.

        Returns:
           Filter.
        """
        subject = self.subject._normalize(Filter.ENTITY)
        subject_mask = self.subject_mask & subject.datatype_mask
        property = self.property._normalize(Filter.PROPERTY)
        property_mask = self.property_mask & property.datatype_mask
        value = self.value._normalize(
            self.value_mask & property.range_datatype_mask)
        value_mask = self.value_mask & value.datatype_mask
        snak_mask = self.snak_mask
        if property_mask.value == 0:
            snak_mask = self.SnakMask(0)
        if not value.is_full() and not value.is_empty():
            snak_mask &= self.VALUE_SNAK
        elif value.is_empty():
            snak_mask &= ~self.VALUE_SNAK
        return Filter(
            subject, property, value, snak_mask,
            subject_mask, property_mask, value_mask, self.language)

    def _unpack_legacy(
            self
    ) -> tuple[
        Value | SnakSet | None,
        Value | SnakSet | None,
        Value | SnakSet | None,
        Filter.SnakMask
    ]:
        filter = self.normalize()
        assert isinstance(filter.subject, Fingerprint)
        assert isinstance(filter.property, Fingerprint)
        assert isinstance(filter.value, Fingerprint)
        subject: Value | SnakSet | None
        property: Value | SnakSet | None
        value: Value | SnakSet | None
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
