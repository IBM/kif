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
from .filter import Filter
from .fingerprint import (
    And,
    AndFingerprint,
    AtomicFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    EmptyFingerprint,
    Fingerprint,
    FullFingerprint,
    Or,
    OrFingerprint,
    SnakFingerprint,
    TFingerprint,
    ValueFingerprint,
)
from .kif_object import KIF_Object
from .pattern import Pattern
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
    TEntity,
    Text,
    TextDatatype,
    TExternalId,
    TextTemplate,
    TextVariable,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    TItem,
    TLexeme,
    TProperty,
    TQuantity,
    TString,
    TText,
    TTime,
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

    # kif_object
    'KIF_Object',

    # pattern
    'Pattern',

    # template
    'Template',

    # variable
    'Theta',
    'Variable',
    'Variables',

    # datatype
    'Datatype',
    'DatatypeVariable',
    'TDatatype',
    'VDatatype',
    'VTDatatype',

    # value
    'TValue',
    'Value',
    'ValueTemplate',
    'ValueVariable',
    'VTValue',
    'VValue',

    # value.entity
    'Entity',
    'EntityTemplate',
    'EntityVariable',
    'TEntity',
    'VEntity',
    'VTEntity',

    # value.item
    'Item',
    'ItemDatatype',
    'Items',
    'ItemTemplate',
    'ItemVariable',
    'TItem',
    'VItem',
    'VTItem',

    # value.property
    'Properties',
    'Property',
    'PropertyDatatype',
    'PropertyTemplate',
    'PropertyVariable',
    'TProperty',
    'VProperty',
    'VTProperty',

    # value.lexeme
    'Lexeme',
    'LexemeDatatype',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',
    'TLexeme',
    'VLexeme',

    # value.data_value
    'DataValue',
    'DataValueTemplate',
    'DataValueVariable',

    # value.shallow_data_value
    'ShallowDataValue',
    'ShallowDataValueTemplate',
    'ShallowDataValueVariable',

    # value.iri
    'IRI',
    'IRI_Datatype',
    'IRI_Template',
    'IRI_Variable',
    'T_IRI',
    'V_IRI',
    'VT_IRI',

    # value.text
    'Text',
    'TextDatatype',
    'TextTemplate',
    'TextVariable',
    'TText',
    'VText',

    # value.string
    'String',
    'StringDatatype',
    'StringTemplate',
    'StringVariable',
    'TString',
    'VString',

    # value.external_id
    'ExternalId',
    'ExternalIdDatatype',
    'ExternalIdTemplate',
    'ExternalIdVariable',
    'TExternalId',
    'VExternalId',

    # value.deep_data_value
    'DeepDataValue',
    'DeepDataValueTemplate',
    'DeepDataValueVariable',

    # value.quantity
    'Quantity',
    'QuantityDatatype',
    'QuantityTemplate',
    'QuantityVariable',
    'TQuantity',
    'VQuantity',

    # value.time
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',
    'TTime',
    'TTimePrecision',
    'VTime',

    # snak
    'NoValueSnak',
    'NoValueSnakTemplate',
    'NoValueSnakVariable',
    'Snak',
    'SnakTemplate',
    'SnakVariable',
    'SomeValueSnak',
    'SomeValueSnakTemplate',
    'SomeValueSnakVariable',
    'TSnak',
    'ValueSnak',
    'ValueSnakTemplate',
    'ValueSnakVariable',
    'VNoValueSnak',
    'VSnak',
    'VSomeValueSnak',
    'VTSnak',
    'VValueSnak',

    # statement
    'Statement',
    'StatementTemplate',
    'StatementVariable',
    'TStatement',
    'VStatement',
    'VTStatement',

    # annotation
    'AnnotationRecord',
    'AnnotationRecordSet',
    'Deprecated',
    'DeprecatedRank',
    'Normal',
    'NormalRank',
    'Preferred',
    'PreferredRank',
    'Rank',
    'TAnnotationRecordSet',

    # descriptor
    'Descriptor',
    'ItemDescriptor',
    'LexemeDescriptor',
    'PlainDescriptor',
    'PropertyDescriptor',

    # set
    'KIF_ObjectSet',
    'ReferenceRecord',
    'ReferenceRecordSet',
    'SnakSet',
    'TextSet',
    'TReferenceRecord',
    'TReferenceRecordSet',
    'TSnakSet',
    'TTextSet',
    'TValueSet',
    'ValueSet',

    # fingerprint
    'And',
    'AndFingerprint',
    'AtomicFingerprint',
    'CompoundFingerprint',
    'ConverseSnakFingerprint',
    'EmptyFingerprint',
    'Fingerprint',
    'FullFingerprint',
    'Or',
    'OrFingerprint',
    'SnakFingerprint',
    'TFingerprint',
    'ValueFingerprint',

    # filter
    'Filter',
)
