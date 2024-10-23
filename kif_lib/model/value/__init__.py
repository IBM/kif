# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .data_value import DataValue, DataValueTemplate, DataValueVariable
from .datatype import (
    Datatype,
    DatatypeVariable,
    TDatatype,
    VDatatype,
    VTDatatype,
)
from .deep_data_value import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
)
from .entity import (
    Entity,
    EntityTemplate,
    EntityVariable,
    TEntity,
    VEntity,
    VTEntity,
)
from .external_id import (
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    TExternalId,
    VExternalId,
)
from .iri import (
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    T_IRI,
    V_IRI,
    VT_IRI,
)
from .item import (
    Item,
    ItemDatatype,
    Items,
    ItemTemplate,
    ItemVariable,
    TItem,
    VItem,
    VTItem,
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
    AliasProperty,
    DescriptionProperty,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    LexicalCategoryProperty,
    Properties,
    Property,
    PropertyDatatype,
    PropertyTemplate,
    PropertyVariable,
    PseudoProperty,
    PseudoPropertyVariable,
    TProperty,
    VProperty,
    VTProperty,
)
from .quantity import (
    Quantity,
    QuantityDatatype,
    QuantityTemplate,
    QuantityVariable,
    TQuantity,
    VQuantity,
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
)
from .text import Text, TextDatatype, TextTemplate, TextVariable, TText, VText
from .time import (
    Time,
    TimeDatatype,
    TimeTemplate,
    TimeVariable,
    TTime,
    TTimePrecision,
    VTime,
)
from .value import TValue, Value, ValueTemplate, ValueVariable, VTValue, VValue

__all__ = (

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

    # entity
    'Entity',
    'EntityTemplate',
    'EntityVariable',
    'TEntity',
    'VEntity',
    'VTEntity',

    # item
    'Item',
    'ItemDatatype',
    'Items',
    'ItemTemplate',
    'ItemVariable',
    'TItem',
    'VItem',
    'VTItem',

    # property
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
    'TProperty',
    'VProperty',
    'VTProperty',

    # lexeme
    'Lexeme',
    'LexemeDatatype',
    'Lexemes',
    'LexemeTemplate',
    'LexemeVariable',
    'TLexeme',
    'VLexeme',

    # data value
    'DataValue',
    'DataValueTemplate',
    'DataValueVariable',

    # shallow data value
    'ShallowDataValue',
    'ShallowDataValueTemplate',
    'ShallowDataValueVariable',

    # iri
    'IRI',
    'IRI_Datatype',
    'IRI_Template',
    'IRI_Variable',
    'T_IRI',
    'V_IRI',
    'VT_IRI',

    # text
    'Text',
    'TextDatatype',
    'TextTemplate',
    'TextVariable',
    'TText',
    'VText',

    # string
    'String',
    'StringDatatype',
    'StringTemplate',
    'StringVariable',
    'TString',
    'VString',

    # external id
    'ExternalId',
    'ExternalIdDatatype',
    'ExternalIdTemplate',
    'ExternalIdVariable',
    'TExternalId',
    'VExternalId',

    # deep data value
    'DeepDataValue',
    'DeepDataValueTemplate',
    'DeepDataValueVariable',

    # quantity
    'Quantity',
    'QuantityDatatype',
    'QuantityTemplate',
    'QuantityVariable',
    'TQuantity',
    'VQuantity',

    # time
    'Time',
    'TimeDatatype',
    'TimeTemplate',
    'TimeVariable',
    'TTime',
    'TTimePrecision',
    'VTime',
)
