# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
from typing import Any, NoReturn, Optional, Union

from . import object
from .annotation_record import AnnotationRecord
from .annotation_record_set import AnnotationRecordSet
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
from .kif_object_set import KIF_ObjectSet
from .pattern import FilterPattern, Pattern
from .rank import DeprecatedRank, NormalRank, PreferredRank, Rank
from .reference_record import ReferenceRecord
from .reference_record_set import ReferenceRecordSet, TReferenceRecordSet
from .snak import NoValueSnak, Snak, SomeValueSnak, ValueSnak
from .snak_set import SnakSet
from .statement import Statement
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
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
    Value,
)
from .value_set import TextSet, ValueSet

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

    # -- Datetime --

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

    # -- decimal --

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

    # -- inherited from Object --

    @classmethod
    def _check_arg_statement(
            cls,
            arg: Optional[Statement],
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Statement, NoReturn]:
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
    def _check_optional_arg_reference_record_set(
            cls,
            arg: Optional[TReferenceRecordSet],
            default: Optional[ReferenceRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Union[Optional[ReferenceRecordSet], NoReturn]:
        ...

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

    def check_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DataValue, NoReturn]:
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

    def check_no_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[NoValueSnak, NoReturn]:
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

    def check_shallow_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[ShallowDataValue, NoReturn]:
        ...

    def check_some_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[SomeValueSnak, NoReturn]:
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

    def check_statement(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Statement, NoReturn]:
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

    @classmethod
    def from_json(
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

    def is_annotation_record(self) -> bool: ...
    def is_annotation_record_set(self) -> bool: ...
    def is_data_value(self) -> bool: ...
    def is_datatype(self) -> bool: ...
    def is_deep_data_value(self) -> bool: ...
    def is_deprecated_rank(self) -> bool: ...
    def is_descriptor(self) -> bool: ...
    def is_entity(self) -> bool: ...
    def is_entity_fingerprint(self) -> bool: ...
    def is_external_id(self) -> bool: ...
    def is_external_id_datatype(self) -> bool: ...
    def is_filter_pattern(self) -> bool: ...
    def is_fingerprint(self) -> bool: ...
    def is_iri(self) -> bool: ...
    def is_iri_datatype(self) -> bool: ...
    def is_item(self) -> bool: ...
    def is_item_datatype(self) -> bool: ...
    def is_item_descriptor(self) -> bool: ...
    def is_kif_object(self) -> bool: ...
    def is_kif_object_set(self) -> bool: ...
    def is_lexeme(self) -> bool: ...
    def is_lexeme_datatype(self) -> bool: ...
    def is_lexeme_descriptor(self) -> bool: ...
    def is_no_value_snak(self) -> bool: ...
    def is_normal_rank(self) -> bool: ...
    def is_object(self) -> bool: ...
    def is_pattern(self) -> bool: ...
    def is_plain_descriptor(self) -> bool: ...
    def is_preferred_rank(self) -> bool: ...
    def is_property(self) -> bool: ...
    def is_property_datatype(self) -> bool: ...
    def is_property_descriptor(self) -> bool: ...
    def is_property_fingerprint(self) -> bool: ...
    def is_quantity(self) -> bool: ...
    def is_quantity_datatype(self) -> bool: ...
    def is_rank(self) -> bool: ...
    def is_reference_record(self) -> bool: ...
    def is_reference_record_set(self) -> bool: ...
    def is_shallow_data_value(self) -> bool: ...
    def is_snak(self) -> bool: ...
    def is_snak_set(self) -> bool: ...
    def is_some_value_snak(self) -> bool: ...
    def is_statement(self) -> bool: ...
    def is_string(self) -> bool: ...
    def is_string_datatype(self) -> bool: ...
    def is_text(self) -> bool: ...
    def is_text_datatype(self) -> bool: ...
    def is_text_set(self) -> bool: ...
    def is_time(self) -> bool: ...
    def is_time_datatype(self) -> bool: ...
    def is_value(self) -> bool: ...
    def is_value_set(self) -> bool: ...
    def is_value_snak(self) -> bool: ...

    def test_annotation_record(self) -> bool: ...
    def test_annotation_record_set(self) -> bool: ...
    def test_data_value(self) -> bool: ...
    def test_datatype(self) -> bool: ...
    def test_deep_data_value(self) -> bool: ...
    def test_deprecated_rank(self) -> bool: ...
    def test_descriptor(self) -> bool: ...
    def test_entity(self) -> bool: ...
    def test_entity_fingerprint(self) -> bool: ...
    def test_external_id(self) -> bool: ...
    def test_external_id_datatype(self) -> bool: ...
    def test_filter_pattern(self) -> bool: ...
    def test_fingerprint(self) -> bool: ...
    def test_iri(self) -> bool: ...
    def test_iri_datatype(self) -> bool: ...
    def test_item(self) -> bool: ...
    def test_item_datatype(self) -> bool: ...
    def test_item_descriptor(self) -> bool: ...
    def test_kif_object(self) -> bool: ...
    def test_kif_object_set(self) -> bool: ...
    def test_lexeme(self) -> bool: ...
    def test_lexeme_datatype(self) -> bool: ...
    def test_lexeme_descriptor(self) -> bool: ...
    def test_no_value_snak(self) -> bool: ...
    def test_normal_rank(self) -> bool: ...
    def test_object(self) -> bool: ...
    def test_pattern(self) -> bool: ...
    def test_plain_descriptor(self) -> bool: ...
    def test_preferred_rank(self) -> bool: ...
    def test_property(self) -> bool: ...
    def test_property_datatype(self) -> bool: ...
    def test_property_descriptor(self) -> bool: ...
    def test_property_fingerprint(self) -> bool: ...
    def test_quantity(self) -> bool: ...
    def test_quantity_datatype(self) -> bool: ...
    def test_rank(self) -> bool: ...
    def test_reference_record(self) -> bool: ...
    def test_reference_record_set(self) -> bool: ...
    def test_shallow_data_value(self) -> bool: ...
    def test_snak(self) -> bool: ...
    def test_snak_set(self) -> bool: ...
    def test_some_value_snak(self) -> bool: ...
    def test_statement(self) -> bool: ...
    def test_string(self) -> bool: ...
    def test_string_datatype(self) -> bool: ...
    def test_text(self) -> bool: ...
    def test_text_datatype(self) -> bool: ...
    def test_text_set(self) -> bool: ...
    def test_time(self) -> bool: ...
    def test_time_datatype(self) -> bool: ...
    def test_value(self) -> bool: ...
    def test_value_set(self) -> bool: ...
    def test_value_snak(self) -> bool: ...

    def to_json(self, **kwargs: Any) -> str: ...
    def to_markdown(self, **kwargs: Any) -> str: ...
    def to_sexp(self, **kwargs: Any) -> str: ...

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

    def unpack_external_id(
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

    def unpack_some_value_snak(
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
