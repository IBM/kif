# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from ... import namespace as NS
from ...error import ShouldNotGetHere
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
    Property,
    PropertyTemplate,
    PropertyVariable,
    ShallowDataValue,
    ShallowDataValueTemplate,
    StringVariable,
    Template,
    V_IRI,
    Value,
    ValueTemplate,
    ValueVariable,
    Variable,
    VItem,
    VLexeme,
    VProperty,
)
from ...typing import (
    Any,
    cast,
    MutableMapping,
    Set,
    TypeAlias,
    TypeVar,
    Union,
)
from .builder import SelectQuery
from .builder import URIRef as QueryURI
from .builder import Variable as QueryVariable

T = TypeVar('T')
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

    def _variant(self, name: str, avoid: Set[str] = set()) -> str:
        var = self.__variant(name)
        while var in avoid:
            var = self.__variant(var)
        return var

    def __variant(self, name: str, _re=re.compile(r'(.*?)(\d*)$')) -> str:
        prefix, suffix = _re.match(name).groups()
        if suffix:
            return prefix + str(int(suffix) + 1)
        else:
            return prefix + '0'

    def _as_qvar(self, var: Variable) -> QueryVariable:
        return self._q.var(var.name)

    def _as_qvar_variant(self, var: Variable) -> QueryVariable:
        return self._q.var(self._variant(var.name))

    def _push(self, obj: KIF_Object) -> Any:
        if isinstance(obj, Template):
            if isinstance(obj, ValueTemplate):
                return self._push_value_template(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Variable):
            if isinstance(obj, ValueVariable):
                return self._push_value_variable(obj)
            else:
                raise ShouldNotGetHere
        elif isinstance(obj, Value):
            return self._push_value(obj)
        else:
            raise ShouldNotGetHere

    def _push_value_template(self, obj: ValueTemplate) -> Any:
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

    def _push_value_variable(self, obj: ValueVariable) -> Any:
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
            raise ShouldNotGetHere

    def _push_value(self, obj: Value) -> Any:
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

# -- Entity ----------------------------------------------------------------

    def _push_entity_variable(self, obj: EntityVariable) -> VQueryURI:
        with self._q.union():
            with self._q.group():
                var1 = self._push_item_variable(ItemVariable(obj.name))
            with self._q.group():
                var2 = self._push_property_variable(PropertyVariable(obj.name))
            with self._q.group():
                var3 = self._push_lexeme_variable(LexemeVariable(obj.name))
        assert var1 == var2 and var2 == var3
        return var1

# -- Item ------------------------------------------------------------------

    def _push_item_template(self, obj: ItemTemplate) -> VQueryURI:
        uri = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(uri, NS.SCHEMA.version, self._q.bnode())
        return uri

    def _push_item_variable(self, obj: ItemVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        uri = self._push_item_template(
            self._theta.add(obj, ItemTemplate(iri)))
        assert isinstance(uri, QueryVariable)
        return uri

    def _push_item(self, obj: Item) -> QueryURI:
        uri = self._push_item_template(ItemTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

# -- Property --------------------------------------------------------------

    def _push_property_template(self, obj: PropertyTemplate) -> VQueryURI:
        uri = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(uri, NS.RDF.type, NS.WIKIBASE.Property)
        return uri

    def _push_property_variable(self, obj: PropertyVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        uri = self._push_property_template(
            self._theta.add(obj, PropertyTemplate(iri)))
        assert isinstance(uri, QueryVariable)
        return uri

    def _push_property(self, obj: Property) -> QueryURI:
        uri = self._push_property_template(PropertyTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

# -- Lexeme ----------------------------------------------------------------

    def _push_lexeme_template(self, obj: LexemeTemplate) -> VQueryURI:
        uri = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(uri, NS.RDF.type, NS.ONTOLEX.LexicalEntry)
        return uri

    def _push_lexeme_variable(self, obj: LexemeVariable) -> QueryVariable:
        iri = IRI_Variable(obj.name)
        uri = self._push_lexeme_template(
            self._theta.add(obj, LexemeTemplate(iri)))
        assert isinstance(uri, QueryVariable)
        return uri

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
            str_var = self._theta.add(content, self._as_qvar_variant(content))
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
