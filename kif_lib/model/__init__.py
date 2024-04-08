# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

# flake8: noqa
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
from .kif_object import (
    Datetime,
    Decimal,
    KIF_Object,
    Nil,
    TCallable,
    TDatetime,
    TDecimal,
    TNil,
    UTC,
)
from .kif_object_set import KIF_ObjectSet, T_KIF_ObjectSet
from .pattern import Pattern, Template, Variable
from .pattern_deprecated import FilterPattern
from .rank import (
    Deprecated,
    DeprecatedRank,
    Normal,
    NormalRank,
    Preferred,
    PreferredRank,
    Rank,
)
from .reference_record import ReferenceRecord, TReferenceRecord
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
    DeepDataValue,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityDatatype,
    ShallowDataValue,
    ShallowDataValueTemplate,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    T_IRI,
    TDatatype,
    Text,
    TextDatatype,
    TExternalId,
    Time,
    TimeDatatype,
    TimeVariable,
    TString,
    TText,
    TTimePrecision,
    V_IRI,
    Value,
    ValueTemplate,
    ValueVariable,
    VItem,
    VLexeme,
    VProperty,
    VValue,
)
from .value_set import TextSet, TTextSet, TValueSet, ValueSet
