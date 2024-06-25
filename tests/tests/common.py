# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools
import logging
import pathlib
import re
import unittest

from kif_lib import (
    AnnotationRecord,
    AnnotationRecordSet,
    Datatype,
    DataValue,
    DeepDataValue,
    DeprecatedRank,
    Descriptor,
    Entity,
    EntityFingerprint,
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    FilterPattern,
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
    Pattern,
    PlainDescriptor,
    PreferredRank,
    Property,
    PropertyDatatype,
    PropertyDescriptor,
    PropertyFingerprint,
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
    DatatypeClass,
    DataValueTemplate,
    DataValueVariable,
    Datetime,
    Decimal,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    EntityTemplate,
    EntityVariable,
    ItemTemplate,
    ItemVariable,
    KIF_ObjectClass,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    PropertyTemplate,
    PropertyVariable,
    QuantityTemplate,
    QuantityVariable,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    SnakTemplate,
    SnakVariable,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    StatementTemplate,
    StatementVariable,
    TCallable,
    Template,
    TemplateClass,
    TextTemplate,
    TextVariable,
    TimeTemplate,
    TimeVariable,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    VariableClass,
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
    VTEntity,
    VText,
    VTime,
    VTItemContent,
    VTPropertyContent,
    VTQuantityContent,
    VTStringContent,
    VTTimeContent,
    VTTimePrecisionContent,
    VTTimeTimezoneContent,
    VTValue,
    VValue,
    VValueSnak,
    VVDatatype,
    VVSnak,
)
from kif_lib.model.object import Object
from kif_lib.namespace import WIKIBASE, XSD
from kif_lib.typing import (
    Any,
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

LIB_TESTS_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent

_Dty = TypeVar('_Dty', bound=Datatype)
_Ent = TypeVar('_Ent', bound=Entity)
_Tpl = TypeVar('_Tpl', bound=Template)
_Val = TypeVar('_Val', bound=Value)
_Var = TypeVar('_Var', bound=Variable)


class kif_TestCase(unittest.TestCase):

    ALL_KIF_OBJECT_CLASSES: ClassVar[Set[KIF_ObjectClass]] = frozenset(filter(
        lambda c: isinstance(c, type) and issubclass(c, KIF_Object), map(
            lambda s: getattr(KIF_Object, s),
            filter(lambda s: re.match('^_[A-Z]', s), dir(KIF_Object)))))

    ALL_TEMPLATE_CLASSES: ClassVar[Set[TemplateClass]] = frozenset(
        cast(Iterator[TemplateClass], filter(
            lambda c: issubclass(c, Template), ALL_KIF_OBJECT_CLASSES)))

    ALL_VARIABLE_CLASSES: ClassVar[Set[VariableClass]] = frozenset(
        cast(Iterator[VariableClass], filter(
            lambda c: issubclass(c, Variable), ALL_KIF_OBJECT_CLASSES)))

    ALL_DATATYPE_CLASSES: ClassVar[Set[DatatypeClass]] = frozenset(
        cast(Iterator[DatatypeClass], filter(
            lambda c: issubclass(c, Datatype), ALL_KIF_OBJECT_CLASSES)))

    def _variable_class_can_check_from(
            self,
            cls: VariableClass
    ) -> Iterable[VariableClass]:
        return set(itertools.chain(
            filter(lambda x: issubclass(x, Variable), cls.__mro__),
            filter(lambda x: issubclass(x, cls), self.ALL_VARIABLE_CLASSES)))

    def _variable_class_cannot_check_from(
            self,
            cls: VariableClass
    ) -> Iterable[VariableClass]:
        return self.ALL_VARIABLE_CLASSES - set(
            self._variable_class_can_check_from(cls))

    @classmethod
    def main(cls):
        return unittest.main()

    @classmethod
    def _debug(cls, *args: Any):
        logging.getLogger(__name__).debug(' '.join(map(str, args)))

    def test_test_case_class_name(self):
        import inspect
        path = pathlib.Path(inspect.getfile(self.__class__))
        if path.parent == LIB_TESTS_DIR:
            return              # nothing to do
        name = self.__class__.__name__
        # self.assertEqual(path.stem, KIF_Object._camel2snake(name))
        with open(path) as fp:
            text = fp.read()
            self.assertTrue(text.endswith(f'''\
if __name__ == '__main__':
    {name}.main()
'''))

# -- Assertions ------------------------------------------------------------

    def assert_abstract_class(self, cls):
        self.assertRaisesRegex(TypeError, 'abstract class', cls)

    def assert_raises_bad_argument(
            self,
            exception: type[Exception],
            position: Optional[int],
            name: Optional[str],
            details: Optional[str],
            function: Union[TCallable, tuple[TCallable, str]],
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

    def assert_raises_check_error(
            self,
            cls: KIF_ObjectClass,
            arg: Any,
            function: Optional[Union[TCallable, tuple[TCallable, str]]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None,
            exception: Optional[type[Exception]] = None
    ):
        src_cls = arg if isinstance(arg, type) else type(arg)
        self.assert_raises_bad_argument(
            exception or TypeError, position, name,
            f'cannot coerce {src_cls.__qualname__} into {cls.__qualname__}',
            function or cls.check, arg)

    def assert_test_is_defined_for_kif_object_classes(
            self,
            name: str,
            classes: Optional[Set[KIF_ObjectClass]] = None
    ):
        if name.startswith('_'):
            prefix = 'test' + name
        else:
            prefix = 'test_' + name
        tests = set(filter(
            lambda s: s.startswith(prefix), dir(self)))
        meths = set(map(
            lambda c: prefix + c._snake_case_name,
            classes if classes is not None else self.ALL_KIF_OBJECT_CLASSES))
        self.assertEqual(meths, tests - (tests - meths))

    def assert_test_is_defined_for_template_classes(self, name: str):
        self.assert_test_is_defined_for_kif_object_classes(
            name, self.ALL_TEMPLATE_CLASSES)

    def assert_test_is_defined_for_variable_classes(self, name: str):
        self.assert_test_is_defined_for_kif_object_classes(
            name, self.ALL_VARIABLE_CLASSES)

# -- KIF_Object ------------------------------------------------------------

    def assert_kif_object(self, obj: KIF_Object):
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, Object)
        self.assertTrue(obj.is_object())
        self.assertIsInstance(obj, KIF_Object)
        self.assertTrue(obj.is_kif_object())

# -- KIF_ObjectSet ---------------------------------------------------------

    def assert_kif_object_set(self, obj: KIF_ObjectSet, *args: KIF_Object):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, KIF_ObjectSet)
        self.assertTrue(obj.is_kif_object_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, KIF_Object)
            self.assertEqual(arg, args[i])
        self.assertEqual(obj.frozenset, set(args))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for arg in args:
            self.assertIn(arg, obj)

    def assert_value_set(self, obj: ValueSet, *values: Value):
        self.assert_kif_object_set(obj, *values)
        self.assertIsInstance(obj, ValueSet)
        self.assertTrue(obj.is_value_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Value)
            self.assertEqual(arg, values[i])
        self.assertEqual(obj.frozenset, set(values))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for value in values:
            self.assertIn(value, obj)

    def assert_text_set(self, obj: TextSet, *texts: Text):
        self.assert_value_set(obj, *texts)
        self.assertIsInstance(obj, TextSet)
        self.assertTrue(obj.is_text_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Text)
            self.assertEqual(arg, texts[i])
        self.assertEqual(obj.frozenset, set(texts))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for text in texts:
            self.assertIn(text, obj)

    def assert_snak_set(self, obj: SnakSet, *snaks: Snak):
        self.assert_kif_object_set(obj, *snaks)
        self.assertIsInstance(obj, SnakSet)
        self.assertTrue(obj.is_snak_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, Snak)
            self.assertEqual(arg, snaks[i])
        self.assertEqual(obj.frozenset, set(snaks))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for snak in snaks:
            self.assertIn(snak, obj)

    def assert_reference_record_set(
            self,
            obj: ReferenceRecordSet,
            *refs: ReferenceRecord
    ):
        self.assert_kif_object_set(obj, *refs)
        self.assertIsInstance(obj, ReferenceRecordSet)
        self.assertTrue(obj.is_reference_record_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, ReferenceRecord)
            self.assertEqual(arg, refs[i])
        self.assertEqual(obj.frozenset, set(refs))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for ref in refs:
            self.assertIn(ref, obj)

    def assert_annotation_record_set(
            self,
            obj: AnnotationRecordSet,
            *annots: AnnotationRecord
    ):
        self.assert_kif_object_set(obj, *annots)
        self.assertIsInstance(obj, AnnotationRecordSet)
        self.assertTrue(obj.is_annotation_record_set())
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, AnnotationRecord)
            self.assertEqual(arg, annots[i])
        self.assertEqual(obj.frozenset, set(annots))
        self.assertEqual(obj.get_frozenset(), obj.frozenset)
        for ref in annots:
            self.assertIn(ref, obj)

