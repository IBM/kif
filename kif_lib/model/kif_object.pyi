#
# ** GENERATED FILE, DO NOT EDIT! **
#

# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..context import Context
from ..typing import (
    Any,
    Callable,
    ClassVar,
    Iterator,
    Optional,
    Self,
    TypeAlias,
    Union,
)
from . import object
from .annotation import (
    AnnotationRecord,
    AnnotationRecordSet,
    DeprecatedRank,
    NormalRank,
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
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
)
from .statement import Statement, StatementTemplate, StatementVariable
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
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeDatatype,
    LexemeTemplate,
    LexemeVariable,
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
    TItem,
    TLexeme,
    TProperty,
    TQuantity,
    TString,
    TText,
    TTime,
    TValue,
    Value,
    ValueTemplate,
    ValueVariable,
)
from .variable import Variable

Codec = object.Codec
CodecError = object.CodecError
Decoder = object.Decoder
DecoderError = object.DecoderError
Encoder = object.Encoder
EncoderError = object.EncoderError
Error = object.Error
MustBeImplementedInSubclass = object.MustBeImplementedInSubclass
Nil = object.Nil
Object = object.Object
ShouldNotGetHere = object.ShouldNotGetHere

TArgs: TypeAlias = object.TArgs
TCallable: TypeAlias = object.TFun
TDetails: TypeAlias = object.TDet
TLocation: TypeAlias = object.TLoc
TNil: TypeAlias = object.TNil

KIF_ObjectClass: TypeAlias = type['KIF_Object']


# == Codecs ================================================================

class KIF_JSON_Encoder(
        object.JSON_Encoder, format='json', description='JSON encoder'):
    ...


class KIF_ReprDecoder(
        object.ReprDecoder, format='repr', description='Repr. decoder'):
    ...


class KIF_ReprEncoder(
        object.ReprEncoder, format='repr', description='Repr. encoder'):
    ...


class KIF_SExpEncoder(
        object.SExpEncoder, format='sexp', description='S-expression encoder'):
    ...


# == KIF_Object ============================================================

class KIF_Object(object.Object, metaclass=object.ObjectMeta):

    #: Template class associated with this object class.
    template_class: ClassVar[type[Template]]

    #: Variable class associated with this object class.
    variable_class: ClassVar[type[Variable]]

    @classmethod
    def _issubclass_template(cls, arg: Any) -> bool:
        ...

    @classmethod
    def _isinstance_template_or_variable(cls, arg: Any) -> bool:
        ...

# -- Codecs ----------------------------------------------------------------

    @classmethod
    def from_json(
        cls,
        s: str,
        **kwargs: Any
    ) -> Self:
        ...

    @classmethod
    def from_repr(
        cls,
        s: str,
        **kwargs: Any
    ) -> Self:
        ...

    @classmethod
    def from_sexp(
        cls,
        s: str,
        **kwargs: Any
    ) -> Self:
        ...

    @classmethod
    def from_sparql(
        cls,
        s: str,
        **kwargs: Any
    ) -> Self:
        ...

    def to_json(self, **kwargs: Any) -> str: ...
    def to_markdown(self, **kwargs: Any) -> str: ...
    def to_repr(self, **kwargs: Any) -> str: ...
    def to_sexp(self, **kwargs: Any) -> str: ...

# -- context ---------------------------------------------------------------

    def __init__(self, *args: Any, context: Optional[Context] = None):
        ...

    @property
    def context(self) -> Context:
        ...

    def get_context(self) -> Context:
        ...

# -- misc ------------------------------------------------------------------

    def _repr_markdown_(self) -> str:
        ...

    def traverse(
        self,
        filter: Optional[Callable[[Any], bool]] = None,
        visit: Optional[Callable[[Any], bool]] = None,
    ) -> Iterator[Any]:
        ...

    def _traverse(
        self,
        filter: Callable[[Any], bool],
        visit: Callable[[Any], bool]
    ) -> Iterator[Any]:
        ...

# -- auto-generated stuff --------------------------------------------------

