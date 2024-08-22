# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal
import itertools
import logging
import pathlib
import re
import unittest

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Datatype,
    DatatypeVariable,
    DataValue,
    DeepDataValue,
    DeprecatedRank,
    Descriptor,
    Entity,
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
    KIF_Object,
    KIF_ObjectSet,
    Lexeme,
    LexemeDatatype,
    LexemeDescriptor,
    NormalRank,
    NoValueSnak,
    PlainDescriptor,
    PreferredRank,
    Property,
    PropertyDatatype,
    PropertyDescriptor,
    Quantity,
    QuantityDatatype,
    Rank,
    ReferenceRecord,
    ReferenceRecordSet,
    ShallowDataValue,
    Snak,
    SnakSet,
    SomeValueSnak,
    Statement,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    Text,
    TextDatatype,
    TextSet,
    Time,
    TimeDatatype,
    Value,
    ValueSet,
    ValueSnak,
    Variable,
)
from kif_lib.model import (
    AndFingerprint,
    AtomicFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    DataValueTemplate,
    DataValueVariable,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    EmptyFingerprint,
    EntityTemplate,
    EntityVariable,
    FullFingerprint,
    ItemTemplate,
    ItemVariable,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    OrFingerprint,
    PropertyTemplate,
    PropertyVariable,
    QuantityTemplate,
    QuantityVariable,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    SnakFingerprint,
    SnakTemplate,
    SnakVariable,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    StatementTemplate,
    StatementVariable,
    Template,
    TextTemplate,
    TextVariable,
    TimeTemplate,
    TimeVariable,
    ValueFingerprint,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    VEntity,
    VExternalId,
    VItem,
    VLexeme,
    VNoValueSnak,
    VProperty,
    VQuantity,
    VSnak,
    VSomeValueSnak,
    VStatement,
    VString,
    VT_IRI,
    VTDatatype,
    VTEntity,
    VText,
    VTime,
    VTItem,
    VTProperty,
    VTSnak,
    VTValue,
    VValue,
    VValueSnak,
)
from kif_lib.model.object import Object
from kif_lib.model.value.quantity import VTQuantityContent
from kif_lib.model.value.string import VTStringContent
from kif_lib.model.value.time import VTTimeContent
from kif_lib.namespace import XSD
from kif_lib.typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Final,
    Iterable,
    Iterator,
    Optional,
    Set,
    TypeVar,
    Union,
)

TESTS_TESTS_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent
TObj = TypeVar('TObj', bound=KIF_Object)


class TestCase(unittest.TestCase):

    ALL_KIF_OBJECT_CLASSES: ClassVar[Set[type[KIF_Object]]] = frozenset(filter(
        lambda c: isinstance(c, type) and issubclass(c, KIF_Object), map(
            lambda s: getattr(KIF_Object, s),
            filter(lambda s: re.match('^_[A-Z]', s), dir(KIF_Object)))))

    ALL_TEMPLATE_CLASSES: ClassVar[Set[type[Template]]] = frozenset(
        cast(Iterator[type[Template]], filter(
            lambda c: issubclass(c, Template), ALL_KIF_OBJECT_CLASSES)))

    ALL_VARIABLE_CLASSES: ClassVar[Set[type[Variable]]] = frozenset(
        cast(Iterator[type[Variable]], filter(
            lambda c: issubclass(c, Variable), ALL_KIF_OBJECT_CLASSES)))

    ALL_DATATYPE_CLASSES: ClassVar[Set[type[Datatype]]] = frozenset(
        cast(Iterator[type[Datatype]], filter(
            lambda c: issubclass(c, Datatype), ALL_KIF_OBJECT_CLASSES)))

    @classmethod
    def _variable_class_can_check_from(
            cls,
            variable_class: type[Variable]
    ) -> Iterable[type[Variable]]:
        return set(itertools.chain(
            filter(lambda x: issubclass(x, Variable),
                   variable_class.__mro__),
            filter(lambda x: issubclass(x, variable_class),
                   cls.ALL_VARIABLE_CLASSES)))

    @classmethod
    def _variable_class_cannot_check_from(
            cls,
            variable_class: type[Variable]
    ) -> Iterable[type[Variable]]:
        return cls.ALL_VARIABLE_CLASSES - set(
            cls._variable_class_can_check_from(variable_class))

    @classmethod
    def main(cls) -> unittest.main:
        return unittest.main()

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def assert_abstract_class(self, cls):
        self.assertRaisesRegex(TypeError, 'abstract class', cls)

    def assert_raises_bad_argument(
            self,
            exception: type[Exception],
            position: Optional[int],
            name: Optional[str],
            details: Optional[str],
            function: Union[
                Callable[..., Any], tuple[Callable[..., Any], str]],
            *args: Any,
            **kwargs: Any
    ):
        if isinstance(function, tuple):
            func, func_name = function
        elif hasattr(function, '__qualname__'):
            func, func_name = function, function.__qualname__
        else:
            func, func_name = function, str(function)
        regex = re.escape(str(KIF_Object._arg_error(
            details, func_name, name, position, exception)))
        self.assertRaisesRegex(
            exception, regex, func, *args, **kwargs)

