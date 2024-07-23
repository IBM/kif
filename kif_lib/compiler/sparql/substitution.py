# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import networkx as nx

from ...model import KIF_Object, Template, Variable
from ...typing import (
    Any,
    cast,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
)
from .builder import Query

T = TypeVar('T')


class Substitution(Mapping):
    """Substitution.

    Maps KIF variables to KIF objects or query variables.
    """

    __slots__ = (
        '_map',
        '_name_map',
        '_defaults',
        '_G',
        '_cached_topsorted_G',
    )

    #: Maps KIF variables to KIF objects or query variables.
    _map: MutableMapping[Variable, Union[KIF_Object, Query.Variable]]

    #: Maps variable names to sets of homonymous (compatible) variables.
    _name_map: MutableMapping[str, set[Variable]]

    #: Keeps the default values of variables.
    _defaults: MutableMapping[Variable, Optional[KIF_Object]]

    #: Variable name dependency graph.
    _G: nx.DiGraph

    #: Order produced by top-soritng `_G`.
    _cached_topsorted_G: Optional[list[str]]

    def __init__(self):
        self._map = {}
        self._name_map = {}
        self._defaults = {}
        self._G = nx.DiGraph()
        self._cached_topsorted_G = None

    def __str__(self):
        return ''.join(self._dump())

    def _dump(self, _attrs=(
            '_map',
            '_name_map',
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

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def add(
            self,
            variable: Variable,
            value: T,
    ) -> T:
        """Associates `variable` to `value` in substitution.

        Parameters:
           variable: Variable.
           value: KIF_Object or Query.Variable.

        Returns:
           The given `value`.
        """
        assert isinstance(variable, Variable)
        assert isinstance(value, (KIF_Object, Query.Variable))
        assert variable not in self or self[variable] == value
        self._map[variable] = value
        if variable.name not in self._name_map:
            self._name_map[variable.name] = set()
        self._name_map[variable.name].add(variable)
        if isinstance(value, Variable):
            self._G.add_edge(value.name, variable.name)
        elif isinstance(value, Template):
            self._G.add_edges_from(map(
                lambda x: (x.name, variable.name), value.variables))
        assert nx.is_directed_acyclic_graph(self._G)
        return cast(T, value)

    def add_default(
            self,
            var: Variable,
            value: Optional[KIF_Object]
    ) -> Variable:
        """Associates default `value` to variable in substitution.

        Parameters:
           variable: Variable.
           value: Value.

        Returns:
           The given `variable`.
        """
        self._defaults[var] = value
        return var

    def _topsorted_G(self) -> list[str]:
        if self._cached_topsorted_G is None:
            self._cached_topsorted_G = list(nx.topological_sort(self._G))
        return self._cached_topsorted_G

    class Theta(Mapping):
        """Auxiliary instantiation table.

        Used by :meth:`Substitution.instantiate`.
        """

        __slots__ = (
            '_map',
            '_name_map',
        )

        #: Maps KIF variables to KIF objects or ``None``.
        _map: MutableMapping[Variable, Optional[KIF_Object]]

        #: Maps variable names to sets of homonymous (compatible) variables.
        _name_map: MutableMapping[str, set[Variable]]

        def __init__(self):
            self._map = {}
            self._name_map = {}

        def __getitem__(self, k: Variable) -> Optional[KIF_Object]:
            homonyms = self._name_map[k.name]
            if len(homonyms) == 1:
                return self._map[k]
            else:
                # Gets the most "grounded" homonyms variable, i.e., the one
                # with fewer variables.
                return next(iter(sorted(
                    map(lambda h: self._map[h], homonyms),
                    key=self._count_vars)))

        def _count_vars(self, obj: Optional[KIF_Object]):
            if isinstance(obj, Variable):
                return 1
            elif isinstance(obj, Template):
                return len(obj.variables)
            else:
                return 0

        def __iter__(self):
            return iter(self._map)

        def __len__(self):
            return len(self._map)

        def _add(self, k: Variable, v: Optional[KIF_Object]):
            self._map[k] = v
            if k.name not in self._name_map:
                self._name_map[k.name] = set()
            self._name_map[k.name].add(k)
            # print(f'𝜃[{k}] := {v}')

    def instantiate(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Mapping[Variable, Optional[KIF_Object]]:
        """Computes variable instantiation (theta) from `binding`.

        Parameters:
           binding: SPARQL results binding.

        Returns:
           The resulting variable instantiation (theta).
        """
        theta = self.Theta()
        for name in self._topsorted_G():
            assert name in self._name_map
            if name in binding:
                for var in self._name_map[name]:
                    value = self._map[var]
                    if isinstance(value, Query.Variable):
                        theta._add(
                            var, var.object_class(binding[name]['value']))
            for var in self._name_map[name]:
                assert var in self._map
                value = self._map[var]
                if isinstance(value, Query.Variable):
                    if var not in theta and var in self._defaults:
                        theta._add(var, self._defaults[var])
                    continue  # nothing to do
                assert isinstance(value, (Template, Variable))
                if isinstance(value, Variable):
                    if value in theta:
                        theta._add(var, var.instantiate({var: theta[value]}))
                elif isinstance(value, Template):
                    if all(map(
                            lambda v: v.name in theta._name_map,
                            value.variables)):
                        theta._add(var, value.instantiate(theta))
                else:
                    raise RuntimeError('should not get here')
        return theta._map
