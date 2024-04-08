# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...error import ShouldNotGetHere
from ...itertools import chain
from ...model import (
    Datatype,
    Datetime,
    Decimal,
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
    ValueTemplate,
    ValueVariable,
    Variable,
    VExternalId,
    VItem,
    VLexeme,
    VProperty,
    VQuantity,
    VString,
    VText,
    VTime,
    VValue,
)
from ...typing import (
    Any,
    cast,
    Iterator,
    MutableMapping,
    TypeAlias,
    TypeVar,
    Union,
)
from .builder import Literal as QueryLiteral
from .builder import SelectQuery
from .builder import URIRef as QueryURI
from .builder import Variable as QueryVariable

T = TypeVar('T')

TQueryVariable: TypeAlias = Union[QueryVariable, str]

VQueryLiteral: TypeAlias = Union[QueryLiteral, QueryVariable]
VQueryTerm: TypeAlias = Union[QueryURI, QueryLiteral, QueryVariable]
VQueryURI: TypeAlias = Union[QueryURI, QueryVariable]


class CompiledQuery(SelectQuery):
    pass


class Substitution(MutableMapping):
    _data: dict[Variable, Union[KIF_Object, QueryVariable]]

    __slots__ = (
        '_data',
    )

    def __init__(self):
        self._data = dict()

    def __str__(self):
        def f():
            for k, v in self._data.items():
                yield f'{k} := {v if isinstance(v, KIF_Object) else v.n3()}'
        return '\n'.join(f())

    def __getitem__(self, k):
        return self._data[k]

    def __setitem__(self, k, v):
        self._data[k] = v

    def __delitem__(self, k):
        del self._data[k]

    def __iter__(self, k):
        return iter(self._data)

    def __len__(self, k):
        return len(self._data)

    def add(self, var: Variable, value: T) -> T:
        assert isinstance(var, Variable)
        assert (var not in self._data or self._data.get(var) == value)
        assert isinstance(value, (KIF_Object, QueryVariable))
        self._data[var] = value
        return cast(T, value)


# == Compiler ==============================================================

class Compiler:

    _input: KIF_Object
    _q: CompiledQuery
    _theta: Substitution
    _debug: bool

    __slots__ = (
        '_input',
        '_q',
        '_theta',
        '_debug',
    )

    def __init__(self, obj: KIF_Object, debug: bool = False):
        self._input = obj
        self._q = CompiledQuery()
        self._theta = Substitution()
        self._debug = debug

    @property
    def input(self) -> KIF_Object:
        return self.get_input()

    def get_input(self) -> KIF_Object:
        return self._input

    @property
    def query(self) -> CompiledQuery:
        return self.get_query()

    def get_query(self) -> CompiledQuery:
        return self._q

    @property
    def theta(self) -> Substitution:
        return self.get_theta()

    def get_theta(self) -> Substitution:
        return self._theta

    @property
    def debug(self) -> bool:
        return self.get_debug()

    def get_debug(self) -> bool:
        return self._debug

# -- Internal aliases ------------------------------------------------------

    def _theta_add(self, var: Variable, v: T) -> T:
        if self.debug:
            self._q.comments()(
                f'{var} := {v.n3() if isinstance(v, QueryVariable) else v}')
        return self._theta.add(var, v)

    def _qvar(self, var: TQueryVariable) -> QueryVariable:
        return self._q.var(var)

    def _qvars(
            self,
            var: TQueryVariable,
            *vars: TQueryVariable
    ) -> Iterator[QueryVariable]:
        return map(self._qvar, chain((var,), vars))

    def _fresh_qvar(self) -> QueryVariable:
        return self._q.fresh_var()

    def _fresh_qvars(self, n: int) -> Iterator[QueryVariable]:
        return self._q.fresh_vars(n)

    def _as_qvar(self, var: Variable) -> QueryVariable:
        return self._qvar(var.name)

    def _as_qvars(
            self,
            var: Variable,
            *vars: Variable
    ) -> Iterator[QueryVariable]:
        return map(self._as_qvar, chain((var,), vars))

    def _fresh_variable(self, variable_class: type[Variable]) -> Variable:
        return variable_class(str(self._fresh_qvar()))

    def _fresh_variables(
            self,
            variable_class: type[Variable],
            n: int
    ) -> Iterator[Variable]:
        return map(
            lambda qvar: variable_class(str(qvar)), self._fresh_qvars(n))

    def _fresh_value_variable(self) -> ValueVariable:
        return cast(ValueVariable, self._fresh_variable(ValueVariable))

    def _fresh_item_variable(self) -> ItemVariable:
        return cast(ItemVariable, self._fresh_variable(ItemVariable))

    def _fresh_property_variable(self) -> PropertyVariable:
        return cast(PropertyVariable, self._fresh_variable(PropertyVariable))

    def _fresh_string_variable(self) -> StringVariable:
        return cast(StringVariable, self._fresh_variable(StringVariable))

    def _fresh_quantity_variable(self) -> QuantityVariable:
        return cast(QuantityVariable, self._fresh_variable(QuantityVariable))

    def _fresh_time_variable(self) -> TimeVariable:
        return cast(TimeVariable, self._fresh_variable(TimeVariable))

