# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import datetime
import decimal

from ... import itertools
from ... import namespace as NS
from ...error import ShouldNotGetHere
from ...model import (
    Datatype,
    DatatypeVariable,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    NoValueSnakVariable,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityTemplate,
    QuantityVariable,
    Snak,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    StringTemplate,
    StringVariable,
    Template,
    Text,
    TextTemplate,
    TextVariable,
    Time,
    TimeTemplate,
    TimeVariable,
    V_IRI,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    Variable,
    VEntity,
    VExternalId,
    VItem,
    VLexeme,
    VNoValueSnak,
    VProperty,
    VQuantity,
    VSnak,
    VSomeValueSnak,
    VString,
    VText,
    VTime,
    VValue,
    VValueSnak,
)
from ...typing import (
    Any,
    cast,
    Iterator,
    Optional,
    override,
    Self,
    TypeAlias,
    TypeVar,
)
from .builder import Query
from .compiler import SPARQL_Compiler
from .substitution import Substitution

T = TypeVar('T')
TPattern: TypeAlias = KIF_Object


class SPARQL_PatternCompiler(SPARQL_Compiler):
    """SPARQL pattern compiler."""

    __slots__ = (
        '_pattern',
        '_theta',
    )

    #: The source pattern.
    _pattern: TPattern

    #: The compiled substitution.
    _theta: Substitution

    def __init__(
            self,
            pattern: TPattern,
            flags: Optional['SPARQL_PatternCompiler.Flags'] = None
    ):
        super().__init__(flags)
        self._pattern = pattern
        self._theta = Substitution()

    @property
    def pattern(self) -> TPattern:
        """The source pattern."""
        return self.get_pattern()

    def get_pattern(self) -> TPattern:
        """Gets the source pattern.

        Returns:
           Pattern.
        """
        return self._pattern

    @property
    def theta(self) -> Substitution:
        """The compiled substitution."""
        return self.get_theta()

    def get_theta(self) -> Substitution:
        """Gets the compiled substitution.

        Returns:
           Substitution.
        """
        return self._theta

# -- Helper methods --------------------------------------------------------

    def _theta_add(self, var: Variable, v: T) -> T:
        if self.has_flags(self.DEBUG):
            self._q.comments()(f'{var} := {Substitution._dump_value(v)}')
        return self._theta.add(var, v)

    def _theta_add_default(
            self,
            var: Variable,
            value: Optional[KIF_Object]
    ) -> Variable:
        return self._theta.add_default(var, value)

    def _as_qvar(self, var: Variable) -> Query.Variable:
        return self._qvar(var.name)

    def _as_qvars(
            self,
            var: Variable,
            *vars: Variable
    ) -> Iterator[Query.Variable]:
        return map(self._as_qvar, itertools.chain((var,), vars))

    def _fresh_variable(self, variable_class: type[Variable]) -> Variable:
        return variable_class(str(self._fresh_qvar()))

    def _fresh_variables(
            self,
            variable_class: type[Variable],
            n: int
    ) -> Iterator[Variable]:
        return map(
            lambda qvar: variable_class(str(qvar)), self._fresh_qvars(n))

    def _fresh_datatype_variable(self) -> DatatypeVariable:
        return cast(DatatypeVariable, self._fresh_variable(DatatypeVariable))

    def _fresh_value_variable(self) -> ValueVariable:
        return cast(ValueVariable, self._fresh_variable(ValueVariable))

    def _fresh_entity_variable(self) -> EntityVariable:
        return cast(EntityVariable, self._fresh_variable(EntityVariable))

    def _fresh_item_variable(self) -> ItemVariable:
        return cast(ItemVariable, self._fresh_variable(ItemVariable))

    def _fresh_property_variable(self) -> PropertyVariable:
        return cast(PropertyVariable, self._fresh_variable(PropertyVariable))

    def _fresh_lexeme_variable(self) -> LexemeVariable:
        return cast(LexemeVariable, self._fresh_variable(LexemeVariable))

    def _fresh_iri_variable(self) -> IRI_Variable:
        return cast(IRI_Variable, self._fresh_variable(IRI_Variable))

    def _fresh_string_variable(self) -> StringVariable:
        return cast(StringVariable, self._fresh_variable(StringVariable))

    def _fresh_quantity_variable(self) -> QuantityVariable:
        return cast(QuantityVariable, self._fresh_variable(QuantityVariable))

    def _fresh_time_variable(self) -> TimeVariable:
        return cast(TimeVariable, self._fresh_variable(TimeVariable))

    def _fresh_snak_variable(self) -> SnakVariable:
        return cast(SnakVariable, self._fresh_variable(SnakVariable))

    def _fresh_value_snak_variable(self) -> ValueSnakVariable:
        return cast(ValueSnakVariable, self._fresh_variable(
            ValueSnakVariable))

    def _fresh_some_value_snak_variable(self) -> SomeValueSnakVariable:
        return cast(SomeValueSnakVariable, self._fresh_variable(
            SomeValueSnakVariable))

    def _fresh_no_value_snak_variable(self) -> NoValueSnakVariable:
        return cast(NoValueSnakVariable, self._fresh_variable(
            NoValueSnakVariable))

    def _fresh_statement_variable(self) -> StatementVariable:
        return cast(StatementVariable, self._fresh_variable(StatementVariable))

