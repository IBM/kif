# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import datetime
import decimal
import functools
import logging
import os
import pathlib
import re
import unittest

from kif_lib import (
    AliasProperty,
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    AnnotatedStatementVariable,
    ClosedTerm,
    ClosedTermSet,
    Context,
    Datatype,
    DatatypeVariable,
    DataValue,
    DeepDataValue,
    DeprecatedRank,
    DescriptionProperty,
    Entity,
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
    itertools,
    KIF_Object,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexemeDatatype,
    LexicalCategoryProperty,
    NormalRank,
    NoValueSnak,
    OpenTerm,
    PreferredRank,
    Property,
    PropertyDatatype,
    PseudoProperty,
    QualifierRecord,
    QualifierRecordVariable,
    Quantity,
    QuantityDatatype,
    Rank,
    RankVariable,
    ReferenceRecord,
    ReferenceRecordSet,
    ReferenceRecordVariable,
    ShallowDataValue,
    Snak,
    SnakSet,
    SnakSetVariable,
    SomeValueSnak,
    Statement,
    Store,
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    Term,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
    Value,
    ValuePair,
    ValuePairVariable,
    ValueSnak,
    Variable,
)
from kif_lib.context import Section
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
    VQualifierRecord,
    VQuantity,
    VRank,
    VReferenceRecordSet,
    VSnak,
    VSomeValueSnak,
    VStatement,
    VString,
    VT_IRI,
    VTDatatype,
    VText,
    VTime,
    VTItem,
    VTProperty,
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
    Literal,
    Sequence,
    Set,
    TypeAlias,
    TypeVar,
)

T = TypeVar('T')
_TClosedTerm = TypeVar('_TClosedTerm', bound=ClosedTerm)


# == Test case =============================================================

class TestCase(unittest.IsolatedAsyncioTestCase):
    """Base class for KIF test cases."""

    ALL_KIF_OBJECT_CLASSES: ClassVar[Set[type[KIF_Object]]] =\
        frozenset(KIF_Object._get_subclasses())

    ALL_TEMPLATE_CLASSES: ClassVar[Set[type[Template]]] =\
        frozenset(Template._get_subclasses())

    ALL_VARIABLE_CLASSES: ClassVar[Set[type[Variable]]] =\
        frozenset(Variable._get_subclasses())

    ALL_DATATYPE_CLASSES: ClassVar[Set[type[Datatype]]] =\
        frozenset(Datatype._get_subclasses())

    ALL_RANK_CLASSES: ClassVar[Set[type[Rank]]] =\
        frozenset(Rank._get_subclasses())

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

    @classmethod
    def SKIP(cls, message: str) -> unittest.SkipTest:
        return unittest.SkipTest(message)

    @classmethod
    def TODO(cls, message: str | None = None) -> unittest.SkipTest:
        return cls.SKIP(message or 'to-do')

    @classmethod
    def _clamp(
            cls,
            x: T | None,
            lb: T | None = None,
            ub: T | None = None
    ) -> T | None:
        if x is None:
            return None
        assert (lb is None or ub is None or lb < ub)  # type: ignore
        if lb is not None and x < lb:                 # type: ignore
            return lb
        if ub is not None and x > ub:  # type: ignore
            return ub
        return x

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def assert_abstract_class(self, cls: Any) -> None:
        self.assertRaisesRegex(TypeError, 'abstract class', cls)

    def assert_raises_bad_argument(
            self,
            exception: type[Exception],
            position: int | None,
            name: str | None,
            details: str | None,
            function: Callable[..., Any] | tuple[Callable[..., Any], str],
            *args: Any,
            **kwargs: Any
    ) -> None:
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

    def assert_it(
            self,
            empty: Iterable[Iterable[T]] = (),
            equals: Iterable[tuple[Iterable[T], T]] = (),
            contains: Iterable[tuple[Iterable[T], Iterable[T]]] = ()
    ) -> None:
        for it in empty:
            self.assert_it_empty(it)
        for it, x in equals:
            self.assert_it_equals(it, x)
        for it, xs in contains:
            self.assert_it_contains(it, *xs)

    def assert_it_empty(self, it: Iterable[T]) -> None:
        self.assertFalse(set(it))

    def assert_it_equals(self, it: Iterable[T], *args: T) -> None:
        self.assertEqual(set(it), set(args))

    def assert_it_contains(self, it: Iterable[T], *args: T) -> None:
        it_set = set(it)
        for arg in args:
            self.assertIn(arg, it_set)

# -- KIF_Object ------------------------------------------------------------

    def assert_kif_object(self, obj: KIF_Object) -> None:
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, Object)
        self.assertIsInstance(obj, KIF_Object)

# -- Term ------------------------------------------------------------------

    def assert_term(self, obj: Term) -> None:
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Term)

    def assert_closed_term(self, obj: ClosedTerm) -> None:
        self.assert_term(obj)
        self.assertIsInstance(obj, ClosedTerm)
        self.assertTrue(Term.is_closed(obj))
        self.assertFalse(Term.is_open(obj))
        self.assertFalse(bool(obj.variables))

    def assert_open_term(self, obj: OpenTerm) -> None:
        self.assert_term(obj)
        self.assertIsInstance(obj, OpenTerm)
        self.assertTrue(Term.is_open(obj))
        self.assertFalse(Term.is_closed(obj))
        self.assertTrue(obj.variables)

# -- ClosedTermSet ---------------------------------------------------------

    def assert_closed_term_set(
            self,
            obj: ClosedTermSet[_TClosedTerm],
            *args: _TClosedTerm
    ) -> None:
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, ClosedTermSet)
        for i, arg in enumerate(obj):
            self.assertIsInstance(arg, ClosedTerm)
            self.assertEqual(arg, args[i])
        self.assertEqual(obj._frozenset, set(args))
        for arg in args:
            self.assertIn(arg, obj)

    def assert_snak_set(self, obj: SnakSet, *snaks: Snak) -> None:
        self.assertIsInstance(obj, SnakSet)
        self.assert_closed_term_set(obj, *snaks)

    def assert_graph(self, obj: Graph, *statements: Statement) -> None:
        self.assertIsInstance(obj, Graph)
        self.assert_closed_term_set(obj, *statements)

    def assert_qualifier_record(
            self,
            obj: QualifierRecord,
            *snaks: Snak
    ) -> None:
        self.assertIsInstance(obj, QualifierRecord)
        self.assert_snak_set(obj, *snaks)

    def assert_reference_record(
            self,
            obj: ReferenceRecord,
            *snaks: Snak
    ) -> None:
        self.assertIsInstance(obj, ReferenceRecord)
        self.assert_snak_set(obj, *snaks)

    def assert_reference_record_set(
            self,
            obj: ReferenceRecordSet,
            *refs: ReferenceRecord
    ) -> None:
        self.assertIsInstance(obj, ReferenceRecordSet)
        self.assert_closed_term_set(obj, *refs)