# -- KIF_Object ------------------------------------------------------------

    def assert_kif_object(self, obj: KIF_Object):
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, KIF_Object)

# -- KIF_ObjectSet ---------------------------------------------------------

    def assert_kif_object_set(self, obj: KIF_ObjectSet[TObj], *args: TObj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, KIF_ObjectSet)
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, KIF_Object)
            self.assertEqual(arg, args[i])
        self.assertEqual(obj._frozenset, set(args))
        for arg in args:
            self.assertIn(arg, obj)

    def assert_value_set(self, obj: ValueSet, *values: Value):
        self.assertIsInstance(obj, ValueSet)
        self.assert_kif_object_set(obj, *values)

    def assert_text_set(self, obj: TextSet, *texts: Text):
        self.assertIsInstance(obj, TextSet)
        self.assert_value_set(obj, *texts)

    def assert_snak_set(self, obj: SnakSet, *snaks: Snak):
        self.assertIsInstance(obj, SnakSet)
        self.assert_kif_object_set(obj, *snaks)

    def assert_reference_record(self, obj: ReferenceRecord, *snaks: Snak):
        self.assertIsInstance(obj, ReferenceRecord)
        self.assert_snak_set(obj, *snaks)

    def assert_reference_record_set(
            self,
            obj: ReferenceRecordSet,
            *refs: ReferenceRecord
    ):
        self.assertIsInstance(obj, ReferenceRecordSet)
        self.assert_kif_object_set(obj, *refs)

    def assert_annotation_record_set(
            self,
            obj: AnnotationRecordSet,
            *annots: AnnotationRecord
    ):
        self.assertIsInstance(obj, AnnotationRecordSet)
        self.assert_kif_object_set(obj, *annots)

# -- Datatype --------------------------------------------------------------

    def assert_datatype(self, obj: Datatype):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Datatype)

    def assert_item_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ItemDatatype)

    def assert_property_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, PropertyDatatype)

    def assert_lexeme_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, LexemeDatatype)

    def assert_iri_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, IRI_Datatype)

    def assert_text_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TextDatatype)

    def assert_string_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, StringDatatype)

    def assert_external_id_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ExternalIdDatatype)

    def assert_quantity_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, QuantityDatatype)

    def assert_time_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TimeDatatype)