# -- Compilation -----------------------------------------------------------

    @override
    def compile(self) -> Self:
        self._compile(self._pattern)
        return self

    def _compile(self, obj: KIF_Object) -> Any:
        if isinstance(obj, Template):
            if isinstance(obj, ValueTemplate):
                return self._compile_value_template(obj)
            elif isinstance(obj, SnakTemplate):
                return self._compile_snak_template(obj)
            elif isinstance(obj, StatementTemplate):
                return self._compile_statement_template(obj)
            else:
                raise self._cannot_compile_error(obj)
        elif isinstance(obj, Variable):
            if isinstance(obj, ValueVariable):
                return self._compile_value_variable(obj)
            elif isinstance(obj, SnakVariable):
                return self._compile_snak_variable(obj)
            elif isinstance(obj, StatementVariable):
                return self._compile_statement_variable(obj)
            else:
                raise self._cannot_compile_error(obj)
        elif isinstance(obj, Value):
            return self._compile_value(obj)
        elif isinstance(obj, Snak):
            return self._compile_snak(obj)
        elif isinstance(obj, Statement):
            return self._compile_statement(obj)
        else:
            raise self._cannot_compile_error(obj)

    def _compile_value_template(self, obj: ValueTemplate) -> Any:
        if isinstance(obj, EntityTemplate):
            if isinstance(obj, ItemTemplate):
                return self._push_item_template(obj)
            elif isinstance(obj, PropertyTemplate):
                return self._push_property_template(obj)
            elif isinstance(obj, LexemeTemplate):
                return self._push_lexeme_template(obj)
            else:
                raise ShouldNotGetHere
        else:
            return self._push_value_snak_template(
                ValueSnakTemplate(self._fresh_property_variable(), obj))

    def _compile_value_variable(self, obj: ValueVariable) -> Any:
        if isinstance(obj, EntityVariable):
            if isinstance(obj, ItemVariable):
                return self._push_item_variable(obj)
            elif isinstance(obj, PropertyVariable):
                return self._push_property_variable(obj)
            elif isinstance(obj, LexemeVariable):
                return self._push_lexeme_variable(obj)
            else:
                return self._push_entity_variable(obj)
        else:
            return self._push_value_snak_template(
                ValueSnakTemplate(self._fresh_property_variable(), obj))

    def _compile_value(self, obj: Value) -> Any:
        if isinstance(obj, Entity):
            if isinstance(obj, Item):
                return self._push_item(obj)
            elif isinstance(obj, Property):
                return self._push_property(obj)
            elif isinstance(obj, Lexeme):
                return self._push_lexeme(obj)
            else:
                raise ShouldNotGetHere
        else:
            return self._push_value_snak_template(
                ValueSnakTemplate(self._fresh_property_variable(), obj))

    def _compile_snak_template(self, obj: SnakTemplate) -> Any:
        if isinstance(obj, ValueSnakTemplate):
            return self._push_value_snak_template(obj)
        elif isinstance(obj, SomeValueSnakTemplate):
            return self._push_some_value_snak_template(obj)
        elif isinstance(obj, NoValueSnakTemplate):
            return self._push_no_value_snak_template(obj)
        else:
            raise ShouldNotGetHere

    def _compile_snak_variable(self, obj: SnakVariable) -> Any:
        if isinstance(obj, ValueSnakVariable):
            return self._push_value_snak_variable(obj)
        elif isinstance(obj, SomeValueSnakVariable):
            return self._push_some_value_snak_variable(obj)
        elif isinstance(obj, NoValueSnakVariable):
            return self._push_no_value_snak_variable(obj)
        elif isinstance(obj, SnakVariable):
            return self._push_snak_variable(obj)
        else:
            raise ShouldNotGetHere

    def _compile_snak(self, obj: Snak) -> Any:
        if isinstance(obj, ValueSnak):
            return self._push_value_snak(obj)
        elif isinstance(obj, SomeValueSnak):
            return self._push_some_value_snak(obj)
        elif isinstance(obj, NoValueSnak):
            return self._push_no_value_snak(obj)
        else:
            raise ShouldNotGetHere

    def _compile_statement_template(self, obj: StatementTemplate) -> Any:
        return self._push_statement_template(obj)

    def _compile_statement_variable(self, obj: StatementVariable) -> Any:
        return self._push_statement_variable(obj)

    def _compile_statement(self, obj: Statement) -> Any:
        return self._push_statement(obj)

