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
from .pattern import Pattern
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
    VNoValueSnak,
    VSnak,
    VSomeValueSnak,
    VValueSnak,
)
from .snak_set import SnakSet, TSnakSet
from .statement import Statement, StatementTemplate, StatementVariable
from .template import Template
from .value import (
    Datatype,
    DataValue,
    DataValueTemplate,
    DataValueVariable,
    DeepDataValue,
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
    TTimePrecision,
    V_IRI,
    Value,
    ValueTemplate,
    ValueVariable,
    VEntity,
    VExternalId,
    VItem,
    VLexeme,
    VProperty,
    VQuantity,
    VString,
    VText,
    VTime,
    VValue,
)
from .value_set import TextSet, TTextSet, TValueSet, ValueSet
from .variable import Variable, Variables
