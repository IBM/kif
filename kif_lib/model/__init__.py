# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .annotation import (
    Deprecated,
    DeprecatedRank,
    Normal,
    NormalRank,
    Preferred,
    PreferredRank,
    Rank,
    RankVariable,
    TRank,
    VRank,
    VTRank,
)
from .constraint import (
    AtomicConstraint,
    Constraint,
    FalseConstraint,
    TConstraint,
    TrueConstraint,
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
from .pattern import (
    ClosedPattern,
    OpenPattern,
    Pattern,
    TClosedPattern,
    TemplatePattern,
    TOpenPattern,
    TPattern,
    TTemplatePattern,
    TVariablePattern,
    VariablePattern,
)
from .set import (
    ClosedTermSet,
    QualifierRecord,
    QualifierRecordVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordSetVariable,
    ReferenceRecordVariable,
    SnakSet,
    SnakSetVariable,
    TextSet,
    TQualifierRecord,
    TReferenceRecord,
    TReferenceRecordSet,
    TSnakSet,
    TTextSet,
    TValueSet,
    ValueSet,
    VQualifierRecord,
    VReferenceRecord,
    VReferenceRecordSet,
    VSnakSet,
    VTQualifierRecord,
    VTReferenceRecord,
    VTReferenceRecordSet,
    VTSnakSet,
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
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    AnnotatedStatementVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    TAnnotatedStatement,
    TStatement,
    VAnnotatedStatement,
    VStatement,
    VTAnnotatedStatement,
    VTStatement,
)
from .term import (
    ClosedTerm,
    OpenTerm,
    Template,
    Term,
    Theta,
    Variable,
    Variables,
)
from .value import (
    AliasProperty,
    Datatype,
    DatatypeVariable,
    DataValue,
    DataValueTemplate,
    DataValueVariable,
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    DescriptionProperty,
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
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    LexicalCategoryProperty,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    PseudoProperty,
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

__all__ = (

    # kif_object
    'KIF_Object',

    # term
    'ClosedTerm',
    'OpenTerm',
    'Template',
    'Term',
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
    'AliasProperty',
    'DescriptionProperty',
    'LabelProperty',
    'LanguageProperty',
    'LemmaProperty',
    'LexicalCategoryProperty',
    'Properties',
    'Property',
    'PropertyDatatype',
    'PropertyTemplate',
    'PropertyVariable',
    'PseudoProperty',
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
    'AnnotatedStatement',
    'AnnotatedStatementTemplate',
    'AnnotatedStatementVariable',
    'Statement',
    'StatementTemplate',
    'StatementVariable',
    'TAnnotatedStatement',
    'TStatement',
    'VAnnotatedStatement',
    'VStatement',
    'VTAnnotatedStatement',
    'VTStatement',

    # annotation
    'Deprecated',
    'DeprecatedRank',
    'Normal',
    'NormalRank',
    'Preferred',
    'PreferredRank',
    'Rank',
    'RankVariable',
    'TRank',
    'VRank',
    'VTRank',

    # descriptor
    'Descriptor',
    'ItemDescriptor',
    'LexemeDescriptor',
    'PlainDescriptor',
    'PropertyDescriptor',

    # set
    'ClosedTermSet',
    'QualifierRecord',
    'QualifierRecordVariable',
    'ReferenceRecord',
    'ReferenceRecordSet',
    'ReferenceRecordSetVariable',
    'ReferenceRecordVariable',
    'SnakSet',
    'SnakSetVariable',
    'TextSet',
    'TQualifierRecord',
    'TReferenceRecord',
    'TReferenceRecordSet',
    'TSnakSet',
    'TTextSet',
    'TValueSet',
    'ValueSet',
    'VQualifierRecord',
    'VReferenceRecord',
    'VReferenceRecordSet',
    'VSnakSet',
    'VTQualifierRecord',
    'VTReferenceRecord',
    'VTReferenceRecordSet',
    'VTSnakSet',

    # pattern
    'ClosedPattern',
    'OpenPattern',
    'Pattern',
    'TClosedPattern',
    'TemplatePattern',
    'TOpenPattern',
    'TPattern',
    'TTemplatePattern',
    'TVariablePattern',
    'VariablePattern',

    # constraint
    'AtomicConstraint',
    'Constraint',
    'FalseConstraint',
    'TConstraint',
    'TrueConstraint',

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