# -- Entity ----------------------------------------------------------------

    def _push_entity_variable(self, obj: EntityVariable) -> Query.Variable:
        with self._q.union():
            v = self._as_qvar(obj)
            with self._q.group():
                v1 = self._push_item_variable(self._theta_add(
                    ItemVariable(obj.name),
                    self._fresh_item_variable()))
                self._q.bind(v1, v)
            with self._q.group():
                v2 = self._push_property_variable(self._theta_add(
                    PropertyVariable(obj.name),
                    self._fresh_property_variable()))
                self._q.bind(v2, v)
            with self._q.group():
                v3 = self._push_lexeme_variable(self._theta_add(
                    LexemeVariable(obj.name),
                    self._fresh_lexeme_variable()))
                self._q.bind(v3, v)
        return v

# -- Item ------------------------------------------------------------------

    def _push_v_item(self, obj: VItem) -> Query.V_URI:
        if isinstance(obj, ItemTemplate):
            return self._push_item_template(obj)
        elif isinstance(obj, ItemVariable):
            return self._push_item_variable(obj)
        elif isinstance(obj, Item):
            return self._push_item(obj)
        else:
            raise ShouldNotGetHere

    def _push_item_template(self, obj: ItemTemplate) -> Query.V_URI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.SCHEMA.version, self._q.bnode()))
        return iri

    def _push_item_variable(self, obj: ItemVariable) -> Query.Variable:
        obj_iri = IRI_Variable(obj.name)
        var = self._push_item_template(
            self._theta_add(obj, ItemTemplate(obj_iri)))
        assert isinstance(var, Query.Variable)
        return var

    def _push_item(self, obj: Item) -> Query.URI:
        iri = self._push_item_template(ItemTemplate(*obj.args))
        assert isinstance(iri, Query.URI)
        return iri

# -- Property --------------------------------------------------------------

    def _push_v_property(self, obj: VProperty) -> Query.V_URI:
        if isinstance(obj, PropertyTemplate):
            return self._push_property_template(obj)
        elif isinstance(obj, PropertyVariable):
            return self._push_property_variable(obj)
        elif isinstance(obj, Property):
            return self._push_property(obj)
        else:
            raise ShouldNotGetHere

    def _push_property_template(self, obj: PropertyTemplate) -> Query.V_URI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.RDF.type, NS.WIKIBASE.Property))
        return iri

    def _push_property_variable(self, obj: PropertyVariable) -> Query.Variable:
        obj_iri = IRI_Variable(obj.name)
        iri = self._push_property_template(
            self._theta_add(obj, PropertyTemplate(obj_iri)))
        assert isinstance(iri, Query.Variable)
        return iri

    def _push_property(self, obj: Property) -> Query.URI:
        iri = self._push_property_template(PropertyTemplate(*obj.args))
        assert isinstance(iri, Query.URI)
        return iri

# -- Lexeme ----------------------------------------------------------------

    def _push_v_lexeme(self, obj: VLexeme) -> Query.V_URI:
        if isinstance(obj, LexemeTemplate):
            return self._push_lexeme_template(obj)
        elif isinstance(obj, LexemeVariable):
            return self._push_lexeme_variable(obj)
        elif isinstance(obj, Lexeme):
            return self._push_lexeme(obj)
        else:
            raise ShouldNotGetHere

    def _push_lexeme_template(self, obj: LexemeTemplate) -> Query.V_URI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        return iri

    def _push_lexeme_variable(self, obj: LexemeVariable) -> Query.Variable:
        obj_iri = IRI_Variable(obj.name)
        iri = self._push_lexeme_template(
            self._theta_add(obj, LexemeTemplate(obj_iri)))
        assert isinstance(iri, Query.Variable)
        return iri

    def _push_lexeme(self, obj: Lexeme) -> Query.URI:
        iri = self._push_lexeme_template(LexemeTemplate(*obj.args))
        assert isinstance(iri, Query.URI)
        return iri