# -- Value -----------------------------------------------------------------

    def assert_value(self, obj: Value):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Value)

    def assert_entity(self, obj: Entity, iri: IRI):
        self.assert_value(obj)
        self.assertIsInstance(obj, Entity)
        self.assertIsInstance(obj.args[0], IRI)
        self.assertEqual(obj.args[0], iri)
        self.assertIs(obj.iri, obj.args[0])
        self.assertIs(obj.get_iri(), obj.args[0])
        self.assertEqual(obj.n3(), obj.iri.n3())

    def assert_item(self, obj: Item, iri: IRI):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Item)
        self.assert_item_datatype(obj.datatype)

    def assert_property(
            self,
            obj: Property,
            iri: IRI,
            range: Optional[Datatype] = None
    ):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Property)
        self.assert_datatype(obj.datatype)
        self.assertEqual(obj.range, range)
        self.assertEqual(obj.get_range(), range)
        self.assertEqual(obj.args[1], range)

    def assert_lexeme(self, obj: Lexeme, iri: IRI):
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Lexeme)
        self.assert_lexeme_datatype(obj.datatype)

    def assert_data_value(self, obj: DataValue):
        self.assert_value(obj)
        self.assertIsInstance(obj, DataValue)

    def assert_shallow_data_value(self, obj: ShallowDataValue):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, ShallowDataValue)
        self.assertIs(obj.content, obj.args[0])
        self.assertIs(obj.get_content(), obj.args[0])

    def assert_iri(self, obj: IRI, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, IRI)
        self.assert_iri_datatype(obj.datatype)
        self.assertIsInstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.n3(), f'<{obj.content}>')

    def assert_text(
            self,
            obj: Text,
            content: str,
            language: Optional[str] = None
    ):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, Text)
        self.assert_text_datatype(obj.datatype)
        self.assertEqual(obj.args[0], content)
        if language is None:
            language = obj.context.options.default_language
        assert isinstance(language, str)
        self.assertEqual(obj.args[1], language)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)
        self.assertEqual(obj.n3(), f'"{obj.content}"@{obj.language}')

    def assert_string(self, obj: String, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assert_string_datatype(obj.datatype)
        self.assertIsInstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.n3(), f'"{obj.content}"')

    def assert_external_id(self, obj: ExternalId, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assertIsInstance(obj, ExternalId)
        self.assert_external_id_datatype(obj.datatype)
        assert isinstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.n3(), f'"{obj.content}"')

    def assert_deep_data_value(self, obj: DeepDataValue):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, DeepDataValue)

    def assert_quantity(
            self,
            obj: Quantity,
            amount: decimal.Decimal,
            unit: Optional[Item] = None,
            lb: Optional[decimal.Decimal] = None,
            ub: Optional[decimal.Decimal] = None
    ):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Quantity)
        self.assert_quantity_datatype(obj.datatype)
        self.assertEqual(obj.args[0], decimal.Decimal(amount))
        self.assertEqual(obj.n3(), f'"{obj.amount}"^^<{XSD.decimal}>')
        self.assertEqual(obj.amount, obj.args[0])
        self.assertEqual(obj.get_amount(), obj.args[0])
        self.assertEqual(obj.args[1], unit)
        self.assertEqual(obj.unit, obj.args[1])
        self.assertEqual(obj.get_unit(), obj.args[1])
        self.assertEqual(
            obj.args[2], decimal.Decimal(lb) if lb is not None else None)
        self.assertEqual(obj.lower_bound, obj.args[2])
        self.assertEqual(obj.get_lower_bound(), obj.args[2])
        self.assertEqual(
            obj.args[3], decimal.Decimal(ub) if ub is not None else None)
        self.assertEqual(obj.upper_bound, obj.args[3])
        self.assertEqual(obj.get_upper_bound(), obj.args[3])

    def assert_time(
            self,
            obj: Time,
            time: datetime.datetime,
            prec: Optional[Time.Precision] = None,
            tz: Optional[int] = None,
            cal: Optional[Item] = None
    ):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Time)
        self.assert_time_datatype(obj.datatype)
        self.assertEqual(obj.args[0], time)
        self.assertEqual(
            obj.n3(), f'"{obj.time.isoformat()}"^^<{XSD.dateTime}>')
        self.assertEqual(obj.time, obj.args[0])
        self.assertEqual(obj.get_time(), obj.args[0])
        self.assertEqual(obj.args[1], prec)
        self.assertEqual(obj.precision, obj.args[1])
        self.assertEqual(obj.get_precision(), obj.args[1])
        self.assertEqual(
            obj.args[2], tz if tz is not None else None)
        self.assertEqual(obj.timezone, obj.args[2])
        self.assertEqual(obj.get_timezone(), obj.args[2])
        self.assertEqual(
            obj.args[3], cal if cal is not None else None)
        self.assertEqual(obj.calendar, obj.args[3])
        self.assertEqual(obj.get_calendar(), obj.args[3])