# -- Value -----------------------------------------------------------------

    def assert_value(self, obj: Value):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Value)
        self.assertTrue(obj.is_value())

    def assert_entity(self, obj: Entity, iri: IRI):
        self.assert_value(obj)
        self.assertIsInstance(obj, Entity)
        self.assertTrue(obj.is_entity())
        self.assertIsInstance(obj.args[0], IRI)
        self.assertTrue(obj.args[0].is_iri())
        self.assertEqual(obj.args[0], iri)
        self.assertIs(obj.iri, obj.args[0])
        self.assertIs(obj.get_iri(), obj.args[0])
        self.assertEqual(obj.value, obj.iri.value)
        self.assertEqual(obj.get_value(), obj.iri.get_value())
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
        self.assertTrue(obj.is_data_value())

    def assert_shallow_data_value(self, obj: ShallowDataValue):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, ShallowDataValue)
        self.assertTrue(obj.is_shallow_data_value())
        self.assertIs(obj.content, obj.args[0])
        self.assertIs(obj.get_content(), obj.args[0])

    def assert_iri(self, obj: IRI, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, IRI)
        self.assert_iri_datatype(obj.datatype)
        self.assertIsInstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'<{obj.value}>')

    def assert_text(
            self,
            obj: Text,
            content: str,
            language: Optional[str] = None
    ):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, Text)
        self.assertTrue(obj.is_text())
        self.assert_text_datatype(obj.datatype)
        self.assertEqual(obj.args[0], content)
        if language is None:
            language = Text.default_language
        assert isinstance(language, str)
        self.assertEqual(obj.args[1], language)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"@{language}')

    def assert_string(self, obj: String, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assert_string_datatype(obj.datatype)
        self.assertIsInstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"')

    def assert_external_id(self, obj: ExternalId, content: str):
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assertIsInstance(obj, ExternalId)
        self.assert_external_id_datatype(obj.datatype)
        assert isinstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.value, obj.args[0])
        self.assertEqual(obj.get_value(), obj.args[0])
        self.assertEqual(obj.n3(), f'"{obj.value}"')

    def assert_deep_data_value(self, obj: DeepDataValue):
        self.assert_data_value(obj)
        self.assertIsInstance(obj, DeepDataValue)
        self.assertTrue(obj.is_deep_data_value())

    def assert_quantity(
            self,
            obj: Quantity,
            amount: Decimal,
            unit: Optional[Item] = None,
            lb: Optional[Decimal] = None,
            ub: Optional[Decimal] = None
    ):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Quantity)
        self.assertTrue(obj.is_quantity())
        self.assert_quantity_datatype(obj.datatype)
        self.assertEqual(obj.args[0], Decimal(amount))
        self.assertEqual(obj.value, str(obj.args[0]))
        self.assertEqual(obj.get_value(), str(obj.args[0]))
        self.assertEqual(obj.n3(), f'"{obj.value}"^^<{XSD.decimal}>')
        self.assertEqual(obj.amount, obj.args[0])
        self.assertEqual(obj.get_amount(), obj.args[0])
        self.assertEqual(obj.args[1], unit)
        self.assertEqual(obj.unit, obj.args[1])
        self.assertEqual(obj.get_unit(), obj.args[1])
        self.assertEqual(
            obj.args[2], Decimal(lb) if lb is not None else None)
        self.assertEqual(obj.lower_bound, obj.args[2])
        self.assertEqual(obj.get_lower_bound(), obj.args[2])
        self.assertEqual(
            obj.args[3], Decimal(ub) if ub is not None else None)
        self.assertEqual(obj.upper_bound, obj.args[3])
        self.assertEqual(obj.get_upper_bound(), obj.args[3])

    def assert_time(
            self,
            obj: Time,
            time: Datetime,
            prec: Optional[Time.Precision] = None,
            tz: Optional[int] = None,
            cal: Optional[Item] = None
    ):
        self.assert_deep_data_value(obj)
        self.assertIsInstance(obj, Time)
        self.assertTrue(obj.is_time())
        self.assert_time_datatype(obj.datatype)
        self.assertEqual(obj.args[0], time)
        self.assertEqual(obj.value, obj.args[0].isoformat())
        self.assertEqual(obj.get_value(), obj.args[0].isoformat())
        self.assertEqual(obj.n3(), f'"{obj.value}"^^<{XSD.dateTime}>')
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