# -- Compilation -----------------------------------------------------------

    def compile(self) -> 'Compiler':
        self._compile(self._input)
        return self

    def _compile(self, obj: KIF_Object) -> Any:
        if isinstance(obj, Template):
            if isinstance(obj, ValueTemplate):
                return self._compile_value_template(obj)
            elif isinstance(obj, SnakTemplate):
                return self._compile_snak_template(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Variable):
            if isinstance(obj, ValueVariable):
                return self._compile_value_variable(obj)
            elif isinstance(obj, SnakVariable):
                return self._compile_snak_variable(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Value):
            return self._compile_value(obj)
        elif isinstance(obj, Snak):
            return self._compile_snak(obj)
        else:
            raise ShouldNotGetHere

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

# -- Entity ----------------------------------------------------------------

    def _push_entity_variable(self, obj: EntityVariable) -> QueryVariable:
        with self._q.union():
            with self._q.group():
                v1 = self._push_item_variable(ItemVariable(obj.name))
            with self._q.group():
                v2 = self._push_property_variable(PropertyVariable(obj.name))
            with self._q.group():
                v3 = self._push_lexeme_variable(LexemeVariable(obj.name))
        assert v1 == v2 and v2 == v3
        return v1

# -- Item ------------------------------------------------------------------

    def _push_v_item(self, obj: VItem) -> VQueryURI:
        if isinstance(obj, ItemTemplate):
            return self._push_item_template(obj)
        elif isinstance(obj, ItemVariable):
            return self._push_item_variable(obj)
        elif isinstance(obj, Item):
            return self._push_item(obj)
        else:
            raise ShouldNotGetHere

    def _push_item_template(self, obj: ItemTemplate) -> VQueryURI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.SCHEMA.version, self._q.bnode()))
        return iri

    def _push_item_variable(self, obj: ItemVariable) -> QueryVariable:
        obj_iri = IRI_Variable(obj.name)
        iri = self._push_item_template(
            self._theta_add(obj, ItemTemplate(obj_iri)))
        assert isinstance(iri, QueryVariable)
        return iri

    def _push_item(self, obj: Item) -> QueryURI:
        iri = self._push_item_template(ItemTemplate(*obj.args))
        assert isinstance(iri, QueryURI)
        return iri

# -- Property --------------------------------------------------------------

    def _push_v_property(self, obj: VProperty) -> VQueryURI:
        if isinstance(obj, PropertyTemplate):
            return self._push_property_template(obj)
        elif isinstance(obj, PropertyVariable):
            return self._push_property_variable(obj)
        elif isinstance(obj, Property):
            return self._push_property(obj)
        else:
            raise ShouldNotGetHere

    def _push_property_template(self, obj: PropertyTemplate) -> VQueryURI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.RDF.type, NS.WIKIBASE.Property))
        return iri

    def _push_property_variable(self, obj: PropertyVariable) -> QueryVariable:
        obj_iri = IRI_Variable(obj.name)
        iri = self._push_property_template(
            self._theta_add(obj, PropertyTemplate(obj_iri)))
        assert isinstance(iri, QueryVariable)
        return iri

    def _push_property(self, obj: Property) -> QueryURI:
        iri = self._push_property_template(PropertyTemplate(*obj.args))
        assert isinstance(iri, QueryURI)
        return iri

