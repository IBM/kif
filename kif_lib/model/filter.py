# Copyright (C) 2023-2025 IBM Corp.
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
    Self,
    TypeAlias,
    Union,
)
from .fingerprint import Fingerprint, TFingerprint
from .flags import Flags
from .kif_object import KIF_Object
from .rank import DeprecatedRank, NormalRank, PreferredRank, Rank, TRank
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
    TTextLanguage,
    Value,
)

at_property = property


class Filter(KIF_Object):
    """Criterion for matching statements.

    A statement matches a filter if:

    * Its subject matches the filter `subject`.
    * Its property matches the filter `property`.
    * Its value (if any) matches the filter `value`.
    * Its snak type matches the filter `snak_mask`.
    * Its subject type matches the filter `subject_mask`.
    * Its property type matches the filter `property_mask`
    * Its value type (if any) matches the filter `value_mask`.
    * Its rank (if any) matches the filter `rank_mask`.
    * Its value language (if any) matches the filter `language`.

    Parameters:
       subject: Subject fingerprint.
       property: Property fingerprint.
       value: Value fingerprint.
       snak_mask: Snak mask.
       subject_mask: Datatype mask.
       property_mask: Datatype mask.
       value_mask: Datatype mask.
       rank_mask: Rank mask.
       language: Language.
       annotated: Annotated flag.
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

    #: Type alias of DatatypeMask.
    TDatatypeMask: TypeAlias = Union[DatatypeMask, TDatatype, int]

    class RankMask(Flags):
        """Mask for concrete rank classes."""

        #: Mask for :class:`PreferredRank`.
        PREFERRED = Flags.auto()

        #: Mask for :class:`NormalRank`.
        NORMAL = Flags.auto()

        #: Mask for :class:`DeprecatedRank`.
        DEPRECATED = Flags.auto()

        #: Mask for all rank classes.
        ALL = PREFERRED | NORMAL | DEPRECATED

        @classmethod
        @override
        def check(
                cls,
                arg: Any,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> Filter.RankMask:
            if isinstance(arg, (cls, int)):
                return super().check(arg, function, name, position)
            elif isinstance(arg, type) and issubclass(arg, Rank):
                return cls._from_rank_class(arg)
            else:
                return cls._from_rank(Rank.check(
                    arg, function or cls.check, name, position))

        @classmethod
        def _from_rank_class(
                cls,
                rank_class: type[Rank],
                _cache: dict[type[Rank], Filter.RankMask] = {}
        ) -> Filter.RankMask:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[Rank] = cls.ALL
                _cache[PreferredRank] = cls.PREFERRED
                _cache[NormalRank] = cls.NORMAL
                _cache[DeprecatedRank] = cls.DEPRECATED
            return _cache[rank_class]

        @classmethod
        def _from_rank(
                cls,
                rank: Rank,
                _cache: dict[Rank, Filter.RankMask] = {}
        ) -> Filter.RankMask:
            ###
            # IMPORTANT: functools.cache doesn't work with classmethods of
            # enum.Flags subclasses.
            ###
            if not _cache:
                _cache[PreferredRank()] = cls.PREFERRED
                _cache[NormalRank()] = cls.NORMAL
                _cache[DeprecatedRank()] = cls.DEPRECATED
            return _cache[rank]

        def match(self, rank: TRank) -> bool:
            """Tests whether rank mask matches `rank`.

            Parameters:
               rank: Rank.

            Returns:
               ``True`` if successful; ``False`` otherwise.
            """
            return bool(self & self.check(rank))

    #: Mask for :class:`PreferredRank`.
    PREFERRED: Final[RankMask] = RankMask.PREFERRED

    #: Mask for :class:`NormalRank`.
    NORMAL: Final[RankMask] = RankMask.NORMAL

    #: Mask for :class:`DeprecatedRank`.
    DEPRECATED: Final[RankMask] = RankMask.DEPRECATED

    #: Type alias of RankMask.
    TRankMask: TypeAlias = Union[RankMask, TRank, int]

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

    #: Type alias of SnakMask.
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
            rank_mask: TRankMask | None = None,
            language: TTextLanguage | None = None,
            annotated: bool | None = None
    ) -> None:
        super().__init__(
            subject, property, value, snak_mask,
            subject_mask, property_mask, value_mask,
            rank_mask, language, annotated)

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
        elif i == 8:            # rank mask
            return self.RankMask.check_optional(
                arg, self.RankMask.ALL, type(self), None, i)
        elif i == 9:            # language
            arg = String.check_optional(
                arg, None, type(self), None, i)
            return arg.content if arg is not None else arg
        elif i == 10:           # annotated
            return bool(arg)
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
    def rank_mask(self) -> RankMask:
        """The rank mask of filter."""
        return self.get_rank_mask()

    def get_rank_mask(self) -> RankMask:
        """Gets the rank mask of filter.

        Returns:
           Rank mask.
        """
        return self.args[7]

    @at_property
    def language(self) -> str | None:
        """The language of filter."""
        return self.get_language()

    def get_language(self) -> str | None:
        """Gets the language of filter.

        Returns:
           Language or ``None``.
        """
        return self.args[8]

    @at_property
    def annotated(self) -> bool:
        """The annotated flag of filter."""
        return self.get_annotated()

    def get_annotated(self) -> bool:
        """Gets the annotated flag of filter.

        This flag determines whether to fetch statement annotations.

        Returns:
           Annotated flag.
        """
        return self.args[9]

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

    def unannotated(self) -> Self:
        """Gets the unannotated version of filter.

        Returns:
           Filter.
        """
        if self.annotated is False:
            return self
        else:
            return cast(Self, self.replace(
                self.KEEP,      # subject
                self.KEEP,      # property
                self.KEEP,      # value
                self.KEEP,      # snak_mask
                self.KEEP,      # subject_mask
                self.KEEP,      # property_mask
                self.KEEP,      # value_mask
                self.KEEP,      # rank_mask
                self.KEEP,      # language
                False))         # annotated

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
        return type(f1)(
            f1.subject & f2.subject,
            f1.property & f2.property,
            f1.value & f2.value,
            f1.snak_mask & f2.snak_mask,
            f1.subject_mask & f2.subject_mask,
            f1.property_mask & f2.property_mask,
            f1.value_mask & f2.value_mask,
            f1.rank_mask & f2.rank_mask,
            language,
            f1.annotated or f2.annotated
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
        """Reduces filter to a normal form.

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
            subject_mask, property_mask, value_mask,
            self.rank_mask, self.language, self.annotated)