# -- Datatype --------------------------------------------------------------

    def assert_datatype(self, obj: Datatype):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Datatype)
        self.assertTrue(obj.is_datatype())

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
        self.assertTrue(obj.is_quantity_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Quantity)

    def assert_time_datatype(self, obj: Datatype):
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TimeDatatype)
        self.assertTrue(obj.is_time_datatype())
        self.assertEqual(obj._uri, WIKIBASE.Time)

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
            range: Optional[VVDatatype] = None
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
        assert isinstance(obj, IRI_Template)
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
            language = Text.default_language
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
            precision: Optional[VTTimePrecisionContent],
            timezone: Optional[VTTimeTimezoneContent],
            calendar: Optional[VTItemContent]
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
            property: VTPropertyContent
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
            property: VTPropertyContent,
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
            property: VTPropertyContent
    ):
        self.assert_snak_template(obj, property)
        self.assertIsInstance(obj, SomeValueSnakTemplate)

    def assert_no_value_snak_template(
            self,
            obj: VNoValueSnak,
            property: VTPropertyContent,
    ):
        obj_ = cast(NoValueSnakTemplate, obj)
        self.assert_snak_template(obj_, property)
        self.assertIsInstance(obj_, NoValueSnakTemplate)

    def assert_statement_template(
            self,
            obj: VStatement,
            subject: VTEntity,
            snak: VVSnak
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

# -- Snak ------------------------------------------------------------------

    def assert_snak(self, obj: Snak, prop: Property):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Snak)
        self.assertTrue(obj.is_snak())
        self.assertIsInstance(obj.property, Property)
        self.assertTrue(obj.property.is_property())
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
        self.assertTrue(obj.is_value_snak())
        self.assert_value(obj.args[1])
        self.assertEqual(obj.args[1], value)
        self.assertEqual(obj.value, obj.args[1])
        self.assertEqual(obj.get_value(), obj.args[1])
        self.assertEqual(obj.mask, Snak.VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.VALUE_SNAK)

    def assert_some_value_snak(
            self,
            obj: Snak,
            prop: Property
    ):
        self.assertIsInstance(obj, SomeValueSnak)
        assert isinstance(obj, SomeValueSnak)
        self.assert_snak(obj, prop)
        self.assertTrue(obj.is_some_value_snak())
        self.assertEqual(obj.mask, Snak.SOME_VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.SOME_VALUE_SNAK)

    def assert_no_value_snak(
            self,
            obj: Snak,
            prop: Property
    ):
        self.assertIsInstance(obj, NoValueSnak)
        assert isinstance(obj, NoValueSnak)
        self.assert_snak(obj, prop)
        self.assertTrue(obj.is_no_value_snak())
        self.assertEqual(obj.mask, Snak.NO_VALUE_SNAK)
        self.assertEqual(obj.get_mask(), Snak.NO_VALUE_SNAK)