# -- Template --------------------------------------------------------------

    def assert_template(self, obj: Template):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Template)

    def assert_value_template(self, obj: VValue):
        self.assertIsInstance(obj, ValueTemplate)
        assert isinstance(obj, ValueTemplate)
        self.assert_template(obj)

    def assert_entity_template(self, obj: VEntity, iri: VT_IRI):
        self.assertIsInstance(obj, EntityTemplate)
        assert isinstance(obj, EntityTemplate)
        self.assert_value_template(obj)
        self.assertEqual(obj.iri, iri)
        self.assertEqual(obj.get_iri(), iri)
        self.assertEqual(obj.args[0], iri)

    def assert_item_template(self, obj: VItem, iri: VT_IRI):
        self.assertIsInstance(obj, ItemTemplate)
        assert isinstance(obj, ItemTemplate)
        self.assert_entity_template(obj, iri)

    def assert_property_template(
            self,
            obj: VProperty,
            iri: VT_IRI,
            range: Optional[VTDatatype] = None
    ):
        self.assertIsInstance(obj, PropertyTemplate)
        assert isinstance(obj, PropertyTemplate)
        self.assert_entity_template(obj, iri)
        self.assertEqual(obj.range, range)
        self.assertEqual(obj.get_range(), range)
        self.assertEqual(obj.args[1], range)

    def assert_lexeme_template(self, obj: VLexeme, iri: VT_IRI):
        self.assertIsInstance(obj, LexemeTemplate)
        assert isinstance(obj, LexemeTemplate)
        self.assert_entity_template(obj, iri)

    def assert_data_value_template(self, obj: DataValueTemplate):
        self.assert_value_template(obj)
        self.assertIsInstance(obj, DataValueTemplate)

    def assert_shallow_data_value_template(
            self,
            obj: ShallowDataValueTemplate,
            content: VTStringContent
    ):
        self.assert_data_value_template(obj)
        self.assertIsInstance(obj, ShallowDataValueTemplate)
        self.assertEqual(obj.content, content)
        self.assertEqual(obj.get_content(), content)
        self.assertEqual(obj.args[0], content)

    def assert_iri_template(
            self,
            obj: IRI_Template,
            content: Variable
    ):
        self.assertIsInstance(obj, IRI_Template)
        assert isinstance(content, StringVariable)
        self.assert_shallow_data_value_template(obj, content)

    def assert_text_template(
            self,
            obj: VText,
            content: VTStringContent,
            language: Optional[VTStringContent] = None
    ):
        self.assertIsInstance(obj, TextTemplate)
        assert isinstance(obj, TextTemplate)
        assert isinstance(content, (StringVariable, str))
        if language is None:
            language = obj.context.options.default_language
        assert isinstance(language, (StringVariable, str))
        self.assert_shallow_data_value_template(obj, content)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)
        self.assertEqual(obj.args[1], language)

    def assert_string_template(
            self,
            obj: VString,
            content: Variable
    ):
        self.assertIsInstance(obj, StringTemplate)
        assert isinstance(obj, StringTemplate)
        assert isinstance(content, StringVariable)
        self.assert_shallow_data_value_template(obj, content)

    def assert_external_id_template(
            self,
            obj: VExternalId,
            content: Variable
    ):
        self.assertIsInstance(obj, ExternalIdTemplate)
        assert isinstance(obj, ExternalIdTemplate)
        assert isinstance(content, StringVariable)
        self.assert_string_template(obj, content)

    def assert_deep_data_value_template(self, obj: DeepDataValueTemplate):
        self.assert_data_value_template(obj)
        self.assertIsInstance(obj, DeepDataValueTemplate)

    def assert_quantity_template(
            self,
            obj: VQuantity,
            amount: VTQuantityContent,
            unit: Optional[VItem],
            lower_bound: Optional[VTQuantityContent],
            upper_bound: Optional[VTQuantityContent]
    ):
        self.assertIsInstance(obj, QuantityTemplate)
        assert isinstance(obj, QuantityTemplate)
        self.assert_deep_data_value_template(obj)
        self.assertEqual(obj.amount, amount)
        self.assertEqual(obj.get_amount(), amount)
        self.assertEqual(obj.args[0], amount)
        self.assertEqual(obj.unit, unit)
        self.assertEqual(obj.get_unit(), unit)
        self.assertEqual(obj.args[1], unit)
        self.assertEqual(obj.lower_bound, lower_bound)
        self.assertEqual(obj.get_lower_bound(), lower_bound)
        self.assertEqual(obj.args[2], lower_bound)
        self.assertEqual(obj.upper_bound, upper_bound)
        self.assertEqual(obj.get_upper_bound(), upper_bound)
        self.assertEqual(obj.args[3], upper_bound)

    def assert_time_template(
            self,
            obj: VTime,
            time: VTTimeContent,
            precision: Optional[VTQuantityContent],
            timezone: Optional[VTQuantityContent],
            calendar: Optional[VTItem]
    ):
        self.assertIsInstance(obj, TimeTemplate)
        assert isinstance(obj, TimeTemplate)
        self.assert_deep_data_value_template(obj)
        self.assertEqual(obj.time, time)
        self.assertEqual(obj.get_time(), time)
        self.assertEqual(obj.args[0], time)
        self.assertEqual(obj.precision, precision)
        self.assertEqual(obj.get_precision(), precision)
        self.assertEqual(obj.args[1], precision)
        self.assertEqual(obj.timezone, timezone)
        self.assertEqual(obj.get_timezone(), timezone)
        self.assertEqual(obj.args[2], timezone)
        self.assertEqual(obj.calendar, calendar)
        self.assertEqual(obj.get_calendar(), calendar)
        self.assertEqual(obj.args[3], calendar)

    def assert_snak_template(
            self,
            obj: VSnak,
            property: VTProperty
    ):
        self.assertIsInstance(obj, SnakTemplate)
        assert isinstance(obj, SnakTemplate)
        self.assert_template(obj)
        self.assertEqual(obj.property, property)
        self.assertEqual(obj.get_property(), property)
        self.assertEqual(obj.args[0], property)

    def assert_value_snak_template(
            self,
            obj: VValueSnak,
            property: VTProperty,
            value: VTValue
    ):
        self.assertIsInstance(obj, ValueSnakTemplate)
        assert isinstance(obj, ValueSnakTemplate)
        self.assert_snak_template(obj, property)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)
        self.assertEqual(obj.args[1], value)

    def assert_some_value_snak_template(
            self,
            obj: VSomeValueSnak,
            property: VTProperty
    ):
        self.assertIsInstance(obj, SomeValueSnakTemplate)
        assert isinstance(obj, SomeValueSnakTemplate)
        assert isinstance(property, (PropertyTemplate, PropertyVariable))
        self.assert_snak_template(obj, property)

    def assert_no_value_snak_template(
            self,
            obj: VNoValueSnak,
            property: VProperty,
    ):
        self.assertIsInstance(obj, NoValueSnakTemplate)
        assert isinstance(obj, NoValueSnakTemplate)
        assert isinstance(property, (PropertyTemplate, PropertyVariable))
        self.assert_snak_template(obj, property)

    def assert_statement_template(
            self,
            obj: VStatement,
            subject: VTEntity,
            snak: VTSnak
    ):
        self.assertIsInstance(obj, StatementTemplate)
        assert isinstance(obj, StatementTemplate)
        self.assert_template(obj)
        self.assertEqual(obj.subject, subject)
        self.assertEqual(obj.get_subject(), subject)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.snak, snak)
        self.assertEqual(obj.get_snak(), snak)
        self.assertEqual(obj.args[1], snak)