# -- Datatype --------------------------------------------------------------

    def assert_datatype(self, obj: Datatype) -> None:
        self.assert_closed_term(obj)
        self.assertIsInstance(obj, Datatype)

    def assert_item_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ItemDatatype)

    def assert_property_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, PropertyDatatype)

    def assert_lexeme_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, LexemeDatatype)

    def assert_iri_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, IRI_Datatype)

    def assert_text_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TextDatatype)

    def assert_string_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, StringDatatype)

    def assert_external_id_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, ExternalIdDatatype)

    def assert_quantity_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, QuantityDatatype)

    def assert_time_datatype(self, obj: Datatype) -> None:
        self.assert_datatype(obj)
        self.assertIsInstance(obj, TimeDatatype)

# -- Value -----------------------------------------------------------------

    def assert_value(self, obj: Value) -> None:
        self.assert_closed_term(obj)
        self.assertIsInstance(obj, Value)

    def assert_entity(self, obj: Entity, iri: IRI) -> None:
        self.assert_value(obj)
        self.assertIsInstance(obj, Entity)
        self.assertIsInstance(obj.args[0], IRI)
        self.assertEqual(obj.args[0], iri)
        self.assertIs(obj.iri, obj.args[0])
        self.assertIs(obj.get_iri(), obj.args[0])
        self.assertEqual(obj.n3(), obj.iri.n3())

    def assert_item(self, obj: Item, iri: IRI) -> None:
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Item)
        self.assert_item_datatype(obj.datatype)

    def assert_property(
            self,
            obj: Property,
            iri: IRI,
            range: Datatype | None = None
    ) -> None:
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Property)
        self.assert_datatype(obj.datatype)
        self.assertEqual(obj.range, range)
        self.assertEqual(obj.get_range(), range)
        self.assertEqual(obj.args[1], range)

    def assert_pseudo_property(
            self,
            obj: PseudoProperty,
            iri: IRI,
            range: Datatype
    ) -> None:
        self.assert_property(obj, iri, range)
        self.assertIsInstance(obj, PseudoProperty)

    def assert_label_property(self, obj: LabelProperty) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, LabelProperty)

    def assert_alias_property(self, obj: AliasProperty) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, AliasProperty)

    def assert_description_property(self, obj: DescriptionProperty) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, DescriptionProperty)

    def assert_lemma_property(self, obj: LemmaProperty) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, LemmaProperty)

    def assert_lexical_category_property(
            self,
            obj: LexicalCategoryProperty
    ) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, LexicalCategoryProperty)

    def assert_language_property(self, obj: LanguageProperty) -> None:
        self.assert_pseudo_property(obj, obj.expected_iri, obj.expected_range)
        self.assertIsInstance(obj, LanguageProperty)

    def assert_lexeme(self, obj: Lexeme, iri: IRI) -> None:
        self.assert_entity(obj, iri)
        self.assertIsInstance(obj, Lexeme)
        self.assert_lexeme_datatype(obj.datatype)

    def assert_data_value(self, obj: DataValue) -> None:
        self.assert_value(obj)
        self.assertIsInstance(obj, DataValue)

    def assert_shallow_data_value(self, obj: ShallowDataValue) -> None:
        self.assert_data_value(obj)
        self.assertIsInstance(obj, ShallowDataValue)
        self.assertIs(obj.content, obj.args[0])
        self.assertIs(obj.get_content(), obj.args[0])

    def assert_iri(self, obj: IRI, content: str) -> None:
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
            language: str | None = None
    ) -> None:
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, Text)
        self.assert_text_datatype(obj.datatype)
        self.assertEqual(obj.args[0], content)
        if language is None:
            language = obj.context.options.language
        assert isinstance(language, str)
        self.assertEqual(obj.args[1], language)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)
        self.assertEqual(obj.n3(), f'"{obj.content}"@{obj.language}')

    def assert_string(self, obj: String, content: str) -> None:
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assert_string_datatype(obj.datatype)
        self.assertIsInstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.n3(), f'"{obj.content}"')

    def assert_external_id(self, obj: ExternalId, content: str) -> None:
        self.assert_shallow_data_value(obj)
        self.assertIsInstance(obj, String)
        self.assertIsInstance(obj, ExternalId)
        self.assert_external_id_datatype(obj.datatype)
        assert isinstance(content, str)
        self.assertEqual(obj.args[0], content)
        self.assertEqual(obj.n3(), f'"{obj.content}"')

    def assert_deep_data_value(self, obj: DeepDataValue) -> None:
        self.assert_data_value(obj)
        self.assertIsInstance(obj, DeepDataValue)

    def assert_quantity(
            self,
            obj: Quantity,
            amount: decimal.Decimal,
            unit: Item | None = None,
            lb: decimal.Decimal | None = None,
            ub: decimal.Decimal | None = None
    ) -> None:
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
            prec: Time.Precision | None = None,
            tz: int | None = None,
            cal: Item | None = None
    ) -> None:
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

    def assert_template(self, obj: Template) -> None:
        self.assert_open_term(obj)
        self.assertIsInstance(obj, Template)

    def assert_value_template(self, obj: VValue) -> None:
        self.assertIsInstance(obj, ValueTemplate)
        assert isinstance(obj, ValueTemplate)
        self.assert_template(obj)

    def assert_entity_template(self, obj: VEntity, iri: VT_IRI) -> None:
        self.assertIsInstance(obj, EntityTemplate)
        assert isinstance(obj, EntityTemplate)
        self.assert_value_template(obj)
        self.assertEqual(obj.iri, iri)
        self.assertEqual(obj.get_iri(), iri)
        self.assertEqual(obj.args[0], iri)

    def assert_item_template(self, obj: VItem, iri: VT_IRI) -> None:
        self.assertIsInstance(obj, ItemTemplate)
        assert isinstance(obj, ItemTemplate)
        self.assert_entity_template(obj, iri)

    def assert_property_template(
            self,
            obj: VProperty,
            iri: VT_IRI,
            range: VTDatatype | None = None
    ) -> None:
        self.assertIsInstance(obj, PropertyTemplate)
        assert isinstance(obj, PropertyTemplate)
        self.assert_entity_template(obj, iri)
        self.assertEqual(obj.range, range)
        self.assertEqual(obj.get_range(), range)
        self.assertEqual(obj.args[1], range)

    def assert_lexeme_template(self, obj: VLexeme, iri: VT_IRI) -> None:
        self.assertIsInstance(obj, LexemeTemplate)
        assert isinstance(obj, LexemeTemplate)
        self.assert_entity_template(obj, iri)

    def assert_data_value_template(self, obj: DataValueTemplate) -> None:
        self.assert_value_template(obj)
        self.assertIsInstance(obj, DataValueTemplate)

    def assert_shallow_data_value_template(
            self,
            obj: ShallowDataValueTemplate,
            content: VTStringContent
    ) -> None:
        self.assert_data_value_template(obj)
        self.assertIsInstance(obj, ShallowDataValueTemplate)
        self.assertEqual(obj.content, content)
        self.assertEqual(obj.get_content(), content)
        self.assertEqual(obj.args[0], content)

    def assert_iri_template(
            self,
            obj: IRI_Template,
            content: Variable
    ) -> None:
        self.assertIsInstance(obj, IRI_Template)
        assert isinstance(content, StringVariable)
        self.assert_shallow_data_value_template(obj, content)

    def assert_text_template(
            self,
            obj: VText,
            content: VTStringContent,
            language: VTStringContent | None = None
    ) -> None:
        self.assertIsInstance(obj, TextTemplate)
        assert isinstance(obj, TextTemplate)
        assert isinstance(content, (StringVariable, str))
        if language is None:
            language = obj.context.options.language
        assert isinstance(language, (StringVariable, str))
        self.assert_shallow_data_value_template(obj, content)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)
        self.assertEqual(obj.args[1], language)

    def assert_string_template(
            self,
            obj: VString,
            content: Variable
    ) -> None:
        self.assertIsInstance(obj, StringTemplate)
        assert isinstance(obj, StringTemplate)
        assert isinstance(content, StringVariable)
        self.assert_shallow_data_value_template(obj, content)

    def assert_external_id_template(
            self,
            obj: VExternalId,
            content: Variable
    ) -> None:
        self.assertIsInstance(obj, ExternalIdTemplate)
        assert isinstance(obj, ExternalIdTemplate)
        assert isinstance(content, StringVariable)
        self.assert_string_template(obj, content)

    def assert_deep_data_value_template(
            self,
            obj: DeepDataValueTemplate
    ) -> None:
        self.assert_data_value_template(obj)
        self.assertIsInstance(obj, DeepDataValueTemplate)

    def assert_quantity_template(
            self,
            obj: VQuantity,
            amount: VTQuantityContent,
            unit: VItem | None = None,
            lower_bound: VTQuantityContent | None = None,
            upper_bound: VTQuantityContent | None = None
    ) -> None:
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
            precision: VTQuantityContent | None,
            timezone: VTQuantityContent | None,
            calendar: VTItem | None
    ) -> None:
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
    ) -> None:
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
    ) -> None:
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
    ) -> None:
        self.assertIsInstance(obj, SomeValueSnakTemplate)
        assert isinstance(obj, SomeValueSnakTemplate)
        assert isinstance(property, (PropertyTemplate, PropertyVariable))
        self.assert_snak_template(obj, property)

    def assert_no_value_snak_template(
            self,
            obj: VNoValueSnak,
            property: VProperty,
    ) -> None:
        self.assertIsInstance(obj, NoValueSnakTemplate)
        assert isinstance(obj, NoValueSnakTemplate)
        assert isinstance(property, (PropertyTemplate, PropertyVariable))
        self.assert_snak_template(obj, property)

    def assert_statement_template(
            self,
            obj: VStatement,
            subject: VEntity | Variable,
            snak: VSnak | Variable
    ) -> None:
        self.assertIsInstance(obj, StatementTemplate)
        assert isinstance(obj, StatementTemplate)
        self.assert_template(obj)
        self.assertEqual(obj.subject, subject)
        self.assertEqual(obj.get_subject(), subject)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.snak, snak)
        self.assertEqual(obj.get_snak(), snak)
        self.assertEqual(obj.args[1], snak)

    def assert_annotated_statement_template(
            self,
            obj: VStatement,
            subject: VEntity | Variable,
            snak: VSnak | Variable,
            qualifiers: VQualifierRecord | Variable = QualifierRecord(),
            references: VReferenceRecordSet | Variable = ReferenceRecordSet(),
            rank: VRank | Variable = NormalRank()
    ) -> None:
        self.assertIsInstance(obj, AnnotatedStatementTemplate)
        assert isinstance(obj, AnnotatedStatementTemplate)
        self.assert_statement_template(obj, subject, snak)
        self.assertEqual(obj.qualifiers, qualifiers)
        self.assertEqual(obj.get_qualifiers(), qualifiers)
        self.assertEqual(obj.args[2], qualifiers)
        self.assertEqual(obj.references, references)
        self.assertEqual(obj.get_references(), references)
        self.assertEqual(obj.args[3], references)
        self.assertEqual(obj.rank, rank)
        self.assertEqual(obj.get_rank(), rank)
        self.assertEqual(obj.args[4], rank)