# -- Annotations -----------------------------------------------------------

    def assert_reference_record(self, obj: ReferenceRecord, *snaks: Snak):
        self.assert_snak_set(obj, *snaks)
        self.assertIsInstance(obj, ReferenceRecord)
        self.assertTrue(obj.is_reference_record())

    def assert_rank(self, obj: Rank):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Rank)
        self.assertTrue(obj.is_rank())

    def assert_preferred_rank(self, obj: PreferredRank):
        self.assert_rank(obj)
        self.assertIsInstance(obj, PreferredRank)
        self.assertTrue(obj.is_preferred_rank())

    def assert_normal_rank(self, obj: NormalRank):
        self.assert_rank(obj)
        self.assertIsInstance(obj, NormalRank)
        self.assertTrue(obj.is_normal_rank())

    def assert_deprecated_rank(self, obj: DeprecatedRank):
        self.assert_rank(obj)
        self.assertIsInstance(obj, DeprecatedRank)
        self.assertTrue(obj.is_deprecated_rank())

    def assert_annotation_record(
            self,
            obj: AnnotationRecord,
            quals: SnakSet,
            refs: ReferenceRecordSet,
            rank: Rank
    ):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, AnnotationRecord)
        self.assertTrue(obj.is_annotation_record())
        self.assertIsInstance(obj.args[0], SnakSet)
        self.assertTrue(obj.args[0].is_snak_set())
        self.assertEqual(obj.args[0], quals)
        self.assertEqual(obj.qualifiers, obj.args[0])
        self.assertEqual(obj.get_qualifiers(), obj.args[0])
        self.assertIsInstance(obj.args[1], ReferenceRecordSet)
        self.assertTrue(obj.args[1].is_reference_record_set())
        self.assertEqual(obj.args[1], refs)
        self.assertEqual(obj.references, obj.args[1])
        self.assertEqual(obj.get_references(), obj.args[1])
        self.assertIsInstance(obj.args[2], Rank)
        self.assertTrue(obj.args[2].is_rank())
        self.assertEqual(obj.args[2], rank)
        self.assertEqual(obj.rank, obj.args[2])
        self.assertEqual(obj.get_rank(), obj.args[2])

