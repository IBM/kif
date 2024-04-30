# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from ..typing import Any, Callable, Iterator, NoReturn, Optional, Union
from . import object
from .annotation_record import AnnotationRecord
from .annotation_record_set import AnnotationRecordSet, TAnnotationRecordSet
from .descriptor import (
    Descriptor,
    ItemDescriptor,
    LexemeDescriptor,
    PlainDescriptor,
    PropertyDescriptor,
)
from .fingerprint import (
    EntityFingerprint,
    Fingerprint,
    PropertyFingerprint,
    TEntityFingerprint,
    TFingerprint,
    TPropertyFingerprint,
)
from .kif_object_set import KIF_ObjectSet, T_KIF_ObjectSet
from .pattern import Pattern, Template, Variable
from .pattern_deprecated import FilterPattern
from .rank import DeprecatedRank, NormalRank, PreferredRank, Rank
from .reference_record import ReferenceRecord
from .reference_record_set import ReferenceRecordSet, TReferenceRecordSet
from .snak import (
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    Snak,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
)
from .snak_set import SnakSet, TSnakSet
from .statement import Statement, StatementTemplate, StatementVariable
from .value import (
    Datatype,
    DataValue,
    DataValueTemplate,
    DataValueVariable,
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeDatatype,
    LexemeTemplate,
    LexemeVariable,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    T_IRI,
    TDatatype,
    Text,
    TextDatatype,
    TExternalId,
    TextTemplate,
    TextVariable,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    TString,
    TText,
    Value,
    ValueTemplate,
    ValueVariable,
)
from .value_set import TextSet, TTextSet, TValueSet, ValueSet

Datetime = datetime.datetime
Decimal = decimal.Decimal
UTC = datetime.timezone.utc

Codec = object.Codec
CodecError = object.CodecError
Decoder = object.Decoder
DecoderError = object.DecoderError
Encoder = object.Encoder
EncoderError = object.EncoderError
Error = object.Error
MustBeImplementedInSubclass = object.MustBeImplementedInSubclass
Nil = object.Nil
Object = object.Object
ShouldNotGetHere = object.ShouldNotGetHere
TArgs = object.TArgs
TCallable = object.TFun
TDatetime = Union[Datetime, str]
TDecimal = Union[Decimal, float, int, str]
TNil = object.TNil


class KIF_Object(object.Object, metaclass=object.ObjectMeta):

    @classmethod
    def _issubclass_template(cls, arg: Any) -> bool:
        ...

    @classmethod
    def _isinstance_template_or_variable(cls, arg: Any) -> bool:
        ...

