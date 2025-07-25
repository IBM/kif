# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from . import codec  # noqa: F401
from .__version__ import __description__, __title__, __version__  # noqa: F401
from .context import Context
from .error import Error
from .model import (
    AliasProperty,
    And,
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    AnnotatedStatementVariable,
    ClosedPattern,
    ClosedTerm,
    ClosedTermPair,
    ClosedTermSet,
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
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    Filter,
    Fingerprint,
    Graph,
    GraphVariable,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexemeDatatype,
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
    Path,
    Pattern,
    Preferred,
    PreferredRank,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    PseudoProperty,
    QualifierRecord,
    QualifierRecordVariable,
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    Rank,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordSetVariable,
    ReferenceRecordVariable,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    Snak,
    SnakSet,
    SnakSetVariable,
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
    SubtypeProperty,
    Template,
    TemplatePattern,
    Term,
    Text,
    TextDatatype,
    TextTemplate,
    TextVariable,
    Theta,
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    TypeProperty,
    Value,
    ValuePair,
    ValuePairVariable,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    Variable,
    VariablePattern,
    Variables,
)
from .search import Search
from .store import Store

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
    'SubtypeProperty',
    'TypeProperty',

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
    'AnnotatedStatement',
    'AnnotatedStatementTemplate',
    'AnnotatedStatementVariable',
    'Statement',
    'StatementTemplate',
    'StatementVariable',

    # model.rank
    'Deprecated',
    'DeprecatedRank',
    'Normal',
    'NormalRank',
    'Preferred',
    'PreferredRank',
    'Rank',
    'RankVariable',

    # model.pair
    'ClosedTermPair',
    'ValuePair',
    'ValuePairVariable',

    # model.set
    'ClosedTermSet',
    'QualifierRecord',
    'QualifierRecordVariable',
    'ReferenceRecord',
    'ReferenceRecordSet',
    'ReferenceRecordSetVariable',
    'ReferenceRecordVariable',
    'SnakSet',
    'SnakSetVariable',

    # model.graph,
    'Graph',
    'GraphVariable',

    # model.path
    'Path',

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
    'Fingerprint',
    'Or',

    # model.filter
    'Filter',

    # search
    'Search',

    # store
    'Store',
)


def _reset_logging(
        debug: bool | None = bool(os.getenv('KIF_DEBUG')),
        info: bool | None = bool(os.getenv('KIF_INFO'))
) -> None:
    if debug or info:
        import logging
        logging.basicConfig()
        if debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.getLogger('httpx').setLevel(logging.INFO)
        logging.getLogger('kif_lib').setLevel(level)


_reset_logging()