# -- Statement -------------------------------------------------------------

    def assert_statement(self, obj: Statement, subject: Entity, snak: Snak):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Statement)
        self.assertTrue(obj.is_statement())
        self.assertIsInstance(obj.args[0], Entity)
        self.assertTrue(obj.args[0].is_entity())
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, obj.args[0])
        self.assertEqual(obj.get_subject(), obj.args[0])
        self.assertIsInstance(obj.args[1], Snak)
        self.assertTrue(obj.args[1].is_snak())
        self.assertEqual(obj.args[1], snak)
        self.assertEqual(obj.snak, obj.args[1])
        self.assertEqual(obj.get_snak(), obj.args[1])

# -- Descriptor ------------------------------------------------------------

    def assert_descriptor(self, obj: Descriptor):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Descriptor)
        self.assertTrue(obj.is_descriptor())

    def assert_plain_descriptor(
            self,
            obj: PlainDescriptor,
            label: Optional[Text] = None,
            aliases: TextSet = TextSet(),
            description: Optional[Text] = None
    ):
        self.assert_descriptor(obj)
        self.assertIsInstance(obj, PlainDescriptor)
        self.assertTrue(obj.is_plain_descriptor())
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
        self.assertTrue(obj.is_item_descriptor())

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
        self.assertTrue(obj.is_property_descriptor())
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
        self.assertTrue(obj.is_descriptor())
        self.assertEqual(obj.args[0], lemma)
        self.assertEqual(obj.lemma, lemma)
        self.assertEqual(obj.get_lemma(), lemma)
        self.assertEqual(obj.args[1], category)
        self.assertEqual(obj.category, category)
        self.assertEqual(obj.get_category(), category)
        self.assertEqual(obj.args[2], language)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)

# -- Fingerprint -----------------------------------------------------------

    def assert_fingerprint(self, obj, val):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Fingerprint)
        self.assertTrue(obj.is_fingerprint())
        self.assertIsInstance(obj.args[0], (Value, SnakSet))
        self.assertEqual(obj.args[0], val)
        if isinstance(obj.args[0], Value):
            self.assertEqual(obj.value, obj.args[0])
            self.assertEqual(obj.value, val)
            self.assertIsNone(obj.snak_set)
        else:
            self.assertEqual(obj.snak_set, obj.args[0])
            self.assertEqual(obj.snak_set, val)
            self.assertIsNone(obj.value)

    def assert_entity_fingerprint(self, obj, val):
        self.assert_fingerprint(obj, val)
        self.assertIsInstance(obj, EntityFingerprint)
        self.assertTrue(obj.is_entity_fingerprint())

    def assert_property_fingerprint(self, obj, val):
        self.assert_fingerprint(obj, val)
        self.assertIsInstance(obj, PropertyFingerprint)
        self.assertTrue(obj.is_property_fingerprint())

    def assert_pattern(self, obj):
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Pattern)
        self.assertTrue(obj.is_pattern())

    def assert_filter_pattern(
            self, obj, subject=None, property=None, value=None, mask=Snak.ALL):
        self.assertIsInstance(obj, FilterPattern)
        self.assertTrue(obj.is_filter_pattern())
        if subject is not None:
            subject = EntityFingerprint(subject)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, subject)
        self.assertEqual(obj.get_subject(), subject)
        if property is not None:
            property = PropertyFingerprint(property)
        self.assertEqual(obj.args[1], property)
        self.assertEqual(obj.property, property)
        self.assertEqual(obj.get_property(), property)
        if value is not None:
            value = Fingerprint(value)
        self.assertEqual(obj.args[2], value)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)
        self.assertEqual(Snak.Mask(obj.args[3]), mask)
        self.assertEqual(obj.snak_mask, mask)