# -- kif_object_class ------------------------------------------------------

    @classmethod
    def _check_arg_kif_object_class(
            cls,
            arg: type['KIF_Object'],
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[type['KIF_Object'], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_kif_object_class(
            cls,
            arg: Optional[type['KIF_Object']],
            default: Optional[type['KIF_Object']] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[type['KIF_Object']], NoReturn]:
        ...

    @classmethod
    def _preprocess_arg_kif_object_class(
            cls,
            arg: type['KIF_Object'],
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[type['KIF_Object'], NoReturn]:
        ...

    @classmethod
    def _preprocess_optional_arg_kif_object_class(
            cls,
            arg: Optional[type['KIF_Object']],
            i: int,
            default: Optional[type['KIF_Object']] = ...,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[Optional[type['KIF_Object']], NoReturn]:
        ...

# -- datetime --------------------------------------------------------------

    @classmethod
    def _check_arg_datetime(
            cls,
            arg: TDatetime,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Datetime, NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_datetime(
            cls,
            arg: Optional[TDatetime],
            default: Optional[Datetime] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Datetime], NoReturn]:
        ...

    @classmethod
    def _preprocess_arg_datetime(
            cls,
            arg: TDatetime,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[Datetime, NoReturn]:
        ...

    @classmethod
    def _preprocess_optional_arg_datetime(
            cls,
            arg: Optional[TDatetime],
            i: int,
            default: Optional[Datetime] = ...,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[Optional[Datetime], NoReturn]:
        ...

# -- decimal ---------------------------------------------------------------

    @classmethod
    def _check_arg_decimal(
            cls,
            arg: TDecimal,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Decimal, NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_decimal(
            cls,
            arg: Optional[TDecimal],
            default: Optional[Decimal] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Decimal], NoReturn]:
        ...

    @classmethod
    def _preprocess_arg_decimal(
            cls,
            arg: TDecimal,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[Decimal, NoReturn]:
        ...

    @classmethod
    def _preprocess_optional_arg_decimal(
            cls,
            arg: Optional[TDecimal],
            i: int,
            default: Optional[Decimal] = ...,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Union[Optional[Decimal], NoReturn]:
        ...

# -- _check_arg_ -----------------------------------------------------------

    @classmethod
    def _check_arg_annotation_record(
            cls,
            arg: AnnotationRecord,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[AnnotationRecord, NoReturn]:
        ...

    @classmethod
    def _check_arg_annotation_record_set(
            cls,
            arg: TAnnotationRecordSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[AnnotationRecordSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_data_value(
            cls,
            arg: DataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DataValue, NoReturn]:
        ...

    @classmethod
    def _check_arg_data_value_template(
            cls,
            arg: DataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DataValueTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_data_value_variable(
            cls,
            arg: DataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DataValueVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Datatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_deep_data_value(
            cls,
            arg: DeepDataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DeepDataValue, NoReturn]:
        ...

    @classmethod
    def _check_arg_deep_data_value_template(
            cls,
            arg: DeepDataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DeepDataValueTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_deep_data_value_variable(
            cls,
            arg: DeepDataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DeepDataValueVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_deprecated_rank(
            cls,
            arg: DeprecatedRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[DeprecatedRank, NoReturn]:
        ...

    @classmethod
    def _check_arg_descriptor(
            cls,
            arg: Descriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Descriptor, NoReturn]:
        ...

    @classmethod
    def _check_arg_entity(
            cls,
            arg: Entity,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Entity, NoReturn]:
        ...

    @classmethod
    def _check_arg_entity_template(
            cls,
            arg: EntityTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[EntityTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_entity_variable(
            cls,
            arg: EntityVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[EntityVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_entity_fingerprint(
            cls,
            arg: EntityFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[EntityFingerprint, NoReturn]:
        ...

    @classmethod
    def _check_arg_external_id(
            cls,
            arg: TExternalId,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ExternalId, NoReturn]:
        ...

    @classmethod
    def _check_arg_external_id_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ExternalIdDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_external_id_template(
            cls,
            arg: ExternalIdTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ExternalIdTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_external_id_variable(
            cls,
            arg: ExternalIdVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ExternalIdVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_filter_pattern(
            cls,
            arg: FilterPattern,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[FilterPattern, NoReturn]:
        ...

    @classmethod
    def _check_arg_fingerprint(
            cls,
            arg: TFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Fingerprint, NoReturn]:
        ...

    @classmethod
    def _check_arg_iri(
            cls,
            arg: T_IRI,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[IRI, NoReturn]:
        ...

    @classmethod
    def _check_arg_iri_template(
            cls,
            arg: IRI_Template,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[IRI_Template, NoReturn]:
        ...

    @classmethod
    def _check_arg_iri_variable(
            cls,
            arg: IRI_Variable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[IRI_Variable, NoReturn]:
        ...

    @classmethod
    def _check_arg_iri_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[IRI_Datatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_item(
            cls,
            arg: Item,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Item, NoReturn]:
        ...

    @classmethod
    def _check_arg_item_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ItemDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_item_descriptor(
            cls,
            arg: ItemDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ItemDescriptor, NoReturn]:
        ...

    @classmethod
    def _check_arg_item_template(
            cls,
            arg: ItemTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ItemTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_item_variable(
            cls,
            arg: ItemVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ItemTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_kif_object(
            cls,
            arg: 'KIF_Object',
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union['KIF_Object', NoReturn]:
        ...

    @classmethod
    def _check_arg_kif_object_set(
            cls,
            arg: T_KIF_ObjectSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[KIF_ObjectSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_lexeme(
            cls,
            arg: Lexeme,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Lexeme, NoReturn]:
        ...

    @classmethod
    def _check_arg_lexeme_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[LexemeDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_lexeme_descriptor(
            cls,
            arg: LexemeDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[LexemeDescriptor, NoReturn]:
        ...

    @classmethod
    def _check_arg_lexeme_template(
            cls,
            arg: LexemeTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[LexemeTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_lexeme_variable(
            cls,
            arg: LexemeVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[LexemeVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_no_value_snak(
            cls,
            arg: NoValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[NoValueSnak, NoReturn]:
        ...

    @classmethod
    def _check_arg_no_value_snak_template(
            cls,
            arg: NoValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[NoValueSnakTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_no_value_snak_variable(
            cls,
            arg: NoValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[NoValueSnakVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_normal_rank(
            cls,
            arg: NormalRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[NormalRank, NoReturn]:
        ...

    @classmethod
    def _check_arg_object(
            cls,
            arg: Object,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Object, NoReturn]:
        ...

    @classmethod
    def _check_arg_pattern(
            cls,
            arg: Pattern,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Pattern, NoReturn]:
        ...

    @classmethod
    def _check_arg_plain_descriptor(
            cls,
            arg: PlainDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PlainDescriptor, NoReturn]:
        ...

    @classmethod
    def _check_arg_preferred_rank(
            cls,
            arg: PreferredRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PreferredRank, NoReturn]:
        ...

    @classmethod
    def _check_arg_property(
            cls,
            arg: Property,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Property, NoReturn]:
        ...

    @classmethod
    def _check_arg_property_template(
            cls,
            arg: PropertyTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PropertyTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_property_variable(
            cls,
            arg: PropertyVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PropertyVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_property_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PropertyDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_property_descriptor(
            cls,
            arg: PropertyDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PropertyDescriptor, NoReturn]:
        ...

    @classmethod
    def _check_arg_property_fingerprint(
            cls,
            arg: TPropertyFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[PropertyFingerprint, NoReturn]:
        ...

    @classmethod
    def _check_arg_quantity(
            cls,
            arg: Quantity,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Quantity, NoReturn]:
        ...

    @classmethod
    def _check_arg_quantity_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[QuantityDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_quantity_template(
            cls,
            arg: QuantityTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[QuantityTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_quantity_variable(
            cls,
            arg: QuantityVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[QuantityVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_rank(
            cls,
            arg: Rank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Rank, NoReturn]:
        ...

    @classmethod
    def _check_arg_reference_record(
            cls,
            arg: ReferenceRecord,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ReferenceRecord, NoReturn]:
        ...

    @classmethod
    def _check_arg_reference_record_set(
            cls,
            arg: TReferenceRecordSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ReferenceRecordSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_shallow_data_value(
            cls,
            arg: ShallowDataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ShallowDataValue, NoReturn]:
        ...

    @classmethod
    def _check_arg_shallow_data_value_template(
            cls,
            arg: ShallowDataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ShallowDataValueTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_shallow_data_value_variable(
            cls,
            arg: ShallowDataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ShallowDataValueVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_snak(
            cls,
            arg: Snak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Snak, NoReturn]:
        ...

    @classmethod
    def _check_arg_snak_template(
            cls,
            arg: SnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SnakTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_snak_variable(
            cls,
            arg: SnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SnakVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_snak_set(
            cls,
            arg: TSnakSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SnakSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_some_value_snak(
            cls,
            arg: SomeValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SomeValueSnak, NoReturn]:
        ...

    @classmethod
    def _check_arg_some_value_snak_template(
            cls,
            arg: SomeValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SomeValueSnakTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_some_value_snak_variable(
            cls,
            arg: SomeValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[SomeValueSnakVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_statement(
            cls,
            arg: Statement,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Statement, NoReturn]:
        ...

    @classmethod
    def _check_arg_statement_template(
            cls,
            arg: StatementTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[StatementTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_statement_variable(
            cls,
            arg: StatementVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[StatementVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_string(
            cls,
            arg: TString,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[String, NoReturn]:
        ...

    @classmethod
    def _check_arg_string_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[StringDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_string_template(
            cls,
            arg: StringTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[StringTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_string_variable(
            cls,
            arg: StringVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[StringVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_template(
            cls,
            arg: Template,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Template, NoReturn]:
        ...

    @classmethod
    def _check_arg_text(
            cls,
            arg: TText,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Text, NoReturn]:
        ...

    @classmethod
    def _check_arg_text_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TextDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_text_set(
            cls,
            arg: TTextSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TextSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_text_template(
            cls,
            arg: TextTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TextTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_text_variable(
            cls,
            arg: TextVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TextVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_time(
            cls,
            arg: Time,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Time, NoReturn]:
        ...

    @classmethod
    def _check_arg_time_datatype(
            cls,
            arg: TDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TimeDatatype, NoReturn]:
        ...

    @classmethod
    def _check_arg_time_template(
            cls,
            arg: TimeTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TimeTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_time_variable(
            cls,
            arg: TimeVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[TimeVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_value(
            cls,
            arg: Value,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Value, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_template(
            cls,
            arg: ValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_variable(
            cls,
            arg: ValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_set(
            cls,
            arg: TValueSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueSet, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_snak(
            cls,
            arg: ValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueSnak, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_snak_template(
            cls,
            arg: ValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueSnakTemplate, NoReturn]:
        ...

    @classmethod
    def _check_arg_value_snak_variable(
            cls,
            arg: ValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[ValueSnakVariable, NoReturn]:
        ...

    @classmethod
    def _check_arg_variable(
            cls,
            arg: Variable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Variable, NoReturn]:
        ...

# -- _check_optional_arg_ --------------------------------------------------

    @classmethod
    def _check_optional_arg_annotation_record(
            cls,
            arg: Optional[AnnotationRecord],
            default: Optional[AnnotationRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[AnnotationRecord], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_annotation_record_set(
            cls,
            arg: Optional[TAnnotationRecordSet],
            default: Optional[AnnotationRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[AnnotationRecordSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_data_value(
            cls,
            arg: Optional[DataValue],
            default: Optional[DataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DataValue], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_data_value_template(
            cls,
            arg: Optional[DataValueTemplate],
            default: Optional[DataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DataValueTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_data_value_variable(
            cls,
            arg: Optional[DataValueVariable],
            default: Optional[DataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DataValueVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Datatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value(
            cls,
            arg: Optional[DeepDataValue],
            default: Optional[DeepDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DeepDataValue], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value_template(
            cls,
            arg: Optional[DeepDataValueTemplate],
            default: Optional[DeepDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DeepDataValueTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value_variable(
            cls,
            arg: Optional[DeepDataValueVariable],
            default: Optional[DeepDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DeepDataValueVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_deprecated_rank(
            cls,
            arg: Optional[DeprecatedRank],
            default: Optional[DeprecatedRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[DeprecatedRank], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_descriptor(
            cls,
            arg: Optional[Descriptor],
            default: Optional[Descriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Descriptor], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_entity(
            cls,
            arg: Optional[Entity],
            default: Optional[Entity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Entity], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_entity_template(
            cls,
            arg: Optional[EntityTemplate],
            default: Optional[EntityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[EntityTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_entity_variable(
            cls,
            arg: Optional[EntityVariable],
            default: Optional[EntityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[EntityVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_entity_fingerprint(
            cls,
            arg: Optional[TEntityFingerprint],
            default: Optional[EntityFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[EntityFingerprint], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_external_id(
            cls,
            arg: Optional[TExternalId],
            default: Optional[ExternalId] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ExternalId], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_external_id_template(
            cls,
            arg: Optional[ExternalIdTemplate],
            default: Optional[ExternalIdTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ExternalIdTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_external_id_variable(
            cls,
            arg: Optional[ExternalIdVariable],
            default: Optional[ExternalIdVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ExternalIdVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_external_id_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[ExternalIdDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ExternalIdDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_filter_pattern(
            cls,
            arg: Optional[FilterPattern],
            default: Optional[FilterPattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[FilterPattern], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_fingerprint(
            cls,
            arg: Optional[TFingerprint],
            default: Optional[Fingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Fingerprint], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_iri(
            cls,
            arg: Optional[T_IRI],
            default: Optional[IRI] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[IRI], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_iri_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[IRI_Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[IRI_Datatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_iri_template(
            cls,
            arg: Optional[IRI_Template],
            default: Optional[IRI_Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[IRI_Template], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_iri_variable(
            cls,
            arg: Optional[IRI_Variable],
            default: Optional[IRI_Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[IRI_Variable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_item(
            cls,
            arg: Optional[Item],
            default: Optional[Item] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Item], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_item_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[ItemDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ItemDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_item_descriptor(
            cls,
            arg: Optional[ItemDescriptor],
            default: Optional[ItemDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ItemDescriptor], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_item_template(
            cls,
            arg: Optional[ItemTemplate],
            default: Optional[ItemTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ItemTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_item_variable(
            cls,
            arg: Optional[ItemVariable],
            default: Optional[ItemVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ItemVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_kif_object(
            cls,
            arg: Optional['KIF_Object'],
            default: Optional['KIF_Object'] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional['KIF_Object'], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_kif_object_set(
            cls,
            arg: Optional[T_KIF_ObjectSet],
            default: Optional[KIF_ObjectSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[KIF_ObjectSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_lexeme(
            cls,
            arg: Optional[Lexeme],
            default: Optional[Lexeme] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Lexeme], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[LexemeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[LexemeDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_descriptor(
            cls,
            arg: Optional[LexemeDescriptor],
            default: Optional[LexemeDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[LexemeDescriptor], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_template(
            cls,
            arg: Optional[LexemeTemplate],
            default: Optional[LexemeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[LexemeTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_variable(
            cls,
            arg: Optional[LexemeVariable],
            default: Optional[LexemeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[LexemeVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak(
            cls,
            arg: Optional[NoValueSnak],
            default: Optional[NoValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[NoValueSnak], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak_template(
            cls,
            arg: Optional[NoValueSnakTemplate],
            default: Optional[NoValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[NoValueSnakTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak_variable(
            cls,
            arg: Optional[NoValueSnakVariable],
            default: Optional[NoValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[NoValueSnakVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_normal_rank(
            cls,
            arg: Optional[NormalRank],
            default: Optional[NormalRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[NormalRank], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_object(
            cls,
            arg: Optional[Object],
            default: Optional[Object] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Object], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_pattern(
            cls,
            arg: Optional[Pattern],
            default: Optional[Pattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Pattern], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_plain_descriptor(
            cls,
            arg: Optional[PlainDescriptor],
            default: Optional[PlainDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PlainDescriptor], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_preferred_rank(
            cls,
            arg: Optional[PreferredRank],
            default: Optional[PreferredRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PreferredRank], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property(
            cls,
            arg: Optional[Property],
            default: Optional[Property] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Property], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[PropertyDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PropertyDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property_descriptor(
            cls,
            arg: Optional[PropertyDescriptor],
            default: Optional[PropertyDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PropertyDescriptor], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property_fingerprint(
            cls,
            arg: Optional[TPropertyFingerprint],
            default: Optional[PropertyFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PropertyFingerprint], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property_template(
            cls,
            arg: Optional[PropertyTemplate],
            default: Optional[PropertyTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PropertyTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_property_variable(
            cls,
            arg: Optional[PropertyVariable],
            default: Optional[PropertyVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[PropertyVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_quantity(
            cls,
            arg: Optional[Quantity],
            default: Optional[Quantity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Quantity], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_quantity_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[QuantityDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[QuantityDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_quantity_template(
            cls,
            arg: Optional[QuantityTemplate],
            default: Optional[QuantityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[QuantityTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_quantity_variable(
            cls,
            arg: Optional[QuantityVariable],
            default: Optional[QuantityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[QuantityVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_rank(
            cls,
            arg: Optional[Rank],
            default: Optional[Rank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Rank], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_reference_record(
            cls,
            arg: Optional[ReferenceRecord],
            default: Optional[ReferenceRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ReferenceRecord], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_reference_record_set(
            cls,
            arg: Optional[TReferenceRecordSet],
            default: Optional[ReferenceRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ReferenceRecordSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value(
            cls,
            arg: Optional[ShallowDataValue],
            default: Optional[ShallowDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ShallowDataValue], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value_template(
            cls,
            arg: Optional[ShallowDataValueTemplate],
            default: Optional[ShallowDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ShallowDataValueTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value_variable(
            cls,
            arg: Optional[ShallowDataValueVariable],
            default: Optional[ShallowDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ShallowDataValueVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_snak(
            cls,
            arg: Optional[Snak],
            default: Optional[Snak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Snak], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_snak_template(
            cls,
            arg: Optional[SnakTemplate],
            default: Optional[SnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SnakTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_snak_variable(
            cls,
            arg: Optional[SnakVariable],
            default: Optional[SnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SnakVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_snak_set(
            cls,
            arg: Optional[TSnakSet],
            default: Optional[SnakSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SnakSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak(
            cls,
            arg: Optional[SomeValueSnak],
            default: Optional[SomeValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SomeValueSnak], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak_template(
            cls,
            arg: Optional[SomeValueSnakTemplate],
            default: Optional[SomeValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SomeValueSnakTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak_variable(
            cls,
            arg: Optional[SomeValueSnakVariable],
            default: Optional[SomeValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[SomeValueSnakVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_statement(
            cls,
            arg: Optional[Statement],
            default: Optional[Statement] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Statement], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_statement_template(
            cls,
            arg: Optional[StatementTemplate],
            default: Optional[StatementTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[StatementTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_statement_variable(
            cls,
            arg: Optional[StatementVariable],
            default: Optional[StatementVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[StatementVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_string(
            cls,
            arg: Optional[TString],
            default: Optional[String] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[String], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_string_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[StringDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[StringDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_string_template(
            cls,
            arg: Optional[StringTemplate],
            default: Optional[StringTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[StringTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_string_variable(
            cls,
            arg: Optional[StringVariable],
            default: Optional[StringVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[StringVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_template(
            cls,
            arg: Optional[Template],
            default: Optional[Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Template], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_text(
            cls,
            arg: Optional[TText],
            default: Optional[Text] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Text], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_text_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[TextDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TextDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_text_set(
            cls,
            arg: Optional[TTextSet],
            default: Optional[TextSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TextSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_text_template(
            cls,
            arg: Optional[TextTemplate],
            default: Optional[TextTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TextTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_text_variable(
            cls,
            arg: Optional[TextVariable],
            default: Optional[TextVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TextVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_time(
            cls,
            arg: Optional[Time],
            default: Optional[Time] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Time], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_time_datatype(
            cls,
            arg: Optional[TDatatype],
            default: Optional[TimeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TimeDatatype], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_time_template(
            cls,
            arg: Optional[TimeTemplate],
            default: Optional[TimeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TimeTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_time_variable(
            cls,
            arg: Optional[TimeVariable],
            default: Optional[TimeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[TimeVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value(
            cls,
            arg: Optional[Value],
            default: Optional[Value] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Value], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_set(
            cls,
            arg: Optional[TValueSet],
            default: Optional[ValueSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueSet], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_template(
            cls,
            arg: Optional[ValueTemplate],
            default: Optional[ValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_variable(
            cls,
            arg: Optional[ValueVariable],
            default: Optional[ValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_snak(
            cls,
            arg: Optional[ValueSnak],
            default: Optional[ValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueSnak], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_snak_template(
            cls,
            arg: Optional[ValueSnakTemplate],
            default: Optional[ValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueSnakTemplate], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_value_snak_variable(
            cls,
            arg: Optional[ValueSnakVariable],
            default: Optional[ValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ValueSnakVariable], NoReturn]:
        ...

    @classmethod
    def _check_optional_arg_variable(
            cls,
            arg: Optional[Variable],
            default: Optional[Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[Variable], NoReturn]:
        ...

# -- check_ ----------------------------------------------------------------

    def check_annotation_record(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[AnnotationRecord, NoReturn]:
        ...

    def check_annotation_record_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[AnnotationRecordSet, NoReturn]:
        ...

    def check_deep_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DeepDataValue, NoReturn]:
        ...

    def check_deep_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DeepDataValueTemplate, NoReturn]:
        ...

    def check_deep_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DeepDataValueVariable, NoReturn]:
        ...

    def check_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DataValue, NoReturn]:
        ...

    def check_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DataValueTemplate, NoReturn]:
        ...

    def check_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DataValueVariable, NoReturn]:
        ...

    def check_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Datatype, NoReturn]:
        ...

    def check_deprecated_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DeprecatedRank, NoReturn]:
        ...

    def check_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Descriptor, NoReturn]:
        ...

    def check_entity(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Entity, NoReturn]:
        ...

    def check_entity_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[EntityFingerprint, NoReturn]:
        ...

    def check_entity_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[EntityVariable, NoReturn]:
        ...

    def check_entity_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[EntityTemplate, NoReturn]:
        ...

    def check_external_id(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ExternalId, NoReturn]:
        ...

    def check_external_id_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ExternalIdDatatype, NoReturn]:
        ...

    def check_external_id_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ExternalIdTemplate, NoReturn]:
        ...

    def check_external_id_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ExternalIdVariable, NoReturn]:
        ...

    def check_filter_pattern(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[FilterPattern, NoReturn]:
        ...

    def check_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Fingerprint, NoReturn]:
        ...

    def check_iri(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[IRI, NoReturn]:
        ...

    def check_iri_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[IRI_Datatype, NoReturn]:
        ...

    def check_iri_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[IRI_Template, NoReturn]:
        ...

    def check_iri_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[IRI_Variable, NoReturn]:
        ...

    def check_item(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Item, NoReturn]:
        ...

    def check_item_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ItemDatatype, NoReturn]:
        ...

    def check_item_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ItemDescriptor, NoReturn]:
        ...

    def check_item_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ItemTemplate, NoReturn]:
        ...

    def check_item_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ItemVariable, NoReturn]:
        ...

    def check_kif_object(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['KIF_Object', NoReturn]:
        ...

    def check_kif_object_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[KIF_ObjectSet, NoReturn]:
        ...

    def check_lexeme(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Lexeme, NoReturn]:
        ...

    def check_lexeme_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[LexemeDatatype, NoReturn]:
        ...

    def check_lexeme_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[LexemeDescriptor, NoReturn]:
        ...

    def check_lexeme_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[LexemeTemplate, NoReturn]:
        ...

    def check_lexeme_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[LexemeVariable, NoReturn]:
        ...

    def check_no_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[NoValueSnak, NoReturn]:
        ...

    def check_no_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[NoValueSnakTemplate, NoReturn]:
        ...

    def check_no_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[NoValueSnakVariable, NoReturn]:
        ...

    def check_normal_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[NormalRank, NoReturn]:
        ...

    def check_object(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Object, NoReturn]:
        ...

    def check_pattern(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Pattern, NoReturn]:
        ...

    def check_plain_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PlainDescriptor, NoReturn]:
        ...

    def check_preferred_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PreferredRank, NoReturn]:
        ...

    def check_property(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Property, NoReturn]:
        ...

    def check_property_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PropertyDatatype, NoReturn]:
        ...

    def check_property_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PropertyDescriptor, NoReturn]:
        ...

    def check_property_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PropertyFingerprint, NoReturn]:
        ...

    def check_property_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PropertyTemplate, NoReturn]:
        ...

    def check_property_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[PropertyVariable, NoReturn]:
        ...

    def check_quantity(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Quantity, NoReturn]:
        ...

    def check_quantity_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[QuantityDatatype, NoReturn]:
        ...

    def check_quantity_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[QuantityTemplate, NoReturn]:
        ...

    def check_quantity_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[QuantityVariable, NoReturn]:
        ...

    def check_shallow_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ShallowDataValue, NoReturn]:
        ...

    def check_shallow_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ShallowDataValueTemplate, NoReturn]:
        ...

    def check_shallow_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ShallowDataValueVariable, NoReturn]:
        ...

    def check_some_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SomeValueSnak, NoReturn]:
        ...

    def check_some_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SomeValueSnakTemplate, NoReturn]:
        ...

    def check_some_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SomeValueSnakVariable, NoReturn]:
        ...

    def check_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Snak, NoReturn]:
        ...

    def check_snak_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SnakSet, NoReturn]:
        ...

    def check_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SnakTemplate, NoReturn]:
        ...

    def check_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SnakVariable, NoReturn]:
        ...

    def check_statement(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Statement, NoReturn]:
        ...

    def check_statement_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[StatementTemplate, NoReturn]:
        ...

    def check_statement_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[StatementVariable, NoReturn]:
        ...

    def check_string(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[String, NoReturn]:
        ...

    def check_string_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[StringDatatype, NoReturn]:
        ...

    def check_string_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[StringTemplate, NoReturn]:
        ...

    def check_string_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[StringVariable, NoReturn]:
        ...

    def check_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Template, NoReturn]:
        ...

    def check_text(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Text, NoReturn]:
        ...

    def check_text_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TextDatatype, NoReturn]:
        ...

    def check_text_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TextSet, NoReturn]:
        ...

    def check_text_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TextTemplate, NoReturn]:
        ...

    def check_text_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TextVariable, NoReturn]:
        ...

    def check_time(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Time, NoReturn]:
        ...

    def check_time_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TimeDatatype, NoReturn]:
        ...

    def check_time_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TimeTemplate, NoReturn]:
        ...

    def check_time_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[TimeVariable, NoReturn]:
        ...

    def check_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Rank, NoReturn]:
        ...

    def check_reference_record(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ReferenceRecord, NoReturn]:
        ...

    def check_reference_record_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ReferenceRecordSet, NoReturn]:
        ...

    def check_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Value, NoReturn]:
        ...

    def check_value_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueSet, NoReturn]:
        ...

    def check_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueSnak, NoReturn]:
        ...

    def check_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueSnakTemplate, NoReturn]:
        ...

    def check_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueSnakVariable, NoReturn]:
        ...

    def check_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueTemplate, NoReturn]:
        ...

    def check_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ValueVariable, NoReturn]:
        ...

    def check_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Variable, NoReturn]:
        ...

# -- from_ -----------------------------------------------------------------

    @classmethod
    def from_json(
        cls,
        s: str,
        **kwargs: Any
    ) -> Union['KIF_Object', NoReturn]:
        ...

    @classmethod
    def from_repr(
        cls,
        s: str,
        **kwargs: Any
    ) -> Union['KIF_Object', NoReturn]:
        ...

    @classmethod
    def from_sexp(
        cls,
        s: str,
        **kwargs: Any
    ) -> Union['KIF_Object', NoReturn]:
        ...

    @classmethod
    def from_sparql(
        cls,
        s: str,
        **kwargs: Any
    ) -> Union['KIF_Object', NoReturn]:
        ...

# -- is_ -------------------------------------------------------------------

    def is_annotation_record(self) -> bool: ...
    def is_annotation_record_set(self) -> bool: ...
    def is_data_value(self) -> bool: ...
    def is_data_value_template(self) -> bool: ...
    def is_data_value_variable(self) -> bool: ...
    def is_datatype(self) -> bool: ...
    def is_deep_data_value(self) -> bool: ...
    def is_deep_data_value_template(self) -> bool: ...
    def is_deep_data_value_variable(self) -> bool: ...
    def is_deprecated_rank(self) -> bool: ...
    def is_descriptor(self) -> bool: ...
    def is_entity(self) -> bool: ...
    def is_entity_fingerprint(self) -> bool: ...
    def is_entity_template(self) -> bool: ...
    def is_entity_variable(self) -> bool: ...
    def is_external_id(self) -> bool: ...
    def is_external_id_datatype(self) -> bool: ...
    def is_external_id_template(self) -> bool: ...
    def is_external_id_variable(self) -> bool: ...
    def is_filter_pattern(self) -> bool: ...
    def is_fingerprint(self) -> bool: ...
    def is_iri(self) -> bool: ...
    def is_iri_datatype(self) -> bool: ...
    def is_iri_template(self) -> bool: ...
    def is_iri_variable(self) -> bool: ...
    def is_item(self) -> bool: ...
    def is_item_datatype(self) -> bool: ...
    def is_item_descriptor(self) -> bool: ...
    def is_item_template(self) -> bool: ...
    def is_item_variable(self) -> bool: ...
    def is_kif_object(self) -> bool: ...
    def is_kif_object_set(self) -> bool: ...
    def is_lexeme(self) -> bool: ...
    def is_lexeme_datatype(self) -> bool: ...
    def is_lexeme_descriptor(self) -> bool: ...
    def is_lexeme_template(self) -> bool: ...
    def is_lexeme_variable(self) -> bool: ...
    def is_no_value_snak(self) -> bool: ...
    def is_no_value_snak_template(self) -> bool: ...
    def is_no_value_snak_variable(self) -> bool: ...
    def is_normal_rank(self) -> bool: ...
    def is_object(self) -> bool: ...
    def is_pattern(self) -> bool: ...
    def is_plain_descriptor(self) -> bool: ...
    def is_preferred_rank(self) -> bool: ...
    def is_property(self) -> bool: ...
    def is_property_datatype(self) -> bool: ...
    def is_property_descriptor(self) -> bool: ...
    def is_property_fingerprint(self) -> bool: ...
    def is_property_template(self) -> bool: ...
    def is_property_variable(self) -> bool: ...
    def is_quantity(self) -> bool: ...
    def is_quantity_datatype(self) -> bool: ...
    def is_quantity_template(self) -> bool: ...
    def is_quantity_variable(self) -> bool: ...
    def is_rank(self) -> bool: ...
    def is_reference_record(self) -> bool: ...
    def is_reference_record_set(self) -> bool: ...
    def is_shallow_data_value(self) -> bool: ...
    def is_shallow_data_value_template(self) -> bool: ...
    def is_shallow_data_value_variable(self) -> bool: ...
    def is_snak(self) -> bool: ...
    def is_snak_set(self) -> bool: ...
    def is_snak_template(self) -> bool: ...
    def is_snak_variable(self) -> bool: ...
    def is_some_value_snak(self) -> bool: ...
    def is_some_value_snak_template(self) -> bool: ...
    def is_some_value_snak_variable(self) -> bool: ...
    def is_statement(self) -> bool: ...
    def is_statement_template(self) -> bool: ...
    def is_statement_variable(self) -> bool: ...
    def is_string(self) -> bool: ...
    def is_string_datatype(self) -> bool: ...
    def is_string_template(self) -> bool: ...
    def is_string_variable(self) -> bool: ...
    def is_template(self) -> bool: ...
    def is_text(self) -> bool: ...
    def is_text_datatype(self) -> bool: ...
    def is_text_set(self) -> bool: ...
    def is_text_template(self) -> bool: ...
    def is_text_variable(self) -> bool: ...
    def is_time(self) -> bool: ...
    def is_time_datatype(self) -> bool: ...
    def is_time_template(self) -> bool: ...
    def is_time_variable(self) -> bool: ...
    def is_value(self) -> bool: ...
    def is_value_set(self) -> bool: ...
    def is_value_snak(self) -> bool: ...
    def is_value_snak_template(self) -> bool: ...
    def is_value_snak_variable(self) -> bool: ...
    def is_value_template(self) -> bool: ...
    def is_value_variable(self) -> bool: ...
    def is_variable(self) -> bool: ...

# -- test_ -----------------------------------------------------------------

    def test_annotation_record(self) -> bool: ...
    def test_annotation_record_set(self) -> bool: ...
    def test_data_value(self) -> bool: ...
    def test_data_value_template(self) -> bool: ...
    def test_data_value_variable(self) -> bool: ...
    def test_datatype(self) -> bool: ...
    def test_deep_data_value(self) -> bool: ...
    def test_deep_data_value_template(self) -> bool: ...
    def test_deep_data_value_variable(self) -> bool: ...
    def test_deprecated_rank(self) -> bool: ...
    def test_descriptor(self) -> bool: ...
    def test_entity(self) -> bool: ...
    def test_entity_fingerprint(self) -> bool: ...
    def test_entity_template(self) -> bool: ...
    def test_entity_variable(self) -> bool: ...
    def test_external_id(self) -> bool: ...
    def test_external_id_datatype(self) -> bool: ...
    def test_external_id_template(self) -> bool: ...
    def test_external_id_variable(self) -> bool: ...
    def test_filter_pattern(self) -> bool: ...
    def test_fingerprint(self) -> bool: ...
    def test_iri(self) -> bool: ...
    def test_iri_datatype(self) -> bool: ...
    def test_iri_template(self) -> bool: ...
    def test_iri_variable(self) -> bool: ...
    def test_item(self) -> bool: ...
    def test_item_datatype(self) -> bool: ...
    def test_item_descriptor(self) -> bool: ...
    def test_item_template(self) -> bool: ...
    def test_item_variable(self) -> bool: ...
    def test_kif_object(self) -> bool: ...
    def test_kif_object_set(self) -> bool: ...
    def test_lexeme(self) -> bool: ...
    def test_lexeme_datatype(self) -> bool: ...
    def test_lexeme_descriptor(self) -> bool: ...
    def test_lexeme_template(self) -> bool: ...
    def test_lexeme_variable(self) -> bool: ...
    def test_no_value_snak(self) -> bool: ...
    def test_no_value_snak_template(self) -> bool: ...
    def test_no_value_snak_variable(self) -> bool: ...
    def test_normal_rank(self) -> bool: ...
    def test_object(self) -> bool: ...
    def test_pattern(self) -> bool: ...
    def test_plain_descriptor(self) -> bool: ...
    def test_preferred_rank(self) -> bool: ...
    def test_property(self) -> bool: ...
    def test_property_datatype(self) -> bool: ...
    def test_property_descriptor(self) -> bool: ...
    def test_property_fingerprint(self) -> bool: ...
    def test_property_template(self) -> bool: ...
    def test_property_variable(self) -> bool: ...
    def test_quantity(self) -> bool: ...
    def test_quantity_datatype(self) -> bool: ...
    def test_quantity_template(self) -> bool: ...
    def test_quantity_variable(self) -> bool: ...
    def test_rank(self) -> bool: ...
    def test_reference_record(self) -> bool: ...
    def test_reference_record_set(self) -> bool: ...
    def test_shallow_data_value(self) -> bool: ...
    def test_shallow_data_value_template(self) -> bool: ...
    def test_shallow_data_value_variable(self) -> bool: ...
    def test_snak(self) -> bool: ...
    def test_snak_set(self) -> bool: ...
    def test_snak_template(self) -> bool: ...
    def test_snak_variable(self) -> bool: ...
    def test_some_value_snak(self) -> bool: ...
    def test_some_value_snak_template(self) -> bool: ...
    def test_some_value_snak_variable(self) -> bool: ...
    def test_statement(self) -> bool: ...
    def test_statement_template(self) -> bool: ...
    def test_statement_variable(self) -> bool: ...
    def test_string(self) -> bool: ...
    def test_string_datatype(self) -> bool: ...
    def test_string_template(self) -> bool: ...
    def test_string_variable(self) -> bool: ...
    def test_template(self) -> bool: ...
    def test_text(self) -> bool: ...
    def test_text_datatype(self) -> bool: ...
    def test_text_set(self) -> bool: ...
    def test_text_template(self) -> bool: ...
    def test_text_variable(self) -> bool: ...
    def test_time(self) -> bool: ...
    def test_time_datatype(self) -> bool: ...
    def test_time_template(self) -> bool: ...
    def test_time_variable(self) -> bool: ...
    def test_value(self) -> bool: ...
    def test_value_set(self) -> bool: ...
    def test_value_snak(self) -> bool: ...
    def test_value_snak_template(self) -> bool: ...
    def test_value_snak_variable(self) -> bool: ...
    def test_value_template(self) -> bool: ...
    def test_value_variable(self) -> bool: ...
    def test_variable(self) -> bool: ...

# -- to_ -------------------------------------------------------------------

    def to_json(self, **kwargs: Any) -> str: ...
    def to_markdown(self, **kwargs: Any) -> str: ...
    def to_repr(self, **kwargs: Any) -> str: ...
    def to_sexp(self, **kwargs: Any) -> str: ...

# -- unpack_ ---------------------------------------------------------------

    def unpack_annotation_record(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_annotation_record_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_data_value(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_data_value_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_data_value_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_deprecated_rank(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_deep_data_value(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_deep_data_value_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_deep_data_value_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_descriptor(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_entity(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_entity_fingerprint(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_entity_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_entity_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_external_id(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_external_id_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_external_id_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_external_id_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_filter_pattern(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_fingerprint(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_iri(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_iri_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_iri_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_iri_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_item(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_item_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_item_descriptor(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_item_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_item_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_kif_object(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_object(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_pattern(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property_descriptor(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_quantity(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_quantity_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_quantity_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_quantity_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_lexeme(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_lexeme_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_lexeme_descriptor(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_lexeme_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_lexeme_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_plain_descriptor(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_preferred_rank(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_kif_object_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_no_value_snak(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_no_value_snak_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_no_value_snak_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_normal_rank(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_property_fingerprint(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_rank(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_reference_record(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_reference_record_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_shallow_data_value(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_shallow_data_value_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_shallow_data_value_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_some_value_snak(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_some_value_snak_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_some_value_snak_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_statement(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_statement_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_statement_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_string(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_string_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_string_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_string_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_snak(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_snak_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_snak_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_snak_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_text(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_text_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_text_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_text_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_text_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_time(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_time_datatype(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_time_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_time_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_set(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_snak(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_snak_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_snak_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_template(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_value_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

    def unpack_variable(
        self,
        function: Optional[Union[TCallable, str]] = None,
        name: Optional[str] = None,
        position: Optional[int] = None
    ) -> Union[TArgs, NoReturn]:
        ...

# -- misc ------------------------------------------------------------------

    def _repr_markdown_(self) -> str:
        ...

    def traverse(
        self,
        filter: Optional[Callable[[Any], bool]] = None,
        visit: Optional[Callable[[Any], bool]] = None,
    ) -> Iterator[Any]:
        ...

    def _traverse(
        self,
        filter: Optional[Callable[[Any], bool]] = None,
        visit: Optional[Callable[[Any], bool]] = None,
    ) -> Iterator[Any]:
        ...