# -- Variable --------------------------------------------------------------

    def assert_variable(self, obj: Variable, name: str):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Variable)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.get_name(), name)
        self.assertEqual(obj.args[0], name)

    def assert_datatype_variable(self, obj: Variable, name: str):
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, DatatypeVariable)

    def assert_value_variable(self, obj: Variable, name: str):
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, ValueVariable)

    def assert_entity_variable(self, obj: Variable, name: str):
        self.assert_value_variable(obj, name)
        self.assertIsInstance(obj, EntityVariable)

    def assert_item_variable(self, obj: Variable, name: str):
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, ItemVariable)

    def assert_property_variable(self, obj: Variable, name: str):
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, PropertyVariable)

    def assert_lexeme_variable(self, obj: Variable, name: str):
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, LexemeVariable)

    def assert_data_value_variable(self, obj: Variable, name: str):
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, DataValueVariable)

    def assert_shallow_data_value_variable(self, obj: Variable, name: str):
        self.assert_data_value_variable(obj, name)
        self.assertIsInstance(obj, ShallowDataValueVariable)

    def assert_iri_variable(self, obj: Variable, name: str):
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, IRI_Variable)

    def assert_text_variable(self, obj: Variable, name: str):
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, TextVariable)

    def assert_string_variable(self, obj: Variable, name: str):
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, StringVariable)

    def assert_external_id_variable(self, obj: Variable, name: str):
        self.assert_string_variable(obj, name)
        self.assertIsInstance(obj, ExternalIdVariable)

    def assert_deep_data_value_variable(self, obj: Variable, name: str):
        self.assert_data_value_variable(obj, name)
        self.assertIsInstance(obj, DeepDataValueVariable)

    def assert_quantity_variable(self, obj: Variable, name: str):
        self.assert_deep_data_value_variable(obj, name)
        self.assertIsInstance(obj, QuantityVariable)

    def assert_time_variable(self, obj: Variable, name: str):
        self.assert_deep_data_value_variable(obj, name)
        self.assertIsInstance(obj, TimeVariable)

    def assert_snak_variable(self, obj: Variable, name: str):
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, SnakVariable)

    def assert_value_snak_variable(self, obj: Variable, name: str):
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, ValueSnakVariable)

    def assert_some_value_snak_variable(self, obj: Variable, name: str):
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, SomeValueSnakVariable)

    def assert_no_value_snak_variable(self, obj: Variable, name: str):
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, NoValueSnakVariable)

    def assert_statement_variable(self, obj: Variable, name: str):
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, StatementVariable)

