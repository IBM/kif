# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...error import ShouldNotGetHere
from ...itertools import chain
from ...model import (
    DataValue,
    DataValueTemplate,
    Entity,
    EntityTemplate,
    EntityVariable,
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
    ShallowDataValue,
    ShallowDataValueTemplate,
    Snak,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    StringVariable,
    Template,
    V_IRI,
    Value,
    ValueSnak,
    ValueSnakTemplate,
    ValueSnakVariable,
    ValueTemplate,
    ValueVariable,
    Variable,
    VItem,
    VLexeme,
    VProperty,
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

    __slots__ = (
        '_input',
        '_q',
        '_theta',
    )

    def __init__(self, obj: KIF_Object):
        self._input = obj
        self._q = CompiledQuery()
        self._theta = Substitution()

    def compile(self) -> 'Compiler':
        self._push(self._input)
        return self

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

# -- _push -----------------------------------------------------------------

    def _push(self, obj: KIF_Object) -> Any:
        if isinstance(obj, Template):
            if isinstance(obj, ValueTemplate):
                return self._do_push_value_template(obj)
            elif isinstance(obj, SnakTemplate):
                return self._do_push_snak_template(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Variable):
            if isinstance(obj, ValueVariable):
                return self._do_push_value_variable(obj)
            elif isinstance(obj, SnakVariable):
                return self._do_push_snak_variable(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Value):
            return self._do_push_value(obj)
        elif isinstance(obj, Snak):
            return self._do_push_snak(obj)
        else:
            raise ShouldNotGetHere

    def _do_push_value_template(self, obj: ValueTemplate) -> Any:
        if isinstance(obj, EntityTemplate):
            if isinstance(obj, ItemTemplate):
                return self._push_item_template(obj)
            elif isinstance(obj, PropertyTemplate):
                return self._push_property_template(obj)
            elif isinstance(obj, LexemeTemplate):
                return self._push_lexeme_template(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, DataValueTemplate):
            if isinstance(obj, ShallowDataValueTemplate):
                if isinstance(obj, IRI_Template):
                    return self._push_iri_template(obj)
                else:
                    raise ShouldNotGetHere
        else:
            raise ShouldNotGetHere

    def _do_push_value_variable(self, obj: ValueVariable) -> Any:
        if isinstance(obj, EntityVariable):
            if isinstance(obj, ItemVariable):
                return self._push_item_variable(obj)
            elif isinstance(obj, PropertyVariable):
                return self._push_property_variable(obj)
            elif isinstance(obj, LexemeVariable):
                return self._push_lexeme_variable(obj)
            else:
                return self._push_entity_variable(obj)
        elif isinstance(obj, IRI_Variable):
            return self._push_iri_variable(obj)
        else:
            return self._push_value_variable(obj)

    def _do_push_value(self, obj: Value) -> Any:
        if isinstance(obj, Entity):
            if isinstance(obj, Item):
                return self._push_item(obj)
            elif isinstance(obj, Property):
                return self._push_property(obj)
            elif isinstance(obj, Lexeme):
                return self._push_lexeme(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, DataValue):
            if isinstance(obj, ShallowDataValue):
                if isinstance(obj, IRI):
                    return self._push_iri(obj)
                else:
                    raise ShouldNotGetHere
            else:
                raise ShouldNotGetHere
        else:
            raise ShouldNotGetHere

    def _do_push_snak_template(self, obj: SnakTemplate) -> Any:
        if isinstance(obj, ValueSnakTemplate):
            return self._push_value_snak_template(obj)
        elif isinstance(obj, SomeValueSnakTemplate):
            return self._push_some_value_snak_template(obj)
        elif isinstance(obj, NoValueSnakTemplate):
            return self._push_no_value_snak_template(obj)
        else:
            raise ShouldNotGetHere

    def _do_push_snak_variable(self, obj: SnakVariable) -> Any:
        if isinstance(obj, ValueSnakVariable):
            raise NotImplementedError
        elif isinstance(obj, SomeValueSnakVariable):
            return self._push_some_value_snak_variable(obj)
        elif isinstance(obj, NoValueSnakVariable):
            return self._push_no_value_snak_variable(obj)
        else:
            raise ShouldNotGetHere

    def _do_push_snak(self, obj: Snak) -> Any:
        if isinstance(obj, ValueSnak):
            raise NotImplementedError
        elif isinstance(obj, SomeValueSnak):
            return self._push_some_value_snak(obj)
        elif isinstance(obj, NoValueSnak):
            return self._push_no_value_snak(obj)
        else:
            raise ShouldNotGetHere

# -- Value -----------------------------------------------------------------

    def _push_v_value(self, obj: VValue) -> VQueryTerm:
        if isinstance(obj, (ItemTemplate, ItemVariable, Item)):
            return self._push_v_item(obj)
        elif isinstance(obj, (IRI_Template, IRI_Variable, IRI)):
            return self._push_v_iri(obj)
        elif isinstance(obj, (PropertyTemplate, PropertyVariable, Property)):
            return self._push_v_property(obj)
        elif isinstance(obj, (LexemeTemplate, LexemeVariable, Lexeme)):
            return self._push_v_lexeme(obj)
        elif isinstance(obj, EntityVariable):
            return self._push_entity_variable(obj)
        else:
            raise ShouldNotGetHere

    def _push_value_variable(self, obj: ValueVariable) -> QueryVariable:
        with self._q.union():
            with self._q.group():
                v1 = self._push_entity_variable(EntityVariable(obj.name))
            # with self._q.group():
            #     v2 = self._push_iri_variable(IRI_Variable(obj.name))
        return v1

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
        item = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(item, NS.SCHEMA.version, self._q.bnode())
        return item

    def _push_item_variable(self, obj: ItemVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        var = self._push_item_template(
            self._theta.add(obj, ItemTemplate(iri)))
        assert isinstance(var, QueryVariable)
        return var

    def _push_item(self, obj: Item) -> QueryURI:
        uri = self._push_item_template(ItemTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

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
        prop = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(prop, NS.RDF.type, NS.WIKIBASE.Property)
        return prop

    def _push_property_variable(self, obj: PropertyVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        var = self._push_property_template(
            self._theta.add(obj, PropertyTemplate(iri)))
        assert isinstance(var, QueryVariable)
        return var

    def _push_property(self, obj: Property) -> QueryURI:
        uri = self._push_property_template(PropertyTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

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
        lexeme = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(lexeme, NS.RDF.type, NS.ONTOLEX.LexicalEntry)
        return lexeme

    def _push_lexeme_variable(self, obj: LexemeVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        var = self._push_lexeme_template(
            self._theta.add(obj, LexemeTemplate(iri)))
        assert isinstance(var, QueryVariable)
        return var

    def _push_lexeme(self, obj: Lexeme) -> QueryURI:
        uri = self._push_lexeme_template(LexemeTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

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
        content = obj.content
        if isinstance(content, StringVariable):
            uri_var = self._as_qvar(content)
            str_var = self._theta.add(content, self._fresh_qvar())
            self._q.bind(self._q.str(uri_var), str_var)
            return uri_var
        elif isinstance(content, str):
            uri = self._push(IRI(content))
            assert isinstance(uri, QueryURI)
            return uri
        else:
            raise ShouldNotGetHere

    def _push_iri_variable(self, obj: IRI_Variable) -> QueryVariable:
        return cast(QueryVariable, self._theta.add(obj, self._as_qvar(obj)))

    def _push_iri(self, obj: IRI) -> QueryURI:
        return self._q.uri(obj.content)

# -- ValueSnak -------------------------------------------------------------

    def _push_value_snak_template(
            self,
            obj: ValueSnakTemplate
    ) -> VQueryURI:
        with self._q.group():
            prop = self._push_v_property(obj.property)
            ps, wds = self._fresh_qvars(2)
            with self._q.group():
                self._q.triple(prop, NS.WIKIBASE.statementProperty, ps)
                self._q.triple(wds, ps, self._push_v_value(obj.value))
        return prop

# -- SomeValueSnak ---------------------------------------------------------

    def _push_some_value_snak_template(
            self,
            obj: SomeValueSnakTemplate
    ) -> VQueryURI:
        prop = self._push_v_property(obj.property)
        ps, wds, value = self._fresh_qvars(3)
        with self._q.group():
            self._q.triples(
                (prop, NS.WIKIBASE.statementProperty, ps),
                (wds, ps, value))
            self._q.filter(self._q.call(NS.WIKIBASE.isSomeValue, value))
        return prop

    def _push_some_value_snak_variable(
            self,
            obj: SomeValueSnakVariable
    ) -> VQueryURI:
        prop = PropertyVariable(obj.name)
        var = self._push_some_value_snak_template(
            self._theta.add(obj, SomeValueSnakTemplate(prop)))
        assert isinstance(var, QueryVariable)
        return var

    def _push_some_value_snak(self, obj: SomeValueSnak) -> QueryURI:
        uri = self._push_some_value_snak_template(
            SomeValueSnakTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

# -- NoValueSnak -----------------------------------------------------------

    def _push_no_value_snak_template(
            self,
            obj: NoValueSnakTemplate
    ) -> VQueryURI:
        prop = self._push_v_property(obj.property)
        wdno, wds = self._fresh_qvars(2)
        with self._q.group():
            self._q.triples(
                (prop, NS.WIKIBASE.novalue, wdno),
                (wds, NS.RDF.type, wdno))
        return prop

    def _push_no_value_snak_variable(
            self,
            obj: NoValueSnakVariable
    ) -> VQueryURI:
        prop = PropertyVariable(obj.name)
        var = self._push_no_value_snak_template(
            self._theta.add(obj, NoValueSnakTemplate(prop)))
        assert isinstance(var, QueryVariable)
        return var

    def _push_no_value_snak(self, obj: NoValueSnak) -> QueryURI:
        uri = self._push_no_value_snak_template(
            NoValueSnakTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri
