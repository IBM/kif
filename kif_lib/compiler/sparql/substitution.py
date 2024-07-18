# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...model import KIF_Object, Template, Variable
from ...typing import (
    Any,
    cast,
    Mapping,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
)
from .builder import Query

T = TypeVar('T')


class Substitution(MutableMapping):
    """Substitution."""

    _map: MutableMapping[Variable, Union[KIF_Object, Query.Variable]]
    _dependency_graph: MutableMapping[
        Variable, set[Union[Variable, Query.Variable]]]
    _reverse_dependency_graph: MutableMapping[
        Union[Variable, Query.Variable], set[Variable]]
    _defaults: MutableMapping[Variable, Optional[KIF_Object]]

    __slots__ = (
        '_map',
        '_dependency_graph',
        '_reverse_dependency_graph',
        '_defaults',
    )

    def __init__(self):
        self._map = {}
        self._dependency_graph = {}
        self._reverse_dependency_graph = {}
        self._defaults = {}

    def __str__(self):
        return ''.join(self._dump())

    def _dump(self, _attrs=(
            '_map',
            '_dependency_graph',
            '_reverse_dependency_graph',
            '_defaults'
    )):
        for attr in _attrs:
            yield f'{attr}:\n'
            for k, v in getattr(self, attr).items():
                yield f'{self._dump_value(k)} -> '
                if isinstance(v, set):
                    yield ', '.join(map(self._dump_value, v))
                else:
                    yield self._dump_value(v)
                yield '\n'
            yield '\n'

    @classmethod
    def _dump_value(cls, v: Any) -> str:
        return v.n3() if isinstance(v, Query.Variable) else str(v)

    def __getitem__(self, k):
        return self._map[k]

    def __setitem__(self, k, v):
        self.add(k, v)

    def __delitem__(self, k):
        del self._map[k]

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def add(
            self,
            var: Variable,
            value: T,
    ) -> T:
        assert isinstance(var, Variable)
        assert isinstance(value, (KIF_Object, Query.Variable))
        self._add_to_map(var, value)
        self._add_to_dependency_graph(var, value)
        return cast(T, value)

    def add_default(
            self,
            var: Variable,
            value: Optional[KIF_Object]
    ) -> Variable:
        self._defaults[var] = value
        return var

    def _add_to_map(
            self,
            var: Variable,
            value: Union[KIF_Object, Query.Variable],
    ):
        assert var not in self or self[var] == value
        self._map[var] = value

    def _add_to_dependency_graph(
            self,
            source: Variable,
            target: Union[KIF_Object, Query.Variable]
    ):
        if source not in self._dependency_graph:
            self._dependency_graph[source] = set()
        if isinstance(target, (Variable, Query.Variable)):
            self._dependency_graph[source].add(target)
            self._add_to_reverse_dependency_graph(target, source)
        elif isinstance(target, Template):
            self._dependency_graph[source].update(target.variables)
            for var in target.variables:
                self._add_to_reverse_dependency_graph(var, source)

    def _add_to_reverse_dependency_graph(
            self,
            source: Union[Variable, Query.Variable],
            target: Variable
    ):
        if source not in self._reverse_dependency_graph:
            self._reverse_dependency_graph[source] = set()
        self._reverse_dependency_graph[source].add(target)

    def instantiate(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Mapping[Variable, Optional[KIF_Object]]:
        theta: MutableMapping[Variable, Optional[KIF_Object]] = {}
        it = map(lambda t: (t[0], t[1]['value']), binding.items())
        for qvar_name, qvar_value in it:
            qvar = Query._mk_variable(qvar_name)
            if qvar not in self._reverse_dependency_graph:
                continue
            for rdep in self._reverse_dependency_graph[qvar]:
                assert isinstance(rdep, Variable)
                value = rdep.object_class(qvar_value)
                self._instantiate(rdep, value, theta)
        it_kv_with_free_vars = filter(
            lambda t: isinstance(t[1], Template) and bool(t[1].variables),
            theta.items())
        for k, v in it_kv_with_free_vars:
            assert isinstance(v, Template)
            theta[k] = v.instantiate(self._defaults)
        return theta

    def _instantiate(
            self,
            var: Variable,
            value: Optional[KIF_Object],
            theta: MutableMapping[Variable, Optional[KIF_Object]]
    ):
        theta[var] = value
        for rdep in self._reverse_dependency_graph.get(var, ()):
            dep = self[rdep]
            assert isinstance(dep, (Template, Variable))
            self._instantiate(rdep, dep.instantiate(theta), theta)