# -- IRI -------------------------------------------------------------------

    def _push_v_iri(self, obj: V_IRI) -> Query.V_URI:
        if isinstance(obj, IRI_Template):
            return self._push_iri_template(obj)
        elif isinstance(obj, IRI_Variable):
            return self._push_iri_variable(obj)
        elif isinstance(obj, IRI):
            return self._push_iri(obj)
        else:
            raise ShouldNotGetHere

    def _push_iri_template(self, obj: IRI_Template) -> Query.V_URI:
        obj_content = obj.content
        content: Query.V_URI
        if isinstance(obj_content, StringVariable):
            content = self._as_qvar(obj_content)
            content_str = self._theta_add(obj_content, self._fresh_qvar())
            self._q.bind(self._q.str(content), content_str)
            return content
        elif isinstance(obj_content, str):
            content = self._push_iri(IRI(obj_content))
        else:
            raise ShouldNotGetHere
        return content

    def _push_iri_variable(self, obj: IRI_Variable) -> Query.Variable:
        return cast(Query.Variable, self._theta_add(obj, self._as_qvar(obj)))

    def _push_iri(self, obj: IRI) -> Query.URI:
        return self._q.uri(obj.content)

# -- Text ------------------------------------------------------------------

    def _push_v_text(
            self,
            obj: VText
    ) -> tuple[Query.VLiteral, Query.VLiteral]:
        if isinstance(obj, TextTemplate):
            return self._push_text_template(obj)
        elif isinstance(obj, TextVariable):
            return self._push_text_variable(obj)
        elif isinstance(obj, Text):
            return self._push_text(obj)
        else:
            raise ShouldNotGetHere

    def _push_text_template(
            self,
            obj: TextTemplate
    ) -> tuple[Query.VLiteral, Query.VLiteral]:
        obj_content = obj.content
        obj_lang = obj.language
        content: Query.VLiteral
        lang: Query.VLiteral
        if isinstance(obj_content, StringVariable):
            content = self._as_qvar(obj_content)
            lang = self._push_text_template_language(obj, content)
            self._theta_add(obj_content, content)
        elif isinstance(obj_content, str):
            if isinstance(obj_lang, StringVariable):
                content = self._fresh_qvar()
                self._q.filter(self._q.eq(
                    self._q.str(content), self._q.literal(obj_content)))
                lang = self._push_text_template_language(obj, content)
            else:
                content, lang = self._push_text(Text(obj_content, obj_lang))
        else:
            raise ShouldNotGetHere
        return content, lang

    def _push_text_template_language(
            self,
            obj: TextTemplate,
            content: Query.VLiteral
    ) -> Query.VLiteral:
        obj_lang = obj.language
        lang: Query.VLiteral
        if isinstance(obj_lang, StringVariable):
            lang = self._theta_add(obj_lang, self._fresh_qvar())
            self._q.bind(self._q.lang(content), lang)
        elif isinstance(obj_lang, str):
            lang = self._q.literal(obj_lang)
            self._q.filter(self._q.eq(self._q.lang(content), lang))
        else:
            raise ShouldNotGetHere
        return lang

    def _push_text_variable(
            self,
            obj: TextVariable
    ) -> tuple[Query.Variable, Query.Variable]:
        obj_content = self._fresh_string_variable()
        obj_lang = self._fresh_string_variable()
        tpl = self._theta_add(obj, TextTemplate(obj_content, obj_lang))
        content, lang = self._push_text_template(tpl)
        assert isinstance(content, Query.Variable)
        assert isinstance(lang, Query.Variable)
        return content, lang

    def _push_text(self, obj: Text) -> tuple[Query.Literal, Query.Literal]:
        return (
            self._q.literal(obj.content, language=obj.language),
            self._q.literal(obj.language))

# -- String ----------------------------------------------------------------

    def _push_v_string(self, obj: VString) -> Query.VTerm:
        if isinstance(obj, StringTemplate):
            return self._push_string_template(obj)
        elif isinstance(obj, StringVariable):
            return self._push_string_variable(obj)
        elif isinstance(obj, String):
            return self._push_string(obj)
        else:
            raise ShouldNotGetHere

    def _push_string_template(self, obj: StringTemplate) -> Query.VLiteral:
        obj_content = obj.content
        content: Query.VLiteral
        if isinstance(obj_content, StringVariable):
            content = self._theta_add(obj_content, self._as_qvar(obj_content))
        elif isinstance(obj_content, str):
            content = self._push_string(String(obj_content))
        else:
            raise ShouldNotGetHere
        return content

    def _push_string_variable(self, obj: StringVariable) -> Query.Variable:
        return cast(Query.Variable, self._theta_add(obj, self._as_qvar(obj)))

    def _push_string(self, obj: String) -> Query.Literal:
        return self._q.literal(obj.content)