# -- Variable --------------------------------------------------------------

    def assert_variable(self, obj: Variable, name: str) -> None:
        self.assert_open_term(obj)
        self.assertIsInstance(obj, Variable)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.get_name(), name)
        self.assertEqual(obj.args[0], name)

    def assert_datatype_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, DatatypeVariable)

    def assert_value_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, ValueVariable)

    def assert_entity_variable(self, obj: Variable, name: str) -> None:
        self.assert_value_variable(obj, name)
        self.assertIsInstance(obj, EntityVariable)

    def assert_item_variable(self, obj: Variable, name: str) -> None:
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, ItemVariable)

    def assert_property_variable(self, obj: Variable, name: str) -> None:
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, PropertyVariable)

    def assert_lexeme_variable(self, obj: Variable, name: str) -> None:
        self.assert_entity_variable(obj, name)
        self.assertIsInstance(obj, LexemeVariable)

    def assert_data_value_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, DataValueVariable)

    def assert_shallow_data_value_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_data_value_variable(obj, name)
        self.assertIsInstance(obj, ShallowDataValueVariable)

    def assert_iri_variable(self, obj: Variable, name: str) -> None:
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, IRI_Variable)

    def assert_text_variable(self, obj: Variable, name: str) -> None:
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, TextVariable)

    def assert_string_variable(self, obj: Variable, name: str) -> None:
        self.assert_shallow_data_value_variable(obj, name)
        self.assertIsInstance(obj, StringVariable)

    def assert_external_id_variable(self, obj: Variable, name: str) -> None:
        self.assert_string_variable(obj, name)
        self.assertIsInstance(obj, ExternalIdVariable)

    def assert_deep_data_value_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_data_value_variable(obj, name)
        self.assertIsInstance(obj, DeepDataValueVariable)

    def assert_quantity_variable(self, obj: Variable, name: str) -> None:
        self.assert_deep_data_value_variable(obj, name)
        self.assertIsInstance(obj, QuantityVariable)

    def assert_time_variable(self, obj: Variable, name: str) -> None:
        self.assert_deep_data_value_variable(obj, name)
        self.assertIsInstance(obj, TimeVariable)

    def assert_value_pair_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, ValuePairVariable)

    def assert_snak_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, SnakVariable)

    def assert_value_snak_variable(self, obj: Variable, name: str) -> None:
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, ValueSnakVariable)

    def assert_some_value_snak_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, SomeValueSnakVariable)

    def assert_no_value_snak_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_snak_variable(obj, name)
        self.assertIsInstance(obj, NoValueSnakVariable)

    def assert_statement_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, StatementVariable)

    def assert_annotated_statement_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_statement_variable(obj, name)
        self.assertIsInstance(obj, AnnotatedStatementVariable)

    def assert_snak_set_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, SnakSetVariable)

    def assert_graph_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, GraphVariable)

    def assert_qualifier_record_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_snak_set_variable(obj, name)
        self.assertIsInstance(obj, QualifierRecordVariable)

    def assert_reference_record_variable(
            self,
            obj: Variable,
            name: str
    ) -> None:
        self.assert_snak_set_variable(obj, name)
        self.assertIsInstance(obj, ReferenceRecordVariable)

    def assert_rank_variable(self, obj: Variable, name: str) -> None:
        self.assert_variable(obj, name)
        self.assertIsInstance(obj, RankVariable)

