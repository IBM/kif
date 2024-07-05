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

    @classmethod
    def _check_arg_annotation_record(
            cls,
            arg: AnnotationRecord,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> AnnotationRecord:
        ...

    @classmethod
    def _check_arg_annotation_record_set(
            cls,
            arg: TAnnotationRecordSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> AnnotationRecordSet:
        ...

    @classmethod
    def _check_arg_data_value(
            cls,
            arg: DataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DataValue:
        ...

    @classmethod
    def _check_arg_data_value_template(
            cls,
            arg: DataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DataValueTemplate:
        ...

    @classmethod
    def _check_arg_data_value_variable(
            cls,
            arg: DataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DataValueVariable:
        ...

    @classmethod
    def _check_arg_datatype(
            cls,
            arg: Datatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Datatype:
        ...

    @classmethod
    def _check_arg_datatype_variable(
            cls,
            arg: DatatypeVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DatatypeVariable:
        ...

    @classmethod
    def _check_arg_deep_data_value(
            cls,
            arg: DeepDataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DeepDataValue:
        ...

    @classmethod
    def _check_arg_deep_data_value_template(
            cls,
            arg: DeepDataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DeepDataValueTemplate:
        ...

    @classmethod
    def _check_arg_deep_data_value_variable(
            cls,
            arg: DeepDataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DeepDataValueVariable:
        ...

    @classmethod
    def _check_arg_deprecated_rank(
            cls,
            arg: DeprecatedRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> DeprecatedRank:
        ...

    @classmethod
    def _check_arg_descriptor(
            cls,
            arg: Descriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Descriptor:
        ...

    @classmethod
    def _check_arg_entity(
            cls,
            arg: Entity,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Entity:
        ...

    @classmethod
    def _check_arg_entity_fingerprint(
            cls,
            arg: TEntityFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> EntityFingerprint:
        ...

    @classmethod
    def _check_arg_entity_template(
            cls,
            arg: EntityTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> EntityTemplate:
        ...

    @classmethod
    def _check_arg_entity_variable(
            cls,
            arg: EntityVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> EntityVariable:
        ...

    @classmethod
    def _check_arg_external_id(
            cls,
            arg: TExternalId,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ExternalId:
        ...

    @classmethod
    def _check_arg_external_id_datatype(
            cls,
            arg: ExternalIdDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ExternalIdDatatype:
        ...

    @classmethod
    def _check_arg_external_id_template(
            cls,
            arg: ExternalIdTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ExternalIdTemplate:
        ...

    @classmethod
    def _check_arg_external_id_variable(
            cls,
            arg: ExternalIdVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ExternalIdVariable:
        ...

    @classmethod
    def _check_arg_filter_pattern(
            cls,
            arg: FilterPattern,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> FilterPattern:
        ...

    @classmethod
    def _check_arg_fingerprint(
            cls,
            arg: TFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Fingerprint:
        ...

    @classmethod
    def _check_arg_iri(
            cls,
            arg: T_IRI,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> IRI:
        ...

    @classmethod
    def _check_arg_iri_datatype(
            cls,
            arg: IRI_Datatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> IRI_Datatype:
        ...

    @classmethod
    def _check_arg_iri_template(
            cls,
            arg: IRI_Template,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> IRI_Template:
        ...

    @classmethod
    def _check_arg_iri_variable(
            cls,
            arg: IRI_Variable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> IRI_Variable:
        ...

    @classmethod
    def _check_arg_item(
            cls,
            arg: TItem,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Item:
        ...

    @classmethod
    def _check_arg_item_datatype(
            cls,
            arg: ItemDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ItemDatatype:
        ...

    @classmethod
    def _check_arg_item_descriptor(
            cls,
            arg: ItemDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ItemDescriptor:
        ...

    @classmethod
    def _check_arg_item_template(
            cls,
            arg: ItemTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ItemTemplate:
        ...

    @classmethod
    def _check_arg_item_variable(
            cls,
            arg: ItemVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ItemVariable:
        ...

    @classmethod
    def _check_arg_kif_object(
            cls,
            arg: 'KIF_Object',
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> 'KIF_Object':
        ...

    @classmethod
    def _check_arg_kif_object_set(
            cls,
            arg: KIF_ObjectSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> KIF_ObjectSet:
        ...

    @classmethod
    def _check_arg_lexeme(
            cls,
            arg: TLexeme,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Lexeme:
        ...

    @classmethod
    def _check_arg_lexeme_datatype(
            cls,
            arg: LexemeDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> LexemeDatatype:
        ...

    @classmethod
    def _check_arg_lexeme_descriptor(
            cls,
            arg: LexemeDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> LexemeDescriptor:
        ...

    @classmethod
    def _check_arg_lexeme_template(
            cls,
            arg: LexemeTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> LexemeTemplate:
        ...

    @classmethod
    def _check_arg_lexeme_variable(
            cls,
            arg: LexemeVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> LexemeVariable:
        ...

    @classmethod
    def _check_arg_no_value_snak(
            cls,
            arg: NoValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> NoValueSnak:
        ...

    @classmethod
    def _check_arg_no_value_snak_template(
            cls,
            arg: NoValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> NoValueSnakTemplate:
        ...

    @classmethod
    def _check_arg_no_value_snak_variable(
            cls,
            arg: NoValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> NoValueSnakVariable:
        ...

    @classmethod
    def _check_arg_normal_rank(
            cls,
            arg: NormalRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> NormalRank:
        ...

    @classmethod
    def _check_arg_object(
            cls,
            arg: Object,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Object:
        ...

    @classmethod
    def _check_arg_pattern(
            cls,
            arg: Pattern,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Pattern:
        ...

    @classmethod
    def _check_arg_plain_descriptor(
            cls,
            arg: PlainDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PlainDescriptor:
        ...

    @classmethod
    def _check_arg_preferred_rank(
            cls,
            arg: PreferredRank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PreferredRank:
        ...

    @classmethod
    def _check_arg_property(
            cls,
            arg: TProperty,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Property:
        ...

    @classmethod
    def _check_arg_property_datatype(
            cls,
            arg: PropertyDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PropertyDatatype:
        ...

    @classmethod
    def _check_arg_property_descriptor(
            cls,
            arg: PropertyDescriptor,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PropertyDescriptor:
        ...

    @classmethod
    def _check_arg_property_fingerprint(
            cls,
            arg: TPropertyFingerprint,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PropertyFingerprint:
        ...

    @classmethod
    def _check_arg_property_template(
            cls,
            arg: PropertyTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PropertyTemplate:
        ...

    @classmethod
    def _check_arg_property_variable(
            cls,
            arg: PropertyVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> PropertyVariable:
        ...

    @classmethod
    def _check_arg_quantity(
            cls,
            arg: TQuantity,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Quantity:
        ...

    @classmethod
    def _check_arg_quantity_datatype(
            cls,
            arg: QuantityDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> QuantityDatatype:
        ...

    @classmethod
    def _check_arg_quantity_template(
            cls,
            arg: QuantityTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> QuantityTemplate:
        ...

    @classmethod
    def _check_arg_quantity_variable(
            cls,
            arg: QuantityVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> QuantityVariable:
        ...

    @classmethod
    def _check_arg_rank(
            cls,
            arg: Rank,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Rank:
        ...

    @classmethod
    def _check_arg_reference_record(
            cls,
            arg: TReferenceRecord,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ReferenceRecord:
        ...

    @classmethod
    def _check_arg_reference_record_set(
            cls,
            arg: TReferenceRecordSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ReferenceRecordSet:
        ...

    @classmethod
    def _check_arg_shallow_data_value(
            cls,
            arg: ShallowDataValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ShallowDataValue:
        ...

    @classmethod
    def _check_arg_shallow_data_value_template(
            cls,
            arg: ShallowDataValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ShallowDataValueTemplate:
        ...

    @classmethod
    def _check_arg_shallow_data_value_variable(
            cls,
            arg: ShallowDataValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ShallowDataValueVariable:
        ...

    @classmethod
    def _check_arg_snak(
            cls,
            arg: Snak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Snak:
        ...

    @classmethod
    def _check_arg_snak_set(
            cls,
            arg: TSnakSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SnakSet:
        ...

    @classmethod
    def _check_arg_snak_template(
            cls,
            arg: SnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SnakTemplate:
        ...

    @classmethod
    def _check_arg_snak_variable(
            cls,
            arg: SnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SnakVariable:
        ...

    @classmethod
    def _check_arg_some_value_snak(
            cls,
            arg: SomeValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SomeValueSnak:
        ...

    @classmethod
    def _check_arg_some_value_snak_template(
            cls,
            arg: SomeValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SomeValueSnakTemplate:
        ...

    @classmethod
    def _check_arg_some_value_snak_variable(
            cls,
            arg: SomeValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> SomeValueSnakVariable:
        ...

    @classmethod
    def _check_arg_statement(
            cls,
            arg: Statement,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Statement:
        ...

    @classmethod
    def _check_arg_statement_template(
            cls,
            arg: StatementTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> StatementTemplate:
        ...

    @classmethod
    def _check_arg_statement_variable(
            cls,
            arg: StatementVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> StatementVariable:
        ...

    @classmethod
    def _check_arg_string(
            cls,
            arg: TString,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> String:
        ...

    @classmethod
    def _check_arg_string_datatype(
            cls,
            arg: StringDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> StringDatatype:
        ...

    @classmethod
    def _check_arg_string_template(
            cls,
            arg: StringTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> StringTemplate:
        ...

    @classmethod
    def _check_arg_string_variable(
            cls,
            arg: StringVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> StringVariable:
        ...

    @classmethod
    def _check_arg_template(
            cls,
            arg: Template,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Template:
        ...

    @classmethod
    def _check_arg_text(
            cls,
            arg: TText,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Text:
        ...

    @classmethod
    def _check_arg_text_datatype(
            cls,
            arg: TextDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TextDatatype:
        ...

    @classmethod
    def _check_arg_text_set(
            cls,
            arg: TTextSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TextSet:
        ...

    @classmethod
    def _check_arg_text_template(
            cls,
            arg: TextTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TextTemplate:
        ...

    @classmethod
    def _check_arg_text_variable(
            cls,
            arg: TextVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TextVariable:
        ...

    @classmethod
    def _check_arg_time(
            cls,
            arg: TTime,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Time:
        ...

    @classmethod
    def _check_arg_time_datatype(
            cls,
            arg: TimeDatatype,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TimeDatatype:
        ...

    @classmethod
    def _check_arg_time_template(
            cls,
            arg: TimeTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TimeTemplate:
        ...

    @classmethod
    def _check_arg_time_variable(
            cls,
            arg: TimeVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> TimeVariable:
        ...

    @classmethod
    def _check_arg_value(
            cls,
            arg: TValue,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Value:
        ...

    @classmethod
    def _check_arg_value_set(
            cls,
            arg: TValueSet,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueSet:
        ...

    @classmethod
    def _check_arg_value_snak(
            cls,
            arg: ValueSnak,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueSnak:
        ...

    @classmethod
    def _check_arg_value_snak_template(
            cls,
            arg: ValueSnakTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueSnakTemplate:
        ...

    @classmethod
    def _check_arg_value_snak_variable(
            cls,
            arg: ValueSnakVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueSnakVariable:
        ...

    @classmethod
    def _check_arg_value_template(
            cls,
            arg: ValueTemplate,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueTemplate:
        ...

    @classmethod
    def _check_arg_value_variable(
            cls,
            arg: ValueVariable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> ValueVariable:
        ...

    @classmethod
    def _check_arg_variable(
            cls,
            arg: Variable,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Variable:
        ...

    @classmethod
    def _check_optional_arg_annotation_record(
            cls,
            arg: Optional[AnnotationRecord],
            default: Optional[AnnotationRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[AnnotationRecord]:
        ...

    @classmethod
    def _check_optional_arg_annotation_record_set(
            cls,
            arg: Optional[TAnnotationRecordSet],
            default: Optional[AnnotationRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[AnnotationRecordSet]:
        ...

    @classmethod
    def _check_optional_arg_data_value(
            cls,
            arg: Optional[DataValue],
            default: Optional[DataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DataValue]:
        ...

    @classmethod
    def _check_optional_arg_data_value_template(
            cls,
            arg: Optional[DataValueTemplate],
            default: Optional[DataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DataValueTemplate]:
        ...

    @classmethod
    def _check_optional_arg_data_value_variable(
            cls,
            arg: Optional[DataValueVariable],
            default: Optional[DataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DataValueVariable]:
        ...

    @classmethod
    def _check_optional_arg_datatype(
            cls,
            arg: Optional[Datatype],
            default: Optional[Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Datatype]:
        ...

    @classmethod
    def _check_optional_arg_datatype_variable(
            cls,
            arg: Optional[DatatypeVariable],
            default: Optional[DatatypeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DatatypeVariable]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value(
            cls,
            arg: Optional[DeepDataValue],
            default: Optional[DeepDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DeepDataValue]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value_template(
            cls,
            arg: Optional[DeepDataValueTemplate],
            default: Optional[DeepDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DeepDataValueTemplate]:
        ...

    @classmethod
    def _check_optional_arg_deep_data_value_variable(
            cls,
            arg: Optional[DeepDataValueVariable],
            default: Optional[DeepDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DeepDataValueVariable]:
        ...

    @classmethod
    def _check_optional_arg_deprecated_rank(
            cls,
            arg: Optional[DeprecatedRank],
            default: Optional[DeprecatedRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[DeprecatedRank]:
        ...

    @classmethod
    def _check_optional_arg_descriptor(
            cls,
            arg: Optional[Descriptor],
            default: Optional[Descriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Descriptor]:
        ...

    @classmethod
    def _check_optional_arg_entity(
            cls,
            arg: Optional[Entity],
            default: Optional[Entity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Entity]:
        ...

    @classmethod
    def _check_optional_arg_entity_fingerprint(
            cls,
            arg: Optional[TEntityFingerprint],
            default: Optional[EntityFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[EntityFingerprint]:
        ...

    @classmethod
    def _check_optional_arg_entity_template(
            cls,
            arg: Optional[EntityTemplate],
            default: Optional[EntityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[EntityTemplate]:
        ...

    @classmethod
    def _check_optional_arg_entity_variable(
            cls,
            arg: Optional[EntityVariable],
            default: Optional[EntityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[EntityVariable]:
        ...

    @classmethod
    def _check_optional_arg_external_id(
            cls,
            arg: Optional[TExternalId],
            default: Optional[ExternalId] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ExternalId]:
        ...

    @classmethod
    def _check_optional_arg_external_id_datatype(
            cls,
            arg: Optional[ExternalIdDatatype],
            default: Optional[ExternalIdDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ExternalIdDatatype]:
        ...

    @classmethod
    def _check_optional_arg_external_id_template(
            cls,
            arg: Optional[ExternalIdTemplate],
            default: Optional[ExternalIdTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ExternalIdTemplate]:
        ...

    @classmethod
    def _check_optional_arg_external_id_variable(
            cls,
            arg: Optional[ExternalIdVariable],
            default: Optional[ExternalIdVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ExternalIdVariable]:
        ...

    @classmethod
    def _check_optional_arg_filter_pattern(
            cls,
            arg: Optional[FilterPattern],
            default: Optional[FilterPattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[FilterPattern]:
        ...

    @classmethod
    def _check_optional_arg_fingerprint(
            cls,
            arg: Optional[TFingerprint],
            default: Optional[Fingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Fingerprint]:
        ...

    @classmethod
    def _check_optional_arg_iri(
            cls,
            arg: Optional[T_IRI],
            default: Optional[IRI] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[IRI]:
        ...

    @classmethod
    def _check_optional_arg_iri_datatype(
            cls,
            arg: Optional[IRI_Datatype],
            default: Optional[IRI_Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[IRI_Datatype]:
        ...

    @classmethod
    def _check_optional_arg_iri_template(
            cls,
            arg: Optional[IRI_Template],
            default: Optional[IRI_Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[IRI_Template]:
        ...

    @classmethod
    def _check_optional_arg_iri_variable(
            cls,
            arg: Optional[IRI_Variable],
            default: Optional[IRI_Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[IRI_Variable]:
        ...

    @classmethod
    def _check_optional_arg_item(
            cls,
            arg: Optional[TItem],
            default: Optional[Item] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Item]:
        ...

    @classmethod
    def _check_optional_arg_item_datatype(
            cls,
            arg: Optional[ItemDatatype],
            default: Optional[ItemDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ItemDatatype]:
        ...

    @classmethod
    def _check_optional_arg_item_descriptor(
            cls,
            arg: Optional[ItemDescriptor],
            default: Optional[ItemDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ItemDescriptor]:
        ...

    @classmethod
    def _check_optional_arg_item_template(
            cls,
            arg: Optional[ItemTemplate],
            default: Optional[ItemTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ItemTemplate]:
        ...

    @classmethod
    def _check_optional_arg_item_variable(
            cls,
            arg: Optional[ItemVariable],
            default: Optional[ItemVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ItemVariable]:
        ...

    @classmethod
    def _check_optional_arg_kif_object(
            cls,
            arg: Optional['KIF_Object'],
            default: Optional['KIF_Object'] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional['KIF_Object']:
        ...

    @classmethod
    def _check_optional_arg_kif_object_set(
            cls,
            arg: Optional[KIF_ObjectSet],
            default: Optional[KIF_ObjectSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[KIF_ObjectSet]:
        ...

    @classmethod
    def _check_optional_arg_lexeme(
            cls,
            arg: Optional[TLexeme],
            default: Optional[Lexeme] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Lexeme]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_datatype(
            cls,
            arg: Optional[LexemeDatatype],
            default: Optional[LexemeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[LexemeDatatype]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_descriptor(
            cls,
            arg: Optional[LexemeDescriptor],
            default: Optional[LexemeDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[LexemeDescriptor]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_template(
            cls,
            arg: Optional[LexemeTemplate],
            default: Optional[LexemeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[LexemeTemplate]:
        ...

    @classmethod
    def _check_optional_arg_lexeme_variable(
            cls,
            arg: Optional[LexemeVariable],
            default: Optional[LexemeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[LexemeVariable]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak(
            cls,
            arg: Optional[NoValueSnak],
            default: Optional[NoValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[NoValueSnak]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak_template(
            cls,
            arg: Optional[NoValueSnakTemplate],
            default: Optional[NoValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[NoValueSnakTemplate]:
        ...

    @classmethod
    def _check_optional_arg_no_value_snak_variable(
            cls,
            arg: Optional[NoValueSnakVariable],
            default: Optional[NoValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[NoValueSnakVariable]:
        ...

    @classmethod
    def _check_optional_arg_normal_rank(
            cls,
            arg: Optional[NormalRank],
            default: Optional[NormalRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[NormalRank]:
        ...

    @classmethod
    def _check_optional_arg_object(
            cls,
            arg: Optional[Object],
            default: Optional[Object] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Object]:
        ...

    @classmethod
    def _check_optional_arg_pattern(
            cls,
            arg: Optional[Pattern],
            default: Optional[Pattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Pattern]:
        ...

    @classmethod
    def _check_optional_arg_plain_descriptor(
            cls,
            arg: Optional[PlainDescriptor],
            default: Optional[PlainDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PlainDescriptor]:
        ...

    @classmethod
    def _check_optional_arg_preferred_rank(
            cls,
            arg: Optional[PreferredRank],
            default: Optional[PreferredRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PreferredRank]:
        ...

    @classmethod
    def _check_optional_arg_property(
            cls,
            arg: Optional[TProperty],
            default: Optional[Property] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Property]:
        ...

    @classmethod
    def _check_optional_arg_property_datatype(
            cls,
            arg: Optional[PropertyDatatype],
            default: Optional[PropertyDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PropertyDatatype]:
        ...

    @classmethod
    def _check_optional_arg_property_descriptor(
            cls,
            arg: Optional[PropertyDescriptor],
            default: Optional[PropertyDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PropertyDescriptor]:
        ...

    @classmethod
    def _check_optional_arg_property_fingerprint(
            cls,
            arg: Optional[TPropertyFingerprint],
            default: Optional[PropertyFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PropertyFingerprint]:
        ...

    @classmethod
    def _check_optional_arg_property_template(
            cls,
            arg: Optional[PropertyTemplate],
            default: Optional[PropertyTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PropertyTemplate]:
        ...

    @classmethod
    def _check_optional_arg_property_variable(
            cls,
            arg: Optional[PropertyVariable],
            default: Optional[PropertyVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[PropertyVariable]:
        ...

    @classmethod
    def _check_optional_arg_quantity(
            cls,
            arg: Optional[TQuantity],
            default: Optional[Quantity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Quantity]:
        ...

    @classmethod
    def _check_optional_arg_quantity_datatype(
            cls,
            arg: Optional[QuantityDatatype],
            default: Optional[QuantityDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[QuantityDatatype]:
        ...

    @classmethod
    def _check_optional_arg_quantity_template(
            cls,
            arg: Optional[QuantityTemplate],
            default: Optional[QuantityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[QuantityTemplate]:
        ...

    @classmethod
    def _check_optional_arg_quantity_variable(
            cls,
            arg: Optional[QuantityVariable],
            default: Optional[QuantityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[QuantityVariable]:
        ...

    @classmethod
    def _check_optional_arg_rank(
            cls,
            arg: Optional[Rank],
            default: Optional[Rank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Rank]:
        ...

    @classmethod
    def _check_optional_arg_reference_record(
            cls,
            arg: Optional[TReferenceRecord],
            default: Optional[ReferenceRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ReferenceRecord]:
        ...

    @classmethod
    def _check_optional_arg_reference_record_set(
            cls,
            arg: Optional[TReferenceRecordSet],
            default: Optional[ReferenceRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ReferenceRecordSet]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value(
            cls,
            arg: Optional[ShallowDataValue],
            default: Optional[ShallowDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ShallowDataValue]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value_template(
            cls,
            arg: Optional[ShallowDataValueTemplate],
            default: Optional[ShallowDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ShallowDataValueTemplate]:
        ...

    @classmethod
    def _check_optional_arg_shallow_data_value_variable(
            cls,
            arg: Optional[ShallowDataValueVariable],
            default: Optional[ShallowDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ShallowDataValueVariable]:
        ...

    @classmethod
    def _check_optional_arg_snak(
            cls,
            arg: Optional[Snak],
            default: Optional[Snak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Snak]:
        ...

    @classmethod
    def _check_optional_arg_snak_set(
            cls,
            arg: Optional[TSnakSet],
            default: Optional[SnakSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SnakSet]:
        ...

    @classmethod
    def _check_optional_arg_snak_template(
            cls,
            arg: Optional[SnakTemplate],
            default: Optional[SnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SnakTemplate]:
        ...

    @classmethod
    def _check_optional_arg_snak_variable(
            cls,
            arg: Optional[SnakVariable],
            default: Optional[SnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SnakVariable]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak(
            cls,
            arg: Optional[SomeValueSnak],
            default: Optional[SomeValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SomeValueSnak]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak_template(
            cls,
            arg: Optional[SomeValueSnakTemplate],
            default: Optional[SomeValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SomeValueSnakTemplate]:
        ...

    @classmethod
    def _check_optional_arg_some_value_snak_variable(
            cls,
            arg: Optional[SomeValueSnakVariable],
            default: Optional[SomeValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[SomeValueSnakVariable]:
        ...

    @classmethod
    def _check_optional_arg_statement(
            cls,
            arg: Optional[Statement],
            default: Optional[Statement] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Statement]:
        ...

    @classmethod
    def _check_optional_arg_statement_template(
            cls,
            arg: Optional[StatementTemplate],
            default: Optional[StatementTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[StatementTemplate]:
        ...

    @classmethod
    def _check_optional_arg_statement_variable(
            cls,
            arg: Optional[StatementVariable],
            default: Optional[StatementVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[StatementVariable]:
        ...

    @classmethod
    def _check_optional_arg_string(
            cls,
            arg: Optional[TString],
            default: Optional[String] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[String]:
        ...

    @classmethod
    def _check_optional_arg_string_datatype(
            cls,
            arg: Optional[StringDatatype],
            default: Optional[StringDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[StringDatatype]:
        ...

    @classmethod
    def _check_optional_arg_string_template(
            cls,
            arg: Optional[StringTemplate],
            default: Optional[StringTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[StringTemplate]:
        ...

    @classmethod
    def _check_optional_arg_string_variable(
            cls,
            arg: Optional[StringVariable],
            default: Optional[StringVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[StringVariable]:
        ...

    @classmethod
    def _check_optional_arg_template(
            cls,
            arg: Optional[Template],
            default: Optional[Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Template]:
        ...

    @classmethod
    def _check_optional_arg_text(
            cls,
            arg: Optional[TText],
            default: Optional[Text] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Text]:
        ...

    @classmethod
    def _check_optional_arg_text_datatype(
            cls,
            arg: Optional[TextDatatype],
            default: Optional[TextDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TextDatatype]:
        ...

    @classmethod
    def _check_optional_arg_text_set(
            cls,
            arg: Optional[TTextSet],
            default: Optional[TextSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TextSet]:
        ...

    @classmethod
    def _check_optional_arg_text_template(
            cls,
            arg: Optional[TextTemplate],
            default: Optional[TextTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TextTemplate]:
        ...

    @classmethod
    def _check_optional_arg_text_variable(
            cls,
            arg: Optional[TextVariable],
            default: Optional[TextVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TextVariable]:
        ...

    @classmethod
    def _check_optional_arg_time(
            cls,
            arg: Optional[TTime],
            default: Optional[Time] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Time]:
        ...

    @classmethod
    def _check_optional_arg_time_datatype(
            cls,
            arg: Optional[TimeDatatype],
            default: Optional[TimeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TimeDatatype]:
        ...

    @classmethod
    def _check_optional_arg_time_template(
            cls,
            arg: Optional[TimeTemplate],
            default: Optional[TimeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TimeTemplate]:
        ...

    @classmethod
    def _check_optional_arg_time_variable(
            cls,
            arg: Optional[TimeVariable],
            default: Optional[TimeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[TimeVariable]:
        ...

    @classmethod
    def _check_optional_arg_value(
            cls,
            arg: Optional[TValue],
            default: Optional[Value] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Value]:
        ...

    @classmethod
    def _check_optional_arg_value_set(
            cls,
            arg: Optional[TValueSet],
            default: Optional[ValueSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueSet]:
        ...

    @classmethod
    def _check_optional_arg_value_snak(
            cls,
            arg: Optional[ValueSnak],
            default: Optional[ValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueSnak]:
        ...

    @classmethod
    def _check_optional_arg_value_snak_template(
            cls,
            arg: Optional[ValueSnakTemplate],
            default: Optional[ValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueSnakTemplate]:
        ...

    @classmethod
    def _check_optional_arg_value_snak_variable(
            cls,
            arg: Optional[ValueSnakVariable],
            default: Optional[ValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueSnakVariable]:
        ...

    @classmethod
    def _check_optional_arg_value_template(
            cls,
            arg: Optional[ValueTemplate],
            default: Optional[ValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueTemplate]:
        ...

    @classmethod
    def _check_optional_arg_value_variable(
            cls,
            arg: Optional[ValueVariable],
            default: Optional[ValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[ValueVariable]:
        ...

    @classmethod
    def _check_optional_arg_variable(
            cls,
            arg: Optional[Variable],
            default: Optional[Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
            name: Optional[str] = ...,
            position: Optional[int] = ...
    ) -> Optional[Variable]:
        ...

    @classmethod
    def _preprocess_arg_annotation_record(
            cls,
            arg: AnnotationRecord,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> AnnotationRecord:
        ...

    @classmethod
    def _preprocess_arg_annotation_record_set(
            cls,
            arg: TAnnotationRecordSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> AnnotationRecordSet:
        ...

    @classmethod
    def _preprocess_arg_data_value(
            cls,
            arg: DataValue,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DataValue:
        ...

    @classmethod
    def _preprocess_arg_data_value_template(
            cls,
            arg: DataValueTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DataValueTemplate:
        ...

    @classmethod
    def _preprocess_arg_data_value_variable(
            cls,
            arg: DataValueVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DataValueVariable:
        ...

    @classmethod
    def _preprocess_arg_datatype(
            cls,
            arg: Datatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Datatype:
        ...

    @classmethod
    def _preprocess_arg_datatype_variable(
            cls,
            arg: DatatypeVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DatatypeVariable:
        ...

    @classmethod
    def _preprocess_arg_deep_data_value(
            cls,
            arg: DeepDataValue,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DeepDataValue:
        ...

    @classmethod
    def _preprocess_arg_deep_data_value_template(
            cls,
            arg: DeepDataValueTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DeepDataValueTemplate:
        ...

    @classmethod
    def _preprocess_arg_deep_data_value_variable(
            cls,
            arg: DeepDataValueVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DeepDataValueVariable:
        ...

    @classmethod
    def _preprocess_arg_deprecated_rank(
            cls,
            arg: DeprecatedRank,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> DeprecatedRank:
        ...

    @classmethod
    def _preprocess_arg_descriptor(
            cls,
            arg: Descriptor,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Descriptor:
        ...

    @classmethod
    def _preprocess_arg_entity(
            cls,
            arg: Entity,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Entity:
        ...

    @classmethod
    def _preprocess_arg_entity_fingerprint(
            cls,
            arg: TEntityFingerprint,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> EntityFingerprint:
        ...

    @classmethod
    def _preprocess_arg_entity_template(
            cls,
            arg: EntityTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> EntityTemplate:
        ...

    @classmethod
    def _preprocess_arg_entity_variable(
            cls,
            arg: EntityVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> EntityVariable:
        ...

    @classmethod
    def _preprocess_arg_external_id(
            cls,
            arg: TExternalId,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ExternalId:
        ...

    @classmethod
    def _preprocess_arg_external_id_datatype(
            cls,
            arg: ExternalIdDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ExternalIdDatatype:
        ...

    @classmethod
    def _preprocess_arg_external_id_template(
            cls,
            arg: ExternalIdTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ExternalIdTemplate:
        ...

    @classmethod
    def _preprocess_arg_external_id_variable(
            cls,
            arg: ExternalIdVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ExternalIdVariable:
        ...

    @classmethod
    def _preprocess_arg_filter_pattern(
            cls,
            arg: FilterPattern,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> FilterPattern:
        ...

    @classmethod
    def _preprocess_arg_fingerprint(
            cls,
            arg: TFingerprint,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Fingerprint:
        ...

    @classmethod
    def _preprocess_arg_iri(
            cls,
            arg: T_IRI,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> IRI:
        ...

    @classmethod
    def _preprocess_arg_iri_datatype(
            cls,
            arg: IRI_Datatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> IRI_Datatype:
        ...

    @classmethod
    def _preprocess_arg_iri_template(
            cls,
            arg: IRI_Template,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> IRI_Template:
        ...

    @classmethod
    def _preprocess_arg_iri_variable(
            cls,
            arg: IRI_Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> IRI_Variable:
        ...

    @classmethod
    def _preprocess_arg_item(
            cls,
            arg: TItem,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Item:
        ...

    @classmethod
    def _preprocess_arg_item_datatype(
            cls,
            arg: ItemDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ItemDatatype:
        ...

    @classmethod
    def _preprocess_arg_item_descriptor(
            cls,
            arg: ItemDescriptor,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ItemDescriptor:
        ...

    @classmethod
    def _preprocess_arg_item_template(
            cls,
            arg: ItemTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ItemTemplate:
        ...

    @classmethod
    def _preprocess_arg_item_variable(
            cls,
            arg: ItemVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ItemVariable:
        ...

    @classmethod
    def _preprocess_arg_kif_object(
            cls,
            arg: 'KIF_Object',
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> 'KIF_Object':
        ...

    @classmethod
    def _preprocess_arg_kif_object_set(
            cls,
            arg: KIF_ObjectSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> KIF_ObjectSet:
        ...

    @classmethod
    def _preprocess_arg_lexeme(
            cls,
            arg: TLexeme,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Lexeme:
        ...

    @classmethod
    def _preprocess_arg_lexeme_datatype(
            cls,
            arg: LexemeDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> LexemeDatatype:
        ...

    @classmethod
    def _preprocess_arg_lexeme_descriptor(
            cls,
            arg: LexemeDescriptor,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> LexemeDescriptor:
        ...

    @classmethod
    def _preprocess_arg_lexeme_template(
            cls,
            arg: LexemeTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> LexemeTemplate:
        ...

    @classmethod
    def _preprocess_arg_lexeme_variable(
            cls,
            arg: LexemeVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> LexemeVariable:
        ...

    @classmethod
    def _preprocess_arg_no_value_snak(
            cls,
            arg: NoValueSnak,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> NoValueSnak:
        ...

    @classmethod
    def _preprocess_arg_no_value_snak_template(
            cls,
            arg: NoValueSnakTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> NoValueSnakTemplate:
        ...

    @classmethod
    def _preprocess_arg_no_value_snak_variable(
            cls,
            arg: NoValueSnakVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> NoValueSnakVariable:
        ...

    @classmethod
    def _preprocess_arg_normal_rank(
            cls,
            arg: NormalRank,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> NormalRank:
        ...

    @classmethod
    def _preprocess_arg_object(
            cls,
            arg: Object,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Object:
        ...

    @classmethod
    def _preprocess_arg_pattern(
            cls,
            arg: Pattern,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Pattern:
        ...

    @classmethod
    def _preprocess_arg_plain_descriptor(
            cls,
            arg: PlainDescriptor,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PlainDescriptor:
        ...

    @classmethod
    def _preprocess_arg_preferred_rank(
            cls,
            arg: PreferredRank,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PreferredRank:
        ...

    @classmethod
    def _preprocess_arg_property(
            cls,
            arg: TProperty,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Property:
        ...

    @classmethod
    def _preprocess_arg_property_datatype(
            cls,
            arg: PropertyDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PropertyDatatype:
        ...

    @classmethod
    def _preprocess_arg_property_descriptor(
            cls,
            arg: PropertyDescriptor,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PropertyDescriptor:
        ...

    @classmethod
    def _preprocess_arg_property_fingerprint(
            cls,
            arg: TPropertyFingerprint,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PropertyFingerprint:
        ...

    @classmethod
    def _preprocess_arg_property_template(
            cls,
            arg: PropertyTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PropertyTemplate:
        ...

    @classmethod
    def _preprocess_arg_property_variable(
            cls,
            arg: PropertyVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> PropertyVariable:
        ...

    @classmethod
    def _preprocess_arg_quantity(
            cls,
            arg: TQuantity,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Quantity:
        ...

    @classmethod
    def _preprocess_arg_quantity_datatype(
            cls,
            arg: QuantityDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> QuantityDatatype:
        ...

    @classmethod
    def _preprocess_arg_quantity_template(
            cls,
            arg: QuantityTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> QuantityTemplate:
        ...

    @classmethod
    def _preprocess_arg_quantity_variable(
            cls,
            arg: QuantityVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> QuantityVariable:
        ...

    @classmethod
    def _preprocess_arg_rank(
            cls,
            arg: Rank,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Rank:
        ...

    @classmethod
    def _preprocess_arg_reference_record(
            cls,
            arg: TReferenceRecord,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ReferenceRecord:
        ...

    @classmethod
    def _preprocess_arg_reference_record_set(
            cls,
            arg: TReferenceRecordSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ReferenceRecordSet:
        ...

    @classmethod
    def _preprocess_arg_shallow_data_value(
            cls,
            arg: ShallowDataValue,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ShallowDataValue:
        ...

    @classmethod
    def _preprocess_arg_shallow_data_value_template(
            cls,
            arg: ShallowDataValueTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ShallowDataValueTemplate:
        ...

    @classmethod
    def _preprocess_arg_shallow_data_value_variable(
            cls,
            arg: ShallowDataValueVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ShallowDataValueVariable:
        ...

    @classmethod
    def _preprocess_arg_snak(
            cls,
            arg: Snak,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Snak:
        ...

    @classmethod
    def _preprocess_arg_snak_set(
            cls,
            arg: TSnakSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SnakSet:
        ...

    @classmethod
    def _preprocess_arg_snak_template(
            cls,
            arg: SnakTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SnakTemplate:
        ...

    @classmethod
    def _preprocess_arg_snak_variable(
            cls,
            arg: SnakVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SnakVariable:
        ...

    @classmethod
    def _preprocess_arg_some_value_snak(
            cls,
            arg: SomeValueSnak,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SomeValueSnak:
        ...

    @classmethod
    def _preprocess_arg_some_value_snak_template(
            cls,
            arg: SomeValueSnakTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SomeValueSnakTemplate:
        ...

    @classmethod
    def _preprocess_arg_some_value_snak_variable(
            cls,
            arg: SomeValueSnakVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> SomeValueSnakVariable:
        ...

    @classmethod
    def _preprocess_arg_statement(
            cls,
            arg: Statement,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Statement:
        ...

    @classmethod
    def _preprocess_arg_statement_template(
            cls,
            arg: StatementTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> StatementTemplate:
        ...

    @classmethod
    def _preprocess_arg_statement_variable(
            cls,
            arg: StatementVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> StatementVariable:
        ...

    @classmethod
    def _preprocess_arg_string(
            cls,
            arg: TString,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> String:
        ...

    @classmethod
    def _preprocess_arg_string_datatype(
            cls,
            arg: StringDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> StringDatatype:
        ...

    @classmethod
    def _preprocess_arg_string_template(
            cls,
            arg: StringTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> StringTemplate:
        ...

    @classmethod
    def _preprocess_arg_string_variable(
            cls,
            arg: StringVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> StringVariable:
        ...

    @classmethod
    def _preprocess_arg_template(
            cls,
            arg: Template,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Template:
        ...

    @classmethod
    def _preprocess_arg_text(
            cls,
            arg: TText,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Text:
        ...

    @classmethod
    def _preprocess_arg_text_datatype(
            cls,
            arg: TextDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TextDatatype:
        ...

    @classmethod
    def _preprocess_arg_text_set(
            cls,
            arg: TTextSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TextSet:
        ...

    @classmethod
    def _preprocess_arg_text_template(
            cls,
            arg: TextTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TextTemplate:
        ...

    @classmethod
    def _preprocess_arg_text_variable(
            cls,
            arg: TextVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TextVariable:
        ...

    @classmethod
    def _preprocess_arg_time(
            cls,
            arg: TTime,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Time:
        ...

    @classmethod
    def _preprocess_arg_time_datatype(
            cls,
            arg: TimeDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TimeDatatype:
        ...

    @classmethod
    def _preprocess_arg_time_template(
            cls,
            arg: TimeTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TimeTemplate:
        ...

    @classmethod
    def _preprocess_arg_time_variable(
            cls,
            arg: TimeVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> TimeVariable:
        ...

    @classmethod
    def _preprocess_arg_value(
            cls,
            arg: TValue,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Value:
        ...

    @classmethod
    def _preprocess_arg_value_set(
            cls,
            arg: TValueSet,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueSet:
        ...

    @classmethod
    def _preprocess_arg_value_snak(
            cls,
            arg: ValueSnak,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueSnak:
        ...

    @classmethod
    def _preprocess_arg_value_snak_template(
            cls,
            arg: ValueSnakTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueSnakTemplate:
        ...

    @classmethod
    def _preprocess_arg_value_snak_variable(
            cls,
            arg: ValueSnakVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueSnakVariable:
        ...

    @classmethod
    def _preprocess_arg_value_template(
            cls,
            arg: ValueTemplate,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueTemplate:
        ...

    @classmethod
    def _preprocess_arg_value_variable(
            cls,
            arg: ValueVariable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> ValueVariable:
        ...

    @classmethod
    def _preprocess_arg_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = ...
    ) -> Variable:
        ...

    @classmethod
    def _preprocess_optional_arg_annotation_record(
            cls,
            arg: Optional[AnnotationRecord],
            i: int,
            default: Optional[AnnotationRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[AnnotationRecord]:
        ...

    @classmethod
    def _preprocess_optional_arg_annotation_record_set(
            cls,
            arg: Optional[TAnnotationRecordSet],
            i: int,
            default: Optional[AnnotationRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[AnnotationRecordSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_data_value(
            cls,
            arg: Optional[DataValue],
            i: int,
            default: Optional[DataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DataValue]:
        ...

    @classmethod
    def _preprocess_optional_arg_data_value_template(
            cls,
            arg: Optional[DataValueTemplate],
            i: int,
            default: Optional[DataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DataValueTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_data_value_variable(
            cls,
            arg: Optional[DataValueVariable],
            i: int,
            default: Optional[DataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DataValueVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_datatype(
            cls,
            arg: Optional[Datatype],
            i: int,
            default: Optional[Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Datatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_datatype_variable(
            cls,
            arg: Optional[DatatypeVariable],
            i: int,
            default: Optional[DatatypeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DatatypeVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_deep_data_value(
            cls,
            arg: Optional[DeepDataValue],
            i: int,
            default: Optional[DeepDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DeepDataValue]:
        ...

    @classmethod
    def _preprocess_optional_arg_deep_data_value_template(
            cls,
            arg: Optional[DeepDataValueTemplate],
            i: int,
            default: Optional[DeepDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DeepDataValueTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_deep_data_value_variable(
            cls,
            arg: Optional[DeepDataValueVariable],
            i: int,
            default: Optional[DeepDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DeepDataValueVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_deprecated_rank(
            cls,
            arg: Optional[DeprecatedRank],
            i: int,
            default: Optional[DeprecatedRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[DeprecatedRank]:
        ...

    @classmethod
    def _preprocess_optional_arg_descriptor(
            cls,
            arg: Optional[Descriptor],
            i: int,
            default: Optional[Descriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Descriptor]:
        ...

    @classmethod
    def _preprocess_optional_arg_entity(
            cls,
            arg: Optional[Entity],
            i: int,
            default: Optional[Entity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Entity]:
        ...

    @classmethod
    def _preprocess_optional_arg_entity_fingerprint(
            cls,
            arg: Optional[TEntityFingerprint],
            i: int,
            default: Optional[EntityFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[EntityFingerprint]:
        ...

    @classmethod
    def _preprocess_optional_arg_entity_template(
            cls,
            arg: Optional[EntityTemplate],
            i: int,
            default: Optional[EntityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[EntityTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_entity_variable(
            cls,
            arg: Optional[EntityVariable],
            i: int,
            default: Optional[EntityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[EntityVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_external_id(
            cls,
            arg: Optional[TExternalId],
            i: int,
            default: Optional[ExternalId] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ExternalId]:
        ...

    @classmethod
    def _preprocess_optional_arg_external_id_datatype(
            cls,
            arg: Optional[ExternalIdDatatype],
            i: int,
            default: Optional[ExternalIdDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ExternalIdDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_external_id_template(
            cls,
            arg: Optional[ExternalIdTemplate],
            i: int,
            default: Optional[ExternalIdTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ExternalIdTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_external_id_variable(
            cls,
            arg: Optional[ExternalIdVariable],
            i: int,
            default: Optional[ExternalIdVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ExternalIdVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_filter_pattern(
            cls,
            arg: Optional[FilterPattern],
            i: int,
            default: Optional[FilterPattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[FilterPattern]:
        ...

    @classmethod
    def _preprocess_optional_arg_fingerprint(
            cls,
            arg: Optional[TFingerprint],
            i: int,
            default: Optional[Fingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Fingerprint]:
        ...

    @classmethod
    def _preprocess_optional_arg_iri(
            cls,
            arg: Optional[T_IRI],
            i: int,
            default: Optional[IRI] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[IRI]:
        ...

    @classmethod
    def _preprocess_optional_arg_iri_datatype(
            cls,
            arg: Optional[IRI_Datatype],
            i: int,
            default: Optional[IRI_Datatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[IRI_Datatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_iri_template(
            cls,
            arg: Optional[IRI_Template],
            i: int,
            default: Optional[IRI_Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[IRI_Template]:
        ...

    @classmethod
    def _preprocess_optional_arg_iri_variable(
            cls,
            arg: Optional[IRI_Variable],
            i: int,
            default: Optional[IRI_Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[IRI_Variable]:
        ...

    @classmethod
    def _preprocess_optional_arg_item(
            cls,
            arg: Optional[TItem],
            i: int,
            default: Optional[Item] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Item]:
        ...

    @classmethod
    def _preprocess_optional_arg_item_datatype(
            cls,
            arg: Optional[ItemDatatype],
            i: int,
            default: Optional[ItemDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ItemDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_item_descriptor(
            cls,
            arg: Optional[ItemDescriptor],
            i: int,
            default: Optional[ItemDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ItemDescriptor]:
        ...

    @classmethod
    def _preprocess_optional_arg_item_template(
            cls,
            arg: Optional[ItemTemplate],
            i: int,
            default: Optional[ItemTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ItemTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_item_variable(
            cls,
            arg: Optional[ItemVariable],
            i: int,
            default: Optional[ItemVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ItemVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_kif_object(
            cls,
            arg: Optional['KIF_Object'],
            i: int,
            default: Optional['KIF_Object'] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional['KIF_Object']:
        ...

    @classmethod
    def _preprocess_optional_arg_kif_object_set(
            cls,
            arg: Optional[KIF_ObjectSet],
            i: int,
            default: Optional[KIF_ObjectSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[KIF_ObjectSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_lexeme(
            cls,
            arg: Optional[TLexeme],
            i: int,
            default: Optional[Lexeme] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Lexeme]:
        ...

    @classmethod
    def _preprocess_optional_arg_lexeme_datatype(
            cls,
            arg: Optional[LexemeDatatype],
            i: int,
            default: Optional[LexemeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[LexemeDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_lexeme_descriptor(
            cls,
            arg: Optional[LexemeDescriptor],
            i: int,
            default: Optional[LexemeDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[LexemeDescriptor]:
        ...

    @classmethod
    def _preprocess_optional_arg_lexeme_template(
            cls,
            arg: Optional[LexemeTemplate],
            i: int,
            default: Optional[LexemeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[LexemeTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_lexeme_variable(
            cls,
            arg: Optional[LexemeVariable],
            i: int,
            default: Optional[LexemeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[LexemeVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_no_value_snak(
            cls,
            arg: Optional[NoValueSnak],
            i: int,
            default: Optional[NoValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[NoValueSnak]:
        ...

    @classmethod
    def _preprocess_optional_arg_no_value_snak_template(
            cls,
            arg: Optional[NoValueSnakTemplate],
            i: int,
            default: Optional[NoValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[NoValueSnakTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_no_value_snak_variable(
            cls,
            arg: Optional[NoValueSnakVariable],
            i: int,
            default: Optional[NoValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[NoValueSnakVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_normal_rank(
            cls,
            arg: Optional[NormalRank],
            i: int,
            default: Optional[NormalRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[NormalRank]:
        ...

    @classmethod
    def _preprocess_optional_arg_object(
            cls,
            arg: Optional[Object],
            i: int,
            default: Optional[Object] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Object]:
        ...

    @classmethod
    def _preprocess_optional_arg_pattern(
            cls,
            arg: Optional[Pattern],
            i: int,
            default: Optional[Pattern] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Pattern]:
        ...

    @classmethod
    def _preprocess_optional_arg_plain_descriptor(
            cls,
            arg: Optional[PlainDescriptor],
            i: int,
            default: Optional[PlainDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PlainDescriptor]:
        ...

    @classmethod
    def _preprocess_optional_arg_preferred_rank(
            cls,
            arg: Optional[PreferredRank],
            i: int,
            default: Optional[PreferredRank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PreferredRank]:
        ...

    @classmethod
    def _preprocess_optional_arg_property(
            cls,
            arg: Optional[TProperty],
            i: int,
            default: Optional[Property] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Property]:
        ...

    @classmethod
    def _preprocess_optional_arg_property_datatype(
            cls,
            arg: Optional[PropertyDatatype],
            i: int,
            default: Optional[PropertyDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PropertyDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_property_descriptor(
            cls,
            arg: Optional[PropertyDescriptor],
            i: int,
            default: Optional[PropertyDescriptor] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PropertyDescriptor]:
        ...

    @classmethod
    def _preprocess_optional_arg_property_fingerprint(
            cls,
            arg: Optional[TPropertyFingerprint],
            i: int,
            default: Optional[PropertyFingerprint] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PropertyFingerprint]:
        ...

    @classmethod
    def _preprocess_optional_arg_property_template(
            cls,
            arg: Optional[PropertyTemplate],
            i: int,
            default: Optional[PropertyTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PropertyTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_property_variable(
            cls,
            arg: Optional[PropertyVariable],
            i: int,
            default: Optional[PropertyVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[PropertyVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_quantity(
            cls,
            arg: Optional[TQuantity],
            i: int,
            default: Optional[Quantity] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Quantity]:
        ...

    @classmethod
    def _preprocess_optional_arg_quantity_datatype(
            cls,
            arg: Optional[QuantityDatatype],
            i: int,
            default: Optional[QuantityDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[QuantityDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_quantity_template(
            cls,
            arg: Optional[QuantityTemplate],
            i: int,
            default: Optional[QuantityTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[QuantityTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_quantity_variable(
            cls,
            arg: Optional[QuantityVariable],
            i: int,
            default: Optional[QuantityVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[QuantityVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_rank(
            cls,
            arg: Optional[Rank],
            i: int,
            default: Optional[Rank] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Rank]:
        ...

    @classmethod
    def _preprocess_optional_arg_reference_record(
            cls,
            arg: Optional[TReferenceRecord],
            i: int,
            default: Optional[ReferenceRecord] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ReferenceRecord]:
        ...

    @classmethod
    def _preprocess_optional_arg_reference_record_set(
            cls,
            arg: Optional[TReferenceRecordSet],
            i: int,
            default: Optional[ReferenceRecordSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ReferenceRecordSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_shallow_data_value(
            cls,
            arg: Optional[ShallowDataValue],
            i: int,
            default: Optional[ShallowDataValue] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ShallowDataValue]:
        ...

    @classmethod
    def _preprocess_optional_arg_shallow_data_value_template(
            cls,
            arg: Optional[ShallowDataValueTemplate],
            i: int,
            default: Optional[ShallowDataValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ShallowDataValueTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_shallow_data_value_variable(
            cls,
            arg: Optional[ShallowDataValueVariable],
            i: int,
            default: Optional[ShallowDataValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ShallowDataValueVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_snak(
            cls,
            arg: Optional[Snak],
            i: int,
            default: Optional[Snak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Snak]:
        ...

    @classmethod
    def _preprocess_optional_arg_snak_set(
            cls,
            arg: Optional[TSnakSet],
            i: int,
            default: Optional[SnakSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SnakSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_snak_template(
            cls,
            arg: Optional[SnakTemplate],
            i: int,
            default: Optional[SnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SnakTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_snak_variable(
            cls,
            arg: Optional[SnakVariable],
            i: int,
            default: Optional[SnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SnakVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_some_value_snak(
            cls,
            arg: Optional[SomeValueSnak],
            i: int,
            default: Optional[SomeValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SomeValueSnak]:
        ...

    @classmethod
    def _preprocess_optional_arg_some_value_snak_template(
            cls,
            arg: Optional[SomeValueSnakTemplate],
            i: int,
            default: Optional[SomeValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SomeValueSnakTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_some_value_snak_variable(
            cls,
            arg: Optional[SomeValueSnakVariable],
            i: int,
            default: Optional[SomeValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[SomeValueSnakVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_statement(
            cls,
            arg: Optional[Statement],
            i: int,
            default: Optional[Statement] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Statement]:
        ...

    @classmethod
    def _preprocess_optional_arg_statement_template(
            cls,
            arg: Optional[StatementTemplate],
            i: int,
            default: Optional[StatementTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[StatementTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_statement_variable(
            cls,
            arg: Optional[StatementVariable],
            i: int,
            default: Optional[StatementVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[StatementVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_string(
            cls,
            arg: Optional[TString],
            i: int,
            default: Optional[String] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[String]:
        ...

    @classmethod
    def _preprocess_optional_arg_string_datatype(
            cls,
            arg: Optional[StringDatatype],
            i: int,
            default: Optional[StringDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[StringDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_string_template(
            cls,
            arg: Optional[StringTemplate],
            i: int,
            default: Optional[StringTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[StringTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_string_variable(
            cls,
            arg: Optional[StringVariable],
            i: int,
            default: Optional[StringVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[StringVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_template(
            cls,
            arg: Optional[Template],
            i: int,
            default: Optional[Template] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Template]:
        ...

    @classmethod
    def _preprocess_optional_arg_text(
            cls,
            arg: Optional[TText],
            i: int,
            default: Optional[Text] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Text]:
        ...

    @classmethod
    def _preprocess_optional_arg_text_datatype(
            cls,
            arg: Optional[TextDatatype],
            i: int,
            default: Optional[TextDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TextDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_text_set(
            cls,
            arg: Optional[TTextSet],
            i: int,
            default: Optional[TextSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TextSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_text_template(
            cls,
            arg: Optional[TextTemplate],
            i: int,
            default: Optional[TextTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TextTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_text_variable(
            cls,
            arg: Optional[TextVariable],
            i: int,
            default: Optional[TextVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TextVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_time(
            cls,
            arg: Optional[TTime],
            i: int,
            default: Optional[Time] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Time]:
        ...

    @classmethod
    def _preprocess_optional_arg_time_datatype(
            cls,
            arg: Optional[TimeDatatype],
            i: int,
            default: Optional[TimeDatatype] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TimeDatatype]:
        ...

    @classmethod
    def _preprocess_optional_arg_time_template(
            cls,
            arg: Optional[TimeTemplate],
            i: int,
            default: Optional[TimeTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TimeTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_time_variable(
            cls,
            arg: Optional[TimeVariable],
            i: int,
            default: Optional[TimeVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[TimeVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_value(
            cls,
            arg: Optional[TValue],
            i: int,
            default: Optional[Value] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Value]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_set(
            cls,
            arg: Optional[TValueSet],
            i: int,
            default: Optional[ValueSet] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueSet]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_snak(
            cls,
            arg: Optional[ValueSnak],
            i: int,
            default: Optional[ValueSnak] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueSnak]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_snak_template(
            cls,
            arg: Optional[ValueSnakTemplate],
            i: int,
            default: Optional[ValueSnakTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueSnakTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_snak_variable(
            cls,
            arg: Optional[ValueSnakVariable],
            i: int,
            default: Optional[ValueSnakVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueSnakVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_template(
            cls,
            arg: Optional[ValueTemplate],
            i: int,
            default: Optional[ValueTemplate] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueTemplate]:
        ...

    @classmethod
    def _preprocess_optional_arg_value_variable(
            cls,
            arg: Optional[ValueVariable],
            i: int,
            default: Optional[ValueVariable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[ValueVariable]:
        ...

    @classmethod
    def _preprocess_optional_arg_variable(
            cls,
            arg: Optional[Variable],
            i: int,
            default: Optional[Variable] = ...,
            function: Optional[Union[TCallable, str]] = ...,
    ) -> Optional[Variable]:
        ...

    def check_annotation_record(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> AnnotationRecord:
        ...

    def check_annotation_record_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> AnnotationRecordSet:
        ...

    def check_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DataValue:
        ...

    def check_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DataValueTemplate:
        ...

    def check_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DataValueVariable:
        ...

    def check_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Datatype:
        ...

    def check_datatype_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DatatypeVariable:
        ...

    def check_deep_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DeepDataValue:
        ...

    def check_deep_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DeepDataValueTemplate:
        ...

    def check_deep_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DeepDataValueVariable:
        ...

    def check_deprecated_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> DeprecatedRank:
        ...

    def check_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Descriptor:
        ...

    def check_entity(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Entity:
        ...

    def check_entity_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> EntityFingerprint:
        ...

    def check_entity_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> EntityTemplate:
        ...

    def check_entity_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> EntityVariable:
        ...

    def check_external_id(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ExternalId:
        ...

    def check_external_id_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ExternalIdDatatype:
        ...

    def check_external_id_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ExternalIdTemplate:
        ...

    def check_external_id_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ExternalIdVariable:
        ...

    def check_filter_pattern(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> FilterPattern:
        ...

    def check_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Fingerprint:
        ...

    def check_iri(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> IRI:
        ...

    def check_iri_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> IRI_Datatype:
        ...

    def check_iri_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> IRI_Template:
        ...

    def check_iri_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> IRI_Variable:
        ...

    def check_item(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Item:
        ...

    def check_item_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ItemDatatype:
        ...

    def check_item_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ItemDescriptor:
        ...

    def check_item_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ItemTemplate:
        ...

    def check_item_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ItemVariable:
        ...

    def check_kif_object(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'KIF_Object':
        ...

    def check_kif_object_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> KIF_ObjectSet:
        ...

    def check_lexeme(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Lexeme:
        ...

    def check_lexeme_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> LexemeDatatype:
        ...

    def check_lexeme_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> LexemeDescriptor:
        ...

    def check_lexeme_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> LexemeTemplate:
        ...

    def check_lexeme_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> LexemeVariable:
        ...

    def check_no_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> NoValueSnak:
        ...

    def check_no_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> NoValueSnakTemplate:
        ...

    def check_no_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> NoValueSnakVariable:
        ...

    def check_normal_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> NormalRank:
        ...

    def check_object(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Object:
        ...

    def check_pattern(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Pattern:
        ...

    def check_plain_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PlainDescriptor:
        ...

    def check_preferred_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PreferredRank:
        ...

    def check_property(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Property:
        ...

    def check_property_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PropertyDatatype:
        ...

    def check_property_descriptor(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PropertyDescriptor:
        ...

    def check_property_fingerprint(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PropertyFingerprint:
        ...

    def check_property_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PropertyTemplate:
        ...

    def check_property_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> PropertyVariable:
        ...

    def check_quantity(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Quantity:
        ...

    def check_quantity_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> QuantityDatatype:
        ...

    def check_quantity_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> QuantityTemplate:
        ...

    def check_quantity_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> QuantityVariable:
        ...

    def check_rank(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Rank:
        ...

    def check_reference_record(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ReferenceRecord:
        ...

    def check_reference_record_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ReferenceRecordSet:
        ...

    def check_shallow_data_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ShallowDataValue:
        ...

    def check_shallow_data_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ShallowDataValueTemplate:
        ...

    def check_shallow_data_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ShallowDataValueVariable:
        ...

    def check_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Snak:
        ...

    def check_snak_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SnakSet:
        ...

    def check_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SnakTemplate:
        ...

    def check_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SnakVariable:
        ...

    def check_some_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SomeValueSnak:
        ...

    def check_some_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SomeValueSnakTemplate:
        ...

    def check_some_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> SomeValueSnakVariable:
        ...

    def check_statement(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Statement:
        ...

    def check_statement_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> StatementTemplate:
        ...

    def check_statement_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> StatementVariable:
        ...

    def check_string(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> String:
        ...

    def check_string_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> StringDatatype:
        ...

    def check_string_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> StringTemplate:
        ...

    def check_string_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> StringVariable:
        ...

    def check_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Template:
        ...

    def check_text(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Text:
        ...

    def check_text_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TextDatatype:
        ...

    def check_text_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TextSet:
        ...

    def check_text_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TextTemplate:
        ...

    def check_text_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TextVariable:
        ...

    def check_time(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Time:
        ...

    def check_time_datatype(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TimeDatatype:
        ...

    def check_time_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TimeTemplate:
        ...

    def check_time_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> TimeVariable:
        ...

    def check_value(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Value:
        ...

    def check_value_set(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueSet:
        ...

    def check_value_snak(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueSnak:
        ...

    def check_value_snak_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueSnakTemplate:
        ...

    def check_value_snak_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueSnakVariable:
        ...

    def check_value_template(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueTemplate:
        ...

    def check_value_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> ValueVariable:
        ...

    def check_variable(
            self,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Variable:
        ...

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
