# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from . import codec  # noqa: F401
from .context import Context
from .error import Error
from .model import (
    AliasProperty,
    And,
    AnnotationRecord,
    AnnotationRecordSet,
    ClosedPattern,
    ClosedTerm,
    Constraint,
    Datatype,
    DatatypeVariable,
    DataValue,
    DataValueTemplate,
    DataValueVariable,
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    Deprecated,
    DeprecatedRank,
    DescriptionProperty,
    Descriptor,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    Filter,
    Fingerprint,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemDescriptor,
    Items,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    KIF_ObjectSet,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexemeDatatype,
    LexemeDescriptor,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    LexicalCategoryProperty,
    Normal,
    NormalRank,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    OpenPattern,
    OpenTerm,
    Or,
    Pattern,
    PlainDescriptor,
    Preferred,
    PreferredRank,
    Properties,
    Property,
    PropertyDatatype,
    PropertyDescriptor,
    PropertyTemplate,
    PropertyVariable,
    PseudoProperty,
    PseudoPropertyVariable,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    Rank,
    ReferenceRecord,
    ReferenceRecordSet,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    Snak,
    SnakSet,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    Template,
    TemplatePattern,
    Term,
    Text,
    TextDatatype,
    TextSet,
    TextTemplate,
    TextVariable,
    Theta,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    Value,
    ValueSet,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    Variable,
    VariablePattern,
    Variables,
)
from .store import Store
from .version import __version__  # noqa: F401

__all__ = (

    # context
    'Context',

    # error
    'Error',

    # model.kif_object
    'KIF_Object',

    # model.term
    'ClosedTerm',
    'OpenTerm',
    'Template',
    'Term',
    'Theta',
    'Variable',
    'Variables',

    # model.value.datatype
    'Datatype',
    'DatatypeVariable',

    # model.value
    'Value',
    'ValueTemplate',
    'ValueVariable',

    # model.value.entity
    'Entity',
    'EntityTemplate',
    'EntityVariable',

    # model.value.item
    'Item',
    'ItemDatatype',
    'Items',
    'ItemTemplate',
    'ItemVariable',

    # model.value.property
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
    'PseudoPropertyVariable',

    # model.value.lexeme
    'Lexeme',
    'LexemeDatatype',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',

    # model.value.data_value
    'DataValue',
    'DataValueTemplate',
    'DataValueVariable',

    # model.value.shallow_data_value
    'ShallowDataValue',
    'ShallowDataValueTemplate',
    'ShallowDataValueVariable',

    # model.value.iri
    'IRI',
    'IRI_Datatype',
    'IRI_Template',
    'IRI_Variable',

    # model.value.text
    'Text',
    'TextDatatype',
    'TextSet',
    'TextTemplate',
    'TextVariable',

    # model.value.string
    'String',
    'StringDatatype',
    'StringTemplate',
    'StringVariable',

    # model.value.external_id
    'ExternalId',
    'ExternalIdDatatype',
    'ExternalIdTemplate',
    'ExternalIdVariable',

    # model.value.deep_data_value
    'DeepDataValue',
    'DeepDataValueTemplate',
    'DeepDataValueVariable',

    # model.value.quantity
    'Quantity',
    'QuantityDatatype',
    'QuantityTemplate',
    'QuantityVariable',

    # model.value.time
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',

    # model.snak
    'NoValueSnak',
    'NoValueSnakTemplate',
    'NoValueSnakVariable',
    'Snak',
    'SnakTemplate',
    'SnakVariable',
    'SomeValueSnak',
    'SomeValueSnakTemplate',
    'SomeValueSnakVariable',
    'ValueSnak',
    'ValueSnakTemplate',
    'ValueSnakVariable',

    # model.statement
    'Statement',
    'StatementTemplate',
    'StatementVariable',

    # model.annotation
    'AnnotationRecord',
    'AnnotationRecordSet',
    'Deprecated',
    'DeprecatedRank',
    'Normal',
    'NormalRank',
    'Preferred',
    'PreferredRank',
    'Rank',

    # model.descriptor
    'Descriptor',
    'ItemDescriptor',
    'LexemeDescriptor',
    'PlainDescriptor',
    'PropertyDescriptor',

    # model.set
    'KIF_ObjectSet',
    'ReferenceRecord',
    'ReferenceRecordSet',
    'SnakSet',
    'TextSet',
    'ValueSet',

    # model.pattern
    'ClosedPattern',
    'OpenPattern',
    'Pattern',
    'TemplatePattern',
    'VariablePattern',

    # model.constraint
    'Constraint',

    # model.fingerprint
    'And',
    'Error',
    'Fingerprint',
    'Or',
    'Store',

    # model.filter
    'Filter',

    # store
    'Store',
)