# -- Fingerprint -----------------------------------------------------------

    def assert_fingerprint(self, obj: Fingerprint) -> None:
        self.assert_kif_object(obj)
        self.assertIsInstance(obj, Fingerprint)

    def assert_compound_fingerprint(
            self,
            obj: Fingerprint,
            *args: Fingerprint
    ) -> None:
        self.assert_fingerprint(obj)
        self.assertIsInstance(obj, CompoundFingerprint)
        assert isinstance(obj, CompoundFingerprint)
        for i, arg in enumerate(args):
            self.assertEqual(obj.args[i], arg)

    def assert_and_fingerprint(
            self,
            obj: Fingerprint,
            *args: Fingerprint
    ) -> None:
        self.assert_compound_fingerprint(obj)
        self.assertIsInstance(obj, AndFingerprint)

    def assert_or_fingerprint(
            self,
            obj: Fingerprint,
            *args: Fingerprint
    ) -> None:
        self.assert_compound_fingerprint(obj)
        self.assertIsInstance(obj, OrFingerprint)

    def assert_atomic_fingerprint(self, obj: Fingerprint) -> None:
        self.assert_fingerprint(obj)
        self.assertIsInstance(obj, AtomicFingerprint)

    def assert_snak_fingerprint(self, obj: Fingerprint, snak: Snak) -> None:
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, SnakFingerprint)
        assert isinstance(obj, SnakFingerprint)
        self.assertFalse(obj.is_full())
        self.assertFalse(obj.is_empty())
        self.assertEqual(obj.args[0], snak)
        self.assertEqual(obj.snak, snak)
        self.assertEqual(obj.get_snak(), snak)

    def assert_converse_snak_fingerprint(
            self,
            obj: Fingerprint,
            snak: Snak
    ) -> None:
        self.assert_snak_fingerprint(obj, snak)
        self.assertIsInstance(obj, ConverseSnakFingerprint)

    def assert_value_fingerprint(
            self,
            obj: Fingerprint,
            value: Value
    ) -> None:
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, ValueFingerprint)
        assert isinstance(obj, ValueFingerprint)
        self.assertFalse(obj.is_full())
        self.assertFalse(obj.is_empty())
        self.assertEqual(obj.args[0], value)
        self.assertEqual(obj.value, value)
        self.assertEqual(obj.get_value(), value)

    def assert_full_fingerprint(self, obj: Fingerprint) -> None:
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, FullFingerprint)
        assert isinstance(obj, FullFingerprint)
        self.assertTrue(obj.is_full())
        self.assertFalse(obj.is_empty())

    def assert_empty_fingerprint(self, obj: Fingerprint) -> None:
        self.assert_atomic_fingerprint(obj)
        self.assertIsInstance(obj, EmptyFingerprint)
        assert isinstance(obj, EmptyFingerprint)
        self.assertFalse(obj.is_full())
        self.assertTrue(obj.is_empty())

# -- Snak ------------------------------------------------------------------

    def assert_snak(self, obj: Snak, prop: Property) -> None:
        self.assert_closed_term(obj)
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
    ) -> None:
        self.assertIsInstance(obj, ValueSnak)
        assert isinstance(obj, ValueSnak)
        self.assert_snak(obj, prop)
        self.assert_value(obj.args[1])
        self.assertEqual(obj.args[1], value)
        self.assertEqual(obj.value, obj.args[1])
        self.assertEqual(obj.get_value(), obj.args[1])

    def assert_some_value_snak(self, obj: Snak, prop: Property) -> None:
        self.assertIsInstance(obj, SomeValueSnak)
        assert isinstance(obj, SomeValueSnak)
        self.assert_snak(obj, prop)

    def assert_no_value_snak(self, obj: Snak, prop: Property) -> None:
        self.assertIsInstance(obj, NoValueSnak)
        assert isinstance(obj, NoValueSnak)
        self.assert_snak(obj, prop)

# -- Annotations -----------------------------------------------------------

    def assert_rank(self, obj: Rank) -> None:
        self.assertIsInstance(obj, Rank)

    def assert_preferred_rank(self, obj: Rank) -> None:
        self.assertIsInstance(obj, PreferredRank)
        self.assert_rank(obj)

    def assert_normal_rank(self, obj: Rank) -> None:
        self.assertIsInstance(obj, NormalRank)
        self.assert_rank(obj)

    def assert_deprecated_rank(self, obj: Rank) -> None:
        self.assertIsInstance(obj, DeprecatedRank)
        self.assert_rank(obj)