# -- Fingerprint -----------------------------------------------------------

    def assert_fingerprint(self, obj: Fingerprint):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Fingerprint)

    def assert_compound_fingerprint(
            self,
            obj: Fingerprint,
            *args: Fingerprint
    ):
        self.assert_fingerprint(obj)
        self.assertIsInstance(obj, CompoundFingerprint)
        assert isinstance(obj, CompoundFingerprint)
        for i, arg in enumerate(args):
            self.assertEqual(obj.args[i], arg)

    def assert_and_fingerprint(self, obj: Fingerprint, *args: Fingerprint):
        self.assert_compound_fingerprint(obj)
        self.assertIsInstance(obj, AndFingerprint)

    def assert_or_fingerprint(self, obj: Fingerprint, *args: Fingerprint):
        self.assert_compound_fingerprint(obj)
        self.assertIsInstance(obj, OrFingerprint)

    def assert_atomic_fingerprint(self, obj: Fingerprint):
        self.assert_fingerprint(obj)
        self.assertIsInstance(obj, AtomicFingerprint)

    def assert_snak_fingerprint(self, obj: Fingerprint, snak: Snak):
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, SnakFingerprint)
        assert isinstance(obj, SnakFingerprint)
        self.assertFalse(obj.is_full())
        self.assertFalse(obj.is_empty())
        self.assertEqual(obj.args[0], snak)
        self.assertEqual(obj.snak, snak)
        self.assertEqual(obj.get_snak(), snak)

    def assert_converse_snak_fingerprint(self, obj: Fingerprint, snak: Snak):
        self.assert_snak_fingerprint(obj, snak)
        self.assertIsInstance(obj, ConverseSnakFingerprint)

    def assert_value_fingerprint(self, obj: Fingerprint, value: Value):
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, ValueFingerprint)
        assert isinstance(obj, ValueFingerprint)
        self.assertFalse(obj.is_full())
        self.assertFalse(obj.is_empty())
        self.assertEqual(obj.args[0], value)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)

    def assert_full_fingerprint(self, obj: Fingerprint):
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, FullFingerprint)
        assert isinstance(obj, FullFingerprint)
        self.assertTrue(obj.is_full())
        self.assertFalse(obj.is_empty())

    def assert_empty_fingerprint(self, obj: Fingerprint):
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, EmptyFingerprint)
        assert isinstance(obj, EmptyFingerprint)
        self.assertFalse(obj.is_full())
        self.assertTrue(obj.is_empty())

