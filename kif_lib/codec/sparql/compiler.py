# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...error import ShouldNotGetHere
from ...model import (
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
    StringVariable,
    V_IRI,
    Variable,
    VItem,
    VLexeme,
)
from ...typing import (
    Any,
    cast,
    MutableMapping,
    Optional,
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
        assert var not in self._data
        assert isinstance(value, (KIF_Object, QueryVariable))
        self._data[var] = value
        return cast(T, value)


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

    def _as(
            self,
            var: Variable,
            cls: type[Variable],
            suffix: Optional[str] = None
    ) -> Variable:
        if suffix is not None:
            return cls(f'{var.name}_{suffix}')
        else:
            return cls(var.name)

    def _as_qvar(
            self,
            var: Variable,
            suffix: Optional[str] = None
    ) -> QueryVariable:
        if suffix is not None:
            return self._q.var(f'{var.name}_{suffix}')
        else:
            return self._q.var(var.name)

    def _push(self, obj: KIF_Object) -> Any:
        if isinstance(obj, ItemTemplate):
            return self._push_item_template(obj)
        elif isinstance(obj, ItemVariable):
            return self._push_item_variable(obj)
        elif isinstance(obj, Item):
            return self._push_item(obj)
        elif isinstance(obj, LexemeTemplate):
            return self._push_lexeme_template(obj)
        elif isinstance(obj, LexemeVariable):
            return self._push_lexeme_variable(obj)
        elif isinstance(obj, Lexeme):
            return self._push_lexeme(obj)
        elif isinstance(obj, IRI_Template):
            return self._push_iri_template(obj)
        elif isinstance(obj, IRI_Variable):
            return self._push_iri_variable(obj)
        elif isinstance(obj, IRI):
            return self._push_iri(obj)
        else:
            raise NotImplementedError

# -- Item ------------------------------------------------------------------

    def _push_v_item(self, obj: VItem) -> VQueryURI:
        return cast(VQueryURI, self._push(obj))

    def _push_item_template(self, obj: ItemTemplate):
        uri = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(uri, NS.SCHEMA.version, self._q.bnode())
        return uri

    def _push_item_variable(self, obj: ItemVariable):
        iri = cast(IRI_Variable, self._as(obj, IRI_Variable, 'IRI'))
        uri = self._push_item_template(
            self._theta.add(obj, ItemTemplate(iri)))
        assert isinstance(uri, QueryVariable)
        return uri

    def _push_item(self, obj: Item) -> QueryURI:
        uri = self._push_item_template(ItemTemplate(*obj.args))
        assert isinstance(uri, QueryURI)
        return uri

# -- Lexeme ----------------------------------------------------------------

    def _push_v_lexeme(self, obj: VLexeme) -> VQueryURI:
        return cast(VQueryURI, self._push(obj))

    def _push_lexeme_template(self, obj: LexemeTemplate) -> VQueryURI:
        uri = self._push_v_iri(obj.iri)
        with self._q.group():
            self._q.triple(uri, NS.RDF.type, NS.ONTOLEX.LexicalEntry)
        return uri

    def _push_lexeme_variable(self, obj: LexemeVariable) -> QueryVariable:
        iri = cast(IRI_Variable, self._as(obj, IRI_Variable, 'IRI'))
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
        return cast(VQueryURI, self._push(obj))

    def _push_iri_template(self, obj: IRI_Template) -> VQueryURI:
        content = obj.content
        if isinstance(content, StringVariable):
            uri_var = self._as_qvar(content, 'IRI')
            str_var = self._theta.add(content, self._as_qvar(content))
            self._q.bind(self._q.str(uri_var), str_var)
            return uri_var
        elif isinstance(content, str):
            uri = self._push(IRI(content))
            assert isinstance(uri, QueryURI)
            return uri
        else:
            raise ShouldNotGetHere

    def _push_iri_variable(self, obj: IRI_Variable) -> QueryVariable:
        return cast(
            QueryVariable, self._theta.add(obj, self._q.var(obj.name)))

    def _push_iri(self, obj: IRI) -> QueryURI:
        return self._q.uri(obj.content)