# -- Lexeme ----------------------------------------------------------------

    def _push_v_lexeme(self, obj: VLexeme) -> VQueryURI:
        if isinstance(obj, LexemeTemplate):
            return self._push_lexeme_template(obj)
        elif isinstance(obj, LexemeVariable):
            return self._push_lexeme_variable(obj)
        elif isinstance(obj, Lexeme):
            return self._push_lexeme(obj)
        else:
            raise ShouldNotGetHere

    def _push_lexeme_template(self, obj: LexemeTemplate) -> VQueryURI:
        iri = self._push_v_iri(obj.iri)
        self._q.triples()((iri, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        return iri

    def _push_lexeme_variable(self, obj: LexemeVariable) -> QueryVariable:
        obj_iri = IRI_Variable(obj.name)
        iri = self._push_lexeme_template(
            self._theta_add(obj, LexemeTemplate(obj_iri)))
        assert isinstance(iri, QueryVariable)
        return iri

    def _push_lexeme(self, obj: Lexeme) -> QueryURI:
        iri = self._push_lexeme_template(LexemeTemplate(*obj.args))
        assert isinstance(iri, QueryURI)
        return iri

# -- IRI -------------------------------------------------------------------

    def _push_v_iri(self, obj: V_IRI) -> VQueryURI:
        if isinstance(obj, IRI_Template):
            return self._push_iri_template(obj)
        elif isinstance(obj, IRI_Variable):
            return self._push_iri_variable(obj)
        elif isinstance(obj, IRI):
            return self._push_iri(obj)
        else:
            raise ShouldNotGetHere

    def _push_iri_template(self, obj: IRI_Template) -> VQueryURI:
        obj_content = obj.content
        content: VQueryURI
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

    def _push_iri_variable(self, obj: IRI_Variable) -> QueryVariable:
        return cast(QueryVariable, self._theta_add(obj, self._as_qvar(obj)))

    def _push_iri(self, obj: IRI) -> QueryURI:
        return self._q.uri(obj.content)

# -- Text ------------------------------------------------------------------

    def _push_v_text(self, obj: VText) -> VQueryLiteral:
        if isinstance(obj, TextTemplate):
            return self._push_text_template(obj)
        elif isinstance(obj, TextVariable):
            return self._push_text_variable(obj)
        elif isinstance(obj, Text):
            return self._push_text(obj)
        else:
            raise ShouldNotGetHere

    def _push_text_template(self, obj: TextTemplate) -> VQueryLiteral:
        obj_content = obj.content
        obj_lang = obj.language
        content: VQueryLiteral
        if isinstance(obj_content, StringVariable):
            content = self._as_qvar(obj_content)
            self._push_text_template_language(obj, content)
            return self._theta_add(obj_content, content)
        elif isinstance(obj_content, str):
            if isinstance(obj_lang, StringVariable):
                content = self._fresh_qvar()
                self._q.filter(self._q.eq(
                    self._q.str(content), self._q.literal(obj_content)))
                self._push_text_template_language(obj, content)
            else:
                content = self._push_text(Text(obj_content, obj_lang))
        else:
            raise ShouldNotGetHere
        return content

    def _push_text_template_language(
            self,
            obj: TextTemplate,
            content: VQueryLiteral
    ) -> VQueryLiteral:
        obj_lang = obj.language
        lang: VQueryLiteral
        if isinstance(obj_lang, StringVariable):
            lang = self._theta_add(obj_lang, self._fresh_qvar())
            self._q.bind(self._q.lang(content), lang)
        elif isinstance(obj_lang, str):
            lang = self._q.literal(obj_lang)
            self._q.filter(self._q.eq(self._q.lang(content), lang))
        else:
            raise ShouldNotGetHere
        return lang

    def _push_text_variable(self, obj: TextVariable) -> QueryVariable:
        obj_content = self._fresh_string_variable()
        obj_lang = self._fresh_string_variable()
        tpl = self._theta_add(obj, TextTemplate(obj_content, obj_lang))
        content = self._push_text_template(tpl)
        assert isinstance(content, QueryVariable)
        return content

    def _push_text(self, obj: Text) -> QueryLiteral:
        return self._q.literal(obj.content, language=obj.language)

# -- String ----------------------------------------------------------------

    def _push_v_string(self, obj: VString) -> VQueryTerm:
        if isinstance(obj, StringTemplate):
            return self._push_string_template(obj)
        elif isinstance(obj, StringVariable):
            return self._push_string_variable(obj)
        elif isinstance(obj, String):
            return self._push_string(obj)
        else:
            raise ShouldNotGetHere

    def _push_string_template(self, obj: StringTemplate) -> VQueryLiteral:
        obj_content = obj.content
        content: VQueryLiteral
        if isinstance(obj_content, StringVariable):
            content = self._theta_add(obj_content, self._as_qvar(obj_content))
        elif isinstance(obj_content, str):
            content = self._push_string(String(obj_content))
        else:
            raise ShouldNotGetHere
        return content

    def _push_string_variable(self, obj: StringVariable) -> QueryVariable:
        return cast(QueryVariable, self._theta_add(obj, self._as_qvar(obj)))

    def _push_string(self, obj: String) -> QueryLiteral:
        return self._q.literal(obj.content)

# -- External id -----------------------------------------------------------

    def _push_v_external_id(self, obj: VExternalId) -> VQueryTerm:
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
    ) -> VQueryLiteral:
        obj_content = obj.content
        content: VQueryLiteral
        if isinstance(obj_content, StringVariable):
            content = self._theta_add(obj_content, self._as_qvar(obj_content))
        elif isinstance(obj_content, str):
            content = self._push_external_id(ExternalId(obj_content))
        else:
            raise ShouldNotGetHere
        return content

    def _push_external_id_variable(
            self,
            obj: ExternalIdVariable
    ) -> QueryVariable:
        return self._theta_add(obj, self._as_qvar(obj))

    def _push_external_id(self, obj: ExternalId) -> QueryLiteral:
        return self._q.literal(obj.content)

# -- Quantity --------------------------------------------------------------

    def _push_v_quantity(
            self,
            obj: VQuantity,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> VQueryLiteral:
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
            prop: VQueryURI,
            wds: VQueryURI
    ) -> VQueryLiteral:
        obj_amount, obj_unit, obj_lb, obj_ub = obj.args
        amount: VQueryLiteral
        unit: VQueryURI
        lb: VQueryLiteral
        ub: VQueryLiteral
        with self._q.group():
            if isinstance(obj_amount, QuantityVariable):
                amount = self._as_qvar(obj_amount)
                self._theta_add(obj_amount, amount)
            elif isinstance(obj_amount, Decimal):
                amount = self._q.literal(obj_amount)
            else:
                raise ShouldNotGetHere
            if obj_unit is None:
                obj_unit = self._fresh_item_variable()
            if isinstance(obj_unit, ItemVariable):
                unit = self._push_item_variable(obj_unit)
            elif isinstance(obj_unit, Item):
                unit = self._push_item(obj_unit)
            else:
                raise ShouldNotGetHere
            if obj_lb is None:
                obj_lb = self._fresh_quantity_variable()
            if isinstance(obj_lb, QuantityVariable):
                lb = self._theta_add(obj_lb, self._as_qvar(obj_lb))
            else:
                lb = self._q.literal(obj_lb)
            if obj_ub is None:
                obj_ub = self._fresh_quantity_variable()
            if isinstance(obj_ub, QuantityVariable):
                ub = self._theta_add(obj_ub, self._as_qvar(obj_ub))
            else:
                ub = self._q.literal(obj_ub)
            wdv, psv = self._fresh_qvars(2)
            self._q.triples()(
                (prop, NS.WIKIBASE.statementValue, psv),
                (wds, psv, wdv),
                (wdv, NS.RDF.type, NS.WIKIBASE.QuantityValue),
                (wdv, NS.WIKIBASE.quantityAmount, amount))
            with self._q.optional_if(isinstance(unit, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityUnit, unit))
            with self._q.optional_if(isinstance(lb, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityLowerBound, lb))
            with self._q.optional_if(isinstance(ub, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.quantityUpperBound, ub))
            return amount

    def _push_quantity_variable(
            self,
            obj: QuantityVariable,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> QueryVariable:
        obj_amount = self._fresh_quantity_variable()
        obj_unit = self._fresh_item_variable()
        obj_lb = self._fresh_quantity_variable()
        obj_ub = self._fresh_quantity_variable()
        tpl = self._theta_add(
            obj, QuantityTemplate(obj_amount, obj_unit, obj_lb, obj_ub))
        amount = self._push_quantity_template(tpl, prop, wds)
        assert isinstance(amount, QueryVariable)
        return amount

    def _push_quantity(
            self,
            obj: Quantity,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> QueryLiteral:
        tpl = QuantityTemplate(*obj.args)
        amount = self._push_quantity_template(tpl, prop, wds)
        assert isinstance(amount, QueryLiteral)
        return amount

# -- Time ------------------------------------------------------------------

    def _push_v_time(
            self,
            obj: VTime,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> VQueryLiteral:
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
            prop: VQueryURI,
            wds: VQueryURI
    ) -> VQueryLiteral:
        obj_time, obj_prec, obj_tz, obj_cal = obj.args
        time: VQueryLiteral
        prec: VQueryLiteral
        tz: VQueryLiteral
        cal: VQueryURI
        with self._q.group():
            if isinstance(obj_time, TimeVariable):
                time = self._theta_add(obj_time, self._as_qvar(obj_time))
            elif isinstance(obj_time, Datetime):
                time = self._q.literal(obj_time)
            else:
                raise ShouldNotGetHere
            if obj_prec is None:
                obj_prec = self._fresh_quantity_variable()
            if isinstance(obj_prec, QuantityVariable):
                prec = self._theta_add(obj_prec, self._as_qvar(obj_prec))
            else:
                prec = self._q.literal(obj_prec.value)
            if obj_tz is None:
                obj_tz = self._fresh_quantity_variable()
            if isinstance(obj_tz, QuantityVariable):
                tz = self._theta_add(obj_tz, self._as_qvar(obj_tz))
            else:
                tz = self._q.literal(obj_tz)
            if obj_cal is None:
                obj_cal = self._fresh_item_variable()
            if isinstance(obj_cal, ItemVariable):
                cal = self._push_item_variable(obj_cal)
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
            with self._q.optional_if(isinstance(prec, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.timePrecision, prec))
            with self._q.optional_if(isinstance(tz, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.timeTimezone, tz))
            with self._q.optional_if(isinstance(cal, QueryVariable)):
                self._q.triples()((wdv, NS.WIKIBASE.timeCalendarModel, cal))
            return time

    def _push_time_variable(
            self,
            obj: TimeVariable,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> QueryVariable:
        obj_time = self._fresh_time_variable()
        obj_prec = self._fresh_quantity_variable()
        obj_tz = self._fresh_quantity_variable()
        obj_cal = self._fresh_item_variable()
        tpl = self._theta_add(
            obj, TimeTemplate(obj_time, obj_prec, obj_tz, obj_cal))
        time = self._push_time_template(tpl, prop, wds)
        assert isinstance(time, QueryVariable)
        return time

    def _push_time(
            self,
            obj: Time,
            prop: VQueryURI,
            wds: VQueryURI
    ) -> QueryLiteral:
        tpl = TimeTemplate(*obj.args)
        time = self._push_time_template(tpl, prop, wds)
        assert isinstance(time, QueryLiteral)
        return time

# -- Value snak ------------------------------------------------------------

    def _push_value_snak_template(
            self,
            obj: ValueSnakTemplate
    ) -> VQueryURI:
        with self._q.group():
            obj_property = obj.property
            prop = self._push_v_property(obj_property)
            self._q.begin_union()
            it = self._iter_possible_datatypes_for_v_value(obj.value)
            for dt in it:
                ps, wds = self._fresh_qvars(2)
                obj_value: VValue
                if isinstance(obj.value, ValueVariable):
                    obj_value_var_class = dt.to_value_variable_class()
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
            return prop

    def _iter_possible_datatypes_for_v_value(
            self,
            obj: VValue
    ) -> Iterator[Datatype]:
        if isinstance(obj, ValueTemplate):
            yield Datatype.from_value_template_class(obj.__class__)
        elif isinstance(obj, Value):
            yield Datatype.from_value_class(obj.__class__)
        elif isinstance(obj, ValueVariable):
            def it(cls):
                try:
                    yield Datatype.from_value_variable_class(cls)
                except ValueError:
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
            prop: VQueryURI,
            wds: VQueryURI
    ) -> VQueryTerm:
        if isinstance(obj, (ItemTemplate, ItemVariable, Item)):
            return self._push_v_item(obj)
        elif isinstance(obj, (PropertyTemplate, PropertyVariable, Property)):
            return self._push_v_property(obj)
        elif isinstance(obj, (LexemeTemplate, LexemeVariable, Lexeme)):
            return self._push_v_lexeme(obj)
        elif isinstance(obj, (IRI_Template, IRI_Variable, IRI)):
            return self._push_v_iri(obj)
        elif isinstance(obj, (TextTemplate, TextVariable, Text)):
            return self._push_v_text(obj)
        elif isinstance(obj, (
                ExternalIdTemplate, ExternalIdVariable, ExternalId)):
            return self._push_v_external_id(obj)
        elif isinstance(obj, (StringTemplate, StringVariable, String)):
            return self._push_v_string(obj)
        elif isinstance(obj, (QuantityTemplate, QuantityVariable, Quantity)):
            return self._push_v_quantity(obj, prop, wds)
        elif isinstance(obj, (TimeTemplate, TimeVariable, Time)):
            return self._push_v_time(obj, prop, wds)
        else:
            raise ShouldNotGetHere

    def _push_value_snak_variable(
            self,
            obj: ValueSnakVariable
    ) -> VQueryURI:
        obj_prop = self._fresh_property_variable()
        obj_value = self._fresh_value_variable()
        tpl = self._theta_add(obj, ValueSnakTemplate(obj_prop, obj_value))
        var = self._push_value_snak_template(tpl)
        assert isinstance(var, QueryVariable)
        return var

    def _push_value_snak(self, obj: ValueSnak) -> QueryURI:
        tpl = ValueSnakTemplate(*obj.args)
        uri = self._push_value_snak_template(tpl)
        assert isinstance(uri, QueryURI)
        return uri

# -- Some-value snak -------------------------------------------------------

    def _push_some_value_snak_template(
            self,
            obj: SomeValueSnakTemplate
    ) -> VQueryURI:
        with self._q.group():
            prop = self._push_v_property(obj.property)
            ps, wds, value = self._fresh_qvars(3)
            self._q.triples()(
                (prop, NS.WIKIBASE.statementProperty, ps),
                (wds, ps, value))
            self._q.filter(self._q.call(NS.WIKIBASE.isSomeValue, value))
        return prop

    def _push_some_value_snak_variable(
            self,
            obj: SomeValueSnakVariable
    ) -> QueryVariable:
        obj_prop = self._fresh_property_variable()
        tpl = self._theta_add(obj, SomeValueSnakTemplate(obj_prop))
        prop = self._push_some_value_snak_template(tpl)
        assert isinstance(prop, QueryVariable)
        return prop

    def _push_some_value_snak(self, obj: SomeValueSnak) -> QueryURI:
        tpl = SomeValueSnakTemplate(*obj.args)
        prop = self._push_some_value_snak_template(tpl)
        assert isinstance(prop, QueryURI)
        return prop

# -- No-value snak ---------------------------------------------------------

    def _push_no_value_snak_template(
            self,
            obj: NoValueSnakTemplate
    ) -> VQueryURI:
        with self._q.group():
            prop = self._push_v_property(obj.property)
            wdno, wds = self._fresh_qvars(2)
            self._q.triples()(
                (prop, NS.WIKIBASE.novalue, wdno),
                (wds, NS.RDF.type, wdno))
        return prop

    def _push_no_value_snak_variable(
            self,
            obj: NoValueSnakVariable
    ) -> QueryVariable:
        obj_prop = self._fresh_property_variable()
        tpl = self._theta_add(obj, NoValueSnakTemplate(obj_prop))
        prop = self._push_no_value_snak_template(tpl)
        assert isinstance(prop, QueryVariable)
        return prop

    def _push_no_value_snak(self, obj: NoValueSnak) -> QueryURI:
        tpl = NoValueSnakTemplate(*obj.args)
        prop = self._push_no_value_snak_template(tpl)
        assert isinstance(prop, QueryURI)
        return prop