# -- Statement -------------------------------------------------------------

    def assert_statement(
            self,
            obj: Statement,
            subject: Entity,
            snak: Snak
    ) -> None:
        self.assert_closed_term(obj)
        self.assertIsInstance(obj, Statement)
        self.assertIsInstance(obj.args[0], Entity)
        self.assertEqual(obj.args[0], subject)
        self.assertEqual(obj.subject, obj.args[0])
        self.assertEqual(obj.get_subject(), obj.args[0])
        self.assertIsInstance(obj.args[1], Snak)
        self.assertEqual(obj.args[1], snak)
        self.assertEqual(obj.snak, obj.args[1])
        self.assertEqual(obj.get_snak(), obj.args[1])

    def assert_annotated_statement(
            self,
            obj: Statement,
            subject: Entity,
            snak: Snak,
            qualifiers: QualifierRecord = QualifierRecord(),
            references: ReferenceRecordSet = ReferenceRecordSet(),
            rank: Rank = NormalRank()
    ) -> None:
        self.assert_statement(obj, subject, snak)
        self.assertIsInstance(obj, AnnotatedStatement)
        assert isinstance(obj, AnnotatedStatement)
        self.assertIsInstance(obj.args[2], QualifierRecord)
        self.assertEqual(obj.args[2], qualifiers)
        self.assertEqual(obj.qualifiers, obj.args[2])
        self.assertEqual(obj.get_qualifiers(), obj.args[2])
        self.assertIsInstance(obj.args[3], ReferenceRecordSet)
        self.assertEqual(obj.args[3], references)
        self.assertEqual(obj.references, obj.args[3])
        self.assertEqual(obj.get_references(), obj.args[3])
        self.assertIsInstance(obj.args[4], Rank)
        self.assertEqual(obj.args[4], rank)
        self.assertEqual(obj.rank, obj.args[4])
        self.assertEqual(obj.get_rank(), obj.args[4])

# -- Filter ----------------------------------------------------------------

    def assert_filter(
            self,
            obj: Filter,
            subject: Fingerprint | None = None,
            property: Fingerprint | None = None,
            value: Fingerprint | None = None,
            snak_mask: Filter.SnakMask = Filter.SnakMask.ALL,
            subject_mask: Filter.DatatypeMask = Filter.DatatypeMask.ENTITY,
            property_mask: Filter.DatatypeMask = Filter.DatatypeMask.PROPERTY,
            value_mask: Filter.DatatypeMask = Filter.DatatypeMask.VALUE,
            rank_mask: Filter.RankMask = Filter.RankMask.ALL,
            best_ranked: bool | None = None,
            language: str | None = None,
            annotated: bool | None = None
    ) -> None:
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
        self.assertEqual(Filter.SnakMask(obj.args[3]), snak_mask)
        self.assertEqual(obj.snak_mask, snak_mask)
        self.assertEqual(obj.get_snak_mask(), snak_mask)
        self.assertEqual(Filter.DatatypeMask(obj.args[4]), subject_mask)
        self.assertEqual(obj.subject_mask, subject_mask)
        self.assertEqual(obj.get_subject_mask(), subject_mask)
        self.assertEqual(Filter.DatatypeMask(obj.args[5]), property_mask)
        self.assertEqual(obj.property_mask, property_mask)
        self.assertEqual(obj.get_property_mask(), property_mask)
        self.assertEqual(Filter.DatatypeMask(obj.args[6]), value_mask)
        self.assertEqual(obj.value_mask, value_mask)
        self.assertEqual(obj.get_value_mask(), value_mask)
        self.assertEqual(Filter.RankMask(obj.args[7]), rank_mask)
        self.assertEqual(obj.rank_mask, rank_mask)
        self.assertEqual(obj.get_rank_mask(), rank_mask)
        if best_ranked is None:
            best_ranked = True
        self.assertEqual(obj.args[8], bool(best_ranked))
        self.assertEqual(obj.best_ranked, bool(best_ranked))
        self.assertEqual(obj.get_best_ranked(), bool(best_ranked))
        self.assertEqual(obj.args[9], language)
        self.assertEqual(obj.language, language)
        self.assertEqual(obj.get_language(), language)
        self.assertEqual(obj.args[10], bool(annotated))
        self.assertEqual(obj.annotated, bool(annotated))
        self.assertEqual(obj.get_annotated(), bool(annotated))


# == Option test case ======================================================

