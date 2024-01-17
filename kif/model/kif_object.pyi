# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
from typing import Any, NoReturn, Optional, Union

from . import object
from .fingerprint import (
    EntityFingerprint,
    Fingerprint,
    PropertyFingerprint,
    TEntityFingerprint,
    TFingerprint,
    TPropertyFingerprint,
)
from .reference_record_set import ReferenceRecordSet, TReferenceRecordSet

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

    # -- Signatures --

    def is_annotation_record(self) -> bool: ...
    def is_annotation_record_set(self) -> bool: ...
    def is_deep_data_value(self) -> bool: ...
    def is_descriptor(self) -> bool: ...
    def is_entity(self) -> bool: ...
    def is_entity_fingerprint(self) -> bool: ...
    def is_filter_pattern(self) -> bool: ...
    def is_fingerprint(self) -> bool: ...
    def is_iri(self) -> bool: ...
    def is_item(self) -> bool: ...
    def is_kif_object_set(self) -> bool: ...
    def is_no_value_snak(self) -> bool: ...
    def is_property(self) -> bool: ...
    def is_property_fingerprint(self) -> bool: ...
    def is_quantity(self) -> bool: ...
    def is_rank(self) -> bool: ...
    def is_reference_record(self) -> bool: ...
    def is_reference_record_set(self) -> bool: ...
    def is_snak(self) -> bool: ...
    def is_snak_set(self) -> bool: ...
    def is_some_value_snak(self) -> bool: ...
    def is_statement(self) -> bool: ...
    def is_string(self) -> bool: ...
    def is_text(self) -> bool: ...
    def is_time(self) -> bool: ...
    def is_value_snak(self) -> bool: ...

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
