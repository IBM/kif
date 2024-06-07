# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .data_value import (
    DataValue,
    DataValueClass,
    DataValueTemplate,
    DataValueTemplateClass,
    DataValueVariable,
    DataValueVariableClass,
)
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueClass,
    DeepDataValueTemplate,
    DeepDataValueTemplateClass,
    DeepDataValueVariable,
    DeepDataValueVariableClass,
)
from .entity import (
    Entity,
    EntityClass,
    EntityTemplate,
    EntityTemplateClass,
    EntityVariable,
    EntityVariableClass,
    VEntity,
    VVEntity,
)
from .external_id import (
    ExternalId,
    ExternalIdClass,
    ExternalIdDatatype,
    ExternalIdDatatypeClass,
    ExternalIdTemplate,
    ExternalIdTemplateClass,
    ExternalIdVariable,
    ExternalIdVariableClass,
    TExternalId,
    VExternalId,
)
from .iri import IRI, IRI_Datatype, IRI_Template, IRI_Variable, T_IRI, V_IRI
from .item import (
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    TItem,
    VItem,
)
from .lexeme import (
    Lexeme,
    LexemeDatatype,
    Lexemes,
    LexemeTemplate,
    LexemeVariable,
    TLexeme,
    VLexeme,
)
from .property import (
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    TProperty,
    VProperty,
    VVProperty,
)
from .quantity import (
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    VQuantity,
    VQuantityContent,
)
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .string import (
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    TString,
    VString,
    VStringContent,
)
from .text import Text, TextDatatype, TextTemplate, TextVariable, TText, VText
from .time import (
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    TTimePrecision,
    VTime,
    VTimeContent,
    VTimePrecisionContent,
    VTimeTimezoneContent,
)
from .value import (
    Datatype,
    DatatypeClass,
    DatatypeVariable,
    TDatatypeClass,
    TValue,
    Value,
    ValueTemplate,
    ValueVariable,
    VDatatype,
    VValue,
    VVValue,
)

__all__ = (
    'Datatype',
    'DatatypeClass',
    'DatatypeVariable',
    'DataValue',
    'DataValueClass',
    'DataValueTemplate',
    'DataValueTemplateClass',
    'DataValueVariable',
    'DataValueVariableClass',
    'DeepDataValue',
    'DeepDataValueClass',
    'DeepDataValueTemplate',
    'DeepDataValueTemplateClass',
    'DeepDataValueVariable',
    'DeepDataValueVariableClass',
    'Entity',
    'EntityClass',
    'EntityTemplate',
    'EntityTemplateClass',
    'EntityVariable',
    'EntityVariableClass',
    'ExternalId',
    'ExternalIdClass',
    'ExternalIdDatatype',
    'ExternalIdDatatypeClass',
    'ExternalIdTemplate',
    'ExternalIdTemplateClass',
    'ExternalIdVariable',
    'ExternalIdVariableClass',
    'IRI',
    'IRI_Datatype',
    'IRI_Template',
    'IRI_Variable',
    'Item',
    'ItemDatatype',
    'Items',
    'ItemTemplate',
    'ItemVariable',
    'Lexeme',
    'LexemeDatatype',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',
    'Properties',
    'Property',
    'PropertyDatatype',
    'PropertyTemplate',
    'PropertyVariable',
    'Quantity',
    'QuantityDatatype',
    'QuantityTemplate',
    'QuantityVariable',
    'ShallowDataValue',
    'ShallowDataValueTemplate',
    'ShallowDataValueVariable',
    'String',
    'StringDatatype',
    'StringTemplate',
    'StringVariable',
    'T_IRI',
    'TDatatypeClass',
    'Text',
    'TextDatatype',
    'TExternalId',
    'TextTemplate',
    'TextVariable',
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',
    'TItem',
    'TLexeme',
    'TProperty',
    'TString',
    'TText',
    'TTimePrecision',
    'TValue',
    'V_IRI',
    'Value',
    'ValueTemplate',
    'ValueVariable',
    'VDatatype',
    'VEntity',
    'VExternalId',
    'VItem',
    'VLexeme',
    'VProperty',
    'VQuantity',
    'VQuantityContent',
    'VString',
    'VStringContent',
    'VText',
    'VTime',
    'VTimeContent',
    'VTimePrecisionContent',
    'VTimeTimezoneContent',
    'VValue',
    'VVEntity',
    'VVProperty',
    'VVValue',
)