# -- External id -----------------------------------------------------------

    def _push_v_external_id(self, obj: VExternalId) -> Query.VTerm:
        if isinstance(obj, ExternalIdTemplate):
            return self._push_external_id_template(obj)
        elif isinstance(obj, ExternalIdVariable):
            return self._push_external_id_variable(obj)
        elif isinstance(obj, ExternalId):
            return self._push_external_id(obj)
        else:
            raise ShouldNotGetHere

    def _push_external_id_template(
            self,
            obj: ExternalIdTemplate
    ) -> Query.VLiteral:
        obj_content = obj.content
        content: Query.VLiteral
        if isinstance(obj_content, StringVariable):
            content = self._theta_add(
                obj_content, self._as_qvar(obj_content))
        elif isinstance(obj_content, str):
            content = self._push_external_id(ExternalId(obj_content))
        else:
            raise ShouldNotGetHere
        return content

    def _push_external_id_variable(
            self,
            obj: ExternalIdVariable
    ) -> Query.Variable:
        return self._theta_add(obj, self._as_qvar(obj))

    def _push_external_id(self, obj: ExternalId) -> Query.Literal:
        return self._q.literal(obj.content)

# -- Quantity --------------------------------------------------------------

    def _push_v_quantity(
            self,
            obj: VQuantity,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.VLiteral, Query.V_URI, Query.VLiteral, Query.VLiteral]:
        if isinstance(obj, QuantityTemplate):
            return self._push_quantity_template(obj, prop, wds)
        elif isinstance(obj, QuantityVariable):
            return self._push_quantity_variable(obj, prop, wds)
        elif isinstance(obj, Quantity):
            return self._push_quantity(obj, prop, wds)
        else:
            raise ShouldNotGetHere

    def _push_quantity_template(
            self,
            obj: QuantityTemplate,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.VLiteral, Query.V_URI, Query.VLiteral, Query.VLiteral]:
        obj_amount, obj_unit, obj_lb, obj_ub = obj.args
        amount: Query.VLiteral
        unit: Query.V_URI
        lb: Query.VLiteral
        ub: Query.VLiteral
        with self._q.group():
            if isinstance(obj_amount, QuantityVariable):
                amount = self._as_qvar(obj_amount)
                self._theta_add(obj_amount, amount)
            elif isinstance(obj_amount, decimal.Decimal):
                amount = self._q.literal(obj_amount)
            else:
                raise ShouldNotGetHere
            if obj_unit is None:
                obj_unit = self._fresh_item_variable()
            if isinstance(obj_unit, ItemVariable):
                unit = self._push_item_variable(obj_unit)
                self._theta_add_default(obj_unit, None)
            elif isinstance(obj_unit, Item):
                unit = self._push_item(obj_unit)
            else:
                raise ShouldNotGetHere
            if obj_lb is None:
                obj_lb = self._fresh_quantity_variable()
            if isinstance(obj_lb, QuantityVariable):
                lb = self._theta_add(obj_lb, self._as_qvar(obj_lb))
                self._theta_add_default(obj_lb, None)
            else:
                lb = self._q.literal(obj_lb)
            if obj_ub is None:
                obj_ub = self._fresh_quantity_variable()
            if isinstance(obj_ub, QuantityVariable):
                ub = self._theta_add(obj_ub, self._as_qvar(obj_ub))
                self._theta_add_default(obj_ub, None)
            else:
                ub = self._q.literal(obj_ub)
            wdv, psv = self._fresh_qvars(2)
            self._q.triples()(
                (prop, NS.WIKIBASE.statementValue, psv),
                (wds, psv, wdv),
                (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue),
                (wdv, NS.WIKIBASE.quantityAmount, amount))
            with self._q.optional_if(isinstance(unit, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, unit))
            with self._q.optional_if(isinstance(lb, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityLowerBound, lb))
            with self._q.optional_if(isinstance(ub, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityUpperBound, ub))
            return amount, unit, lb, ub

    def _push_quantity_variable(
            self,
            obj: QuantityVariable,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.Variable, Query.Variable, Query.Variable, Query.Variable]:
        obj_amount = self._fresh_quantity_variable()
        obj_unit = self._fresh_item_variable()
        obj_lb = self._fresh_quantity_variable()
        obj_ub = self._fresh_quantity_variable()
        tpl = self._theta_add(
            obj, QuantityTemplate(obj_amount, obj_unit, obj_lb, obj_ub))
        amount, unit, lb, ub = self._push_quantity_template(tpl, prop, wds)
        assert isinstance(amount, Query.Variable)
        assert isinstance(unit, Query.Variable)
        assert isinstance(lb, Query.Variable)
        assert isinstance(ub, Query.Variable)
        return amount, unit, lb, ub

    def _push_quantity(
            self,
            obj: Quantity,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.Literal, Query.V_URI, Query.VLiteral, Query.VLiteral]:
        tpl = QuantityTemplate(*obj.args)
        amount, unit, lb, ub = self._push_quantity_template(tpl, prop, wds)
        assert isinstance(amount, Query.Literal)
        return amount, unit, lb, ub

