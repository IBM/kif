# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

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
    KIF_ObjectClass,
    Nil,
    TCallable,
    TDatetime,
    TDecimal,
    TLocation,
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
from .template import Template, TemplateClass
from .value import (
    Datatype,
    DatatypeVariable,
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
    VDatatype,
    VEntity,
    VExternalId,
    VItem,
    VLexeme,
    VProperty,
    VQuantity,
    VQuantityContent,
    VString,
    VStringContent,
    VText,
    VTime,
    VTimeContent,
    VTimePrecisionContent,
    VTimeTimezoneContent,
    VValue,
)
from .value_set import TextSet, TTextSet, TValueSet, ValueSet
from .variable import Variable, VariableClass, Variables

__all__ = (
    'AnnotationRecord',
    'AnnotationRecordSet',
    'Datatype',
    'DatatypeVariable',
    'DataValue',
    'DataValueTemplate',
    'DataValueVariable',
    'Datetime',
    'Decimal',
    'DeepDataValue',
    'DeepDataValueTemplate',
    'DeepDataValueVariable',
    'Deprecated',
    'DeprecatedRank',
    'Descriptor',
    'Entity',
    'EntityFingerprint',
    'EntityTemplate',
    'EntityVariable',
    'ExternalId',
    'ExternalIdDatatype',
    'ExternalIdTemplate',
    'ExternalIdVariable',
    'FilterPattern',
    'Fingerprint',
    'IRI',
    'IRI_Datatype',
    'IRI_Template',
    'IRI_Variable',
    'Item',
    'ItemDatatype',
    'ItemDescriptor',
    'Items',
    'ItemTemplate',
    'ItemVariable',
    'KIF_Object',
    'KIF_ObjectClass',
    'KIF_ObjectSet',
    'Lexeme',
    'LexemeDatatype',
    'LexemeDescriptor',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',
    'Nil',
    'Normal',
    'NormalRank',
    'NoValueSnak',
    'NoValueSnakTemplate',
    'NoValueSnakVariable',
    'Pattern',
    'PlainDescriptor',
    'Preferred',
    'PreferredRank',
    'Properties',
    'Property',
    'PropertyDatatype',
    'PropertyDescriptor',
    'PropertyFingerprint',
    'PropertyTemplate',
    'PropertyVariable',
    'Quantity',
    'QuantityDatatype',
    'QuantityTemplate',
    'QuantityVariable',
    'Rank',
    'ReferenceRecord',
    'ReferenceRecordSet',
    'ShallowDataValue',
    'ShallowDataValueTemplate',
    'ShallowDataValueVariable',
    'Snak',
    'SnakSet',
    'SnakTemplate',
    'SnakVariable',
    'SomeValueSnak',
    'SomeValueSnakTemplate',
    'SomeValueSnakVariable',
    'Statement',
    'StatementTemplate',
    'StatementVariable',
    'String',
    'StringDatatype',
    'StringTemplate',
    'StringVariable',
    'T_IRI',
    'T_KIF_ObjectSet',
    'TAnnotationRecordSet',
    'TCallable',
    'TDatetime',
    'TDecimal',
    'Template',
    'TemplateClass',
    'TEntityFingerprint',
    'Text',
    'TextDatatype',
    'TExternalId',
    'TextSet',
    'TextTemplate',
    'TextVariable',
    'TFingerprint',
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',
    'TLocation',
    'TNil',
    'TPropertyFingerprint',
    'TReferenceRecord',
    'TReferenceRecordSet',
    'TSnakSet',
    'TString',
    'TText',
    'TTextSet',
    'TTimePrecision',
    'TValueSet',
    'UTC',
    'V_IRI',
    'Value',
    'ValueSet',
    'ValueSnak',
    'ValueSnak',
    'ValueSnakTemplate',
    'ValueSnakVariable',
    'ValueTemplate',
    'ValueVariable',
    'Variable',
    'VariableClass',
    'Variables',
    'VDatatype',
    'VEntity',
    'VExternalId',
    'VItem',
    'VLexeme',
    'VNoValueSnak',
    'VProperty',
    'VQuantity',
    'VQuantityContent',
    'VSnak',
    'VSomeValueSnak',
    'VString',
    'VStringContent',
    'VText',
    'VTime',
    'VTimeContent',
    'VTimePrecisionContent',
    'VTimeTimezoneContent',
    'VValue',
    'VValueSnak',
)
