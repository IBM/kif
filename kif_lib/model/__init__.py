# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .annotation import (
    AnnotationRecord,
    AnnotationRecordSet,
    Deprecated,
    DeprecatedRank,
    Normal,
    NormalRank,
    Preferred,
    PreferredRank,
    Rank,
    TAnnotationRecordSet,
)
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
from .kif_object import KIF_Object
from .pattern import Pattern
from .pattern_deprecated import FilterPattern
from .set import (
    KIF_ObjectSet,
    ReferenceRecord,
    ReferenceRecordSet,
    SnakSet,
    TextSet,
    TReferenceRecord,
    TReferenceRecordSet,
    TSnakSet,
    TTextSet,
    TValueSet,
    ValueSet,
)
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
    TSnak,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    VNoValueSnak,
    VSnak,
    VSomeValueSnak,
    VTSnak,
    VValueSnak,
)
from .statement import (
    Statement,
    StatementTemplate,
    StatementVariable,
    TStatement,
    VStatement,
    VTStatement,
)
from .template import Template
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
    TValue,
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
    VString,
    VT_IRI,
    VTDatatype,
    VTEntity,
    VText,
    VTime,
    VTItem,
    VTProperty,
    VTValue,
    VValue,
)
from .variable import Theta, Variable, Variables

__all__ = (
    'AnnotationRecord',
    'AnnotationRecordSet',
    'Datatype',
    'DatatypeVariable',
    'DataValue',
    'DataValueTemplate',
    'DataValueVariable',
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
    'KIF_ObjectSet',
    'Lexeme',
    'LexemeDatatype',
    'LexemeDescriptor',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',
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
    'TAnnotationRecordSet',
    'TDatatype',
    'Template',
    'TEntityFingerprint',
    'Text',
    'TextDatatype',
    'TExternalId',
    'TextSet',
    'TextTemplate',
    'TextVariable',
    'TFingerprint',
    'Theta',
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',
    'TPropertyFingerprint',
    'TReferenceRecord',
    'TReferenceRecordSet',
    'TSnak',
    'TSnakSet',
    'TStatement',
    'TString',
    'TText',
    'TTextSet',
    'TTimePrecision',
    'TValue',
    'TValueSet',
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
    'Variables',
    'VDatatype',
    'VEntity',
    'VExternalId',
    'VItem',
    'VLexeme',
    'VNoValueSnak',
    'VProperty',
    'VQuantity',
    'VSnak',
    'VSomeValueSnak',
    'VStatement',
    'VString',
    'VT_IRI',
    'VTDatatype',
    'VTEntity',
    'VText',
    'VTime',
    'VTItem',
    'VTProperty',
    'VTSnak',
    'VTStatement',
    'VTValue',
    'VValue',
    'VValueSnak',
)