# -- Snak ------------------------------------------------------------------

    def assert_snak(self, obj: Snak, prop: Property):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Snak)
        self.assertIsInstance(obj.property, Property)
        self.assertEqual(obj.args[0], prop)
        self.assertEqual(obj.property, obj.args[0])
        self.assertEqual(obj.get_property(), obj.args[0])

    def assert_value_snak(
            self,
            obj: Snak,
            prop: Property,
            value: Value
    ):
        self.assertIsInstance(obj, ValueSnak)
        assert isinstance(obj, ValueSnak)
        self.assert_snak(obj, prop)
        self.assert_value(obj.args[1])
        self.assertEqual(obj.args[1], value)
        self.assertEqual(obj.value, obj.args[1])
        self.assertEqual(obj.get_value(), obj.args[1])

    def assert_some_value_snak(self, obj: Snak, prop: Property):
        self.assertIsInstance(obj, SomeValueSnak)
        assert isinstance(obj, SomeValueSnak)
        self.assert_snak(obj, prop)

    def assert_no_value_snak(self, obj: Snak, prop: Property):
        self.assertIsInstance(obj, NoValueSnak)
        assert isinstance(obj, NoValueSnak)
        self.assert_snak(obj, prop)

# -- Annotations -----------------------------------------------------------

    def assert_annotation_record(
            self,
            obj: AnnotationRecord,
            quals: SnakSet,
            refs: ReferenceRecordSet,
            rank: Rank
    ):
        self.assertIsInstance(obj, AnnotationRecord)
        self.assert_kif_object(obj)
        self.assertIsInstance(obj.args[0], SnakSet)
        self.assertEqual(obj.args[0], quals)
        self.assertEqual(obj.qualifiers, obj.args[0])
        self.assertEqual(obj.get_qualifiers(), obj.args[0])
        self.assertIsInstance(obj.args[1], ReferenceRecordSet)
        self.assertEqual(obj.args[1], refs)
        self.assertEqual(obj.references, obj.args[1])
        self.assertEqual(obj.get_references(), obj.args[1])
        self.assertIsInstance(obj.args[2], Rank)
        self.assertEqual(obj.args[2], rank)
        self.assertEqual(obj.rank, obj.args[2])
        self.assertEqual(obj.get_rank(), obj.args[2])

    def assert_rank(self, obj: Rank):
        self.assertIsInstance(obj, Rank)

    def assert_preferred_rank(self, obj: PreferredRank):
        self.assertIsInstance(obj, PreferredRank)
        self.assert_rank(obj)

    def assert_normal_rank(self, obj: NormalRank):
        self.assertIsInstance(obj, NormalRank)
        self.assert_rank(obj)

    def assert_deprecated_rank(self, obj: DeprecatedRank):
        self.assertIsInstance(obj, DeprecatedRank)
        self.assert_rank(obj)