class OptionsTestCase(TestCase):
    """Base class for KIF options test cases."""

    def _test_option_bool(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, bool]] = (),
            envvars: Sequence[str] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            section=section,
            name=name,
            values=[
                (False, False),
                (True, True),
                (0, False),
                (1, True),
                *values],
            envvars=envvars,
            optional=optional)

    def _test_option_float(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, float]] = (),
            envvars: Sequence[str] = (),
            lower_bound: float | None = None,
            upper_bound: float | None = None,
            optional: bool = False
    ) -> None:
        norm = functools.partial(self._clamp, lb=lower_bound, ub=upper_bound)
        self._test_option(
            section=section,
            name=name,
            values=[
                (0., norm(0.)),
                (1., norm(1.)),
                (-33., norm(-33.)),
                (8., norm(8.)),
                (42., norm(42.)),
                *values],
            envvars=envvars,
            type_error={},
            optional=optional)

    def _test_option_int(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, int]] = (),
            envvars: Sequence[str] = (),
            lower_bound: int | None = None,
            upper_bound: int | None = None,
            optional: bool = False
    ) -> None:
        norm = functools.partial(self._clamp, lb=lower_bound, ub=upper_bound)
        self._test_option(
            section=section,
            name=name,
            values=[
                (0, norm(0)),
                (1, norm(1)),
                (-33, norm(-33)),
                (8, norm(8)),
                (42, norm(42)),
                *values],
            envvars=envvars,
            type_error={},
            optional=optional)

    def _test_option_iri(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, IRI]] = (),
            envvars: Sequence[str] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            section=section,
            name=name,
            values=[
                ('x', IRI('x')),
                (IRI('x'), IRI('x')),
                *values],
            envvars=envvars,
            type_error={},
            optional=optional)

    def _test_option_path(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, pathlib.Path]] = (),
            envvars: Sequence[str] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            section=section,
            name=name,
            values=[
                ('x', pathlib.Path('x')),
                (pathlib.Path('x'), pathlib.Path('x')),
                *values],
            envvars=envvars,
            type_error={},
            optional=optional)

    def _test_option_str(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, str]] = (),
            envvars: Sequence[str] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            section=section,
            name=name,
            values=[
                ('x', 'x'),
                ('abc', 'abc'),
                *values],
            envvars=envvars,
            type_error={},
            optional=optional)

    def _test_option(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, Any]],
            envvars: Sequence[str] = (),
            type_error: Any | None = None,
            value_error: Any | None = None,
            optional: bool = False,
    ) -> None:
        values = list(values)
        if optional:
            values.append((None, None))

        def save_environ() -> dict[str, str]:
            return {var: os.environ[var]
                    for var in envvars if var in os.environ}

        def cleanup_environ() -> dict[str, str]:
            save = save_environ()
            for var in envvars:
                if var in os.environ:
                    del os.environ[var]
            return save

        def restore_environ(save: dict[str, str]) -> None:
            for var in envvars:
                if var in os.environ:
                    del os.environ[var]
            for k, v in save.items():
                os.environ[k] = v

        def get_fn(opts: Section) -> Any:
            return getattr(opts, name)

        def set_fn(opts: Section, value: Any) -> None:
            setattr(opts, name, value)
        default_name = 'DEFAULT_' + name.upper()

        def envvars_it(v):
            for input, output in values:
                if input is None:
                    yield v, ('', output)
                elif not isinstance(input, KIF_Object):
                    yield v, (str(input), output)
        saved_environ = cleanup_environ()
        with Context() as ctx:
            opts = section(ctx)
            value = get_fn(opts)
            default_value = getattr(opts, default_name)
            if (type(value) is not type(default_value)
                    and isinstance(value, KIF_Object)):
                default_value = type(value).check(default_value)
            if type(value) is not type(default_value):
                self.assertEqual(value, type(value)(default_value))
            else:
                self.assertEqual(value, default_value)
        restore_environ(saved_environ)
        with Context() as ctx:
            opts = section(ctx)
            if type_error is not None:
                self.assertRaises(TypeError, set_fn, opts, type_error)
            if value_error is not None:
                self.assertRaises(ValueError, set_fn, opts, value_error)
            for t in values:
                input, output = t
                set_fn(opts, input)
                self.assertEqual(get_fn(opts), output, t)
        saved_environ = cleanup_environ()
        with Context() as ctx:
            it = list(itertools.chain(*map(envvars_it, envvars)))
            for t in reversed(it):
                var, (input, output) = t
                os.environ[var] = input
                opts = type(section(ctx))()
                self.assertEqual(get_fn(opts), output, t)
        restore_environ(saved_environ)


# == Store test case =======================================================