#
# ** START OF GENERATED CODE **
#
    _AnnotationRecord: type[AnnotationRecord]

    _AnnotationRecordSet: type[AnnotationRecordSet]

    _DataValue: type[DataValue]

    _DataValueTemplate: type[DataValueTemplate]

    _DataValueVariable: type[DataValueVariable]

    _Datatype: type[Datatype]

    _DatatypeVariable: type[DatatypeVariable]

    _DeepDataValue: type[DeepDataValue]

    _DeepDataValueTemplate: type[DeepDataValueTemplate]

    _DeepDataValueVariable: type[DeepDataValueVariable]

    _DeprecatedRank: type[DeprecatedRank]

    _Descriptor: type[Descriptor]

    _Entity: type[Entity]

    _EntityFingerprint: type[EntityFingerprint]

    _EntityTemplate: type[EntityTemplate]

    _EntityVariable: type[EntityVariable]

    _ExternalId: type[ExternalId]

    _ExternalIdDatatype: type[ExternalIdDatatype]

    _ExternalIdTemplate: type[ExternalIdTemplate]

    _ExternalIdVariable: type[ExternalIdVariable]

    _FilterPattern: type[FilterPattern]

    _Fingerprint: type[Fingerprint]

    _IRI: type[IRI]

    _IRI_Datatype: type[IRI_Datatype]

    _IRI_Template: type[IRI_Template]

    _IRI_Variable: type[IRI_Variable]

    _Item: type[Item]

    _ItemDatatype: type[ItemDatatype]

    _ItemDescriptor: type[ItemDescriptor]

    _ItemTemplate: type[ItemTemplate]

    _ItemVariable: type[ItemVariable]

    _KIF_Object: type['KIF_Object']

    _KIF_ObjectSet: type[KIF_ObjectSet]

    _Lexeme: type[Lexeme]

    _LexemeDatatype: type[LexemeDatatype]

    _LexemeDescriptor: type[LexemeDescriptor]

    _LexemeTemplate: type[LexemeTemplate]

    _LexemeVariable: type[LexemeVariable]

    _NoValueSnak: type[NoValueSnak]

    _NoValueSnakTemplate: type[NoValueSnakTemplate]

    _NoValueSnakVariable: type[NoValueSnakVariable]

    _NormalRank: type[NormalRank]

    _Pattern: type[Pattern]

    _PlainDescriptor: type[PlainDescriptor]

    _PreferredRank: type[PreferredRank]

    _Property: type[Property]

    _PropertyDatatype: type[PropertyDatatype]

    _PropertyDescriptor: type[PropertyDescriptor]

    _PropertyFingerprint: type[PropertyFingerprint]

    _PropertyTemplate: type[PropertyTemplate]

    _PropertyVariable: type[PropertyVariable]

    _Quantity: type[Quantity]

    _QuantityDatatype: type[QuantityDatatype]

    _QuantityTemplate: type[QuantityTemplate]

    _QuantityVariable: type[QuantityVariable]

    _Rank: type[Rank]

    _ReferenceRecord: type[ReferenceRecord]

    _ReferenceRecordSet: type[ReferenceRecordSet]

    _ShallowDataValue: type[ShallowDataValue]

    _ShallowDataValueTemplate: type[ShallowDataValueTemplate]

    _ShallowDataValueVariable: type[ShallowDataValueVariable]

    _Snak: type[Snak]

    _SnakSet: type[SnakSet]

    _SnakTemplate: type[SnakTemplate]

    _SnakVariable: type[SnakVariable]

    _SomeValueSnak: type[SomeValueSnak]

    _SomeValueSnakTemplate: type[SomeValueSnakTemplate]

    _SomeValueSnakVariable: type[SomeValueSnakVariable]

    _Statement: type[Statement]

    _StatementTemplate: type[StatementTemplate]

    _StatementVariable: type[StatementVariable]

    _String: type[String]

    _StringDatatype: type[StringDatatype]

    _StringTemplate: type[StringTemplate]

    _StringVariable: type[StringVariable]

    _Template: type[Template]

    _Text: type[Text]

    _TextDatatype: type[TextDatatype]

    _TextSet: type[TextSet]

    _TextTemplate: type[TextTemplate]

    _TextVariable: type[TextVariable]

    _Time: type[Time]

    _TimeDatatype: type[TimeDatatype]

    _TimeTemplate: type[TimeTemplate]

    _TimeVariable: type[TimeVariable]

    _Value: type[Value]

    _ValueSet: type[ValueSet]

    _ValueSnak: type[ValueSnak]

    _ValueSnakTemplate: type[ValueSnakTemplate]

    _ValueSnakVariable: type[ValueSnakVariable]

    _ValueTemplate: type[ValueTemplate]

    _ValueVariable: type[ValueVariable]

    _Variable: type[Variable]

    def is_annotation_record(self) -> bool: ...

    def is_annotation_record_set(self) -> bool: ...

    def is_data_value(self) -> bool: ...

    def is_data_value_template(self) -> bool: ...

    def is_data_value_variable(self) -> bool: ...

    def is_datatype(self) -> bool: ...

    def is_datatype_variable(self) -> bool: ...

    def is_deep_data_value(self) -> bool: ...

    def is_deep_data_value_template(self) -> bool: ...

    def is_deep_data_value_variable(self) -> bool: ...

    def is_deprecated_rank(self) -> bool: ...

    def is_descriptor(self) -> bool: ...

    def is_entity(self) -> bool: ...

    def is_entity_fingerprint(self) -> bool: ...

    def is_entity_template(self) -> bool: ...

    def is_entity_variable(self) -> bool: ...

    def is_external_id(self) -> bool: ...

    def is_external_id_datatype(self) -> bool: ...

    def is_external_id_template(self) -> bool: ...

    def is_external_id_variable(self) -> bool: ...

    def is_filter_pattern(self) -> bool: ...

    def is_fingerprint(self) -> bool: ...

    def is_iri(self) -> bool: ...

    def is_iri_datatype(self) -> bool: ...

    def is_iri_template(self) -> bool: ...

    def is_iri_variable(self) -> bool: ...

    def is_item(self) -> bool: ...

    def is_item_datatype(self) -> bool: ...

    def is_item_descriptor(self) -> bool: ...

    def is_item_template(self) -> bool: ...

    def is_item_variable(self) -> bool: ...

    def is_kif_object(self) -> bool: ...

    def is_kif_object_set(self) -> bool: ...

    def is_lexeme(self) -> bool: ...

    def is_lexeme_datatype(self) -> bool: ...

    def is_lexeme_descriptor(self) -> bool: ...

    def is_lexeme_template(self) -> bool: ...

    def is_lexeme_variable(self) -> bool: ...

    def is_no_value_snak(self) -> bool: ...

    def is_no_value_snak_template(self) -> bool: ...

    def is_no_value_snak_variable(self) -> bool: ...

    def is_normal_rank(self) -> bool: ...

    def is_object(self) -> bool: ...

    def is_pattern(self) -> bool: ...

    def is_plain_descriptor(self) -> bool: ...

    def is_preferred_rank(self) -> bool: ...

    def is_property(self) -> bool: ...

    def is_property_datatype(self) -> bool: ...

    def is_property_descriptor(self) -> bool: ...

    def is_property_fingerprint(self) -> bool: ...

    def is_property_template(self) -> bool: ...

    def is_property_variable(self) -> bool: ...

    def is_quantity(self) -> bool: ...

    def is_quantity_datatype(self) -> bool: ...

    def is_quantity_template(self) -> bool: ...

    def is_quantity_variable(self) -> bool: ...

    def is_rank(self) -> bool: ...

    def is_reference_record(self) -> bool: ...

    def is_reference_record_set(self) -> bool: ...

    def is_shallow_data_value(self) -> bool: ...

    def is_shallow_data_value_template(self) -> bool: ...

    def is_shallow_data_value_variable(self) -> bool: ...

    def is_snak(self) -> bool: ...

    def is_snak_set(self) -> bool: ...

    def is_snak_template(self) -> bool: ...

    def is_snak_variable(self) -> bool: ...

    def is_some_value_snak(self) -> bool: ...

    def is_some_value_snak_template(self) -> bool: ...

    def is_some_value_snak_variable(self) -> bool: ...

    def is_statement(self) -> bool: ...

    def is_statement_template(self) -> bool: ...

    def is_statement_variable(self) -> bool: ...

    def is_string(self) -> bool: ...

    def is_string_datatype(self) -> bool: ...

    def is_string_template(self) -> bool: ...

    def is_string_variable(self) -> bool: ...

    def is_template(self) -> bool: ...

    def is_text(self) -> bool: ...

    def is_text_datatype(self) -> bool: ...

    def is_text_set(self) -> bool: ...

    def is_text_template(self) -> bool: ...

    def is_text_variable(self) -> bool: ...

    def is_time(self) -> bool: ...

    def is_time_datatype(self) -> bool: ...

    def is_time_template(self) -> bool: ...

    def is_time_variable(self) -> bool: ...

    def is_value(self) -> bool: ...

    def is_value_set(self) -> bool: ...

    def is_value_snak(self) -> bool: ...

    def is_value_snak_template(self) -> bool: ...

    def is_value_snak_variable(self) -> bool: ...

    def is_value_template(self) -> bool: ...

    def is_value_variable(self) -> bool: ...

    def is_variable(self) -> bool: ...

    def test_annotation_record(self) -> bool: ...

    def test_annotation_record_set(self) -> bool: ...

    def test_data_value(self) -> bool: ...

    def test_data_value_template(self) -> bool: ...

    def test_data_value_variable(self) -> bool: ...

    def test_datatype(self) -> bool: ...

    def test_datatype_variable(self) -> bool: ...

    def test_deep_data_value(self) -> bool: ...

    def test_deep_data_value_template(self) -> bool: ...

    def test_deep_data_value_variable(self) -> bool: ...

    def test_deprecated_rank(self) -> bool: ...

    def test_descriptor(self) -> bool: ...

    def test_entity(self) -> bool: ...

    def test_entity_fingerprint(self) -> bool: ...

    def test_entity_template(self) -> bool: ...

    def test_entity_variable(self) -> bool: ...

    def test_external_id(self) -> bool: ...

    def test_external_id_datatype(self) -> bool: ...

    def test_external_id_template(self) -> bool: ...

    def test_external_id_variable(self) -> bool: ...

    def test_filter_pattern(self) -> bool: ...

    def test_fingerprint(self) -> bool: ...

    def test_iri(self) -> bool: ...

    def test_iri_datatype(self) -> bool: ...

    def test_iri_template(self) -> bool: ...

    def test_iri_variable(self) -> bool: ...

    def test_item(self) -> bool: ...

    def test_item_datatype(self) -> bool: ...

    def test_item_descriptor(self) -> bool: ...

    def test_item_template(self) -> bool: ...

    def test_item_variable(self) -> bool: ...

    def test_kif_object(self) -> bool: ...

    def test_kif_object_set(self) -> bool: ...

    def test_lexeme(self) -> bool: ...

    def test_lexeme_datatype(self) -> bool: ...

    def test_lexeme_descriptor(self) -> bool: ...

    def test_lexeme_template(self) -> bool: ...

    def test_lexeme_variable(self) -> bool: ...

    def test_no_value_snak(self) -> bool: ...

    def test_no_value_snak_template(self) -> bool: ...

    def test_no_value_snak_variable(self) -> bool: ...

    def test_normal_rank(self) -> bool: ...

    def test_object(self) -> bool: ...

    def test_pattern(self) -> bool: ...

    def test_plain_descriptor(self) -> bool: ...

    def test_preferred_rank(self) -> bool: ...

    def test_property(self) -> bool: ...

    def test_property_datatype(self) -> bool: ...

    def test_property_descriptor(self) -> bool: ...

    def test_property_fingerprint(self) -> bool: ...

    def test_property_template(self) -> bool: ...

    def test_property_variable(self) -> bool: ...

    def test_quantity(self) -> bool: ...

    def test_quantity_datatype(self) -> bool: ...

    def test_quantity_template(self) -> bool: ...

    def test_quantity_variable(self) -> bool: ...

    def test_rank(self) -> bool: ...

    def test_reference_record(self) -> bool: ...

    def test_reference_record_set(self) -> bool: ...

    def test_shallow_data_value(self) -> bool: ...

    def test_shallow_data_value_template(self) -> bool: ...

    def test_shallow_data_value_variable(self) -> bool: ...

    def test_snak(self) -> bool: ...

    def test_snak_set(self) -> bool: ...

    def test_snak_template(self) -> bool: ...

    def test_snak_variable(self) -> bool: ...

    def test_some_value_snak(self) -> bool: ...

    def test_some_value_snak_template(self) -> bool: ...

    def test_some_value_snak_variable(self) -> bool: ...

    def test_statement(self) -> bool: ...

    def test_statement_template(self) -> bool: ...

    def test_statement_variable(self) -> bool: ...

    def test_string(self) -> bool: ...

    def test_string_datatype(self) -> bool: ...

    def test_string_template(self) -> bool: ...

    def test_string_variable(self) -> bool: ...

    def test_template(self) -> bool: ...

    def test_text(self) -> bool: ...

    def test_text_datatype(self) -> bool: ...

    def test_text_set(self) -> bool: ...

    def test_text_template(self) -> bool: ...

    def test_text_variable(self) -> bool: ...

    def test_time(self) -> bool: ...

    def test_time_datatype(self) -> bool: ...

    def test_time_template(self) -> bool: ...

    def test_time_variable(self) -> bool: ...

    def test_value(self) -> bool: ...

    def test_value_set(self) -> bool: ...

    def test_value_snak(self) -> bool: ...

    def test_value_snak_template(self) -> bool: ...

    def test_value_snak_variable(self) -> bool: ...

    def test_value_template(self) -> bool: ...

    def test_value_variable(self) -> bool: ...

    def test_variable(self) -> bool: ...

#
# ** END OF GENERATED CODE **
#