# -- Statement -------------------------------------------------------------

    def assert_statement(self, obj: Statement, subject: Entity, snak: Snak):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Statement)
        self.assertIsInstance(obj.args[0], Entity)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, obj.args[0])
        self.assertEqual(obj.get_subject(), obj.args[0])
        self.assertIsInstance(obj.args[1], Snak)
        self.assertEqual(obj.args[1], snak)
        self.assertEqual(obj.snak, obj.args[1])
        self.assertEqual(obj.get_snak(), obj.args[1])

# -- Descriptor ------------------------------------------------------------

    def assert_descriptor(self, obj: Descriptor):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Descriptor)

    def assert_plain_descriptor(
            self,
            obj: PlainDescriptor,
            label: Optional[Text] = None,
            aliases: TextSet = TextSet(),
            description: Optional[Text] = None
    ):
        self.assert_descriptor(obj)
        self.assertIsInstance(obj, PlainDescriptor)
        label = Text(*label) if label is not None else label
        aliases = TextSet(*aliases) if aliases is not None else aliases
        description = (
            Text(*description) if description is not None else description)
        self.assertEqual(obj.args[0], label)
        self.assertEqual(obj.label, label)
        self.assertEqual(obj.get_label(), label)
        self.assertEqual(obj.args[1], aliases)
        self.assertEqual(obj.aliases, aliases)
        self.assertEqual(obj.get_aliases(), aliases)
        self.assertEqual(obj.args[2], description)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.get_description(), description)

    def assert_item_descriptor(
            self,
            obj: Descriptor,
            label: Optional[Text] = None,
            aliases: TextSet = TextSet(),
            description: Optional[Text] = None
    ):
        self.assertIsInstance(obj, ItemDescriptor)
        assert isinstance(obj, ItemDescriptor)
        self.assert_plain_descriptor(obj, label, aliases, description)

    def assert_property_descriptor(
            self,
            obj: Descriptor,
            label: Optional[Text] = None,
            aliases: TextSet = TextSet(),
            desc: Optional[Text] = None,
            dt: Optional[Datatype] = None
    ):
        self.assertIsInstance(obj, PropertyDescriptor)
        assert isinstance(obj, PropertyDescriptor)
        self.assert_plain_descriptor(obj, label, aliases, desc)
        self.assertEqual(obj.args[3], dt)
        self.assertEqual(obj.datatype, dt)
        self.assertEqual(obj.get_datatype(), dt)

    def assert_lexeme_descriptor(
            self,
            obj: Descriptor,
            lemma: Optional[Text],
            category: Optional[Item],
            language: Optional[Item]
    ):
        self.assertIsInstance(obj, LexemeDescriptor)
        assert isinstance(obj, LexemeDescriptor)
        self.assert_descriptor(obj)
        self.assertEqual(obj.args[0], lemma)
        self.assertEqual(obj.lemma, lemma)
        self.assertEqual(obj.get_lemma(), lemma)
        self.assertEqual(obj.args[1], category)
        self.assertEqual(obj.category, category)
        self.assertEqual(obj.get_category(), category)
        self.assertEqual(obj.args[2], language)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)

# -- Filter ----------------------------------------------------------------

    def assert_filter(
            self,
            obj: Filter,
            subject: Optional[Fingerprint] = None,
            property: Optional[Fingerprint] = None,
            value: Optional[Fingerprint] = None,
            mask: Filter.SnakMask = Filter.SnakMask.ALL
    ):
        self.assertIsInstance(obj, Filter)
        if subject is None:
            subject = FullFingerprint()
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, subject)
        self.assertEqual(obj.get_subject(), subject)
        if property is None:
            property = FullFingerprint()
        self.assertEqual(obj.args[1], property)
        self.assertEqual(obj.property, property)
        self.assertEqual(obj.get_property(), property)
        if value is None:
            value = FullFingerprint()
        self.assertEqual(obj.args[2], value)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)
        self.assertEqual(Filter.SnakMask(obj.args[3]), mask)
        self.assertEqual(obj.snak_mask, mask)