class StoreTestCase(TestCase):
    """Base class for KIF store test cases."""

    #: Alias for the store constructor.
    S: ClassVar[type[Store]] = Store

    #: Alias for the type of select specifications.
    _TAssertStoreSelect: TypeAlias = Iterable[Literal[
        's', 'p', 'v', 'sp', 'sv', 'pv', 'spv']]

    #: All valid select specifications.
    _assert_store_select: Final[_TAssertStoreSelect] = (
        's', 'p', 'v', 'sp', 'sv', 'pv', 'spv')

    def _test_option_bool(
            self,
            store: Store,
            name: str,
            values: Sequence[tuple[Any, bool]] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            store=store,
            name=name,
            values=[
                (False, False),
                (True, True),
                (0, False),
                (1, True),
                *values],
            optional=optional)

    def _test_option_float(
            self,
            store: Store,
            name: str,
            values: Sequence[tuple[Any, float]] = (),
            lower_bound: float | None = None,
            upper_bound: float | None = None,
            optional: bool = False
    ) -> None:
        norm = functools.partial(self._clamp, lb=lower_bound, ub=upper_bound)
        self._test_option(
            store=store,
            name=name,
            values=[
                (0., norm(0.)),
                (1., norm(1.)),
                (-33., norm(-33.)),
                (8., norm(8.)),
                (42., norm(42.)),
                *values],
            type_error={},
            optional=optional)

    def _test_option_int(
            self,
            store: Store,
            name: str,
            values: Sequence[tuple[Any, int]] = (),
            lower_bound: int | None = None,
            upper_bound: int | None = None,
            optional: bool = False
    ) -> None:
        norm = functools.partial(self._clamp, lb=lower_bound, ub=upper_bound)
        self._test_option(
            store=store,
            name=name,
            values=[
                (0, norm(0)),
                (1, norm(1)),
                (-33, norm(-33)),
                (8, norm(8)),
                (42, norm(42)),
                *values],
            type_error={},
            optional=optional)

    def _test_option(
            self,
            store: Store,
            name: str,
            values: Sequence[tuple[Any, Any]],
            type_error: Any | None = None,
            value_error: Any | None = None,
            optional: bool = False
    ) -> None:
        values = list(values)
        if optional:
            values.append((None, None))

        def get_fn() -> Any:
            return getattr(store, name)

        def set_fn(value: Any) -> None:
            setattr(store, name, value)

        def _assert_values() -> None:
            for t in values:
                input, output = t
                set_fn(input)
                self.assertEqual(get_fn(), output, t)

        def _assert_nested_values() -> None:
            def _assert_nested_values_helper(
                    vs: Sequence[tuple[Any, Any]]
            ) -> None:
                if vs:
                    saved_value = get_fn()
                    t = vs[0]
                    input, output = t
                    with store(**{name: input}):
                        if input is not None or not optional:
                            self.assertEqual(get_fn(), output, t)
                        _assert_nested_values_helper(vs[1:])
                    self.assertEqual(get_fn(), saved_value)
            _assert_nested_values_helper(values)

        default_value = getattr(store.options, name)
        if type_error is not None:
            self.assertRaises(TypeError, set_fn, type_error)
        if value_error is not None:
            self.assertRaises(ValueError, set_fn, value_error)
        # one level
        self.assertEqual(getattr(store.options, name), default_value)
        self.assertEqual(default_value, get_fn())
        with store() as options:
            self.assertEqual(getattr(store.options, name), get_fn())
            self.assertEqual(getattr(options, name), get_fn())
            _assert_values()
        self.assertEqual(default_value, get_fn())
        # one level overwrite
        for t in values:
            input, output = t
            with store(**{name: input}) as options:
                self.assertEqual(getattr(options, name), output, t)
                self.assertEqual(getattr(store.options, name), output, t)
                self.assertEqual(get_fn(), output, t)
                _assert_values()
            self.assertEqual(default_value, get_fn())
        self.assertEqual(default_value, get_fn())
        # multiple levels override
        _assert_nested_values()
        # resetting
        for t in values:
            input, output = t
            set_fn(input)
            self.assertEqual(getattr(store.options, name), output, t)
            self.assertEqual(get_fn(), output, t)
        set_fn(None)
        # getter takes an optional argument
        self.assertEqual(default_value, get_fn())
        if optional and default_value is None:
            for _, output in values:
                self.assertEqual(
                    getattr(store, 'get_' + name)(output), output)

    def store_ask_assertion(
            self,
            store: Store
    ) -> tuple[Callable[[bool, Filter], None], type[Filter]]:
        """Constructs a :meth:`Store.ask` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Assertion callback plus alias for filter class.
        """
        return functools.partial(self.assert_store_ask, store), Filter

    def assert_store_ask(
            self,
            store: Store,
            expected: bool,
            filter: Filter
    ) -> None:
        """:meth:`Store.ask` assertion.

        Parameters:
           store: Store.
           expected: Expected result.
           filter: Filter.
        """
        assert isinstance(expected, bool)
        self.assertEqual(
            expected,
            store.ask(filter=filter),
            '*** ASK: FAILED ***')
        loop = asyncio.get_event_loop()

        async def a():
            return await store.aask(filter=filter)
        self.assertEqual(
            expected,
            loop.run_until_complete(a()),
            '*** ASYNC ASK: FAILED ***')

    def store_contains_assertion(
            self,
            store: Store
    ) -> Callable[[bool, Statement], None]:
        """Constructs a :meth:`Store.contains` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Assertion callback.
        """
        return functools.partial(self.assert_store_contains, store)

    def assert_store_contains(
            self,
            store: Store,
            expected: bool,
            statement: Statement
    ) -> None:
        """:meth:`Store.contains` assertion.

        Parameters:
           store: Store.
           expected: Expected result.
           statement: Statement.
        """
        assert isinstance(expected, bool)
        (self.assertTrue if expected else self.assertFalse)(
            store.contains(statement),
            f'*** CONTAINS: FAILED FOR STATEMENT ***\n{statement}')
        loop = asyncio.get_event_loop()

        async def c():
            return await store.acontains(statement)
        (self.assertTrue if expected else self.assertFalse)(
            loop.run_until_complete(c()),
            f'*** ASYNC CONTAINS: FAILED FOR STATEMENT ***\n{statement}')

    def store_count_assertion(
            self,
            store: Store
    ) -> tuple[Callable[[int, Filter], None], type[Filter]]:
        """Constructs a :meth:`Store.count` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Assertion callback plus alias for filter class.
        """
        return functools.partial(self.assert_store_count, store), Filter

    def store_count_assertion_with_projection(
            self,
            store: Store
    ) -> tuple[
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        Callable[[int, Filter], None],
        type[Filter]
    ]:
        """Constructs a :meth:`Store.count_*` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Assertion callback plus alias for filter class.
        """
        c = functools.partial(self.assert_store_count, store)
        return (
            c,
            functools.partial(c, select=('s',)),
            functools.partial(c, select=('p',)),
            functools.partial(c, select=('v',)),
            functools.partial(c, select=('sp',)),
            functools.partial(c, select=('sv',)),
            functools.partial(c, select=('pv',)),
            Filter)

    def assert_store_count(
            self,
            store: Store,
            expected: int,
            filter: Filter,
            select: _TAssertStoreSelect = ('spv',)
    ) -> None:
        """:meth:`Store.count` assertion.

        Parameters:
           store: Store.
           expected: Expected count.
           filter: Filter.
           select: Projections to test.
        """
        assert isinstance(expected, int) and expected >= 0
        for spec in select:
            if spec == 's':
                self.assertEqual(
                    expected,
                    store.count_s(filter=filter),
                    '*** COUNT_S: FAILED ***')
            elif spec == 'p':
                self.assertEqual(
                    expected,
                    store.count_p(filter=filter),
                    '*** COUNT_P: FAILED ***')
            elif spec == 'v':
                self.assertEqual(
                    expected,
                    store.count_v(filter=filter),
                    '*** COUNT_V: FAILED ***')
            elif spec == 'sp':
                self.assertEqual(
                    expected,
                    store.count_sp(filter=filter),
                    '*** COUNT_SP: FAILED ***')
            elif spec == 'sv':
                self.assertEqual(
                    expected,
                    store.count_sv(filter=filter),
                    '*** COUNT_SV: FAILED ***')
            elif spec == 'pv':
                self.assertEqual(
                    expected,
                    store.count_pv(filter=filter),
                    '*** COUNT_PV: FAILED ***')
            elif spec == 'spv':
                self.assertEqual(
                    expected,
                    store.count(filter=filter),
                    '*** COUNT: FAILED ***')
            else:
                raise ValueError('spec')
        loop = asyncio.get_event_loop()

        async def c():
            for spec in select:
                if spec == 's':
                    self.assertEqual(
                        expected,
                        await store.acount_s(filter=filter),
                        '*** ACOUNT_S: FAILED ***')
                elif spec == 'p':
                    self.assertEqual(
                        expected,
                        await store.acount_p(filter=filter),
                        '*** ACOUNT_P: FAILED ***')
                elif spec == 'v':
                    self.assertEqual(
                        expected,
                        await store.acount_v(filter=filter),
                        '*** ACOUNT_V: FAILED ***')
                elif spec == 'sp':
                    self.assertEqual(
                        expected,
                        await store.acount_sp(filter=filter),
                        '*** ACOUNT_SP: FAILED ***')
                elif spec == 'sv':
                    self.assertEqual(
                        expected,
                        await store.acount_sv(filter=filter),
                        '*** ACOUNT_SV: FAILED ***')
                elif spec == 'pv':
                    self.assertEqual(
                        expected,
                        await store.acount_pv(filter=filter),
                        '*** ACOUNT_PV: FAILED ***')
                elif spec == 'spv':
                    self.assertEqual(
                        expected,
                        await store.acount(filter=filter),
                        '*** ACOUNT: FAILED ***')
                else:
                    raise ValueError(spec)
        loop.run_until_complete(c())

    def store_filter_assertion(
            self,
            store: Store
    ) -> tuple[Callable[[Filter, Iterable[Statement]], None], type[Filter]]:
        """Constructs a :meth:`Store.filter` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Assertion callback plus alias for filter class.
        """
        return functools.partial(self.assert_store_filter, store), Filter

    def assert_store_filter(
            self,
            store: Store,
            filter: Filter,
            expected: Iterable[Statement],
            select: _TAssertStoreSelect = _assert_store_select
    ) -> None:
        """:meth:`Store.filter` assertion.

        Parameters:
           store: Store.
           filter: Filter.
           expected: Expected statements.
           select: Projections to test.
        """
        if filter.annotated:
            expected = set(map(lambda s: s if isinstance(
                expected, AnnotatedStatement) else s.annotate(), expected))
        else:
            expected = set(expected)
        for spec in select:
            if spec == 's':
                self.assertEqual(
                    set(store.filter_s(filter=filter)),
                    set(self._assert_store_filter_s(expected)),
                    '*** FILTER_S: FAILED ***')
            elif spec == 'p':
                self.assertEqual(
                    set(store.filter_p(filter=filter)),
                    set(self._assert_store_filter_p(expected)),
                    '*** FILTER_P: FAILED ***')
            elif spec == 'v':
                self.assertEqual(
                    set(store.filter_v(filter=filter)),
                    set(self._assert_store_filter_v(expected)),
                    '*** FILTER_V: FAILED ***')
            elif spec == 'sp':
                self.assertEqual(
                    set(store.filter_sp(filter=filter)),
                    set(self._assert_store_filter_sp(expected)),
                    '*** FILTER_SP: FAILED ***')
            elif spec == 'sv':
                self.assertEqual(
                    set(store.filter_sv(filter=filter)),
                    set(self._assert_store_filter_sv(expected)),
                    '*** FILTER_SV: FAILED ***')
            elif spec == 'pv':
                self.assertEqual(
                    set(store.filter_pv(filter=filter)),
                    set(self._assert_store_filter_pv(expected)),
                    '*** FILTER_PV: FAILED ***')
            elif spec == 'spv':
                self.assertEqual(
                    set(store.filter(filter=filter)),
                    expected,
                    '*** FILTER: FAILED ***')
            else:
                raise ValueError(spec)
        loop = asyncio.get_event_loop()

        async def f():
            for spec in select:
                if spec == 's':
                    self.assertEqual(
                        {x async for x in store.afilter_s(filter=filter)},
                        set(self._assert_store_filter_s(expected)),
                        '*** AFILTER_S: FAILED ***')
                elif spec == 'p':
                    self.assertEqual(
                        {x async for x in store.afilter_p(filter=filter)},
                        set(self._assert_store_filter_p(expected)),
                        '*** AFILTER_P: FAILED ***')
                elif spec == 'v':
                    self.assertEqual(
                        {x async for x in store.afilter_v(filter=filter)},
                        set(self._assert_store_filter_v(expected)),
                        '*** AFILTER_V: FAILED ***')
                elif spec == 'sp':
                    self.assertEqual(
                        {x async for x in store.afilter_sp(filter=filter)},
                        set(self._assert_store_filter_sp(expected)),
                        '*** AFILTER_SP: FAILED ***')
                elif spec == 'sv':
                    self.assertEqual(
                        {x async for x in store.afilter_sv(filter=filter)},
                        set(self._assert_store_filter_sv(expected)),
                        '*** AFILTER_SV: FAILED ***')
                elif spec == 'pv':
                    self.assertEqual(
                        {x async for x in store.afilter_pv(filter=filter)},
                        set(self._assert_store_filter_pv(expected)),
                        '*** AFILTER_PV: FAILED ***')
                elif spec == 'spv':
                    self.assertEqual(
                        {x async for x in store.afilter(filter=filter)},
                        expected,
                        '*** AFILTER: FAILED ***')
                else:
                    raise ValueError(spec)
        loop.run_until_complete(f())

    def _assert_store_filter_s(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[Entity]:
        return map(lambda s: s.subject, stmts)

    def _assert_store_filter_p(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[Property]:
        return map(lambda s: s.snak.property, stmts)

    def _assert_store_filter_v(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[Value]:
        return map(
            lambda s: cast(ValueSnak, s.snak).value,
            itertools.filter(lambda s: isinstance(
                s.snak, ValueSnak), stmts))

    def _assert_store_filter_sp(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[ValuePair[Entity, Property]]:
        return map(lambda s: ValuePair(s.subject, s.snak.property), stmts)

    def _assert_store_filter_sv(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[ValuePair[Entity, Value]]:
        return map(
            lambda s: ValuePair(s.subject, cast(ValueSnak, s.snak).value),
            itertools.filter(lambda s: isinstance(s.snak, ValueSnak), stmts))

    def _assert_store_filter_pv(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[ValueSnak]:
        return map(
            lambda s: cast(ValueSnak, s.snak),
            itertools.filter(lambda s: isinstance(
                s.snak, ValueSnak), stmts))

    def store_xfilter_assertion(
            self,
            store: Store
    ) -> tuple[Callable[[Filter, Iterable[Statement]], None], type[Filter]]:
        """Constructs an extended :meth:`Store.filter` assertion callback.

        Parameters:
           store: Store.

        Returns:
           Extended assertion callback plus alias for filter class.
        """
        return functools.partial(self.assert_store_xfilter, store), Filter

    def assert_store_xfilter(
            self,
            store: Store,
            filter: Filter,
            expected: Iterable[Statement],
            select: _TAssertStoreSelect = _assert_store_select
    ) -> None:
        """Extended :meth:`Store.filter` assertion.

        This function applies :meth:`Store.filter` with and without
        annotations and checks the results of both calls against the
        annotated and unannotated version of the `expected` statements.

        Parameters:
           store: Store.
           filter: Filter.
           expected: Expected (annotated) statements.
           select: Projections to test.
        """
        self.assert_store_filter(
            store,
            filter.replace(annotated=False),
            set(map(Statement.unannotate, expected)), select)
        self.assertEqual(
            set(store.filter_annotated(filter=filter)),
            set(self._assert_store_xfilter_annotate(expected)),
            '*** XFILTER: ANNOTATED FILTER FAILED ***')
        loop = asyncio.get_event_loop()

        async def fa():
            return {stmt async for stmt in store.afilter_annotated(
                filter=filter)}
        self.assertEqual(
            loop.run_until_complete(fa()),
            set(self._assert_store_xfilter_annotate(expected)),
            '*** ASYNC XFILTER: ANNOTATED FILTER FAILED ***')

    def _assert_store_xfilter_annotate(
            self,
            stmts: Iterable[Statement]
    ) -> Iterator[AnnotatedStatement]:
        for stmt in stmts:
            if isinstance(stmt, AnnotatedStatement):
                yield stmt
            else:
                yield stmt.annotate()