# -- Time ------------------------------------------------------------------

    def _push_v_time(
            self,
            obj: VTime,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.VLiteral, Query.VLiteral, Query.VLiteral, Query.V_URI]:
        if isinstance(obj, TimeTemplate):
            return self._push_time_template(obj, prop, wds)
        elif isinstance(obj, TimeVariable):
            return self._push_time_variable(obj, prop, wds)
        elif isinstance(obj, Time):
            return self._push_time(obj, prop, wds)
        else:
            raise ShouldNotGetHere

    def _push_time_template(
            self,
            obj: TimeTemplate,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.VLiteral, Query.VLiteral, Query.VLiteral, Query.V_URI]:
        obj_time, obj_prec, obj_tz, obj_cal = obj.args
        time: Query.VLiteral
        prec: Query.VLiteral
        tz: Query.VLiteral
        cal: Query.V_URI
        with self._q.group():
            if isinstance(obj_time, TimeVariable):
                time = self._theta_add(obj_time, self._as_qvar(obj_time))
            elif isinstance(obj_time, datetime.datetime):
                time = self._q.literal(obj_time)
            else:
                raise ShouldNotGetHere
            if obj_prec is None:
                obj_prec = self._fresh_quantity_variable()
            if isinstance(obj_prec, QuantityVariable):
                prec = self._theta_add(obj_prec, self._as_qvar(obj_prec))
                self._theta_add_default(obj_prec, None)
            else:
                prec = self._q.literal(obj_prec.value)
            if obj_tz is None:
                obj_tz = self._fresh_quantity_variable()
            if isinstance(obj_tz, QuantityVariable):
                tz = self._theta_add(obj_tz, self._as_qvar(obj_tz))
                self._theta_add_default(obj_tz, None)
            else:
                tz = self._q.literal(obj_tz)
            if obj_cal is None:
                obj_cal = self._fresh_item_variable()
            if isinstance(obj_cal, ItemVariable):
                cal = self._push_item_variable(obj_cal)
                self._theta_add_default(obj_cal, None)
            elif isinstance(obj_cal, Item):
                cal = self._push_item(obj_cal)
            else:
                raise ShouldNotGetHere
            wdv, psv = self._fresh_qvars(2)
            self._q.triples()(
                (prop, NS.WIKIBASE.statementValue, psv),
                (wds, psv, wdv),
                (wdv, NS.RDF.type, NS.WIKIBASE.TimeValue),
                (wdv, NS.WIKIBASE.timeValue, time))
            with self._q.optional_if(isinstance(prec, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.timePrecision, prec))
            with self._q.optional_if(isinstance(tz, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.timeTimezone, tz))
            with self._q.optional_if(isinstance(cal, Query.Variable)):
                self._q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, cal))
            return time, prec, tz, cal

    def _push_time_variable(
            self,
            obj: TimeVariable,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.Variable, Query.Variable, Query.Variable, Query.Variable]:
        obj_time = self._fresh_time_variable()
        obj_prec = self._fresh_quantity_variable()
        obj_tz = self._fresh_quantity_variable()
        obj_cal = self._fresh_item_variable()
        tpl = self._theta_add(
            obj, TimeTemplate(obj_time, obj_prec, obj_tz, obj_cal))
        time, prec, tz, cal = self._push_time_template(tpl, prop, wds)
        assert isinstance(time, Query.Variable)
        assert isinstance(prec, Query.Variable)
        assert isinstance(tz, Query.Variable)
        assert isinstance(cal, Query.Variable)
        return time, prec, tz, cal

    def _push_time(
            self,
            obj: Time,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> tuple[Query.Literal, Query.VLiteral, Query.VLiteral, Query.V_URI]:
        tpl = TimeTemplate(*obj.args)
        time, prec, tz, cal = self._push_time_template(tpl, prop, wds)
        assert isinstance(time, Query.Literal)
        return time, prec, tz, cal

# -- Snak ------------------------------------------------------------------

    def _push_snak_variable(
            self,
            obj: SnakVariable,
            wds: Optional[Query.Variable] = None,
            subject: Optional[Query.V_URI] = None
    ) -> Query.Variable:
        def _push_subject(wds, prop):
            if subject is not None:
                p = self._fresh_qvar()
                self._q.triples()(
                    (prop, NS.WIKIBASE.claim, p),
                    (subject, p, wds))
            return wds, prop
        if wds is None:
            wds = self._fresh_qvar()
        assert wds is not None
        with self._q.union():
            with self._q.group():
                v1, _ = _push_subject(*self._push_value_snak_variable(
                    ValueSnakVariable(obj.name), wds))
            with self._q.group():
                v2, _ = _push_subject(*self._push_some_value_snak_variable(
                    SomeValueSnakVariable(obj.name), wds))
            with self._q.group():
                v3, _ = _push_subject(*self._push_no_value_snak_variable(
                    NoValueSnakVariable(obj.name), wds))
            assert v1 == v2 and v2 == v3
            return v1

# -- Value snak ------------------------------------------------------------

    def _push_v_value_snak(
            self,
            obj: VValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        if isinstance(obj, ValueSnakTemplate):
            return self._push_value_snak_template(obj, wds)
        elif isinstance(obj, ValueSnakVariable):
            return self._push_value_snak_variable(obj, wds)
        elif isinstance(obj, ValueSnak):
            return self._push_value_snak(obj, wds)
        else:
            raise ShouldNotGetHere

    def _push_value_snak_template(
            self,
            obj: ValueSnakTemplate,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        with self._q.group():
            obj_property = obj.property
            prop = self._push_v_property(obj_property)
            ps = self._fresh_qvar()
            if wds is None:
                wds = self._fresh_qvar()
            assert wds is not None
            self._q.begin_union()
            it = self._iter_possible_datatypes_for_v_value(obj.value)
            for dt in it:
                obj_value: VValue
                if isinstance(obj.value, ValueVariable):
                    obj_value_var_class = dt.value_class.variable_class
                    obj_value_var = obj_value_var_class(obj.value.name)
                    obj_value = self._theta_add(
                        obj_value_var,
                        cast(ValueVariable, self._fresh_variable(
                            obj_value_var_class)))
                else:
                    obj_value = obj.value
                self._q.begin_group()
                self._q.triples()(
                    (prop, NS.WIKIBASE.propertyType, dt._to_rdflib()),
                    (prop, NS.WIKIBASE.statementProperty, ps),
                    (wds, ps, self._push_v_value(obj_value, prop, wds)))
                self._q.end_group()
            self._q.end_union()
            return wds, prop

    def _iter_possible_datatypes_for_v_value(
            self,
            obj: VValue
    ) -> Iterator[Datatype]:
        if isinstance(obj, ValueTemplate):
            yield obj.object_class.datatype
        elif isinstance(obj, Value):
            yield obj.datatype
        elif isinstance(obj, ValueVariable):
            def it(cls):
                try:
                    yield cls.object_class.datatype
                except AttributeError:
                    pass
                for subclass in cls.__subclasses__():
                    try:
                        yield from it(subclass)
                    except ValueError:
                        pass
            yield from it(obj.__class__)
        else:
            raise ShouldNotGetHere

    def _push_v_value(
            self,
            obj: VValue,
            prop: Query.V_URI,
            wds: Query.V_URI
    ) -> Query.VTerm:
        if isinstance(obj, (EntityTemplate, EntityVariable, Entity)):
            return self._push_v_entity(obj)
        elif isinstance(obj, (IRI_Template, IRI_Variable, IRI)):
            return self._push_v_iri(obj)
        elif isinstance(obj, (TextTemplate, TextVariable, Text)):
            return self._push_v_text(obj)[0]
        elif isinstance(obj, (
                ExternalIdTemplate, ExternalIdVariable, ExternalId)):
            return self._push_v_external_id(obj)
        elif isinstance(obj, (StringTemplate, StringVariable, String)):
            return self._push_v_string(obj)
        elif isinstance(obj, (QuantityTemplate, QuantityVariable, Quantity)):
            return self._push_v_quantity(obj, prop, wds)[0]
        elif isinstance(obj, (TimeTemplate, TimeVariable, Time)):
            return self._push_v_time(obj, prop, wds)[0]
        else:
            raise ShouldNotGetHere

    def _push_v_entity(
            self,
            obj: VEntity,
    ) -> Query.V_URI:
        if isinstance(obj, (ItemTemplate, ItemVariable, Item)):
            return self._push_v_item(obj)
        elif isinstance(obj, (PropertyTemplate, PropertyVariable, Property)):
            return self._push_v_property(obj)
        elif isinstance(obj, (LexemeTemplate, LexemeVariable, Lexeme)):
            return self._push_v_lexeme(obj)
        else:
            raise ShouldNotGetHere

    def _push_value_snak_variable(
            self,
            obj: ValueSnakVariable,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        obj_prop = self._fresh_property_variable()
        obj_value = self._fresh_value_variable()
        tpl = self._theta_add(obj, ValueSnakTemplate(obj_prop, obj_value))
        wds, prop = self._push_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

    def _push_value_snak(
            self,
            obj: ValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        tpl = ValueSnakTemplate(*obj.args)
        wds, prop = self._push_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

# -- Some-value snak -------------------------------------------------------

    def _push_v_some_value_snak(
            self,
            obj: VSomeValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        if isinstance(obj, SomeValueSnakTemplate):
            return self._push_some_value_snak_template(obj, wds)
        elif isinstance(obj, SomeValueSnakVariable):
            return self._push_some_value_snak_variable(obj, wds)
        elif isinstance(obj, SomeValueSnak):
            return self._push_some_value_snak(obj, wds)
        else:
            raise ShouldNotGetHere

    def _push_some_value_snak_template(
            self,
            obj: SomeValueSnakTemplate,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        with self._q.group():
            prop = self._push_v_property(obj.property)
            ps, value = self._fresh_qvars(2)
            if wds is None:
                wds = self._fresh_qvar()
            assert wds is not None
            self._q.triples()(
                (prop, NS.WIKIBASE.statementProperty, ps),
                (wds, ps, value))
            self._q.filter(self._q.call(NS.WIKIBASE.isSomeValue, value))
            return wds, prop

    def _push_some_value_snak_variable(
            self,
            obj: SomeValueSnakVariable,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        obj_prop = self._fresh_property_variable()
        tpl = self._theta_add(obj, SomeValueSnakTemplate(obj_prop))
        wds, prop = self._push_some_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

    def _push_some_value_snak(
            self,
            obj: SomeValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        tpl = SomeValueSnakTemplate(*obj.args)
        wds, prop = self._push_some_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

# -- No-value snak ---------------------------------------------------------

    def _push_v_no_value_snak(
            self,
            obj: VNoValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        if isinstance(obj, NoValueSnakTemplate):
            return self._push_no_value_snak_template(obj, wds)
        elif isinstance(obj, NoValueSnakVariable):
            return self._push_no_value_snak_variable(obj, wds)
        elif isinstance(obj, NoValueSnak):
            return self._push_no_value_snak(obj, wds)
        else:
            raise ShouldNotGetHere

    def _push_no_value_snak_template(
            self,
            obj: NoValueSnakTemplate,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        with self._q.group():
            prop = self._push_v_property(obj.property)
            wdno = self._fresh_qvar()
            if wds is None:
                wds = self._fresh_qvar()
            assert wds is not None
            self._q.triples()(
                (prop, NS.WIKIBASE.novalue, wdno),
                (wds, NS.RDF.type, wdno))
            return wds, prop

    def _push_no_value_snak_variable(
            self,
            obj: NoValueSnakVariable,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        obj_prop = self._fresh_property_variable()
        tpl = self._theta_add(obj, NoValueSnakTemplate(obj_prop))
        wds, prop = self._push_no_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

    def _push_no_value_snak(
            self,
            obj: NoValueSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        tpl = NoValueSnakTemplate(*obj.args)
        wds, prop = self._push_no_value_snak_template(tpl, wds)
        assert isinstance(wds, Query.Variable)
        return wds, prop

# -- Statement -------------------------------------------------------------

    def _push_statement_template(
            self,
            obj: StatementTemplate
    ) -> Query.Variable:
        with self._q.group():
            obj_subj, obj_snak = obj.args
            subj: Query.V_URI
            wds: Query.Variable
            if type(obj_subj) is EntityVariable:
                subj = self._push_entity_variable(obj_subj)
            else:
                subj = self._push_v_entity(obj_subj)
            if type(obj_snak) is SnakVariable:
                wds = self._push_snak_variable(obj_snak, subject=subj)
            else:
                wds, prop = self._push_v_snak(obj_snak)
                p = self._fresh_qvar()
                self._q.triples()(
                    (prop, NS.WIKIBASE.claim, p),
                    (subj, p, wds))
            return wds

    def _push_v_snak(
            self,
            obj: VSnak,
            wds: Optional[Query.Variable] = None
    ) -> tuple[Query.Variable, Query.V_URI]:
        if isinstance(obj, (
                ValueSnakTemplate,
                ValueSnakVariable,
                ValueSnak)):
            return self._push_v_value_snak(obj, wds)
        elif isinstance(obj, (
                SomeValueSnakTemplate,
                SomeValueSnakVariable,
                SomeValueSnak)):
            return self._push_v_some_value_snak(obj, wds)
        elif isinstance(obj, (
                NoValueSnakTemplate,
                NoValueSnakVariable,
                NoValueSnak)):
            return self._push_v_no_value_snak(obj, wds)
        else:
            raise ShouldNotGetHere

    def _push_statement_variable(
            self,
            obj: StatementVariable
    ) -> Query.Variable:
        obj_subj = self._fresh_entity_variable()
        obj_snak = self._fresh_snak_variable()
        tpl = self._theta_add(obj, StatementTemplate(obj_subj, obj_snak))
        wds = self._push_statement_template(tpl)
        assert isinstance(wds, Query.Variable)
        return wds

    def _push_statement(self, obj: Statement) -> Query.Variable:
        tpl = StatementTemplate(*obj.args)
        wds = self._push_statement_template(tpl)
        assert isinstance(wds, Query.Variable)
        return wds
